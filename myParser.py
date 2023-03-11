from myBaseParser import MyBaseParser
from platform import system
from os import path

import myException as EX
import json

class MyParser(MyBaseParser):

    SEPARATOR = "\\" if system() == "Windows" else "/"

    def __init__(self, program_type): 
        
        self.ProgramType = program_type

        super().__init__()

    def parseFromFile(self, input_path, input_filename):

        if not path.exists(input_path): raise EX.MyParserException(f"The path '{input_path}' does NOT exists")

        if not path.exists(input_path): raise EX.MyParserException(f"The file '{input_path + U.SEPARATOR + input_filename}' does NOT exists")

        with open(input_path + self.SEPARATOR + input_filename, 'r') as inputFile: myQuery = inputFile.read()
        
        self.initTokenizer(myQuery)

        return self.program()
    
    def parse(self, string):

        self.initTokenizer(string)

        return self.program()
    
    def write(self, AST, output_path, output_filename):

        if not path.exists(output_path): raise EX.MyParserException(f"The path '{output_path}' does NOT exists")

        with open(output_path + self.SEPARATOR + output_filename, 'w') as resultFile: resultFile.write(json.dumps(AST, indent=4))

    def program(self): return {"type" : self.ProgramType, "queries_list" : self.queriesList()}

    def queriesList(self):

        myQueriesList = [ self.query() ]

        while self.Lookhead and self.Lookhead["type"] == "UNION":
            self.eat("UNION")
            myQueriesList.append(self.query())
        
        return myQueriesList

    def query(self):

        myStatementsList = [ self.selectStatement() ]

        if self.Lookhead and self.Lookhead["type"] == "FROM": myStatementsList.append(self.fromStatement())

        if self.Lookhead and self.Lookhead["type"] == "WHERE": myStatementsList.append(self.whereStatement())

        if self.Lookhead and self.Lookhead["type"] == "GROUP_BY": 

            myStatementsList.append(self.groupByStatement())

            if self.Lookhead and self.Lookhead["type"] == "HAVING": myStatementsList.append(self.havingStatement())

        if self.Lookhead and self.Lookhead["type"] == "ORDER_BY": myStatementsList.append(self.orderByStatement())

        return {"type" : "query", "statements_list" : myStatementsList}

    def subquery(self):
        
        self.eat("OPEN-ROUND-BRACKET")
        
        if self.Lookhead["type"] == "OPEN-ROUND-BRACKET": subquery = {"type" : "block_statement", "body" : self.subquery()}

        elif self.Lookhead["category"] == "LITERAL":

            subquery = [ self.literalExpression(self.getSign()) ]

            while self.Lookhead["type"] == "COMMA":
                self.eat("COMMA")
                subquery.append(self.literalExpression(self.getSign()))

        else: subquery = self.queriesList()

        self.eat("CLOSE-ROUND-BRACKET")

        return subquery

    def table(self, operator):

        table = self.subquery() if self.Lookhead and self.Lookhead["type"] == "OPEN-ROUND-BRACKET" else self.identifier()

        if self.Lookhead and self.Lookhead["type"] == "OPEN-ROUND-BRACKET":

            self.eat("OPEN-ROUND-BRACKET")
            nolock_before = self.eat("NOLOCK")
            self.eat("CLOSE-ROUND-BRACKET")

        else: nolock_before = None

        alias = self.alias()

        if self.Lookhead and self.Lookhead["type"] == "OPEN-ROUND-BRACKET":

            self.eat("OPEN-ROUND-BRACKET")
            nolock_after = self.eat("NOLOCK")
            self.eat("CLOSE-ROUND-BRACKET")
        
        else: nolock_after = None
        
        if nolock_before and nolock_after: raise EX.MyParserException("NOLOCK is declared 2 times")

        return {"type" : "table", "operator" : operator, "nolock" : True if nolock_before else True if nolock_after else False, "body" : table, "alias" : alias}

    def function(self):

        identifier = self.identifier()

        self.eat("OPEN-ROUND-BRACKET")
        
        distinct = self.eat("DISTINCT") if self.Lookhead and self.Lookhead["type"] == "DISTINCT" else None

        if distinct: myArgumentsList = [ self.additiveExpression() ]

        else:
            
            myArgumentsList = [ self.additiveExpression() ] if self.Lookhead["type"] != "CLOSE-ROUND-BRACKET" else []
        
            while self.Lookhead["type"] == "COMMA":
                self.eat("COMMA")
                myArgumentsList.append(self.additiveExpression())

        self.eat("CLOSE-ROUND-BRACKET")

        return {"type" : "function", "distinct" : True if distinct else False, "name" : identifier, "arguments_list" : myArgumentsList}

    def conditionsList(self):
        
        if self.Lookhead:
        
            if self.Lookhead["type"] == "OPEN-ROUND-BRACKET":

                self.eat("OPEN-ROUND-BRACKET")

                aaa = self.conditionsList()

                myConditionsList = [ aaa ] if not isinstance(aaa, list) else aaa

                while self.Lookhead and self.Lookhead["category"] == "CONDITION": myConditionsList.append(self.conditionExpression())

                myConditionsList = {"type" : "block_statement", "body" : myConditionsList}

                self.eat("CLOSE-ROUND-BRACKET")
        
            else:

                myConditionsList = [ self.conditionExpression() ]

                while self.Lookhead and self.Lookhead["category"] == "CONDITION": myConditionsList.append(self.conditionExpression())

            return myConditionsList

