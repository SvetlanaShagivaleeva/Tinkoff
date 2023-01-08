import sys
import argparse
import ast


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str, help='Input text file')
    parser.add_argument('output', type=str, help='Output text file')
    return parser.parse_args()


def Levenshtein_distance(code1, code2):
    n, m = len(code1), len(code2)
    if n < m:
        code1, code2 = code2, code1
        n, m = m, n

    cur_row = range(m+1)
    for i in range(1, n + 1):
        prev_row, cur_row = cur_row, [1] + [0]*m
        for j in range(1, m + 1):
            add, delete, change = prev_row[j] + 1, cur_row[j - 1] + 1, prev_row[j - 1]
            if code2[j - 1] != code1[i - 1]:
                change += 1
            cur_row[j] = min(add, delete, change)

    return 1 - (cur_row[m] / n)


def counting_plagiat_score(file1, file2):
    with open(file1) as f:
        code1 = f.read()
    with open(file2) as f:
        code2 = f.read()
    score = Levenshtein_distance(code1.lower(), code2.lower())
    return score


def main():
    args = parse_args()
    input_file = args.input
    output_file = args.output

    f_input = open(input_file, 'r')
    f_output = open(output_file, 'w')
    for line in f_input:
        file1, file2 = line.split()
        score = counting_plagiat_score(file1, file2)
        f_output.write(str(score) + '\n')


if __name__ == '__main__':
    sys.exit(main())
