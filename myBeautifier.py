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

        #TODO: find a way to avoid self.QueryFormatted = self.QueryFormatted.rstrip("\nUNION\n")
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
            
            if table["type"] == "join_expression": self.visitJoinExpression(table)

            elif table["type"] == "table": self.visitTable(table)

            else: raise Exception(f"Table type '{table['type']}' is NOT valid")

        self.QueryFormatted = self.QueryFormatted.rstrip(", ")

    def visitWhereStatement(self, node): 

        self.QueryFormatted += "\nWHERE "

        for condition in node["conditions_list"]: self.visitCondition(condition)

    def visitBinaryExpression(self, node): 
        
        self.visitExpression(node["left"])

        self.QueryFormatted += f" {node['operator']} "

        self.visitExpression(node["right"])

    def visitField(self, node):
        
        if node["body"]["type"] == "block_statement": self.visitBlockStatement(node["body"])

        else: 

            if node["body"]["type"] == "binary_expression": self.visitBinaryExpression(node["body"])

            elif node["body"]["type"] == "case_expression": self.visitCaseExpression(node["body"])
            
            elif node["body"]["type"] == "identifier": self.visitIdentifier(node["body"])

            elif node["body"]["type"] == "literal": self.visitLiteral(node["body"])

            else: raise Exception(f"Field type '{node['body']['type']}' is NOT valid")

        if node["alias"]: self.QueryFormatted += f" AS {node['alias']['value']}"

    def visitTable(self, node):

        if node["operator"]: self.QueryFormatted += f"{node['operator']} "

        if node["body"]["type"] == "binary_expression": self.visitBinaryExpression(node["body"])

        elif node["body"]["type"] == "identifier": self.visitIdentifier(node["body"])

        else: raise Exception(f"Table type '{node['body']['type']}' is NOT valid")

    def visitCondition(self, node):
        #TODO: find better way to organize this method

        operator = node["operator"]

        if operator: self.QueryFormatted += f" {operator} " if operator != "NOT " else operator

        if isinstance(node["body"], list):

            for item in node["body"]: 

                if item["type"] == "between_expression": self.visitBetweenExpression(item, operator == "NOT")

                elif item["type"] == "in_expression": self.visitInExpression(item, operator == "NOT")

                elif item["type"] == "binary_expression": self.visitBinaryExpression(item)

                elif item["type"] == "exists_expression": self.visitExistsExpression(item)

                elif item["type"] == "condition_expression": self.visitCondition(item)

                elif item["type"] == "block_statement": self.visitBlockStatement(item)

                elif item["type"] == "is_expression": self.visitIsExpression(item)

                elif item["type"] == "literal": self.visitLiteral(item)

                else: raise Exception(f"Condition type '{item['type']}' is NOT valid")

        else:

            if node["body"]["type"] == "between_expression": self.visitBetweenExpression(node["body"], operator == "NOT")

            elif node["body"]["type"] == "in_expression": self.visitInExpression(node["body"], operator == "NOT")

            elif node["body"]["type"] == "binary_expression": self.visitBinaryExpression(node["body"])

            elif node["body"]["type"] == "exists_expression": self.visitExistsExpression(node["body"])

            elif node["body"]["type"] == "condition_expression": self.visitCondition(node["body"])

            elif node["body"]["type"] == "block_statement": self.visitBlockStatement(node["body"])

            elif node["body"]["type"] == "is_expression": self.visitIsExpression(node["body"])

            elif node["body"]["type"] == "literal": self.visitLiteral(node["body"])

            else: raise Exception(f"Condition type '{node['body']['type']}' is NOT valid")

    def visitExpression(self, node):

        if node["type"] == "field": self.visitField(node)
        
        elif node["type"] == "literal": self.visitLiteral(node)

        elif node["type"] == "function": self.visitFunction(node)

        elif node["type"] == "condition_expression": self.visitCondition(node)

        else: raise Exception(f"Expression type '{node['type']}' is NOT valid")

    def visitFunction(self, node):

        self.visitIdentifier(node["name"])

        self.QueryFormatted += "("

        if node["distinct"]: self.QueryFormatted += "DISTINCT "

        for argument in node["arguments_list"]: 
            self.visitExpression(argument)
            self.QueryFormatted += ", "

        #TODO: find a way to avoid self.QueryFormatted = self.QueryFormatted.rstrip(", ")
        self.QueryFormatted = self.QueryFormatted.rstrip(", ")

        self.QueryFormatted += ")"

    def visitBlockStatement(self, node):
        
        self.QueryFormatted += "("

        for item in node["body"]:
            
            if item["type"] == "binary_expression": self.visitBinaryExpression(item)

            elif item["type"] == "condition_expression": self.visitCondition(item)

            else: raise Exception(f"Block statement type '{item['type']}' is NOT valid")
        
        self.QueryFormatted += ")"

    def visitJoinExpression(self, node):

        self.QueryFormatted += f"\n{node['operator']} "

        self.visitTable(node["value"])

        self.QueryFormatted += f" ON "

        for condition in node["conditions_list"]: self.visitCondition(condition)

    def visitExistsExpression(self, node):

        self.QueryFormatted += f"EXISTS "

        self.QueryFormatted += f"("

        for query in node["queries_list"]: self.visitQuery(query)

        self.QueryFormatted += f")"

    def visitCaseExpression(self, node):

        self.QueryFormatted += f"CASE "

        for item in node["body"]: 

            if item["type"] == "when_expression":

                self.QueryFormatted += "WHEN "
                
                for condition in item["conditions_list"]: self.visitCondition(condition)
            
                self.QueryFormatted += " THEN "

                self.visitExpression(item["then_expression"])

            else:

                self.QueryFormatted += " ELSE "

                self.visitExpression(item["then_expression"])

    def visitBetweenExpression(self, node, is_negative):
        
        #TODO: find a better way to implement it
        if is_negative: self.QueryFormatted = self.QueryFormatted.rstrip(" NOT ") + " "

        self.visitExpression(node["target_field"])

        self.QueryFormatted += " NOT BETWEEN " if is_negative else " BETWEEN "

        self.visitExpression(node["before"])

        self.QueryFormatted += f" AND "

        self.visitExpression(node["after"])

    def visitIsExpression(self, node):

        self.visitExpression(node["target_field"])

        self.QueryFormatted += f" IS "

        self.visitExpression(node["right"])

    def visitInExpression(self, node, is_negative):
        
        #TODO: find a better way to implement it
        if is_negative: self.QueryFormatted = self.QueryFormatted.rstrip(" NOT ") + " "

        self.visitExpression(node["target_field"])

        self.QueryFormatted += " NOT IN " if is_negative else " IN "

        self.QueryFormatted += "("

        for item in node["queries_list"]: 
            
            if item["type"] == "query": self.visitQuery(item)
            
            else: 
                self.visitLiteral(item)
                self.QueryFormatted += ", "

        #TODO: find a way to avoid self.QueryFormatted = self.QueryFormatted.rstrip(", ")
        self.QueryFormatted = self.QueryFormatted.rstrip(", ")
        
        self.QueryFormatted += ")"

    def visitLiteral(self, node):

        if node["subtype"] == "numeric_literal": self.visitNumericLiteral(node)

        elif node["subtype"] == "string_literal": self.visitStringLiteral(node)

        elif node["subtype"] == "star_literal": self.visitStarLiteral(node)

        elif node["subtype"] == "null_literal": self.visitNullLiteral(node)

        else: raise Exception(f"Literal subtype '{node['subtype']}' is NOT valid")

    def visitNumericLiteral(self, node):

        number = int(node['value']) if float(node['value']).is_integer() else float(node['value'])

        self.QueryFormatted += f"{self.getSign(node.get('sign', None)) + str(number)}"

    def visitStringLiteral(self, node):

        self.QueryFormatted += f"'{node['value']}'"

    def visitStarLiteral(self, node):

        self.QueryFormatted += "*"

    def visitNullLiteral(self, node):

        self.QueryFormatted += "NULL"

    def visitIdentifier(self, node): 
        
        self.QueryFormatted += f"{node['value']}"

    def getSign(self, iterable):
        
        product = prod(iterable) if iterable else +1

        return "" if int(product) > 0 else "-"

    def printQuery(self): print(self.QueryFormatted)
