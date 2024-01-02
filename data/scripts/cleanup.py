import re

FILE_NAME = "russian-propaganda-raw.csv"
OUTPUT_FILE = "russian-propaganda-restructured.csv"


def is_row_start(row: str) -> bool:
    data = row.split(",")
    return data and data[0].isdigit()


def line_to_skip(line: str) -> bool:
    return not line.strip()


def normalize_line(p: str) -> str:
    if p.startswith('"'):
        p = p[1:-2]
    p = p.strip()
    p = p.replace("\n", "")
    p = p.replace("&nbsp;", "")
    p = p.replace('""', '"')
    p = p.replace("/", "")
    p = p.replace("...", "")
    p = p.replace("[...]", "")
    p = p.replace("[---]", "")
    p = p.replace("[--]", "")
    p = p.replace("[]", "")
    p = re.sub(" +", " ", p)
    return p


def main():
    propaganda = []
    with open(FILE_NAME, "r", encoding="utf-8") as f:
        f.readline()
        line = f.readline()
        while line:
            if line_to_skip(line):
                line = f.readline()
                continue
            if is_row_start(line):
                propaganda.append(line[line.index(",") + 1 :])
            else:
                propaganda[-1] += line
            line = f.readline()

    with open(OUTPUT_FILE, "w", encoding="utf-8") as w:
        w.write("text\n")
        for p in set(propaganda):
            w.write(normalize_line(p) + "\n")


if __name__ == "__main__":
    main()
