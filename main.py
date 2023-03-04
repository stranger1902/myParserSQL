from myParser import MyParser

import myException as EX
import myUtility as U
import json
import os

if __name__ == "__main__":
	
    #filePath = U.CURRENT_PATH + "\\" + U.FILENAME.TEST_INPUT_FILENAME.value
    filePath = U.CURRENT_PATH + "\\" + U.FILENAME.INPUT_FILENAME.value

    with open(filePath, 'r') as inputFile: myQuery = inputFile.read()

    if myQuery.strip() == "": raise EX.MyParserException(f"The file '{INPUT_FILENAME}' is empty")

    AST = MyParser("query_select").parse(myQuery)
    
    with open(U.CURRENT_PATH + "\\" + U.FILENAME.AST_FILENAME.value, 'w') as resultFile: resultFile.write(json.dumps(AST, indent=4))

    '''
    with open(OUTPUT_FILENAME, 'w') as resultFile: resultFile.write(MyParser.QueryFormatted)

    U.writeLog(f"Scrittura del file '{U.FILENAME.OUTPUT_FILENAME.value}' CONCLUSA", U.LEVEL.INFO)
    '''
