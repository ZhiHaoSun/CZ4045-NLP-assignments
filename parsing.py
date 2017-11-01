import ATD
from nltk.parse.corenlp import CoreNLPParser
import hashlib
import random
from nltk import word_tokenize
h = hashlib.md5()
h.update('zpiao1'.encode())
key = h.hexdigest()

ATD.setDefaultKey(key)

parser = CoreNLPParser()


def correct(line, errors):
    correct_line = line
    for error in errors:
        correct_line = correct_line.replace(error.string, error.suggestions[0])
    return correct_line


with open('stackoverflow_content', encoding='utf-8') as f:
    lines = [line.strip() for line in f]
    lines = [line for line in lines if line != ''
             and len(word_tokenize(line)) <= 10
             and line[-1] in '.?!'
             and line[0].isupper()]
    print(len(lines))
    wrong_lines_count = 0
    for line in lines:
        print(line, end=' ')
        if wrong_lines_count == 5:
            break
        errors = ATD.checkDocument(line)
        if len(list(errors)) == 0:
            print('**No errors**')
            continue
        else:
            print()
        correct_line = correct(line, errors)
        print('Original line: ' + line)
        tree = next(parser.raw_parse(line))
        tree.pretty_print()
        print('Correct line: ' + correct_line)
        correct_tree = next(parser.raw_parse(correct_line))
        correct_tree.pretty_print()
        wrong_lines_count += 1
