import os
import sys
import math
import yaml
import settings as sett
import sympy

def get_elements_list(poscar='POSCAR'):
    """
    """
    with open(poscar, 'r') as fposcar:
        poscar_data = fposcar.readlines()
        elems = [e for e in poscar_data[5].strip().split()]
    return elems

def write_potcar(poscar='POSCAR', xc='PBE', version='54'):
    """
    """
    pot_sett_path = os.path.join(os.path.dirname(sett.__file__), 'pot_sett.yml')
    with open(pot_sett_path, 'r') as fpot_sett:
        pot_sett = yaml.safe_load(fpot_sett)
    base_key = "_".join([version.lower(), xc.lower()])
    pot_dir = pot_sett[base_key]['path']
    elem_list = get_elements_list(poscar)
    pot_path = os.path.join(os.path.dirname(poscar), 'POTCAR')
    pot_enmax = 0.
    with open(pot_path, 'w') as fpotcar:
        for e in elem_list:
            vasp_pot_path = os.path.join(pot_dir, pot_sett[base_key]['pot'][e],\
                            'POTCAR')
            with open(vasp_pot_path, 'r') as fvasp_pot:
                for line in fvasp_pot:
                    fpotcar.write(line)
                    if 'ENMAX' in line:
                        enmax = float(line.strip().split()[2].strip(';'))
                        if pot_enmax < enmax:
                            pot_enmax = enmax
    sys.stdout.write('POTCAR written to {loc}\n'.format(loc=pot_path))
    sys.stdout.write('ENMAX = {enmax:0.1f} eV\n'.format(enmax=pot_enmax))
    sys.stdout.flush()
    return pot_enmax

def write_incar(poscar='POSCAR', calc='relaxation', **ext_sett):
    """
    """
    inc_sett_path = os.path.join(os.path.dirname(sett.__file__),\
                    'incar_base.yml')
    with open(inc_sett_path, 'r') as finc_sett:
        inc_sett = yaml.safe_load(finc_sett)
    if ext_sett:
        for tag, val in ext_sett.items():
            inc_sett[tag] = val

    inc_path = os.path.join(os.path.dirname(poscar), 'INCAR'+'.'+calc)
    with open(inc_path, 'w') as fincar:
        for tag, val in sorted(inc_sett.items()):
            fincar.write('{tag} = {val}\n'.format(tag=tag, val=val))
    sys.stdout.write('INCAR written to {loc}\n'.format(loc=inc_path))
    sys.stdout.flush()
    return 

def write_kpoints(poscar='POSCAR', scheme='auto', **ext_sett):
    """
    """
    k_div = 40
    kp_path = os.path.join(os.path.dirname(poscar), 'KPOINTS')
    with open(kp_path, 'w') as fkp:
        fkp.write('KPOINTS\n0\n')
        if scheme=='auto':
            fkp.write('Auto\n{k_div}\n'.format(k_div=k_div))
    sys.stdout.write('KPOINTS written to {loc}\n'.format(loc=kp_path))
    sys.stdout.flush()
    return

def roundup(x):
    return int(math.ceil(x/10.))*10

def write_vasp_input(poscar='POSCAR'):
    pot_enmax = write_potcar(poscar)
    encut = roundup(1.3*pot_enmax)
    ext_sett = {}
    ext_sett['ENCUT'] = 520
    ext_sett['ISPIN'] = 2
    write_incar(poscar, calc='relaxation', **ext_sett)
    ext_sett['ISTART'] = 1
    ext_sett['ICHARG'] = 1
    ext_sett['NSW'] = 0
    ext_sett['IBRION'] = -1
    ext_sett['ISIF'] = 2
    ext_sett['ISMEAR'] = -5
    ext_sett['SIGMA'] = 0.1
    write_incar(poscar, calc='static', **ext_sett)
    write_kpoints(poscar)

