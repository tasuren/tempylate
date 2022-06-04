# tempylate - test

from tempylate import Template


print(Template("""This is the test template.
I can run python on tempylate: ^^ from random import randint
str(randint(1, 6)) ^^, ^^ f"FromPython: {value}" ^^"""
).render(value="Hello"))