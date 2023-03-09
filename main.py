from myBeautifier import MyBeautifier
from myParser import MyParser

import myException as EX
import myUtility as U
import json
import os

if __name__ == "__main__":
	
    #filePath = U.CURRENT_PATH + U.SEPARATOR + U.FILENAME.TEST_INPUT_FILENAME.value
    filePath = U.CURRENT_PATH + U.SEPARATOR + U.FILENAME.INPUT_FILENAME.value

    with open(filePath, 'r') as inputFile: myQuery = inputFile.read()

    myAST = MyParser("query_select").parse(myQuery)
    
    with open(U.CURRENT_PATH + U.SEPARATOR + U.FILENAME.AST_FILENAME.value, 'w') as resultFile: resultFile.write(json.dumps(myAST, indent=4))

    myBeautifier = MyBeautifier()
    
    queryFormatted = myBeautifier.beautify(myAST)

    with open(U.CURRENT_PATH + U.SEPARATOR + U.FILENAME.OUTPUT_FILENAME.value, 'w') as outputFile: outputFile.write(queryFormatted)
    
    myBeautifier.printQuery()