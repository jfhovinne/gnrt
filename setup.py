import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='gnrt',
    version='0.1.0',
    author='jfhovinne',
    author_email='gnrt@hovinne.com',
    description='A fast and lightweight static site generator',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/jfhovinne/gnrt',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
    ],
    python_requires='>=3.6',
    install_requires=[
        'jinja2',
        'markdown2',
        'python-frontmatter',
        'pyyaml',
    ],
)
