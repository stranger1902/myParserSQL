class MyParserException(Exception):

    def __init__(self, msg):
        
        if msg:
            if isinstance(msg, str):
                self.message = msg
            else:
                self.message = None
        else:
            self.message = None

    def __str__(self):

        if self.message:
            return self.message
        else:
            return 'MyParserException has been raised'

class MySyntaxException(Exception):

    def __init__(self, msg):
        
        if msg:
            if isinstance(msg, str):
                self.message = msg
            else:
                self.message = None
        else:
            self.message = None

    def __str__(self):

        if self.message:
            return self.message
        else:
            return 'MySyntaxException has been raised'
            
class MyTypeException(Exception):

    def __init__(self, msg):
        
        if msg:
            if isinstance(msg, str):
                self.message = msg
            else:
                self.message = None
        else:
            self.message = None

    def __str__(self):

        if self.message:
            return self.message
        else:
            return 'MyTypeException has been raised'

class MyDatabaseException(Exception):

    def __init__(self, msg):
        
        if msg:
            if isinstance(msg, str):
                self.message = msg
            else:
                self.message = None
        else:
            self.message = None

    def __str__(self):

        if self.message:
            return self.message
        else:
            return 'MyDatabaseException has been raised'

class MyMailException(Exception):

    def __init__(self, msg):
        
        if msg:
            if isinstance(msg, str):
                self.message = msg
            else:
                self.message = None
        else:
            self.message = None

    def __str__(self):

        if self.message:
            return self.message
        else:
            return 'MyMailException has been raised'