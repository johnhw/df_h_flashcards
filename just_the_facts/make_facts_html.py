from pathlib import Path

def read_template():
    with open("template.html", "r") as f:
        return f.read()


def read_style():
    with open("just_the_facts.css", "r") as f:
        return f.read()


def get_separator(name):
    return (
        '<div class="separator"> <div class="separator-text">' + name + "</div></div>"
    )


def convert_to_html_with_mathjax(input_text):
    # # Regular expression to find LaTeX math expressions
    # latex_pattern = r"\$\$(.*?)\$\$|\$(.*?)\$"

    # # Replace LaTeX math expressions with MathJAX format
    # def mathjax_repl(match):
    #     latex_math = match.group(1) or match.group(2)
    #     return f'<span class="mathjax">{latex_math}</span>'

    # # Convert LaTeX math expressions to MathJAX format
    # modified_text = re.sub(latex_pattern, mathjax_repl, input_text, flags=re.DOTALL)

    # Convert the modified text to HTML using markdown
    return input_text
    


def generate_html(fname, input_string):
    rows = input_string.strip().split("\n")
    cards_html = get_separator(fname)
    cards_html += "<div class='card-container'>"
    for row in rows:
        title, *content = row.split(";")
        content = ";".join(content)
        card_type = "card" if "$$" not in content else "card wide-card"
        card_html = f"""
            <div class="{card_type}">
                <div class="top-half">
                    <p class="card-title">{title}</p>
                </div>
                <div class="bottom-half">
                    <p>{content}</p>
                </div>
            </div>
        """
        cards_html += card_html
    cards_html += "</div>"
    return cards_html


def read_all_cards(path):
    cards = path.glob("*.txt")
    for c in cards:
        with open(c, "r") as f:
            yield c, convert_to_html_with_mathjax(f.read())


template = read_template()

cards_html = ""
for fname, card in read_all_cards(Path("..")):
    fname = fname.stem
    fname = fname.replace("_", " ")
    fname = fname.title()
    cards_html += generate_html(fname, card)

template = template.replace("{{STYLE}}", read_style())
template = template.replace("{{CONTENT}}", cards_html)

with open("facts.html", "w") as f:
    f.write(template)
