# Parser SQL

Python implementation of a Parser SQL based on the Parsing Theory, in particular: 
- it analizes the sintax of a query and generates the relative AST
- it can, eventually, beautify the query from AST

## Table of Contents

- [Installation](#installation)
- [How To Use](#how-to-use)
- [TODO List](#todo-list)

## Installation

```bash
python3 -m venv venv/
source venv/bin/activate
pip install -r requirements.txt
```

## How To Use

This is a simple way to parse and beautify a query from string variable.

```python
from myBeautifier import MyBeautifier
from myParser import MyParser

if __name__ == "__main__":

    #define a SQL Parser
    myParser = MyParser("query_select")
    
    #define query to parse
    myQuery = "SELECT field FROM table WHERE a = b"

    #generate AST from query
    myAST = myParser.parse(myQuery)
    
    #optionally, you can store AST into a file
    myParser.write(myAST, U.CURRENT_PATH, U.FILENAME.AST_FILENAME.value)

    #define a SQL Beautifier
    myBeautifier = MyBeautifier()
    
    #beautify query from AST
    queryFormatted = myBeautifier.beautify(myAST)
    
    #optionally, you can store formatted query into a file
    myBeautifier.write(queryFormatted, U.CURRENT_PATH, U.FILENAME.OUTPUT_FILENAME.value)
    
    print(queryFormatted)
```

This is a simple way to parse and beautify a query from file.

```python
from myBeautifier import MyBeautifier
from myParser import MyParser

if __name__ == "__main__":
    
    #define a SQL Parser
    myParser = MyParser("query_select")
    
    #generate AST from query imported from file
    myAST = myParser.parseFromFile("__file_path__", "__input_file_name__")
    
    #optionally, you can store AST into a file
    myParser.write(myAST, "__file_path__", "__output_file_name__")
    
    #define a SQL Beautifier
    myBeautifier = MyBeautifier()
    
    #beautify query from AST
    queryFormatted = myBeautifier.beautify(myAST)
    
    #optionally, you can store formatted query into a file
    myBeautifier.write(queryFormatted, "__file_path__", "__output_file_name__")
    
    print(queryFormatted)
```

## TODO List
- impedire casi in cui una condizione è costituita soltanto da un identificatore
  - es. SELECT campo FROM tabella a WHERE hgvxnsfj AND a.campo < 3
- impedire alias nelle condizioni
  - es. SELECT campo FROM tabella WHERE a = b AS c
- impedire alias nelle expression
  - es. SELECT 1 AS a + 2 FROM tabella
- gestire le keyword ALL e ANY
