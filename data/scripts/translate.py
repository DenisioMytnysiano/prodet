from deep_translator import GoogleTranslator
from multiprocessing import Pool, Lock

FILE_NAME = "ukrainian-news.csv"
OUTPUT_FILE = "ukrainian-news-translated.csv"
TRANSLATOR = GoogleTranslator(source="ukrainian", target="english")

LOCK = Lock()
OUT = open(OUTPUT_FILE, "a", encoding="utf-8")
PROCESSED = open("processed.txt", "a", encoding="utf-8")


def get_translated_sentence(params):
    i, line = params
    res = TRANSLATOR.translate(line)
    with LOCK:
        write_to_output(line)
        mark_as_processed(i)
    return res

def mark_as_processed(line_idx):
    PROCESSED.write(str(line_idx) + "\n")
    PROCESSED.flush()

def write_to_output(line):
    OUT.write(line + "\n")
    OUT.flush()

def get_processed_ids():
    with open("processed.txt", "r", encoding="utf-8") as f:
        return set([int(line.strip()) for line in f.readlines()])


def get_not_processed_lines():
    processed_ids = get_processed_ids()
    with open(FILE_NAME, "r", encoding="utf-8") as f:
        return [(i, line) for i, line in enumerate(f.readlines()[1:]) if i not in processed_ids]


def main():
    not_processed = get_not_processed_lines()
    with Pool(20) as pool:
        pool.map(get_translated_sentence, not_processed)


if __name__ == "__main__":
    main()
