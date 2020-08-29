import ribs
from inspect import ismodule, isfunction
from dataclasses import dataclass

sr_docs = []
for name, val in ribs.__dict__.items():
    if name[0] == "_": continue
    if ismodule(val): continue

    if isfunction(val):
        sr_docs.append((name, val, [val.__doc__]))
    elif name.isupper():
        sr_docs.append((name, val, []))


def gen_doc(name, docstrings):
    def format_doc(x):
        return "<div class='docstr'>" + x.replace('\n\n', '<br>') + "</div>"

    if docstrings:
        out = "".join([format_doc(x) for x in docstrings])
        return f"<div id='{name}' class='func'><h2>{name}</h2><p>{out}</p></div>"
    else:
        return f"<h2 id='{name}' class='constant'>{name}</h2>"

@dataclass
class Docs:
    name: str = "NO NAME"
    docs = None


def parse_docs(filename):
    with open(filename, "r") as f:
        res = []
        doc = Docs()
        block = ""
        for line in f:
            if line.startswith("# "):
                if block:
                    doc.docs.append(block)
                    block = ""
                    res.append(doc)

                doc = Docs()
                doc.docs = []
                doc.name = line[2:].strip()

            elif line.startswith("## ex"):
                if block:
                    doc.docs.append(block)
                    block = ""

            else:
                block += line
        if block:
            doc.docs.append(block)
            block = ""
            res.append(doc)
        return res


pg_docs = parse_docs("pygame.docs")
sr_docs = sorted(sr_docs, key=lambda x: isfunction(x[1]))
with open("docs.html", "w+") as f:
    intro = "<!--- This file is auto generated, please do not edit --><h1>TODO INTRO</h1>"
    toc = "<h1>TODO TOC</h1>"
    f.write(intro)
    f.write(toc)
    f.write("<hr>")
    f.write("".join([gen_doc(x.name, x.docs) for x in pg_docs]))
    f.write("<hr>")
    f.write("".join([gen_doc(x[0], x[2]) for x in sr_docs]))
