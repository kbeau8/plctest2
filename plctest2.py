class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0

    def parse(self):
        self.stmt_list()

        # If all tokens have been parsed, return True
        return self.index == len(self.tokens)

    def match(self, expected):
        if self.index < len(self.tokens) and self.tokens[self.index] == expected:
            self.index += 1
            return True
        return False

    def stmt_list(self):
        while self.stmt():
            if not self.match(';'):
                return False
        return True

    def stmt(self):
        return self.if_stmt() or self.block() or self.assign() or self.declare() or self.while_loop()

    def if_stmt(self):
        if self.match('if') and self.match('(') and self.bool_expr() and self.match(')') and self.block():
            if self.match('else'):
                return self.block()
            return True
        return False

    def block(self):
        if self.match('{') and self.stmt_list() and self.match('}'):
            return True
        return False

    def declare(self):
        if self.match('DataType') and self.match('ID'):
            while self.match(','):
                if not self.match('ID'):
                    return False
            return True
        return False

    def assign(self):
        if self.match('ID') and self.match('=') and self.expr():
            return True
        return False

    def expr(self):
        if self.term():
            while self.match('+') or self.match('-'):
                if not self.term():
                    return False
            return True
        return False

    def term(self):
        if self.fact():
            while self.match('*') or self.match('/') or self.match('%'):
                if not self.fact():
                    return False
            return True
        return False

    def fact(self):
        if self.match('ID') or self.match('INT_LIT') or self.match('FLOAT_LIT'):
            return True
        elif self.match('(') and self.expr() and self.match(')'):
            return True
        return False

    def bool_expr(self):
        if self.bterm():
            while self.match('>') or self.match('<') or self.match('>=') or self.match('<='):
                if not self.bterm():
                    return False
            return True
        return False

    def bterm(self):
        if self.band():
            while self.match('==') or self.match('!='):
                if not self.band():
                    return False
            return True
        return False

    def band(self):
        if self.bor():
            while self.match('&&'):
                if not self.bor():
                    return False
            return True
        return False

    def bor(self):
        if self.expr():
            while self.match('||'):
                if not self.expr():
                    return False
            return True
        return False
