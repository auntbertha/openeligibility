import yaml

def recurse_into_taxonomy(items, output, level=0):
    for item in items:
        name = item['name']
        if level == 0:
            output.write('# {}\n'.format(name))
        elif level == 1:
            output.write('## {}\n'.format(name))
        elif level == 2:
            output.write('- {}\n'.format(name))
        elif level == 3:
            output.write('  - {}\n'.format(name))
        elif level == 4:
            output.write('    - {}\n'.format(name))
        elif level == 5:
            output.write('      - {}\n'.format(name))
        else:
            assert False
        if item.get('items'):
            recurse_into_taxonomy(item.get('items'), output, level+1)

if __name__ == '__main__':
    taxonomy = yaml.load(open('taxonomy.yaml'))
    with open('TAXONOMIES.md', 'w') as output:
        output.write('# טקסונומיית המענים הפתוחים\n\n')

        recurse_into_taxonomy(taxonomy, output)