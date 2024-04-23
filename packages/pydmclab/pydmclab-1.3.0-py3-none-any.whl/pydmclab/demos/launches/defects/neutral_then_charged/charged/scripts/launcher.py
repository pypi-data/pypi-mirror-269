import os
from pydmclab.hpc.helpers import (
    # get_query,
    check_query,
    # get_strucs,
    check_strucs,
    get_magmoms,
    check_magmoms,
    get_launch_dirs,
    check_launch_dirs,
    submit_calcs,
    get_results,
    check_results,
    get_gs,
    check_gs,
    get_thermo_results,
    check_thermo_results,
    get_launch_configs,
    get_sub_configs,
    get_slurm_configs,
    get_vasp_configs,
    get_analysis_configs,
    make_sub_for_launcher,
)

from pydmclab.core.struc import StrucTools, SiteTools
from pydmclab.core.comp import CompTools
from pydmclab.utils.handy import read_json, write_json
from pydmclab.hpc.analyze import AnalyzeVASP

# where is this file
SCRIPTS_DIR = os.getcwd()

# where are my calculations going to live (maybe on scratch)
CALCS_DIR = SCRIPTS_DIR.replace("scripts", "calcs")

# where is my data going to live
DATA_DIR = SCRIPTS_DIR.replace("scripts", "data")

for d in [CALCS_DIR, DATA_DIR]:
    if not os.path.exists(d):
        os.makedirs(d)

# if you need data from MP as a starting point (often the case), you need your API key
API_KEY = "__API KEY__"

# what to query MP for (if you need MP data)
## e.g., 'MnO2', ['MnO2', 'TiO2'], 'Ca-Ti-O, etc
COMPOSITIONS = ["GaN"]

# any configurations related to LaunchTools
LAUNCH_CONFIGS = get_launch_configs(
    standards=["dmc"],
    xcs=["gga"],
    use_mp_thermo_data=False,
    n_afm_configs=0,
    skip_xcs_for_standards={"mp": ["gga", "metagga"]},
)

# any configurations related to SubmitTools
SUB_CONFIGS = get_sub_configs(
    submit_calculations_in_parallel=False,
    rerun_lobster=False,
    mpi_command="mpirun",
    special_packing=False,
    delete_all_calculations_and_start_over=False,
    machine="msi",
)

# any configurations related to Slurm
SLURM_CONFIGS = get_slurm_configs(
    total_nodes=1,
    cores_per_node=4,
    walltime_in_hours=23,
    mem_per_core="all",
    partition="agsmall,msidmc,preempt",
    error_file="log.e",
    output_file="log.o",
    account="cbartel",
)

# any configurations related to VASPSetUp
VASP_CONFIGS = get_vasp_configs(
    run_lobster=False,
    detailed_dos=False,
    modify_loose_incar=False,
    modify_relax_incar=False,
    modify_static_incar=False,
    modify_loose_kpoints=False,
    modify_relax_kpoints=False,
    modify_static_kpoints=False,
    modify_loose_potcar=False,
    modify_relax_potcar=False,
    modify_static_potcar=False,
)

# any configurations related to AnalyzeBatch
ANALYSIS_CONFIGS = get_analysis_configs(
    analyze_calculations_in_parallel=False,
    analyze_structure=True,
    analyze_mag=False,
    analyze_charge=False,
    analyze_dos=False,
    analyze_bonding=False,
    exclude=[],
)

# whether or not you want to generate MAGMOMs (only if you're running AFM)
GEN_MAGMOMS = True if LAUNCH_CONFIGS["n_afm_configs"] else False

# NOTE: the default is to use the imported functions from pydmclab.hpc.helpers
# You will often want to write your own "get_query" and/or "get_strucs" functions instead
# See below (or within pydmclab.hpc.helpers) for some more detailed docs

""" 
In this launcher, we're going to run charged defect calculations
We are going to start from our neutral defect calculations
    - these must have started running for this launcher to work
        - because it's going to collect NELECT from those calculations
We're going to use the same initial structures as those used for the neutral calculations
    - the only difference is we're going to pass custom INCAR settings (NELECT, ISIF) to different "ID"s to run our charged calculations
"""


def get_query(
    data_dir=os.getcwd().replace("scripts", "data"),
    savename="query.json",
    remake=False,
):
    """Use our neutral calculations strucs dict as our "query" here"""
    fjson = os.path.join(data_dir, savename)
    if os.path.exists(fjson) and not remake:
        return read_json(fjson)

    path_to_neutral = os.getcwd().replace("/charged", "/neutral")
    neutral_data = os.path.join(path_to_neutral.replace("scripts", "data"))
    query = read_json(os.path.join(neutral_data, "strucs.json"))
    write_json(query, fjson)
    return read_json(fjson)


