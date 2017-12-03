from re import match


class Token:

    def __init__(self, lexeme):
        self.lexeme = str(lexeme)

    @property
    def val(self):
        if self.lexeme.isdigit():
            return eval(self.lexeme)

    @property
    def is_temporary(self):
        return match(r"t\d+", self.lexeme)

    @property
    def is_identifier(self):
        return self.lexeme.isalpha()

    @property
    def is_constant(self):
        return self.lexeme.isdigit()

    def __repr__(self):
        return f'<Token(lexeme={self.lexeme})>'

    def __str__(self):
        return self.lexeme
