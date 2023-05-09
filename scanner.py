# AmirHossein Naghi Razlighi 99102423 | Hirad Davari 99106136

import re
import os


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


def get_unclosed_comment_message():
    global file
    message = "/*"
    char = get_next_char()
    counter = 5
    while counter > 0:
        message += char
        char = get_next_char()
        counter -= 1
    file.seek(-5, os.SEEK_CUR)
    return message


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
            if not is_eof(char):
                file.seek(-1, os.SEEK_CUR)
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
            elif not (is_digit(char) or is_letter(char) or is_symbol_except_equal(char)
                      or is_whitespace(char) or char == '=' or char == '/'):
                lexeme += char
                return ('Error', 'Invalid input', line_number, '*' + lexeme)
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
            elif char == '#':
                lexeme += char
                return ('Error', 'Invalid input', line_number, lexeme)
            else:
                file.seek(-1, os.SEEK_CUR)
                token_type = 'SYMBOL'
            break
        # detect comment
        if char == '/':
            error_message = ''
            char = get_next_char()
            if is_eof(char):
                return ('Error', 'Invalid input', line_number, '/')
            elif char == '*':
                error_message = get_unclosed_comment_message() + '...'
                char = get_next_char()
                if is_eof(char):
                    return ('Error', 'Unclosed comment', line_number, error_message)
                while char:
                    if char == '*':
                        char = get_next_char()
                        if is_eof(char):
                            return ('Error', 'Unclosed comment', line_number, error_message)
                        if char == '/':
                            return get_next_token()
                    char = get_next_char()
                    if is_eof(char):
                        return ('Error', 'Unclosed comment', line_number, error_message)
            elif char == '\n':
                line_number += 1
                return ('Error', 'Invalid input', line_number - 1, '/')
            # check for EOF
            elif char == '':
                break
            elif not (is_digit(char) or is_letter(char) or is_symbol_except_equal(char)
                      or is_whitespace(char) or char == '=' or char == '/'):
                lexeme += char
                return ('Error', 'Invalid input', line_number, '/' + lexeme)
            else:
                file.seek(-1, os.SEEK_CUR)
                return ('Error', 'Invalid input', line_number, '/')
        else:
            return ('Error', 'Invalid input', line_number, char)

    return token_type, lexeme, line_number


def save_tokens_to_file(tokens):
    with open('tokens.txt', 'w') as f:
        current_line_number = None
        for token in tokens:
            if token[2] != current_line_number:
                if current_line_number is not None:
                    f.write('\n')
                current_line_number = token[2]
                f.write(str(current_line_number) + '.' + '\t')
            f.write('(' + token[0] + ', ' + token[1] + ') ')
        f.write('\n')


def save_to_errors_file(errors):
    with open('lexical_errors.txt', 'w') as f:
        current_line_number = None
        for error in errors:
            if error[2] != current_line_number:
                if current_line_number is not None:
                    f.write('\n')
                current_line_number = error[2]
                f.write(str(current_line_number) + '.' + '\t')
            f.write('(' + error[-1] + ', ' + error[1] + ') ')
        if len(errors) == 0:
            f.write('There is no lexical error.')
        else:
            f.write('\n')


def save_to_symbols_file(symbol_table):
    counter = 1
    keywords = ['break', 'else', 'if', 'int',
                'repeat', 'return', 'until', 'void']

    with open('symbol_table.txt', 'w') as f:
        for keyword in keywords:
            f.write(str(counter) + '.' + '\t' + keyword + '\n')
            counter += 1

        for index, identifier in enumerate(symbol_table):
            if index != len(symbol_table) - 1:
                f.write(str(counter) + '.' + '\t' + identifier + '\n')
            else:
                f.write(str(counter) + '.' + '\t' + identifier)
            counter += 1
        f.write('\n')


def main():
    global file
    global line_number
    global tokens
    global errors
    global symbol_table

    file = open('input.txt', 'rb')
    line_number = 1
    tokens = []
    errors = []
    symbol_table = []

    while True:
        token = get_next_token()
        if token is None or token[0] is None:
            break
        if token[0] == 'Error':
            errors.append(token)
        else:
            if token[0] == 'ID':
                if token[1] not in symbol_table:
                    symbol_table.append(token[1])
            tokens.append(token)
        # print(token)

    save_tokens_to_file(tokens)
    save_to_errors_file(errors)
    save_to_symbols_file(symbol_table)


if __name__ == '__main__':
    main()
