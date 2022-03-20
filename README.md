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

You may need to add `$HOME/.local/bin` to your `$PATH`.

## Usage

```
gnrt
```

`gnrt` will look for an optional `config.yml` file in the current working directory, optional Jinja2 templates in the `templates` folder, markdown files in the `content` folder, then write the generated output files in the `public` folder, while respecting the `content` folder and sub-folders structure.

To get a list of options, use:

```
gnrt -h
```

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

This is where you define default configuration values, which can be overridden in content files.

Example:

```
defaults:
  template: default.j2
  markdown-extras:
    - break-on-newline
    - fenced-code-blocks
  nav: includes/nav.html
  bar: foo
```

#### Reserved keys

These keys have a specific meaning, and their values can be overridden in content files, like any other `default`.

* `markdown-extras`: allows to enable Markdown extensions, see [Extras](https://github.com/trentm/python-markdown2/wiki/Extras) for a list of values
* `template`: sets the default [Jinja template](https://jinja.palletsprojects.com/en/3.0.x/) to be used while rendering content files

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

Lists can select content through a `filter`, which gets a metadata `key` and a `value` to match.

They can be sorted by metadata value (e.g. a published date, an integer, ...), in forward (default) or `reverse` order.

During rendering, the generated content is saved in the `includes` folder (for caching), while the file path can be customized through the `target` key. This allows to generate a RSS feed for instance.

## Content files

Content files have the `.md` extension and are stored in the `content` folder.

### Frontmatter

Content files may have a [frontmatter](https://python-frontmatter.readthedocs.io/en/latest/) - i.e. structured metadata - written in YAML.

This is where default values can be overridden.

Example:

```
---
id: home
title: Home
link: /
nav-order: 3
---
```

#### Reserved keys

* `id`: the current item identifier, which can be used in any content file to access this item's metadata
* `link`: URL of the generated page
* `target`: path of the generated file
* `title`: title of the current item

### Body

Content `body` is written in [Markdown](https://daringfireball.net/projects/markdown/).

It may also contain Jinja2 syntax and placeholders, allowing injection of `dataset` values, such as links to other pages:

```
Check the [about]({{ data.about.link }}) page or read the [articles]({{ data.articles.link }})!
```

## Example

See the example website in `docs/example`, which you can generate by installing `gnrt`, cloning this repository, moving to `gnrt/docs/example` and executing `gnrt`.

You can then browse it at `http://localhost:8080/` by moving to the generated `public` folder and executing `python3 -m http.server 8080`.

You may also want to check a [live gnrt-generated blog](https://hovinne.com/) and read this [article about gnrt](https://hovinne.com/articles/gnrt-static-site-generator.html).
