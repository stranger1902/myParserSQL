import json

class MyParserException(Exception):

    def __init__(self, msg):
        
        if msg:
            
            if isinstance(msg, str): self.message = msg

            elif isinstance(msg, dict) or isinstance(msg, list): self.message = "\n" + json.dumps(msg, indent=4)

            else: self.message = None

        else: self.message = None

    def __str__(self): return self.message if self.message else "MyParserException has been raised"

class MySyntaxException(Exception):

    def __init__(self, msg):
        
        if msg:
            
            if isinstance(msg, str): self.message = msg

            elif isinstance(msg, dict) or isinstance(msg, list): self.message = "\n" + json.dumps(msg, indent=4)

            else: self.message = None

        else: self.message = None

    def __str__(self): return self.message if self.message else "MySyntaxException has been raised"
            
class MyTypeException(Exception):

    def __init__(self, msg):
        
        if msg:
            
            if isinstance(msg, str): self.message = msg

            elif isinstance(msg, dict) or isinstance(msg, list): self.message = "\n" + json.dumps(msg, indent=4)

            else: self.message = None

        else: self.message = None

    def __str__(self): return self.message if self.message else "MyTypeException has been raised"
