import myException as EX
import json 

from myTokenizer import MyTokenizer
from os import path 

class MyBaseParser():

    def __init__(self): 
        
        self.Tokenizer = MyTokenizer()

    def initTokenizer(self, string):
        
        self.Tokenizer.initialize(string)

        self.Lookhead = self.Tokenizer.getNextToken()

    def eat(self, tokenType):
        
        token = self.Lookhead
        
        if self.Lookhead is None: raise EX.MySyntaxException(f"Position {self.Tokenizer.Position + 1}: end of string reached: we expected '{tokenType}'")
        
        if self.Lookhead["type"] != tokenType: raise EX.MySyntaxException(f"Position {self.Tokenizer.Position + 1}: We expected '{tokenType}' but arrived '{self.Lookhead['type']}'")

        self.Lookhead = self.Tokenizer.getNextToken()

        return token

    def write(self, AST, output_path, output_filename):

        if not path.exists(output_path): raise EX.MyParserException(f"The path '{output_path}' does NOT exists")

        with open(output_path + self.SEPARATOR + output_filename, 'w') as resultFile: resultFile.write(json.dumps(AST, indent=4))