# ************************************************* STATEMENTS ************************************************* #

    def selectStatement(self):

        self.eat("SELECT")

        distinctToken = self.eat("DISTINCT") if self.Lookhead and self.Lookhead["type"] == "DISTINCT" else None
        
        if self.Lookhead and self.Lookhead["type"] == "TOP":
            self.eat("TOP") 
            limitNumberRow = self.numericLiteral(self.getSign())

        else: limitNumberRow = None

        fieldsNameList = [ self.expressionFieldWithAlias() ]

        while self.Lookhead and self.Lookhead["type"] == "COMMA":
            self.eat("COMMA")
            fieldsNameList.append(self.expressionFieldWithAlias())

        return {"type" : "select_statement", "distinct" : True if distinctToken else False, "limit_row" : limitNumberRow, "fields_list" : fieldsNameList}

    def fromStatement(self):

        self.eat("FROM")

        tablesList = [ self.table(None) ]

        while self.Lookhead and self.Lookhead["type"] in ["COMMA", "INNER", "LEFT", "RIGHT", "JOIN"]:

            if self.Lookhead["type"] == "COMMA": tablesList.append(self.table(self.eat("COMMA")["value"]))

            else: tablesList.append(self.joinExpression())

        return {"type" : "from_statement", "tables_list" : tablesList}

    def whereStatement(self):

        self.eat("WHERE")
        
        return {"type" : "where_statement", "conditions_list" : self.conditionsList()}

    def groupByStatement(self): 

        self.eat("GROUP_BY")

        fieldsList = [ self.nameFieldWithAlias() ]

        while self.Lookhead and self.Lookhead["type"] == "COMMA":
            self.eat("COMMA")
            fieldsList.append(self.nameFieldWithAlias())

        return {"type" : "group_by_statement", "fields_list" : fieldsList}

    def havingStatement(self): 

        self.eat("HAVING")

        conditionsList = [ self.conditionExpression() ]
        
        while self.Lookhead and self.Lookhead["category"] == "CONDITION": conditionsList.append(self.conditionExpression())

        return {"type" : "having_statement", "conditions_list" : conditionsList}

    def orderByStatement(self):

        self.eat("ORDER_BY")

        fieldsList = [ self.nameFieldWithOrientation() ]

        while self.Lookhead and self.Lookhead["type"] == "COMMA":
            self.eat("COMMA")
            fieldsList.append(self.nameFieldWithOrientation())

        return {"type" : "order_by_statement", "fields_list" : fieldsList}

    def blockStatement(self):
        
        self.eat("OPEN-ROUND-BRACKET")

        if self.Lookhead and self.Lookhead["type"] == "SELECT": body = self.queriesList()

        else: body = [ self.relationalExpression() ]

        self.eat("CLOSE-ROUND-BRACKET")

        return {"type" : "block_statement", "body" : body}

