import yaml

pot_sett = {}
pot_sett['54_pbe'] = {}
pot_sett['54_pbe']['path'] = '/home/hegde/Codes/vasp_potentials/54/potpaw_pbe'
with open('vasp_rec.yml', 'r') as fvasp_rec:
    vasp_rec_sett = yaml.load(fvasp_rec)
pot_sett['54_pbe']['pot'] = vasp_rec_sett
with open('pot_sett.yml', 'w') as fpot_sett:
    yaml.dump(pot_sett, fpot_sett, default_flow_style=False)
