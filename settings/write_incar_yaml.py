import yaml

sett_dict = {}
with open('INCAR.base' , 'r') as fr:
    incar = fr.readlines()
    for row in incar:
        if not row.strip():
            continue
        if row.strip()[0] == '#':
            continue
        tag, value = row.strip().split('=')
        tag = tag.strip()
        value = value.strip()
        sett_dict[tag] = value

with open('incar_base.yml', 'w') as fw:
    yaml.dump(sett_dict, fw, default_flow_style=False)
