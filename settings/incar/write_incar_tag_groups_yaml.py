import yaml 
from collections import OrderedDict

tag_groups = OrderedDict()

with open('incar_tag_groups.txt', 'r') as fin:
    lines = fin.readlines()
    for line in lines:
        group, tags = line.strip().split(':')
        tags = [ t.strip() for t in tags.split(',') ]
        ##print tags
        tag_groups[group] = tags

with open('incar_tag_groups.yml', 'w') as fout:
    yaml.dump(tag_groups, fout, default_flow_style=False)
    
