# tempylate - test

from timeit import timeit

from tempylate import Template, Manager


TEMPLATE = """This is the test template.
I can run python on tempylate: ^^ from random import randint
str(randint(1, 6)) ^^, ^^ f"FromPython: {value}" ^^"""


print("Normal")
print(Template("""This is the test template.
I can run python on tempylate: ^^ from random import randint
str(randint(1, 6)) ^^, ^^ f"FromPython: {value}" ^^""").render(value="Hello"))


print("Manager")
manager = Manager({"a": 1})
render = lambda: manager.render(TEMPLATE, "test", value="Hello")
print(timeit(render, number=1))
print(timeit(render, number=100))
print(render())