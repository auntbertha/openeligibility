import yaml

def recurse_into_taxonomy(items, output, level=0):
    for item in items:
        name = item['name']
        if isinstance(name, dict):
            name = name.get('tx', dict()).get('he') or name.get('source')
        description = item.get('description')
        if isinstance(description, dict):
            description = description.get('tx', dict()).get('he') or description.get('source')
        prefix = {
            0: '## ',
            1: '### ',
            2: '- ',
            3: '  - ',
            4: '    - ',
            5: '      - ',
            6: '        - ',
        }[level]
        output.write(prefix + name + '\n')
        if description is not None:
            if '#' in prefix:
                prefix = ''
            else:
                prefix = ' '*len(prefix)
            output.write(prefix + description + '\n')
        if item.get('items'):
            recurse_into_taxonomy(item.get('items'), output, level+1)

if __name__ == '__main__':
    taxonomy = yaml.load(open('taxonomy.tx.yaml'))
    with open('TAXONOMIES.md', 'w') as output:
        output.write('<div dir="rtl">\n\n')
        output.write('# טקסונומיית המענים הפתוחים\n\n')

        recurse_into_taxonomy(taxonomy, output)

        output.write('</div>\n')