from myBeautifier import MyBeautifier
from myParser import MyParser
from os import getcwd

if __name__ == "__main__":
    
    CURRENT_PATH = getcwd()

    myParser = MyParser("query_select")
    
    myAST = myParser.parseFromFile(CURRENT_PATH, "queryInput.txt")
    
    myParser.write(myAST, CURRENT_PATH, "AST.json")

    myBeautifier = MyBeautifier()
    
    queryFormatted = myBeautifier.beautify(myAST)

    myBeautifier.write(queryFormatted, CURRENT_PATH, "queryFormatted.txt")
    
    print(queryFormatted)
