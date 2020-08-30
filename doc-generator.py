from dataclasses import dataclass
import pygments
import pygments.lexers as lexers
import pygments.formatters.html as formatters
pygment_lexer = lexers.get_lexer_for_filename("what.py")
pygment_format = formatters.HtmlFormatter()

def highlight(code):
    return pygments.highlight(code, pygment_lexer, pygment_format)


def gen_id(string):
    return string.split("(")[0].replace(".", "_")


def gen_doc(name, docstrings):
    def format_doc(i, x):
        if i == 0:
            classname = "docstr explain"
            prefix = "Doc"
        else:
            classname = "docstr example"
            prefix = "Ex"

        while True:
            start_glyph = "!--"
            end_glyph = "--!"
            if not (start_glyph in x and end_glyph in x):
                break
            start = x.index(start_glyph)
            end = x.index(end_glyph)
            block = x[start+len(start_glyph):end]
            formatted = highlight(block).strip()
            x = x[:start] + formatted + x[end+len(end_glyph):]
            print(x)

        return f"<div class='{classname}'><div class='header {prefix}'>{prefix}</div><div class='content'>" + x.replace('\n\n', '<br>') + "</div></div>"

    id_name = gen_id(name)
    if docstrings:
        out = "".join([format_doc(i, x) for i, x in enumerate(docstrings)])
        return f"<div id='{id_name}' class='func'><h2 class='title'>{name}</h2>{out}</div>"
    else:
        return f"<h2 id='{id_name}' class='constant'>{name}</h2>"

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


style = open("style.css", "r").read()
style += pygment_format.get_style_defs()
pg_docs = parse_docs("pygame.docs")
sr_docs = parse_docs("ribs.docs")
with open("docs.html", "w+") as f:
    intro = "<h1>TODO INTRO</h1>"
    toc = "<h1>TODO TOC</h1>"
    f.write("<!--- This file is auto generated, please do not edit -->")
    f.write(f"<html><head><title>Documentation</title><style>{style}</style></head><body>")
    f.write(intro)
    f.write(toc)
    f.write("<hr><div id='pygame'>")
    f.write("".join([gen_doc(x.name, x.docs) for x in pg_docs]))
    f.write("</div><hr><div id='lithekod'>")
    f.write("".join([gen_doc(x.name, x.docs) for x in sr_docs]))
    f.write("</body></html>")
