line = input()
out = ""
while line != "":
    out += "".join(line.split())
    line = input()
    if line != "" and line is not None:
        out += ','
print(out)