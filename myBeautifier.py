from math import prod

import json

class MyBeautifier():

    def __init__(self): 
        
        self.QueryFormatted = ""
        self.NumIndent = 0

    def beautify(self, AST):

        for query in AST["queries_list"]: 

            self.visitQuery(query)

            self.QueryFormatted += "\nUNION\n"

        self.QueryFormatted = self.QueryFormatted.rstrip("\nUNION\n")

        return self.QueryFormatted

    def visitQuery(self, node): 

        for statement in node["statements_list"]:

            if statement["type"] == "select_statement": self.visitSelectStatement(statement)

            elif statement["type"] == "where_statement": self.visitWhereStatement(statement)

            elif statement["type"] == "from_statement": self.visitFromStatement(statement)

            else: raise Exception(f"Statement type '{statement['type']}' is NOT valid")

    def visitSelectStatement(self, node): 
        
        self.QueryFormatted += "SELECT "

        self.QueryFormatted += f"TOP {node['limit_row']} " if node['limit_row'] else "" + "DISTINCT " if node["distinct"] else ""

        for field in node["fields_list"]:
            
            self.visitField(field)

            self.QueryFormatted += ", "

        self.QueryFormatted = self.QueryFormatted.rstrip(", ")

    def visitFromStatement(self, node): 

        self.QueryFormatted += "\nFROM "

        for table in node["tables_list"]:
            #TODO: gestire la virgola: inserire se lista di tabelle, non inserire se JOIN

            if table["type"] == "table": self.visitTable(table)
            
            elif table["type"] == "join_expression": self.visitJoinExpression(table)

            else: raise Exception(f"Table type '{table['type']}' is NOT valid")

        self.QueryFormatted = self.QueryFormatted.rstrip(", ")

    def visitWhereStatement(self, node): 

        self.QueryFormatted += "\nWHERE "

        for condition in node["conditions_list"]: self.visitCondition(condition)

    def visitBinaryExpression(self, node): 
        
        if node["left"]["type"] == "field": self.visitField(node["left"])
        
        elif node["left"]["type"] == "literal": self.visitLiteral(node["left"])

        else: raise Exception(f"Left operand type '{node['left']['type']}' is NOT valid")

        self.QueryFormatted += f" {node['operator']} "

        if node["right"]["type"] == "field": self.visitField(node["right"])
        
        elif node["right"]["type"] == "literal": self.visitLiteral(node["right"])

        else: raise Exception(f"Right operand type '{node['right']['type']}' is NOT valid")

    def visitField(self, node):
        
        if node["body"]["type"] == "block_statement": 

            self.QueryFormatted += "("
            self.visitBlockStatement(node["body"])
            self.QueryFormatted += ")"

        else: 

            if node["body"]["type"] == "binary_expression": self.visitBinaryExpression(node["body"])

            elif node["body"]["type"] == "identifier": self.visitIdentifier(node["body"])

            elif node["body"]["type"] == "literal": self.visitLiteral(node["body"])

            else: raise Exception(f"Field type '{node['body']['type']}' is NOT valid")

        if node["alias"]: self.QueryFormatted += f" AS {node['alias']['value']}"

    def visitTable(self, node):

        if node["operator"]: self.QueryFormatted += f"{node['operator']} "

        if node["body"]["type"] == "identifier": self.visitIdentifier(node["body"])

        elif node["body"]["type"] == "binary_expression": self.visitBinaryExpression(node["body"])

        else: raise Exception(f"Table type '{node['body']['type']}' is NOT valid")

    def visitCondition(self, node):

        if node["operator"]: self.QueryFormatted += node["operator"]

        if node["body"]["type"] == "binary_expression": self.visitBinaryExpression(node["body"])

        else: raise Exception(f"Condition type '{node['body']['type']}' is NOT valid")

    def visitBlockStatement(self, node):
        
        if node["body"]["type"] == "binary_expression": self.visitBinaryExpression(node["body"])

        else: raise Exception(f"Block statement type '{node['body']['type']}' is NOT valid")
    
    def visitJoinExpression(self, node):

        self.QueryFormatted += f"\n{node['operator']} "

        self.visitTable(node["value"])

        self.QueryFormatted += f" ON "

        for condition in node["conditions_list"]: self.visitCondition(condition)

    def visitLiteral(self, node):

        if node["subtype"] == "numeric_literal": self.visitNumericLiteral(node)

        elif node["subtype"] == "star_literal": self.visitStarLiteral(node)

        else: raise Exception(f"Literal subtype '{node['subtype']}' is NOT valid")

    def visitNumericLiteral(self, node):

        number = int(node['value']) if float(node['value']).is_integer() else float(node['value'])

        self.QueryFormatted += f"{self.getSign(node.get('sign', None)) + str(number)}"

    def visitStarLiteral(self, node):

        self.QueryFormatted += "*"

    def visitIdentifier(self, node): 
        
        self.QueryFormatted += f"{node['value']}"

    def getSign(self, iterable):
        
        product = prod(iterable) if iterable else +1

        return "" if int(product) > 0 else "-"

    def printQuery(self): print(self.QueryFormatted)
