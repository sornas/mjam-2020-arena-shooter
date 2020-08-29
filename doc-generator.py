import ribs
from inspect import ismodule, isfunction

docs = []
for name, val in ribs.__dict__.items():
    if name[0] == "_": continue
    if ismodule(val): continue

    if isfunction(val):
        docs.append((name, val, val.__doc__))
    elif name.isupper():
        docs.append((name, val, "constant"))


def gen_doc(name, docstring):
    if docstring == "constant":
        return f"<h2 id='{name}' class='constant'>name</h2>"
    else:
        docstring = docstring.replace('\n\n', '<br>')
        return f"<div id='{name}' class='func'><h2>name</h2><p>{docstring}</p></div>"


docs = sorted(docs, key=lambda x: isfunction(x[1]))
print(ribs.__dict__)
print("\n".join([gen_doc(x[0], x[2]) for x in docs]))
