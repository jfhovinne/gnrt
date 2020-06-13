# gnrt - lightweight, fast and extensible static site generator

## About

A lightweight static site generator written in Python.

Features:

* Markdown-based content
* Frontmatter support
* Jinja2 templating
* Optional YAML-based configuration

## Requirements

* Python 3.6+

## Installation

```
pip install --upgrade gnrt
```

## Usage

```
gnrt
```

It will look for an optional `config.yml` file in the current directory, optional Jinja2 templates in the `templates` folder, markdown files in the `content` folder, then write the generated output files in the `public` folder, while respecting the `content` folder and sub-folders structure.

## Configuration

Configuration is stored in `config.yml`. Any key-value pair is allowed. These keys and their values can be used in the content and template files.

```
---
sitename: My awesome blog
baseurl: https://example.com
language: en
foo: bar
```

If the `config.yml` file exists, `gnrt` will look for the `defaults` and `lists` entries.

### Defaults

This is where you define default configuration values, which can be overriden in content files.

Example:

```
defaults:
  template: default.j2
  bar: foo
```

### Lists

This is where lists of content are defined, allowing the generation of lists of links for instance.

Example:

```
lists:
  nav1:
  filter:
    key: category
    value: page
    template: nav-page.j2
  nav2:
    filter:
      key: category
      value: article
    sort: published
    reverse: true
    template: nav-article.j2
  rss:
    filter:
      key: category
      value: article
    sort: published
    reverse: true
    template: rss.j2
    target: public/rss.xml
```

## Example

See the example website in `docs/example`.
