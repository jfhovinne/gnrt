#!/usr/bin/python3

from pathlib import Path
import itertools
import frontmatter
import markdown2
import yaml
from jinja2 import Environment, FileSystemLoader, Template

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
        Path(value['target']).write_text(render)
    else:
        Path('includes/' + key + '.html').write_text(render)

print("Generated %d includes" % len(config['lists']))

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
    template = default_template
    if 'template' in item:
        template = env.get_template(item['template'])
    render = template.render(item, config=config, data=dataset)

    # Write item
    out = Path(item['target'])
    Path(out.parent).mkdir(parents=True, exist_ok=True)
    out.write_text(render)

print("Generated %d targets" % len(dataset))
