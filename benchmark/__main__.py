# tempylate - Benchmark

from dataclasses import dataclass
from random import randint

from flask import Flask, render_template
try:
    import tempylate
except ImportError:
    from sys import path as spath
    spath.insert(0, __file__[:-22])
    import tempylate

app = Flask(__name__)
manager = tempylate.Manager({"app": app})

@dataclass
class Team:
    name: str
    score: int

rstring = lambda : "".join(map(str, range(7)))

generate_team = lambda : (Team(rstring(), randint(1, 100)) for _ in range(50))

@app.get("/tempylate")
def miko_test():
    return manager.render_from_file("benchmark/templates/tempylate.html", year=rstring(), teams=generate_team())

@app.get("/jinja")
def jinja_test():
    return render_template("jinja.html", year=rstring(), teams=generate_team())

app.run()