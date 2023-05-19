# AmirHossein Naghi Razlighi 99102423 | Hirad Davari 99106136
# scanner component of C-Minus compiler. When parser calls get_next_token(), this component's class
# attribute current_token will change and with the getter of this component, parser can access to
# current token.

import os


class Scanner:
    def __init__(self, filename):
        self.current_token = None
        self.line_number = 1
        self.file = open(filename, "rb")
        if self.file == None:
            return None

    # @getattr(line_number, "line_number")
    def get_line_number(self):
        return self.line_number

    # @getattr(current_token, "current_token")
    def get_current_token(self):
        return self.current_token

    def is_digit(self, char):
        # without using regex
        return char in "0123456789"

    def is_whitespace(self, char):
        # without regex
        return char in " \t\v\f\r\n"

    def is_letter(self, char):
        # without regex
        return char in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

    def is_keyword(self, word):
        # without regex
        return word in [
            "if",
            "else",
            "void",
            "int",
            "repeat",
            "break",
            "until",
            "return",
        ]

    def is_symbol_except_equal(self, char):
        # without regex
        return char in "+-*<;:()[]{},"

    def is_eof(self, char):
        return char == ""

    def get_next_char(self):
        char = self.file.read(1)
        if type(char) is not str:
            char = char.decode("utf-8")
        return char

    def get_unclosed_comment_message(self):
        message = "/*"
        char = self.get_next_char()
        counter = 5
        while counter > 0:
            message += char
            char = self.get_next_char()
            counter -= 1
        self.file.seek(-5, os.SEEK_CUR)
        return message

    def get_next_token(self):
        temp = self.get_next_token_internal()
        while temp[0] == "Error":
            temp = self.get_next_token_internal()
        return temp

    def get_next_token_internal(self):
        token_type = "$"
        lexeme = ""

        char = self.file.read(1)

        # check if the file has ended, return $ token
        if self.is_eof(char):
            self.current_token = ("$", "$", self.line_number, "$")
            return self.current_token

        while char:
            if type(char) is not str:
                char = char.decode("utf-8")
            if self.is_eof(char):
                self.current_token = ("$", "$", self.line_number, "$")
                return self.current_token

            # skip white space (whitespace, \n, \t, \f, \r, \v)
            if self.is_whitespace(char):
                if char == "\n":
                    self.line_number += 1
                char = self.get_next_char()
                continue
            # detect number
            if self.is_digit(char):
                lexeme += char
                char = self.get_next_char()
                if self.is_eof(char):
                    token_type = "NUM"
                    break
                if self.is_letter(char):
                    lexeme += char
                    return ("Error", "Invalid number", self.line_number, lexeme)
                while self.is_digit(char):
                    lexeme += char
                    char = self.get_next_char()
                    if self.is_eof(char):
                        token_type = "NUM"
                        break
                    if self.is_letter(char):
                        lexeme += char
                        return ("Error", "Invalid number", self.line_number, lexeme)
                if not self.is_eof(char):
                    self.file.seek(-1, os.SEEK_CUR)
                token_type = "NUM"
                break
            # detect identifier and keyword
            if self.is_letter(char):
                lexeme += char
                char = self.get_next_char()
                if self.is_eof(char):
                    if self.is_keyword(lexeme):
                        token_type = "KEYWORD"
                    else:
                        token_type = "ID"
                    break
                if not (
                    self.is_letter(char)
                    or self.is_digit(char)
                    or self.is_whitespace(char)
                    or self.is_symbol_except_equal(char)
                    or char == "="
                ):
                    self.file.seek(-1, os.SEEK_CUR)
                    return ("Error", "Invalid input", self.line_number, lexeme)
                if not self.is_letter(char) and not self.is_digit(char):
                    self.file.seek(-1, os.SEEK_CUR)

                while self.is_letter(char) or self.is_digit(char):
                    lexeme += char
                    char = self.get_next_char()
                    if self.is_eof(char):
                        if self.is_keyword(lexeme):
                            token_type =  "KEYWORD"
                        else:
                            token_type = "ID"
                        break
                    if not (
                        self.is_letter(char)
                        or self.is_digit(char)
                        or self.is_whitespace(char)
                        or self.is_symbol_except_equal(char)
                        or char == "="
                    ):
                        lexeme += char
                        return ("Error", "Invalid input", self.line_number, lexeme)
                    if not self.is_letter(char) and not self.is_digit(char):
                        self.file.seek(-1, os.SEEK_CUR)
                if self.is_keyword(lexeme):
                    token_type = "KEYWORD"
                else:
                    token_type = "ID"
                break
            # detect unmatched comment
            if char == "*":
                char = self.get_next_char()
                if self.is_eof(char):
                    lexeme += "*"
                    token_type = "SYMBOL"
                    break
                if char == "/":
                    return ("Error", "Unmatched comment", self.line_number, "*/")
                elif not (
                    self.is_digit(char)
                    or self.is_letter(char)
                    or self.is_symbol_except_equal(char)
                    or self.is_whitespace(char)
                    or char == "="
                    or char == "/"
                ):
                    lexeme += char
                    return ("Error", "Invalid input", self.line_number, "*" + lexeme)
                else:
                    self.file.seek(-1, os.SEEK_CUR)
                    lexeme += "*"
                    token_type = "SYMBOL"
                    break
            # detect symbol - {=, ==}
            if self.is_symbol_except_equal(char):
                lexeme += char
                token_type = "SYMBOL"
                break
            # detect = and ==
            if char == "=":
                lexeme += char
                char = self.get_next_char()
                if self.is_eof(char):
                    token_type = "SYMBOL"
                    break
                if char == "=":
                    lexeme += char
                    token_type = "SYMBOL"
                elif char == "#":
                    lexeme += char
                    return ("Error", "Invalid input", self.line_number, lexeme)
                else:
                    self.file.seek(-1, os.SEEK_CUR)
                    token_type = "SYMBOL"
                break
            # detect comment
            if char == "/":
                error_message = ""
                char = self.get_next_char()
                if self.is_eof(char):
                    return ("Error", "Invalid input", self.line_number, "/")
                elif char == "*":
                    error_message = self.get_unclosed_comment_message() + "..."
                    char = self.get_next_char()
                    if self.is_eof(char):
                        return (
                            "Error",
                            "Unclosed comment",
                            self.line_number,
                            error_message,
                        )
                    while char:
                        if char == "*":
                            char = self.get_next_char()
                            if self.is_eof(char):
                                return (
                                    "Error",
                                    "Unclosed comment",
                                    self.line_number,
                                    error_message,
                                )
                            if char == "/":
                                return self.get_next_token()
                        char = self.get_next_char()
                        if self.is_eof(char):
                            return (
                                "Error",
                                "Unclosed comment",
                                self.line_number,
                                error_message,
                            )
                elif char == "\n":
                    self.line_number += 1
                    return ("Error", "Invalid input", self.line_number - 1, "/")
                # check for EOF
                elif char == "":
                    break
                elif not (
                    self.is_digit(char)
                    or self.is_letter(char)
                    or self.is_symbol_except_equal(char)
                    or self.is_whitespace(char)
                    or self.char == "="
                    or self.char == "/"
                ):
                    lexeme += char
                    return ("Error", "Invalid input", self.line_number, "/" + lexeme)
                else:
                    self.file.seek(-1, os.SEEK_CUR)
                    return ("Error", "Invalid input", self.line_number, "/")
            else:
                return ("Error", "Invalid input", self.line_number, char)

        self.current_token = (token_type, lexeme, self.line_number)
        return token_type, lexeme, self.line_number


