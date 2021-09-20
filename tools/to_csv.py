import csv
import io
import itertools
from pathlib import Path
import yaml

HEADERS = ('slug', 'level0:name_en', 'level0:name_he', 'level1:name_en', 'level1:name_he', 'level2:name_en', 'level2:name_he')


def node_view(node):
    return [
            node['slug'],
            node['name']['source'] if isinstance(node['name'], dict) else node['name'],
            node['name']['tx']['he'] if isinstance(node['name'], dict) else None,
        ]


def flatten(node, ancestors=None):
    ancestors = ancestors if not ancestors is None else tuple()
    descendents = node.get('items', tuple())
    slug, *current_fields = node_view(node)
    ancestor_fields = list(itertools.chain(*[node_view(view)[1:] for view in ancestors]))
    row = [slug]
    row.extend(ancestor_fields) if ancestors else None
    row.extend(current_fields)
    yield itertools.chain(row)
    for subnode in descendents:
        _ancestors = list(ancestors) + [node]
        yield from flatten(subnode, _ancestors)


def write(filelike, filepath, headers=None):
    with io.open(Path(f'formats/{filepath}'), 'w') as servicesf:
        writer = csv.writer(servicesf)
        writer.writerow(headers) if headers else None
        writer.writerows(filelike)


def run():
    with io.open(Path('taxonomy.tx.yaml')) as f:
        services, situations = yaml.safe_load(f)

    write(flatten(services), 'services.csv', HEADERS)
    write(flatten(situations), 'situations.csv', HEADERS)


if __name__ == '__main__':
    run()
