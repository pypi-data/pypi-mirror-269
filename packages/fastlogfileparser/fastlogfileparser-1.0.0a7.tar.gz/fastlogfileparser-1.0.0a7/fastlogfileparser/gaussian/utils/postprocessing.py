from fastlogfileparser.generic.postprocessing import (
    _charge_and_multiplicity,
    _columns_to_floats,
    _freq_modes,
    _str_list_to_floats,
    _str_to_float,
    _unix_time_to_seconds,
)


def _mulliken(in_list):
    out = []
    for i in in_list:
        inner_out = []
        for row in i.split(sep="\n"):
            atom_idx, _, mulliken_charge, _ = row.split()
            inner_out.append([int(atom_idx), float(mulliken_charge)])
        out.append(inner_out)
    return out


POSTPROCESSING_FUNCTIONS = {
    "cpu_time": _unix_time_to_seconds,
    "wall_time": _unix_time_to_seconds,
    "e0": _str_to_float,
    "e0_h": _str_to_float,
    "hf": _str_to_float,
    "scf": _str_list_to_floats,
    "recovered_energy": _str_list_to_floats,
    "zpe_per_atom": _str_to_float,
    "wavefunction_energy": _str_to_float,
    "e0_zpe": _str_to_float,
    "gibbs": _str_to_float,
    "frequency_modes": _freq_modes,
    "frequencies": lambda in_list: [float(i) for sublist in in_list for i in sublist],
    "max_steps": lambda in_list: int(in_list[0]),
    "std_forces": _columns_to_floats,
    "std_xyz": _columns_to_floats,
    "xyz": _columns_to_floats,
    "route_section": lambda in_list: in_list[0],
    "charge_and_multiplicity": _charge_and_multiplicity,
    "mulliken_charges_summed": _mulliken,
}