def save_tokens_to_file(tokens):
    with open("tokens.txt", "w") as f:
        current_line_number = None
        for token in tokens:
            if token[2] != current_line_number:
                if current_line_number is not None:
                    f.write("\n")
                current_line_number = token[2]
                f.write(str(current_line_number) + "." + "\t")
            f.write("(" + token[0] + ", " + token[1] + ") ")
        f.write("\n")


def save_to_errors_file(errors):
    with open("lexical_errors.txt", "w") as f:
        current_line_number = None
        for error in errors:
            if error[2] != current_line_number:
                if current_line_number is not None:
                    f.write("\n")
                current_line_number = error[2]
                f.write(str(current_line_number) + "." + "\t")
            f.write("(" + error[-1] + ", " + error[1] + ") ")
        if len(errors) == 0:
            f.write("There is no lexical error.")
        else:
            f.write("\n")


def save_to_symbols_file(symbol_table):
    counter = 1
    keywords = ["break", "else", "if", "int", "repeat", "return", "until", "void"]

    with open("symbol_table.txt", "w") as f:
        for keyword in keywords:
            f.write(str(counter) + "." + "\t" + keyword + "\n")
            counter += 1

        for index, identifier in enumerate(symbol_table):
            if index != len(symbol_table) - 1:
                f.write(str(counter) + "." + "\t" + identifier + "\n")
            else:
                f.write(str(counter) + "." + "\t" + identifier)
            counter += 1
        f.write("\n")


def main():
    global line_number
    global tokens
    global errors
    global symbol_table

    scanner = Scanner("input.txt")
    line_number = 1
    tokens = []
    errors = []
    symbol_table = []

    while True:
        token = scanner.get_next_token()
        if token[0] == "Error":
            errors.append(token)
        else:
            if token[0] == "ID":
                if token[1] not in symbol_table:
                    symbol_table.append(token[1])
            tokens.append(token)
        if token[0] == "$":
            break
        # print(token)

    save_tokens_to_file(tokens)
    save_to_errors_file(errors)
    save_to_symbols_file(symbol_table)


if __name__ == "__main__":
    main()
