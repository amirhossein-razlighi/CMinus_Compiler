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
    matched = re.match(r'[ \t \f \r \v]', char)
    if char == '\n':
        line_number += 1
        return True
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
    token_type = None
    lexeme = ''

    char = file.read(1)

    while char:
        if type(char) is not str:
            char = char.decode('utf-8')
        if is_eof(char):
            print('EOF')
            break
        # skip white space (whitespace, \n, \t, \f, \r, \v)
        if is_whitespace(char):
            char = get_next_char()
            continue
        if is_digit(char):
            lexeme += char
            char = get_next_char()
            if is_eof(char):
                token_type = 'NUM'
                break
            if is_letter(char):
                print('Error: invalid token')
                print(f'char is {char} ')
                print('IN DIGIT')
                return None
            while is_digit(char):
                lexeme += char
                char = get_next_char()
                if is_eof(char):
                    token_type = 'NUM'
                    break
                if is_letter(char):
                    print('Error: invalid token')
                    print(f'char is {char} ')
                    print('IN DIGIT')
                    return None
            file.seek(- 1, os.SEEK_CUR)
            token_type = 'NUM'
            break
        if is_letter(char):
            lexeme += char
            char = get_next_char()
            if is_eof(char):
                if is_keyword(lexeme):
                    token_type = 'KEYWORD'
                else:
                    token_type = 'ID'
                break
            if not (is_letter(char) or is_digit(char) or is_whitespace(char)):
                print('Error: invalid token')
                print(f'char is {char} ')
                print('IN LETTER')
                file.seek(-1, os.SEEK_CUR)
                return None
            while is_letter(char) or is_digit(char):
                lexeme += char
                char = get_next_char()
                if is_eof(char):
                    if is_keyword(lexeme):
                        token_type = 'KEYWORD'
                    else:
                        token_type = 'ID'
                    break
                if not (is_letter(char) or is_digit(char) or is_whitespace(char)):
                    print('Error: invalid token')
                    print(f'char is {char} ')
                    print('IN LETTER2')
                    file.seek(-1, os.SEEK_CUR)
                    return None
            if is_keyword(lexeme):
                token_type = 'KEYWORD'
            else:
                token_type = 'ID'
            break
        if is_symbol_except_equal(char):
            lexeme += char
            token_type = 'SYMBOL'
            break
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
                file.seek(- 1, os.SEEK_CUR)
                token_type = 'SYMBOL'
            break
        if char == '/':
            # detect comment
            char = get_next_char()
            if is_eof(char):
                print('Error: invalid token')
                print(f'char is {char} ')
                print('IN COMMENT')
                return None
            if char == '*':
                char = get_next_char()
                if is_eof(char):
                    print('Error: invalid token')
                    print(f'char is {char} ')
                    print('IN COMMENT')
                    return None
                while char:
                    if char == '*':
                        char = get_next_char()
                        if is_eof(char):
                            print('Error: invalid token')
                            print(f'char is {char} ')
                            print('IN COMMENT')
                            return None
                        if char == '/':
                            continue
                    char = get_next_char()
                    if is_eof(char):
                        print('Error: invalid token')
                        print(f'char is {char} ')
                        print('IN COMMENT')
                        return None
                continue
            if char == '':
                continue
            else:
                file.seek(-1, os.SEEK_CUR)
                print('Error: invalid token')
                print(f'char is {char} ')
                print('IN /')
                return None
    return token_type, lexeme


if __name__ == '__main__':
    main()