# ************************************************ EXPRESSIONS ************************************************* #

    def joinExpression(self): 
        
        joinType = ""

        if self.Lookhead["type"] == "INNER": self.eat("INNER")

        elif self.Lookhead["type"] in ("LEFT", "RIGHT"):

            joinType = self.eat(self.Lookhead["type"])["value"]

            if self.Lookhead["type"] == "OUTER": self.eat("OUTER")

        joinType += self.eat("JOIN")["value"] if self.Lookhead["type"] == "JOIN" else None

        table = self.table(None)

        self.eat("ON")
        
        conditionsList = [ self.conditionExpression() ]
        
        while self.Lookhead and self.Lookhead["category"] == "CONDITION": conditionsList.append(self.conditionExpression())

        return {"type" : "join_expression", "operator" : joinType.upper(), "value" : table, "conditions_list" : conditionsList}

    def conditionExpression(self):
        
        if self.Lookhead:

            if self.Lookhead["type"] == "NOT": return {"type" : "condition_expression", "operator" : self.eat("NOT")["value"], "body" : self.conditionExpression()}

            else: 
                
                operator = self.eat(self.Lookhead["type"])["value"] if self.Lookhead["category"] == "CONDITION" else None

                if self.Lookhead["type"] == "OPEN-ROUND-BRACKET": return {"type" : "condition_expression", "operator" : operator, "body" : self.conditionsList()}

                else: 
                    
                    expression = self.conditionExpression() if self.Lookhead and self.Lookhead["type"] == "NOT" else self.relationalExpression()
                    
                    return {"type" : "condition_expression", "operator" : operator, "body" : expression} 
                    
    def relationalExpression(self):

        if self.Lookhead:

            if self.Lookhead["type"] == "EXISTS": return self.existsExpression()

            else:
                
                leftValue = self.additiveExpression()

                if self.Lookhead:
                    
                    notOperator = self.eat("NOT") if self.Lookhead["type"] == "NOT" else None

                    if self.Lookhead["type"] == "BETWEEN": return self.betweenExpression(leftValue, notOperator)

                    elif self.Lookhead["type"] == "LIKE": return self.likeExpression(leftValue, notOperator)

                    elif self.Lookhead["type"] == "IN":  return self.inExpression(leftValue, notOperator)

                    elif self.Lookhead["type"] == "IS": return self.isExpression(leftValue)
                    
                    else:
                        
                        while self.Lookhead and self.Lookhead["type"] == "RELATIONAL_OPERATOR":
                            
                            operator = self.eat("RELATIONAL_OPERATOR")["value"]

                            rightValue = self.additiveExpression()

                            leftValue = {"type" : "binary_expression", "operator" : operator, "left" : leftValue, "right" : rightValue}

        return leftValue
    
    def additiveExpression(self):

        signLeftOperand = self.getSign()
        
        leftValue = self.multiplicativeExpression(signLeftOperand)

        while self.Lookhead and self.Lookhead["type"] == "ADDITIVE_OPERATOR":

            operator = self.eat("ADDITIVE_OPERATOR")["value"]

            signRightOperand = self.getSign()

            rightValue = self.multiplicativeExpression(signRightOperand)

            leftValue = {"type" : "binary_expression", "operator" : operator, "left" : leftValue, "right" : rightValue}

        return leftValue

    def multiplicativeExpression(self, sign=None):

        leftValue = self.primaryExpression(sign)

        while self.Lookhead and self.Lookhead["type"] in ("STAR", "SLASH"):

            operator = self.eat(self.Lookhead["type"])["value"]

            rightValue = self.primaryExpression()

            leftValue = {"type" : "binary_expression", "operator" : operator, "left" : leftValue, "right" : rightValue}

        return leftValue

    def primaryExpression(self, sign=None): 
        
        if self.Lookhead["type"] == "OPEN-ROUND-BRACKET": return self.blockStatement()
        
        elif self.Lookhead["category"] == "LITERAL": return self.literalExpression(sign)
        
        elif self.Lookhead["type"] == "CASE": return self.caseExpression()

        elif self.Lookhead["type"] == "FUNCTION": return self.function()
                
        else: return self.nameFieldWithAlias(sign)

    def caseExpression(self):

        self.eat("CASE")
        
        myArgumentsList = [ self.whenExpression() ]

        while self.Lookhead and self.Lookhead["type"] == "WHEN": myArgumentsList.append(self.whenExpression())

        if self.Lookhead and self.Lookhead["type"] == "ELSE": myArgumentsList.append(self.elseExpression())

        self.eat("END")

        return {"type" : "case_expression", "body" : myArgumentsList, "alias" : self.alias()}

    def whenExpression(self):

        self.eat("WHEN")
        
        conditionsList = [ self.conditionExpression() ]

        while self.Lookhead and self.Lookhead["category"] == "CONDITION": conditionsList.append(self.conditionExpression())

        self.eat("THEN")

        return {"type" : "when_expression", "conditions_list" : conditionsList, "then_expression": self.additiveExpression()}

    def elseExpression(self):

        self.eat("ELSE")

        return {"type" : "else_expression", "then_expression": self.additiveExpression()}

    def existsExpression(self):

        self.eat("EXISTS")

        self.eat("OPEN-ROUND-BRACKET")
        myQueriesList = self.queriesList()
        self.eat("CLOSE-ROUND-BRACKET")
        
        return {"type" : "exists_expression", "queries_list" : myQueriesList}

    def inExpression(self, target_field, is_negative):

        self.eat("IN")

        rightValue = {"type" : "in_expression", "target_field" : target_field, "queries_list" : self.subquery()}

        return {"type" : "condition_expression", "operator" : "NOT", "body" : [rightValue]} if is_negative else rightValue
        
    def likeExpression(self, target_field, is_negative):

        self.eat("LIKE")

        rightValue = {"type" : "like_expression", "target_field" : target_field, "value" : self.literalExpression()}

        return {"type" : "condition_expression", "operator" : "NOT", "body" : [rightValue]} if is_negative else rightValue

    def isExpression(self, target_field):

        self.eat("IS")
        
        is_negative = self.eat("NOT") if self.Lookhead["type"] == "NOT" else None

        rightValue = {"type" : "condition_expression", "operator" : "NOT", "body" : [self.nullLiteral()]} if is_negative else self.nullLiteral()

        return {"type" : "is_expression", "target_field" : target_field, "right" : rightValue}

    def betweenExpression(self, target_field, is_negative):

        self.eat("BETWEEN")
        beforeBetween = self.additiveExpression()
        self.eat("AND")
        afterBetween = self.additiveExpression()

        rightValue = {"type" : "between_expression", "target_field" : target_field, "before" : beforeBetween, "after" : afterBetween}

        return {"type" : "condition_expression", "operator" : "NOT", "body" : [rightValue]} if is_negative else rightValue
        
    def literalExpression(self, sign):

        if self.Lookhead["type"] == "NUMBER": return self.numericLiteral(sign)

        elif self.Lookhead["type"] == "STRING": return self.stringLiteral()

        elif self.Lookhead["type"] == "NULL": return self.nullLiteral()
        
        elif self.Lookhead["type"] == "STAR": return self.starLiteral()
        
        else: raise EX.MySyntaxException(f"Literal '{self.Lookhead}' is NOT valid")

