from tokenizer import Token, Tokenizer
from urllib import parse

class Parser:
    def run(self, tokens: list[Token]) -> str:
        self.tokens = tokens
        self.cursor = 0
        html = ''

        print(tokens)

        while len(tokens) > self.cursor: 
            html += self.walk()

        return html
    
    def removeQuotes(self, str: str) -> str:
        return str.replace('"', '&quot;')
    
    def removeHTML(self, str: str) -> str:
        return str.replace('<', '&lt;').replace('>', '&gt;')

    def walk(self) -> str:
        token = self.tokens[self.cursor]

        if token.type == "rule":
            if token.value in ["'''", "''", "__", "~~", "--", "^^", ",,"]:
                self.cursor += 1
                detail = ''

                while len(self.tokens) > self.cursor and not (
                    self.tokens[self.cursor].type == "rule" and self.tokens[self.cursor].value == token.value
                ):
                    detail += self.walk()
            
                self.cursor += 1

                tag = 'del'
                if token.value == "'''":
                    tag = 'b'
                elif token.value == "''":
                    tag = 'i'
                elif token.value == "__":
                    tag = 'u'
                elif token.value == "^^":
                    tag = 'sup'
                elif token.value == ",,":
                    tag = 'sub'
                
                return '<'+tag+'>'+detail+'</'+tag+'>'

            if token.value == "[[":
                self.cursor += 1
                link = ''
                while len(self.tokens) > self.cursor and not (
                    self.tokens[self.cursor].type == "rule" and (
                        self.tokens[self.cursor].value == "|" or self.tokens[self.cursor].value == "]]"
                    )
                ):
                    link += self.walk()
                name = link
                if self.tokens[self.cursor].value == "|":
                    while len(self.tokens) > self.cursor and not (
                        self.tokens[self.cursor].type == "rule" and self.tokens[self.cursor].value == "]]"
                    ):
                        name += self.walk()
                
                self.cursor += 1

                html = '<a href="/w/'+self.removeQuotes(parse.quote(link))+'">'

                if link.startswith('http://') or link.startswith('https://') or link.startswith('ftp://'):
                    html = '<a href="'+self.removeQuotes(parse.quote(link))+'">'

                html += name

                html += '</a>'
                
                return html

        self.cursor += 1

        return self.removeHTML(token.value)

if __name__ == "__main__":
    print(Parser().run(Tokenizer().run("test [[test]]")))
