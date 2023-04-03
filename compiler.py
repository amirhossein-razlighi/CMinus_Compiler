# This is an implimantation of a C-minus compiler(scanner module)
# It is a part of the C-minus compiler project

import re
import os


def main():
    global file
    global line_number
    file = open('input.txt', 'rb')
    line_number = 1
    while True:
        token = get_next_token()
        if token is None or token[0] is None:
            break
        print(token)


def is_digit(char):
    matched = re.match(r'[0-9]', char)
    return matched is not None


def is_whitespace(char):
    global line_number
    matched = re.match(r'(\s|\t|\v|\f|\r|\n)', char)
    return matched is not None


def is_letter(char):
    matched = re.match(r'[A-Za-z]', char)
    return matched is not None


def is_keyword(word):
    matched = re.match(r'(if|else|void|int|repeat|break|until|return)', word)
    return matched is not None


def is_symbol_except_equal(char):
    matched = re.match(
        r'(\+|-|\*|<|;|:|\(|\)|\[|\]|{|}|,)', char)
    return matched is not None


def is_eof(char):
    return char == ''


def get_next_char():
    global file
    char = file.read(1)
    if type(char) is not str:
        char = char.decode('utf-8')
    return char


def get_next_token():
    global file
    global line_number
    token_type = None
    lexeme = ''

    char = file.read(1)

    while char:
        if type(char) is not str:
            char = char.decode('utf-8')
        if is_eof(char):
            return None

        # skip white space (whitespace, \n, \t, \f, \r, \v)
        if is_whitespace(char):
            if char == '\n':
                line_number += 1
            char = get_next_char()
            continue
        # detect number
        if is_digit(char):
            lexeme += char
            char = get_next_char()
            if is_eof(char):
                token_type = 'NUM'
                break
            if is_letter(char):
                lexeme += char
                return ('Error', 'Invalid number', line_number, lexeme)
            while is_digit(char):
                lexeme += char
                char = get_next_char()
                if is_eof(char):
                    token_type = 'NUM'
                    break
                if is_letter(char):
                    lexeme += char
                    return ('Error', 'Invalid number', line_number, lexeme)
            file.seek(- 1, os.SEEK_CUR)
            token_type = 'NUM'
            break
        # detect identifier and keyword
        if is_letter(char):
            lexeme += char
            char = get_next_char()
            if is_eof(char):
                if is_keyword(lexeme):
                    token_type = 'KEYWORD'
                else:
                    token_type = 'ID'
                break
            if not (is_letter(char) or is_digit(char) or is_whitespace(char) or is_symbol_except_equal(char) or char == '='):
                file.seek(-1, os.SEEK_CUR)
                return ('Error', 'Invalid input', line_number, lexeme)
            if not is_letter(char) and not is_digit(char):
                file.seek(-1, os.SEEK_CUR)

            while is_letter(char) or is_digit(char):
                lexeme += char
                char = get_next_char()
                if is_eof(char):
                    if is_keyword(lexeme):
                        token_type = 'KEYWORD'
                    else:
                        token_type = 'ID'
                    break
                if not (is_letter(char) or is_digit(char) or is_whitespace(char) or is_symbol_except_equal(char) or char == '='):
                    lexeme += char
                    return ('Error', 'Invalid input', line_number, lexeme)
                if not is_letter(char) and not is_digit(char):
                    file.seek(-1, os.SEEK_CUR)
            if is_keyword(lexeme):
                token_type = 'KEYWORD'
            else:
                token_type = 'ID'
            break
        # detect unmatched comment
        if char == '*':
            char = get_next_char()
            if is_eof(char):
                lexeme += '*'
                token_type = 'SYMBOL'
                break
            if char == '/':
                return ('Error', 'Unmatched comment', line_number, '*/')
            else:
                file.seek(-1, os.SEEK_CUR)
                lexeme += '*'
                token_type = 'SYMBOL'
                break
        # detect symbol - {=, ==}
        if is_symbol_except_equal(char):
            lexeme += char
            token_type = 'SYMBOL'
            break
        # detect = and ==
        if char == '=':
            lexeme += char
            char = get_next_char()
            if is_eof(char):
                token_type = 'SYMBOL'
                break
            if char == '=':
                lexeme += char
                token_type = 'SYMBOL'
            else:
                file.seek(-1, os.SEEK_CUR)
                token_type = 'SYMBOL'
            break
        # detect comment
        if char == '/':
            char = get_next_char()
            if is_eof(char):
                return ('Error', 'Invalid input', line_number, '/')
            elif char == '*':
                char = get_next_char()
                if is_eof(char):
                    return ('Error', 'Unclosed comment', line_number, '/*')
                while char:
                    if char == '*':
                        char = get_next_char()
                        if is_eof(char):
                            return ('Error', 'Unclosed comment', line_number, '/*')
                        if char == '/':
                            return get_next_token()
                    char = get_next_char()
                    if is_eof(char):
                        return ('Error', 'Unclosed comment', line_number, '/*')
            if char == '\n':
                line_number += 1
                continue
            # check for EOF
            elif char == '':
                break
            else:
                file.seek(-1, os.SEEK_CUR)
                return ('Error', 'Invalid input', line_number, '/')
        else:
            return ('Error', 'Invalid input', line_number, char)

    return token_type, lexeme, line_number


if __name__ == '__main__':
    main()
