# Introduction
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

## Contributing
Please see [here](https://github.com/tasuren/tempylate/blob/main/contributing.md).

## License
tempylate is available under the MIT license.  
Detail: [LICENSE](https://github.com/tasuren/tempylate/blob/main/LICENSE)