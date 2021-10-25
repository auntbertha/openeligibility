import yaml
from slugify import slugify

def to_slug(path):
    return ':'.join(slugify(p, separator='_', to_lower=True) for p in path)

def split_description(name):
    parts = name.split('||')
    if len(parts) == 1:
        return name.strip(), None
    else:
        return parts[0].strip(), parts[1].strip()

def process_items(nodes, path=[]):
    ret = []
    for node in nodes:
        if isinstance(node, dict):
            name = list(node.keys())[0]
            name, description = split_description(name)
            _path = path + [name]
            node = dict(
                name=name,
                slug=to_slug(_path),
                items=process_items(node[name], _path)
            )
            if description:
                node['description'] = description
            ret.append(node)
        elif isinstance(node, str):
            name = node
            name, description = split_description(name)
            _path = path + [name]
            node = dict(
                name=name,
                slug=to_slug(_path),
            )
            if description:
                node['description'] = description
            ret.append(node)
    return ret

if __name__ == '__main__':
    src = yaml.load(open('taxonomy.simple.yaml'), Loader=yaml.BaseLoader)
    dst = process_items(src)
    with open('taxonomy.yaml', 'w') as f:
        yaml.dump(dst, f, width=4096, sort_keys=False)
    print('Done.', dst)