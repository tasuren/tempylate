[![PyPI](https://img.shields.io/pypi/v/tempylate)](https://pypi.org/project/tempylate/) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/tempylate) ![PyPI - Downloads](https://img.shields.io/pypi/dm/tempylate) ![PyPI - License](https://img.shields.io/pypi/l/tempylate) [![Documentation Status](https://readthedocs.org/projects/tempylate/badge/?version=latest)](https://tempylate.readthedocs.io/en/latest/?badge=latest) [![Discord](https://img.shields.io/discord/777430548951728149?label=chat&logo=discord)](https://discord.gg/kfMwZUyGFG) [![Buy Me a Coffee](https://img.shields.io/badge/-tasuren-E9EEF3?label=Buy%20Me%20a%20Coffee&logo=buymeacoffee)](https://www.buymeacoffee.com/tasuren)
# tempylate
tempylate is a pythonic template engine that is little, lightweight and fast.

**Features:**
* Full python syntax. So there is absolutely nothing to remember in the syntax.
* It runs in Python.
* Little, lightweight and fast. (No dependency)
* Inheriting layouts through template inheritance.
* Easy to use!

## Installation
You can install it using pip.  
`$ pip install tempylate`

## Examples
### Title
```html
<title>^^ title ^^</title>
```
### Members
```python
<body>
  <h1>^^ team.name ^^ members</h1>
  <ul>
    ^^
      "".join(
        f'<li><a href="{ member.url }">{ member.name }</a></li>'
        for member in team.members
      )
    ^^
  </ul>
</body>
```
### Inheritance
```python
^^
  self.manager.render_from_file(
      "blog_page_layout.html", title="My sixteenth birthday.",
      content="""
        <strong>Today is my birthday!</strong><br>
        So give me a gift.
      """
  )
^^
```

## Documentation
You can view the UserGuide and API reference of tempylate [here](https://tempylate.readthedocs.io/en/latest).  

## Contributing
Please see `./contributing.md`.

## License
tempylate is available under the MIT license.  
Detail: [LICENSE](https://github.com/tasuren/tempylate/blob/main/LICENSE)