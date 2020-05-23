#!/usr/bin/python

import frontmatter
import itertools
import markdown2
import yaml
from jinja2 import Environment, FileSystemLoader, Template
from pathlib import Path

with open('config.yml', 'r') as yml:
    config = yaml.load(yml, Loader=yaml.SafeLoader)
    defaults = config['defaults']

env = Environment(loader=FileSystemLoader('templates'))
default_template = env.get_template(defaults['template'])

dataset = {}

# First iteration: get items metadata and generate dataset
for path in Path('content').rglob('*.md'):

    # Get frontmatter metadata
    item = frontmatter.load(path.resolve())
    metadata = {**defaults, **item.metadata}

    # Compute item link and store item in categories dataset
    metadata['link'] = str(path).replace('content/', '/').replace('.md', '.html')
    if 'id' not in metadata:
        metadata['id'] = metadata['link']
    if 'category' in metadata:
        if not metadata['category'] in dataset:
            dataset[metadata['category']] = {}
        dataset[metadata['category']][metadata['id']] = metadata

# Generate includes (lists) from dataset
for key, value in config['lists'].items():
    template = env.get_template(value['template'])
    items = dataset[value['category']].items()
    if 'sort' in value:
        items = sorted(items, key=lambda x: x[1][value['sort']], reverse=value['reverse'])
    if 'limit' in value:
        items = dict(itertools.islice(items, value['limit'])).items()
    render = template.render(list=value, items=items, config=config, data=dataset)
    Path('includes/' + key + '.html').write_text(render)

# Second iteration: render and write items
for path in Path('content').rglob('*.md'):

    # Get frontmatter metadata and body content
    item = frontmatter.load(path.resolve())
    metadata = {**defaults, **item.metadata}

    # Get included content
    for meta in metadata:
        if str(metadata[meta]).startswith('includes/'):
            metadata[meta] = Path(metadata[meta]).read_text()

    # Render body
    template = Template(item.content)
    body = template.render(metadata, config=config, data=dataset)
    metadata['body'] = markdown2.markdown(body)

    # Render item
    template = default_template
    if 'template' in metadata:
        template = env.get_template(metadata['template'])
    render = template.render(metadata, config=config, data=dataset)

    # Write item
    out = Path(str(path).replace('content/', 'public/').replace('.md', '.html'))
    Path(out.parent).mkdir(parents=True, exist_ok=True)
    out.write_text(render)
