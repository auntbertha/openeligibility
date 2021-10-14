from pathlib import Path
import yaml
import json
import requests
import os


TRANSIFEX_TOKEN = os.environ.get('TRANSIFEX_TOKEN') or  os.environ.get('TX_TOKEN')
PROJECT = 'openeligibility'


def transifex_session():
    s = requests.Session()
    s.auth = ('api', TRANSIFEX_TOKEN)
    return s


def transifex_slug(filename):
    return '_'.join(filename.parts).replace('.', '_')


def push_translations(filename: Path, translations):
    translations = dict(en=translations)
    content = yaml.dump(translations, allow_unicode=True, indent=2, width=1000000)

    slug = transifex_slug(filename)
    s = transifex_session()
    resp = s.get(f'https://www.transifex.com/api/2/project/{PROJECT}/resource/{slug}/')

    if resp.status_code == requests.codes.ok:
        print('Update file:')
        data = dict(
            content=content,
        )

        resp = s.put(
            f'https://www.transifex.com/api/2/project/{PROJECT}/resource/{slug}/content/',
            json=data
        )
        print(resp.status_code, resp.content[:50])
        
    else:
        print('New file:', slug)
        data = dict(
            slug=slug,
            name=str(filename),
            accept_translations=True,
            i18n_type='YAML_GENERIC',
            content=content,
        )

        resp = s.post(
            f'https://www.transifex.com/api/2/project/{PROJECT}/resources/',
            json=data
        ) 
        print(resp.status_code, resp.content[:100])


def pull_translations(lang, filename):
    s = transifex_session()
    slug = transifex_slug(filename)
    url = f'https://www.transifex.com/api/2/project/{PROJECT}/resource/{slug}/translation/{lang}/'
    try:
        translations = s.get(url).json()
    except json.decoder.JSONDecodeError:
        print('No data from %s' % url)
        return {}
    print(yaml.load(translations['content'], Loader=yaml.BaseLoader).keys())
    translations = yaml.load(translations['content'], Loader=yaml.BaseLoader)['en']
    ret = dict()
    for k, v in translations.items():
        if v:
            ret.setdefault(k, dict())[lang] = v
    return ret


def collect_keys(nodes, to_push, translated):
    for node in nodes:
        try:
            slug = node['slug']
            description_slug = slug + '::description'
            name = node['name']
        except Exception:
            print('Offending node:', node)
            raise
        to_push[slug] = name
        if slug in translated:
            node['name'] = dict(source=name, tx=translated[slug])
        description = node.get('description')
        if description:
            to_push[description_slug] = description
            if description_slug in translated:
                node['description'] = dict(source=description, tx=translated[description_slug])
        if 'items' in node:
            collect_keys(node['items'], to_push, translated)
    return to_push


if __name__ == '__main__':
    in_file = Path('taxonomy.yaml')
    translated = pull_translations('he', in_file)
    translations = yaml.load(in_file.open(), Loader=yaml.BaseLoader)
    to_push = collect_keys(translations, dict(), translated)
    push_translations(Path('taxonomy.yaml'), to_push)
    out_file = Path('taxonomy.tx.yaml')
    out_file.write_text(yaml.dump(translations, sort_keys=False, width=240, allow_unicode=True))