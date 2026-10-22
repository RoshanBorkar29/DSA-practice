import re
sheet = {
    "A1": 10,
    "A2": 20,
    "A3": "=A1+A2",
    "A4": "=A3*2",
    "A5": "=A4-A1"
}

def evaluate(cell):
    value=sheet[cell]
    if isinstance(value,int):
        return value

    expression=value[1:]
    refs=re.findall(r"[A-Z]\d+",expression)
    for ref in refs:
        expression=expression.replace(ref,str(evaluate(ref)))

    answer=eval(expression)
    sheet[cell]=answer


for cell in list(sheet.keys()):
    evaluate(cell)

print(sheet)