def get_strucs(
    query,
    charge_states=[-2, -1, 1, 2],
    data_dir=os.getcwd().replace("scripts", "data"),
    savename="strucs.json",
    remake=False,
):
    """Create unique IDs for each charge state we want to run for each structure"""
    fjson = os.path.join(data_dir, savename)
    if os.path.exists(fjson) and not remake:
        return read_json(fjson)

    strucs = {}
    for formula in query:
        strucs[formula] = {}
        for ID in query[formula]:
            if "pristine" in ID:
                # we don't want to run charged calculations for the pristine structure
                continue

            for charge_state in charge_states:
                # m for minus; p for plus
                indicator = "m" if charge_state < 0 else "p"

                # our "charge_tag" will be like m_2 for -2 defect or p_1 for +1 defect
                charge_tag = "_".join([indicator, str(abs(charge_state))])

                # our "ID" for this charged calculation will be like <structure ID> - <charge tag>
                # e.g., our structure ID might be V_N-2 for the 3rd structure of the N vacancy calculations we ran in neutral
                # so our charged calculation ID will be V_N-2-m_2 for the -2 charge state of the 3rd structure of the N vacancy calculations
                charge_ID = "-".join([ID, charge_tag])
                strucs[formula][charge_ID] = query[formula][ID]

    write_json(strucs, fjson)
    return read_json(fjson)


def get_ID_specific_vasp_configs(
    strucs,
    data_dir=os.getcwd().replace("scripts", "data"),
    savename="ID_specific_vasp_configs.json",
    remake=False,
):
    """Here is we're we'll prepare our "ID-specific" VASP configs"""
    fjson = os.path.join(data_dir, savename)
    if os.path.exists(fjson) and not remake:
        return read_json(fjson)

    out = {}
    for formula in strucs:
        for ID in strucs[formula]:
            key = "_".join([formula, ID])
            out[key] = {}

            # first, we need the NELECT from our neutral calculation
            path_to_neutral = os.getcwd().replace("/charged", "/neutral")
            neutral_calc = os.path.join(
                path_to_neutral.replace("scripts", "calcs"),
                formula,
                "-".join(ID.split("-")[:-1]),
                "dmc",
                "nm",
                "gga-loose",
            )
            print(os.listdir(neutral_calc))
            av = AnalyzeVASP(neutral_calc)
            neutral_nelect = av.outputs.outcar.nelect

            # now we need to use our "charge_tag" to figure out how to change NELECT
            charge_tag = ID.split("-")[-1]
            indicator, charge_state = charge_tag.split("_")

            # remove e- for positive charge states
            if indicator == "p":
                new_nelect = neutral_nelect - float(charge_state)
            # add e- for negative charge states
            elif indicator == "m":
                new_nelect = neutral_nelect + float(charge_state)

            # modify the loose, relax, and static INCAR
            # new NELECT and optimize only ion positions, not cell shape
            for calc in ["loose", "relax", "static"]:
                out[key][calc + "_incar"] = {"NELECT": int(new_nelect), "ISIF": 2}

    write_json(out, fjson)
    return read_json(fjson)


def main():
    remake_sub_for_launcher = False

    remake_query = False
    print_query_check = False

    remake_strucs = False
    print_strucs_check = True

    remake_magmoms = False
    print_magmoms_check = True

    remake_ID_specific_vasp_configs = False
    print_ID_specific_vasp_configs_check = True

    remake_launch_dirs = False
    print_launch_dirs_check = True

    remake_subs = True
    ready_to_launch = True

    remake_results = True
    print_results_check = True

    remake_gs = True
    print_gs_check = True

    remake_thermo_results = True
    print_thermo_results_check = True

    if remake_sub_for_launcher:
        make_sub_for_launcher()

    comp = COMPOSITIONS
    query = get_query(
        data_dir=DATA_DIR,
        remake=remake_query,
    )
    if print_query_check:
        check_query(query)

    strucs = get_strucs(query=query, data_dir=DATA_DIR, remake=remake_strucs)
    if print_strucs_check:
        check_strucs(strucs)

    if GEN_MAGMOMS:
        magmoms = get_magmoms(strucs=strucs, data_dir=DATA_DIR, remake=remake_magmoms)
        if print_magmoms_check:
            check_magmoms(strucs=strucs, magmoms=magmoms)
    else:
        magmoms = None

    ID_specific_vasp_configs = get_ID_specific_vasp_configs(
        strucs, data_dir=DATA_DIR, remake=remake_ID_specific_vasp_configs
    )

    if print_ID_specific_vasp_configs_check:
        for ID in ID_specific_vasp_configs:
            print("\n")
            print(ID)
            print(ID_specific_vasp_configs[ID])

    launch_configs = LAUNCH_CONFIGS
    launch_dirs = get_launch_dirs(
        strucs=strucs,
        magmoms=magmoms,
        user_configs=launch_configs,
        ID_specific_vasp_configs=ID_specific_vasp_configs,
        data_dir=DATA_DIR,
        calcs_dir=CALCS_DIR,
        remake=remake_launch_dirs,
    )
    if print_launch_dirs_check:
        check_launch_dirs(launch_dirs)

    sub_configs = SUB_CONFIGS
    slurm_configs = SLURM_CONFIGS
    vasp_configs = VASP_CONFIGS
    user_sub_configs = {**sub_configs, **slurm_configs, **vasp_configs}
    if remake_subs:
        submit_calcs(
            launch_dirs=launch_dirs,
            user_configs=user_sub_configs,
            ready_to_launch=ready_to_launch,
            n_procs=sub_configs["n_procs"],
        )

    analysis_configs = ANALYSIS_CONFIGS
    results = get_results(
        launch_dirs=launch_dirs,
        user_configs=analysis_configs,
        data_dir=DATA_DIR,
        remake=remake_results,
    )
    if print_results_check:
        check_results(results)

    gs = get_gs(results=results, data_dir=DATA_DIR, remake=remake_gs)

    if print_gs_check:
        check_gs(gs)

    thermo = get_thermo_results(
        results=results, gs=gs, data_dir=DATA_DIR, remake=remake_thermo_results
    )

    if print_thermo_results_check:
        check_thermo_results(thermo)

    return


