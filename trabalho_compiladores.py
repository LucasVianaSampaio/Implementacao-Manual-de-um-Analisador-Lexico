import re

class Token:
    def __init__(self, tipo, lexema, atributo=None):
        self.tipo = tipo
        self.lexema = lexema
        self.atributo = atributo

    def __repr__(self):
        if self.atributo is not None:
            return f"Token({self.tipo}, '{self.lexema}', {self.atributo})"
        else:
            return f"Token({self.tipo}, '{self.lexema}')"

class Lexer:
    def __init__(self, codigo):
        self.codigo = codigo
        self.pos = 0
        self.linha = 1
        self.coluna = 1
        self.tokens = []
        self.simbolos = {}
        self.palavras_chave = {
            'auto', 'break', 'case', 'char', 'const', 'continue', 'default', 'do',
            'double', 'else', 'enum', 'extern', 'float', 'for', 'goto', 'if',
            'int', 'long', 'register', 'return', 'short', 'signed', 'sizeof',
            'static', 'struct', 'switch', 'typedef', 'union', 'unsigned', 'void',
            'volatile', 'while'
        }
        self.operators = {
            '==', '!=', '<=', '>=', '&&', '||', '+=', '-=', '*=', '/=', '%=',
            '+', '-', '*', '/', '%', '<', '>', '=', '!', '++', '--', '->'
        }
        self.delimiters = {
            ';', ',', '.', '(', ')', '{', '}', '[', ']'
        }

    def peek(self):
        if self.pos < len(self.codigo):
            return self.codigo[self.pos]
        return None

    def advance(self):
        c = self.peek()
        if c is None:
            return None
        self.pos += 1
        if c == '\n':
            self.linha += 1
            self.coluna = 1
        else:
            self.coluna += 1
        return c

    def add_token(self, tipo, lexema, atributo=None):
        self.tokens.append(Token(tipo, lexema, atributo))

    def add_simbolo(self, lexema):
        if lexema in self.simbolos:
            self.simbolos[lexema] += 1
        else:
            self.simbolos[lexema] = 1

    def is_ident_start(self, c):
        return c.isalpha() or c == '_'

    def is_ident_part(self, c):
        return c.isalnum() or c == '_'

    def skip_whitespace(self):
        while True:
            c = self.peek()
            if c in [' ', '\t', '\r', '\n']:
                self.advance()
            else:
                break

    def skip_comment(self):
        if self.peek() == '/' and self.pos + 1 < len(self.codigo) and self.codigo[self.pos+1] == '/':
            self.advance()  
            self.advance()  
            while self.peek() not in [None, '\n']:
                self.advance()
            return True
        
        if self.peek() == '/' and self.pos + 1 < len(self.codigo) and self.codigo[self.pos+1] == '*':
            self.advance()
            self.advance() 
            while True:
                c = self.peek()
                if c is None:
                    self.add_token('ERROR', 'Comentário não fechado')
                    return True
                if c == '*' and self.pos + 1 < len(self.codigo) and self.codigo[self.pos+1] == '/':
                    self.advance()
                    self.advance()
                    break
                else:
                    self.advance()
            return True
        return False

    def lex_number(self):
        lexema = ''
        c = self.peek()
        if c is None:
            return

        if c == '.':
            lexema += self.advance()
            c = self.peek()
            if c is None or not c.isdigit():
                self.add_token('ERROR', lexema)
                return
            while c is not None and c.isdigit():
                lexema += self.advance()
                c = self.peek()
            if c is not None and (c.isalpha() or c == '_'):
                while c is not None and (c.isalnum() or c == '_'):
                    lexema += self.advance()
                    c = self.peek()
                self.add_token('ERROR', lexema)
                return
            self.add_token('FLOAT_LITERAL', lexema, float(lexema))
            return

        while c is not None and c.isdigit():
            lexema += self.advance()
            c = self.peek()

        if c == '.':
            lexema += self.advance()
            c = self.peek()
            if c is None or not c.isdigit():
                self.add_token('ERROR', lexema)
                return
            
            while c is not None and c.isdigit():
                lexema += self.advance()
                c = self.peek()

            if c is not None and (c.isalpha() or c == '_'):
                while c is not None and (c.isalnum() or c == '_'):
                    lexema += self.advance()
                    c = self.peek()
                self.add_token('ERROR', lexema)
                return
            self.add_token('FLOAT_LITERAL', lexema, float(lexema))
            return

        if c == ',':
            while c is not None and not c.isspace() and c not in [';', ')', '(', '{', '}', '[', ']']:
                lexema += self.advance()
                c = self.peek()
            self.add_token('ERROR', lexema)
            return

        if c is not None and (c.isalpha() or c == '_'):
            while c is not None and (c.isalnum() or c == '_'):
                lexema += self.advance()
                c = self.peek()
            self.add_token('ERROR', lexema)
            return

        self.add_token('INT_LITERAL', lexema, int(lexema))


    def lex_identifier_or_keyword(self):
        lexema = ''
        c = self.peek()
        if not self.is_ident_start(c):
            self.add_token('ERROR', c)
            self.advance()
            return

        while c is not None and self.is_ident_part(c):
            lexema += self.advance()
            c = self.peek()

        if lexema in self.palavras_chave:
            self.add_token('KEYWORD', lexema)
        else:
            self.add_token('IDENTIFIER', lexema)
            self.add_simbolo(lexema)

    def lex_char_literal(self):
        lexema = ''
        c = self.advance() 
        lexema += c
        c = self.peek()
        if c == '\\':
            lexema += self.advance()
            c = self.peek()
            if c is None:
                self.add_token('ERROR', lexema)
                return
            lexema += self.advance()
        elif c is None:
            self.add_token('ERROR', lexema)
            return
        else:
            lexema += self.advance()

        if self.peek() != "'":
            self.add_token('ERROR', lexema)
            return
        lexema += self.advance()  # '
        self.add_token('CHAR_LITERAL', lexema)

    def lex_string_literal(self):
        lexema = ''
        c = self.advance()
        lexema += c
        while True:
            c = self.peek()
            if c is None:
                self.add_token('ERROR', lexema)
                return
            if c == '"':
                lexema += self.advance()
                break
            if c == '\\':
                lexema += self.advance()
                c = self.peek()
                if c is None:
                    self.add_token('ERROR', lexema)
                    return
                lexema += self.advance()
            else:
                lexema += self.advance()
        self.add_token('STRING_LITERAL', lexema)

    def lex_operator_or_delimiter(self):
        c = self.peek()
        if c is None:
            return False

        if self.pos + 2 < len(self.codigo):
            tri = self.codigo[self.pos:self.pos+3]
            if tri in self.operators:
                for _ in range(3):
                    self.advance()
                self.add_token('OPERATOR', tri)
                return True

        if self.pos + 1 < len(self.codigo):
            duo = self.codigo[self.pos:self.pos+2]
            if duo in self.operators:
                for _ in range(2):
                    self.advance()
                self.add_token('OPERATOR', duo)
                return True

        if c in self.operators:
            self.advance()
            self.add_token('OPERATOR', c)
            return True

        if c in self.delimiters:
            self.advance()
            self.add_token('DELIMITER', c)
            return True

        return False

    def lex_preprocessor_directive(self):
        if self.peek() == '#':
            lexema = ''
            while self.peek() not in [None, '\n']:
                lexema += self.advance()
            self.add_token('PP_DIRECTIVE', lexema)
            return True
        return False

    def analisar(self):
        while self.pos < len(self.codigo):
            self.skip_whitespace()
            if self.pos >= len(self.codigo):
                break

            if self.skip_comment():
                continue

            if self.lex_preprocessor_directive():
                continue

            c = self.peek()

            if self.is_ident_start(c):
                self.lex_identifier_or_keyword()
                continue

            if c.isdigit() or (c == '.' and self.pos + 1 < len(self.codigo) and self.codigo[self.pos+1].isdigit()):
                self.lex_number()
                continue

            if c == "'":
                self.lex_char_literal()
                continue

            if c == '"':
                self.lex_string_literal()
                continue

            if self.lex_operator_or_delimiter():
                continue

            self.add_token('ERROR', c)
            self.advance()

        return self.tokens, self.simbolos

if __name__ == "__main__":
    codigo_exemplo = '''
int main(void) {
    int i = 0;
    while (i < 5) {
        if (i % 2 == 0) {
            printf("even\n");
        } else {
            printf("odd\n");
        }
        i++;
    }
    return 0;
}
'''

    lexer = Lexer(codigo_exemplo)
    tokens, simbolos = lexer.analisar()

    print("Tokens reconhecidos:")
    for t in tokens:
        print(t)

    print("\nTabela de símbolos (identificadores e ocorrências):")
    for idf, count in simbolos.items():
        print(f"{idf}: {count}")
'''
#include <stdio.h>
int main(void) {
    printf("Hello, world!\n");

    return 0;
}


int main(void) {
    int x = 42;
    float y = 3.14;
    char c = 'a';
    x = x + 10;
    y = y * 2
    c = '\n';
    return x;
}

int main(void) {
    int i = 0;
    while (i < 5) {
        if (i % 2 == 0) {
            printf("even\n");
        } else {
            printf("odd\n");
        }
        i++;
    }
    return 0;
}

'''