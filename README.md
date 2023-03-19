# Parser SQL

Python implementation of a Parser SQL (SQL Server Language) based on the Parsing Theory, in particular: 
- it analizes the sintax of a query and generates the relative AST
- it can, eventually, beautify the query from AST

ATTENTION! This Parser is just a syntactic analizer, NOT a semantic one

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [TODO list](#todo-list)

## Installation

```bash
python3 -m venv venv/
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

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
    myParser.write(myAST, "__some_output_path__", "__some_output_filename__")

    #define a SQL Beautifier
    myBeautifier = MyBeautifier()
    
    #beautify query from AST
    queryFormatted = myBeautifier.beautify(myAST)
    
    #optionally, you can store formatted query into a file
    myBeautifier.write(queryFormatted, "__some_output_path__", "__some_output_filename__")
    
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
    myAST = myParser.parseFromFile("__some_input_path__", "__some_input_filename__")
    
    #optionally, you can store AST into a file
    myParser.write(myAST, "__some_output_path__", "__some_output_filename__")
    
    #define a SQL Beautifier
    myBeautifier = MyBeautifier()
    
    #beautify query from AST
    queryFormatted = myBeautifier.beautify(myAST)
    
    #optionally, you can store formatted query into a file
    myBeautifier.write(queryFormatted, "__some_output_path__", "__some_output_filename__")
    
    print(queryFormatted)
```

## TODO List

- keyword ALL and ANY
- optimize code of MyBeautifier class