if __name__ == "__main__":
    main()

    """
    see [pydmclab docs](https://github.umn.edu/bartel-group/pydmclab/blob/main/docs.md) for help

    The basic idea:

    1. get_query
        - need some data to start with that has at least one crystal structure
        - the imported `get_query` will use pydmclab.core.query.MPQuery to get MP data
        - alternatively, you may want to use other starting points. e.g.,
            - other calculations you've run
            - experimental data

        Must return:
            {ID (str) : {'structure' : Pymatgen Structure as dict,
                        < any other data you want to keep track of >}}

        Notes:
            - ID in this case must be a standalone identifier for that structure
                - e.g., mp-123456

    2. get_strucs
        - now we're going to convert our query into the POSCARs we want to calculate
        - a "structure" corresponds with a chemical composition (formula) and a unique identifier for that formula (ID)
        - the imported `get_strucs` will only work if you are not transforming the structures present in your query
        - you will often want to write your own version of this. e.g.,
            - to replace species, change occupancies, etc from the structures you "queried" for

        Must return:
            {formula identifier (str) :
                {structure identifier for that formula (str) :
                    Pymatgen Structure object as dict}}

        Notes:
            - formula identifier in this case must be a standalone identifier for that formula
            - ID only has to be unique within each formula
                - e.g., if you calculate LiMnO2 with many different Li/Mn orderings, ID could be 0, 1, 2, ... for each ordering

    3. get_magmoms
        - if we're running AFM calculations, this will get us our magmoms for each AFM ordering of each structure
        - you can generally use the imported version of this function

        Must return:
            {formula identifier (str) :
                {structure identifier for that formula (str) :
                    {AFM ordering identifier (str) :
                        [list of magmoms (floats) for each site in the structure]}}}

    4. get_launch_dirs
        - this will get us the directories we want to run our calculations in
        - you can generally use the imported version of this function
        - use LAUNCH_CONFIGS to specify what calculations get launched

        Must return:
            {launch dir (str, formula/ID/stsandard/mag) :
                {'xcs' : [list of final xcs to run (str)],
                'magmoms' : [list of magmoms (floats) for each site in the structure]}}

    5. submit_calcs
        - this will write our submission scripts and submit our calculations
        - you can generally use the imported version of this function
        - use SUB_CONFIGS, SLURM_CONFIGS, VASP_CONFIGS to modify how these calculations are prepared

        Does not return anything

    6. get_results
        - this will collect all of the results we specified to collect
        - you can generally use the imported version of this function
        - use ANALYSIS_CONFIGS to modify what results are collected

        Must return:
            {formula--ID--standard--mag--xc-calc (str) :
                {scraped results from VASP calculation}}

    7. get_gs
        - this will collect the ground-state (lowest energy) result for each calculated formula
        - you can generally use the imported version of this function

        Must return:
            {standard (str) :
                {xc (str) :
                    {formula (str) :
                        {'E' : energy of the ground-structure,
                        'key' : formula.ID.standard.mag.xc_calc for the ground-state structure,
                        'structure' : structure of the ground-state structure,
                        'n_started' : how many polymorphs you tried to calculate,
                        'n_converged' : how many polymorphs are converged,
                        'complete' : True if n_converged = n_started (i.e., all structures for this formula at this xc are done),
                        'Ef' : the formation enthalpy (0 K)}

    8. get_thermo_results
        - this will collect the thermodynamic results for all calculated structures (including non-ground-states)
        - you can generally use the imported version of this function

        Must return:
            {standard (str) :
                {xc (str) :
                    {formula (str) :
                        {ID (str) :
                            {'E' : energy of the structure (DFT total energy in eV/atom),
                            'Ef' : formation enthalpy at 0 K (eV/atom),
                            'is_gs' : True if this is the lowest energy polymorph for this formula,
                            'dE_gs' : how high above the ground-state this structure is in energy (eV/atom)
                            'all_polymorphs_converged' : True if every structure that was computed for this formula is converged}}
    """
