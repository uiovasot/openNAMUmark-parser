RULES = [
    "'''", "''", "__", "~~", "--", "^^", ",,", "{{{", "{{{#", "{{{+", "{{{-", "}}}",
    "[[", "|", "]]"
]
# TODO: 문법 더 추가

RULES.sort(reverse=True)

class Token:
    def __init__(self, value: str, type: str):
        self.value = value
        self.type = type

    def __repr__(self) -> str:
        return "{type: \""+self.type+"\", value: \""+self.value+"\"}"

class Tokenizer: 
    def run(self, input: str) -> list[Token]:
        self.cursor = 0
        self.token = ''
        self.tokens = []
        self.newLine = True
        
        rootContinue = False
        
        while len(input) > self.cursor:
            char: str = input[self.cursor]

            if char == '\\':
                self.token += input[self.cursor]
                self.cursor += 1

                continue

            if input[self.cursor] == '\n':
                self.previousTokenPush()
                self.tokens.append(Token('\n', 'rule'))
                self.cursor += 1

                self.newLine = True
                continue

            # TODO: 문단 문법 추가

            if self.newLine and input[self.cursor:self.cursor+2] == '##':
                self.cursor += 2

                while input[self.cursor] and input[self.cursor] != '\n': self.cursor += 1

                continue

            for rule in RULES:
                if rule == input[self.cursor:self.cursor+len(rule)]:
                    self.previousTokenPush()
                    self.tokens.append(Token(rule, 'rule'))
                    self.cursor += len(rule)

                    rootContinue = True
                    break

            if rootContinue: 
                rootContinue = False
                continue

            self.token += char
            self.newLine = False
            self.cursor += 1

        self.previousTokenPush()

        return self.tokens

    def previousTokenPush(self):
        if self.token != '':
            self.tokens.append(Token(self.token, 'string'))
            self.token = ''

if __name__ == "__main__":
    print(Tokenizer().run("test [[test]]"))
