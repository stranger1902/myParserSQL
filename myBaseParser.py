import myException as EX

from myTokenizer import MyTokenizer

class MyBaseParser():

    def __init__(self): 
        
        self.Tokenizer = MyTokenizer()

    def parse(self, string):
        
        self.Tokenizer.initialize(string)

        self.Lookhead = self.Tokenizer.getNextToken()

    def eat(self, tokenType):
        
        token = self.Lookhead
        
        if self.Lookhead is None: raise EX.MySyntaxException(f"Position {self.Tokenizer.Position + 1}: end of string reached: we expected '{tokenType}'")
        
        if self.Lookhead["type"] != tokenType: raise EX.MySyntaxException(f"Position {self.Tokenizer.Position + 1}: We expected '{tokenType}' but arrived '{self.Lookhead['type']}'")

        self.Lookhead = self.Tokenizer.getNextToken()

        return token
