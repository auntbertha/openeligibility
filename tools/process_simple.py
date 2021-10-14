import yaml
from slugify import slugify

def to_slug(path):
    return ':'.join(slugify(p, separator='-') for p in path)

def process_items(nodes, path=[]):
    ret = []
    for node in nodes:
        if isinstance(node, dict):
            name = list(node.keys())[0]
            _path = path + [name]
            ret.append(dict(
                name=name,
                slug=to_slug(_path),
                items=process_items(node[name], _path)
            ))
        elif isinstance(node, str):
            _path = path + [node]
            ret.append(dict(
                name=node,
                slug=to_slug(_path),
            ))
    return ret

if __name__ == '__main__':
    src = yaml.load(open('taxonomy.simple.yaml'), Loader=yaml.BaseLoader)
    dst = process_items(src)
    with open('taxonomy.yaml', 'w') as f:
        yaml.dump(dst, f, width=4096, sort_keys=False)
