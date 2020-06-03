#!/usr/bin/python3
"""
gnrt is a lightweight static site generator.
"""

from pathlib import Path
import itertools
import frontmatter
import markdown2
import yaml
from jinja2 import Environment, FileSystemLoader, Template

def load_dataset(config):
    # First iteration: get items metadata and generate dataset
    dataset = {}
    defaults = config['defaults']
    for path in Path('content').rglob('*.md'):
        # Get frontmatter metadata
        item = frontmatter.load(path.resolve())
        metadata = {**defaults, **item.metadata}
        metadata['source'] = str(path)
        if 'target' not in metadata:
            metadata['target'] = str(path).replace('content/', 'public/').replace('.md', '.html')
        if 'link' not in metadata:
            metadata['link'] = metadata['target'].replace('public/', '/')
        if 'id' not in metadata:
            metadata['id'] = metadata['link']
        if 'title' not in metadata:
            metadata['title'] = path.stem
        metadata['content'] = item.content
        dataset[metadata['id']] = metadata
    return dataset

def generate_lists(config, env, dataset):
    # Generate includes (lists) from dataset
    for key, value in config['lists'].items():
        template = env.get_template(value['template'])
        items = dataset.items()
        if 'filter' in value:
            items = {k: v for (k, v) in dataset.items() if v[value['filter']['key']] == value['filter']['value']}.items()
        if 'sort' in value:
            items = sorted(items, key=lambda x: x[1][value['sort']], reverse=value['reverse'])
        if 'limit' in value:
            items = dict(itertools.islice(items, value['limit'])).items()
        render = template.render(list=value, items=items, config=config, data=dataset)
        if 'target' in value:
            Path(value['target']).parent.mkdir(parents=True, exist_ok=True)
            Path(value['target']).write_text(render)
        else:
            Path('includes').mkdir(parents=True, exist_ok=True)
            Path('includes/' + key + '.html').write_text(render)

def generate_items(config, env, dataset):
    # Second iteration: render and write items
    for key, item in dataset.items():
        # Get included content
        for meta in item:
            if str(item[meta]).startswith('includes/'):
                item[meta] = Path(item[meta]).read_text()

        # Render body
        template = Template(item['content'])
        body = template.render(item, config=config, data=dataset)
        item['body'] = markdown2.markdown(body)

        # Render item
        if 'template' in item:
            template = env.get_template(item['template'])
        elif 'template' in config['defaults']:
            template = env.get_template(config['defaults']['template'])
        else:
            template = Template("{{ body }}")
        render = template.render(item, config=config, data=dataset)

        # Write item
        out = Path(item['target'])
        Path(out.parent).mkdir(parents=True, exist_ok=True)
        out.write_text(render)

def main():
    config = {'defaults': {}, 'lists': {}}
    if Path('config.yml').is_file():
        with open('config.yml', 'r') as yml:
            config = yaml.load(yml, Loader=yaml.SafeLoader)
            if not type(config) is dict:
                raise TypeError('Incorrect configuration file')
    if 'defaults' not in config:
        config['defaults'] = {}
    if 'lists' not in config:
        config['lists'] = {}
    env = Environment(loader=FileSystemLoader('templates'))
    dataset = load_dataset(config)
    generate_lists(config, env, dataset)
    print("Generated %d includes" % len(config['lists']))
    generate_items(config, env, dataset)
    print("Generated %d targets" % len(dataset))

if __name__ == '__main__':
    main()
