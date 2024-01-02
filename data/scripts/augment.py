import nlpaug.augmenter.word as naw

FILE_NAME = "russian-propaganda-restructured.csv"
OUTPUT_FILE = "russian-propaganda-augmented.csv"

synonim_aug = naw.SynonymAug(aug_src="wordnet")
swap_aug = naw.RandomWordAug(action="swap")

augmenters = [
    synonim_aug,
    swap_aug,
]


def get_augmented_sentences(lines):
    result = []
    result.extend(lines)
    for augmenter in augmenters:
        result.extend(augmenter.augment(lines))
    return result


def main():
    with open(FILE_NAME, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines()[1:]]
        propaganda = get_augmented_sentences(lines)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as w:
        w.write("text\n")
        w.write("\n".join(propaganda))


if __name__ == "__main__":
    main()
