from platform import system
from math import prod

class MyBeautifier():

    SEPARATOR = "\\" if system() == "Windows" else "/"

    def __init__(self): 
        
        self.QueryFormatted = ""
        self.NumIndents = 0
        self.NumSpaces = 0

    def beautify(self, AST):

        for query in AST["queries_list"]: 

            self.visitQuery(query)

            self.QueryFormatted += "UNION"

        #TODO: find a way to avoid self.QueryFormatted = self.QueryFormatted.rstrip("UNION")
        self.QueryFormatted = self.QueryFormatted.rstrip("UNION")

        return self.QueryFormatted

    def write(self, query, path, output_filename):

        with open(path + self.SEPARATOR + output_filename, 'w') as outputFile: outputFile.write(query)

    def addNewLine(self, num_indents, num_spaces): 
        
        self.NumIndents += num_indents
        self.NumSpaces += num_spaces

        self.QueryFormatted = self.QueryFormatted + "\n" + "\t"*self.NumIndents + " "*self.NumSpaces

    def addIndents(self, num_indents, num_spaces): 
        
        self.NumIndents += num_indents
        self.NumSpaces += num_spaces

    def visitQuery(self, node): 

        for statement in node["statements_list"]:

            if statement["type"] == "group_by_statement": self.visitGroupByStatement(statement)

            elif statement["type"] == "having_statement": self.visitHavingStatement(statement)

            elif statement["type"] == "select_statement": self.visitSelectStatement(statement)

            elif statement["type"] == "where_statement": self.visitWhereStatement(statement)

            elif statement["type"] == "from_statement": self.visitFromStatement(statement)

            #TODO: ORDER BY statement

            else: raise Exception(f"Statement type '{statement['type']}' is NOT valid")

    def visitSelectStatement(self, node): 
        
        self.QueryFormatted += "SELECT "

        self.QueryFormatted += f"TOP {node['limit_row']} " if node['limit_row'] else "" + "DISTINCT " if node["distinct"] else ""

        for field in node["fields_list"]:
            
            self.visitField(field)
            
            self.QueryFormatted += ", "

        #TODO: find a way to avoid self.QueryFormatted = self.QueryFormatted.rstrip(", ")
        self.QueryFormatted = self.QueryFormatted.rstrip(", ")

    def visitFromStatement(self, node): 

        self.addNewLine(0, 0)

        self.QueryFormatted += "FROM "

        for table in node["tables_list"]:
            
            if table["type"] == "join_expression": self.visitJoinExpression(table)

            elif table["type"] == "table": self.visitTable(table)

            else: raise Exception(f"Table type '{table['type']}' is NOT valid")

        #TODO: find a way to avoid self.QueryFormatted = self.QueryFormatted.rstrip(", ")
        self.QueryFormatted = self.QueryFormatted.rstrip(", ")

    def visitWhereStatement(self, node): 

        self.addNewLine(0, 0)

        self.QueryFormatted += "WHERE "

        for item in node["conditions_list"]: 

            if item["type"] == "block_statement": self.visitBlockStatementCondition(item)

            else: 
                self.addNewLine(1, 0)
                self.visitCondition(item) 
                self.addIndents(-1, 0)           

    def visitGroupByStatement(self, node): 

        self.addNewLine(0, 0)

        self.QueryFormatted += "GROUP BY "

        for field in node["fields_list"]: 

            self.visitField(field)

            self.QueryFormatted += ", "

        #TODO: find a way to avoid self.QueryFormatted = self.QueryFormatted.rstrip(", ")
        self.QueryFormatted = self.QueryFormatted.rstrip(", ")

    def visitHavingStatement(self, node):

        self.addIndents(0, 0, True)

        self.QueryFormatted += "HAVING "

        for condition in node["conditions_list"]: self.visitCondition(condition)

    def visitBinaryExpression(self, node): 
        
        self.visitExpression(node["left"])

        self.QueryFormatted += f" {node['operator']} "

        self.visitExpression(node["right"])

    def visitField(self, node):
        
        if node["body"]["type"] == "block_statement": self.visitBlockStatementField(node["body"])

        else: 

            if node["body"]["type"] == "binary_expression": self.visitBinaryExpression(node["body"])

            elif node["body"]["type"] == "case_expression": self.visitCaseExpression(node["body"])
            
            elif node["body"]["type"] == "identifier": self.visitIdentifier(node["body"])

            elif node["body"]["type"] == "function": self.visitFunction(node["body"])

            elif node["body"]["type"] == "literal": self.visitLiteral(node["body"])

            else: raise Exception(f"Field type '{node['body']['type']}' is NOT valid")

        if node["alias"]: self.QueryFormatted += f" AS {node['alias']['value']}"

    def visitKeyword(self, node):

        if node["body"]["type"] == "block_statement": self.visitBlockStatement(node["body"])

        else: 
            
            if node["body"]["type"] == "identifier": self.visitIdentifier(node["body"])

            else: raise Exception(f"Keyword type '{node['body']['type']}' is NOT valid")
            
    def visitTable(self, node):

        if node["operator"]: self.QueryFormatted += f"{node['operator']} "

        if node["body"]["type"] == "block_statement": self.visitBlockStatementQueries(node["body"])

        elif node["body"]["type"] == "identifier": 
            
            self.addNewLine(1, 0)
            self.visitIdentifier(node["body"])
            self.addIndents(-1, 0)

        else: raise Exception(f"Table type '{node['body']['type']}' is NOT valid")

        if node["alias"]: self.QueryFormatted += f" AS {node['alias']['value']}"

    def visitCondition(self, node):

        operator = node["operator"]

        if operator: self.QueryFormatted += f" {operator} " if operator != "NOT" else f"{operator} " 

        if node["body"]["type"] == "between_expression": self.visitBetweenExpression(node["body"], operator == "NOT")

        elif node["body"]["type"] == "exists_expression": self.visitExistsExpression(node["body"], operator == "NOT")

        elif node["body"]["type"] == "in_expression": self.visitInExpression(node["body"], operator == "NOT")

        elif node["body"]["type"] == "block_statement": self.visitBlockStatementCondition(node["body"])

        elif node["body"]["type"] == "binary_expression": self.visitBinaryExpression(node["body"])

        elif node["body"]["type"] == "condition_expression": self.visitCondition(node["body"])

        elif node["body"]["type"] == "is_expression": self.visitIsExpression(node["body"])

        elif node["body"]["type"] == "literal": self.visitLiteral(node["body"])

        else: raise Exception(f"Condition type '{node['body']['type']}' is NOT valid")

    def visitExpression(self, node):

        if node["type"] == "block_statement": self.visitBlockStatementQueries(node)

        elif node["type"] == "binary_expression": self.visitBinaryExpression(node)

        elif node["type"] == "condition_expression": self.visitCondition(node)

        elif node["type"] == "keyword_expression": self.visitKeyword(node)

        elif node["type"] == "function": self.visitFunction(node)
        
        elif node["type"] == "literal": self.visitLiteral(node)

        elif node["type"] == "field": self.visitField(node)

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

    def visitBlockStatementField(self, node):

        self.QueryFormatted += "("

        for item in node["body"]:
            
            if item["type"] == "binary_expression": self.visitBinaryExpression(item)

            elif item["type"] == "keyword_expression": self.visitKeyword(item)

            elif item["type"] == "query": self.visitQuery(item)

            else: raise Exception(f"Block statement field type '{item['type']}' is NOT valid")

        self.QueryFormatted += ")"

    def visitBlockStatementCondition(self, node):

        self.addNewLine(1, 0)

        self.QueryFormatted += "("

        for item in node["body"]: 

            if item["type"] == "block_statement": self.visitBlockStatementCondition(item)

            else:
                self.addNewLine(1, 0)
                self.visitCondition(item)
                self.addIndents(-1, 0)

        self.addNewLine(0, 0)

        self.QueryFormatted += ")"

        self.addIndents(-1, 0)
        
    def visitBlockStatementQueries(self, node):

        self.addNewLine(1, 0)

        self.QueryFormatted += "("

        self.addNewLine(1, 0)

        for item in node["body"]:

            self.visitQuery(item)
            self.addNewLine(0, 0)
            self.QueryFormatted += "UNION"
            self.addNewLine(0, 0)
        
        #TODO: find a way to avoid self.QueryFormatted = self.QueryFormatted.rstrip().rstrip("UNION").rstrip()
        self.QueryFormatted = self.QueryFormatted.rstrip().rstrip("UNION").rstrip()

        self.addNewLine(-1, 0)

        self.QueryFormatted += ")"

        self.addIndents(-1, 0)

    def visitBlockStatement(self, node):
        
        self.QueryFormatted += "("

        for item in node["body"]:
            
            if item["type"] == "binary_expression": self.visitBinaryExpression(item)

            elif item["type"] == "keyword_expression": self.visitKeyword(item)

            else: raise Exception(item)

        self.QueryFormatted += ")"

    def visitJoinExpression(self, node):
        
        self.addNewLine(2, 0)

        self.QueryFormatted += f"{node['operator']} "

        self.visitTable(node["value"])

        self.QueryFormatted += " ON "

        for condition in node["conditions_list"]: self.visitCondition(condition)

        self.addIndents(-2, 0)

    def visitExistsExpression(self, node, is_negative):

        self.QueryFormatted += "EXISTS "

        self.QueryFormatted += "("

        self.addNewLine(2, 0)

        #TODO: UNION query
        for query in node["queries_list"]: self.visitQuery(query)

        self.addNewLine(0, 0)

        self.QueryFormatted += f")"

        self.addIndents(-2, 0)

    def visitCaseExpression(self, node):

        self.addNewLine(1, 0)

        self.QueryFormatted += "CASE "

        for item in node["body"]: 

            if item["type"] == "when_expression":

                self.QueryFormatted += "WHEN "
                
                for condition in item["conditions_list"]: self.visitCondition(condition)
            
                self.QueryFormatted += " THEN "

                self.visitExpression(item["then_expression"])

            else:

                self.QueryFormatted += " ELSE "

                self.visitExpression(item["then_expression"])

        self.QueryFormatted += f" END "

        if node["alias"]: self.QueryFormatted += f"AS {node['alias']['value']}"

        self.addNewLine(-1, 0)

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
