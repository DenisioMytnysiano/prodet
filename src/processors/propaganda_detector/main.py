import sys
from src.detector import init_propaganda_detector
from src.normalizer import init_propaganda_normalizer


def main():
    target = sys.argv[1]
    
    match target:
        case 'detector':
            print('Started propaganda detector')
            init_propaganda_detector()
        case 'normalizer':
            print('Started propaganda normalizer')
            init_propaganda_normalizer()
        case _:
            raise Exception(f"Unable to initialize target: {target}")

if __name__ == "__main__":
    main()