# ************************************************** LITERALS ************************************************** #

    def identifier(self): return {"type" : "identifier", "value" : self.eat("FUNCTION" if self.Lookhead["type"] == "FUNCTION" else "FIELDNAME")["value"]} 

    def numericLiteral(self, sign): return {"type" : "literal", "subtype" : "numeric_literal", "sign" : sign, "value" : float(self.eat("NUMBER")["value"])}

    def stringLiteral(self): return {"type" : "literal", "subtype" : "string_literal", "value" : self.eat("STRING")["value"][1:-1]}

    def nullLiteral(self): return {"type" : "literal", "subtype" : "null_literal", "value" : self.eat("NULL")["value"]}

    def starLiteral(self): return {"type" : "literal", "subtype" : "star_literal", "value" : self.eat("STAR")["value"]}
    
# ************************************************** FIELDS **************************************************** #

    def nameFieldWithOrientation(self): 
        
        return {"orientation" : self.eat(self.Lookhead["type"])["type"] if self.Lookhead["type"] in ("DESC", "ASC") else None, "body" : self.nameFieldWithAlias()}
    
    def nameFieldWithAlias(self, sign=None): 
        
        result = {"type" : "field", "body" : self.identifier(), "alias": self.alias()}

        if sign: result["sign"] = sign

        return result

    def expressionFieldWithAlias(self, sign=None): 
        
        value = self.additiveExpression()

        result = value if value["type"] == "field" else {"type" : "field", "body" : value, "alias": self.alias()}

        if sign: result["sign"] = sign

        return result

    def alias(self):

        if self.Lookhead: 
            
            if self.Lookhead["type"] == "AS": self.eat("AS")

            if self.Lookhead["type"] == "FIELDNAME": return self.identifier() 
        
            else: return None

# ************************************************** UTILITY *************************************************** #

    def getSign(self):

        signsList = []
        
        while self.Lookhead and self.Lookhead["type"] == "ADDITIVE_OPERATOR": signsList.append(self.eat("ADDITIVE_OPERATOR")["value"] + "1")
        
        return signsList if len(signsList) > 0 else None

# ************************************************************************************************************** #
