import myException as EX
import myUtility as U
import regex as re

RegexList = [
             # COMMENTS
             ("^\/\*[\s\S]*?\*\/", None, "COMMENT", "LOWER"),                           # multi lines comment
             ("^\-\-.*", None, "COMMENT", "LOWER"),                                     # single line comment

            # NUMBERS
             ("^((\d+(\.\d*)?)|(\.\d+))", "NUMBER", "LITERAL", "LOWER"),                # literal number (integer and float both)
            
             # OPERATORS
             ("^[\<\>\=][\=\>]?", "RELATIONAL_OPERATOR", "OPERATOR", "LOWER"),          # relational operator
             ("^[\+\-]", "ADDITIVE_OPERATOR", "OPERATOR", "LOWER"),                     # plus and minus operator
             ("^[\/]", "SLASH", "OPERATOR", "LOWER"),                                   # slash operator             
             ("^[\*]", "STAR", "LITERAL", "LOWER"),                                     # star operator

             # SYMBOLS
             ("^\)", "CLOSE-ROUND-BRACKET", "SYMBOL", "LOWER"),                         # closed round brackets
             ("^\(", "OPEN-ROUND-BRACKET", "SYMBOL", "LOWER"),                          # opened round brackets
             ("^\;", "SEMICOLON", "SYMBOL", "LOWER"),                                   # semi-colon
             ("^\.", "FULL_STOP", "SYMBOL", "LOWER"),                                   # full-stop
             ("^\,", "COMMA", "SYMBOL", "LOWER"),                                       # comma
             ("^\s+", None, "SYMBOL", "LOWER"),                                         # whitespaces

             # KEYWORDS 
             # La categoria KEYWORDS è messa prima della categoria IDENTIFIERS in modo tale che venga riconosciuta come parole chiave da non poter usare come identificatori
             ("^(?i)\\bDISTINCT\\b", "DISTINCT", "KEYWORD", "UPPER"),                   # distinct keyword
             ("^(?i)\\bGROUP BY\\b", "GROUP_BY", "KEYWORD", "UPPER"),                   # group by keyword
             ("^(?i)\\bORDER BY\\b", "ORDER_BY", "KEYWORD", "UPPER"),                   # order by keyword
             ("^(?i)\\bBETWEEN\\b", "BETWEEN", "KEYWORD", "UPPER"),                     # distinct keyword
             ("^(?i)\\bHAVING\\b", "HAVING", "KEYWORD", "UPPER"),                       # having keyword
             ("^(?i)\\bSELECT\\b", "SELECT", "KEYWORD", "UPPER"),                       # select keyword
             ("^(?i)\\bEXISTS\\b", "EXISTS", "KEYWORD", "UPPER"),                       # exists keyword
             ("^(?i)\\bNOLOCK\\b", "NOLOCK", "KEYWORD", "UPPER"),                       # nolock keyword
             ("^(?i)\\bOUTER\\b", "OUTER", "KEYWORD", "UPPER"),                         # outer keyword
             ("^(?i)\\bINNER\\b", "INNER", "KEYWORD", "UPPER"),                         # inner keyword
             ("^(?i)\\bUNION\\b", "UNION", "KEYWORD", "UPPER"),                         # union keyword
             ("^(?i)\\bWHERE\\b", "WHERE", "KEYWORD", "UPPER"),                         # where keyword
             ("^(?i)\\bRIGHT\\b", "RIGHT", "KEYWORD", "UPPER"),                         # right keyword
             ("^(?i)\\bFROM\\b", "FROM", "KEYWORD", "UPPER"),                           # from keyword
             ("^(?i)\\bJOIN\\b", "JOIN", "KEYWORD", "UPPER"),                           # join keyword
             ("^(?i)\\bLEFT\\b", "LEFT", "KEYWORD", "UPPER"),                           # left keyword
             ("^(?i)\\bELSE\\b", "ELSE", "KEYWORD", "UPPER"),                           # else keyword
             ("^(?i)\\bCASE\\b", "CASE", "KEYWORD", "UPPER"),                           # case keyword
             ("^(?i)\\bWHEN\\b", "WHEN", "KEYWORD", "UPPER"),                           # when keyword
             ("^(?i)\\bTHEN\\b", "THEN", "KEYWORD", "UPPER"),                           # then keyword
             ("^(?i)\\bDESC\\b", "DESC", "KEYWORD", "UPPER"),                           # desc keyword
             ("^(?i)\\bLIKE\\b", "LIKE", "KEYWORD", "UPPER"),                           # like keyword
             ("^(?i)\\bASC\\b", "ASC", "KEYWORD", "UPPER"),                             # asc keyword
             ("^(?i)\\bEND\\b", "END", "KEYWORD", "UPPER"),                             # end keyword
             ("^(?i)\\bTOP\\b", "TOP", "KEYWORD", "UPPER"),                             # top keyword
             ("^(?i)\\bON\\b", "ON", "KEYWORD", "UPPER"),                               # on keyword
             ("^(?i)\\bAS\\b", "AS", "KEYWORD", "UPPER"),                               # as keyword
             ("^(?i)\\bIN\\b", "IN", "KEYWORD", "UPPER"),                               # in keyword
             ("^(?i)\\bIS\\b", "IS", "KEYWORD", "UPPER"),                               # is keyword

             ("^(?i)\\bNULL\\b", "NULL", "LITERAL", "UPPER"),                           # null keyword

             ("^(?i)\\bAND\\b", "AND", "CONDITION", "UPPER"),                           # and keyword
             ("^(?i)\\bNOT\\b", "NOT", "CONDITION", "UPPER"),                           # not keyword
             ("^(?i)\\bOR\\b", "OR", "CONDITION", "UPPER"),                             # or keyword

             # MATHEMATICAL FUNCTIONS
             ("^(?i)\\bRADIANS\b", "FUNCTION", "ID", "UPPER"),                          # radians() function
             ("^(?i)\\bCEILING\b", "FUNCTION", "ID", "UPPER"),                          # ceiling() function
             ("^(?i)\\bDEGREES\b", "FUNCTION", "ID", "UPPER"),                          # degrees() function
             ("^(?i)\\bROUND\\b", "FUNCTION", "ID", "UPPER"),                           # round() function
             ("^(?i)\\bTRUNC\\b", "FUNCTION", "ID", "UPPER"),                           # trunc() function
             ("^(?i)\\bSQUARE\b", "FUNCTION", "ID", "UPPER"),                           # square() function
             ("^(?i)\\bFLOOR\\b", "FUNCTION", "ID", "UPPER"),                           # floor() function
             ("^(?i)\\bPOWER\\b", "FUNCTION", "ID", "UPPER"),                           # power() function
             ("^(?i)\\bROUND\\b", "FUNCTION", "ID", "UPPER"),                           # round() function
             ("^(?i)\\bTRUNC\\b", "FUNCTION", "ID", "UPPER"),                           # trunc() function
             ("^(?i)\\bLOG10\b", "FUNCTION", "ID", "UPPER"),                            # log10() function
             ("^(?i)\\bASIN\\b", "FUNCTION", "ID", "UPPER"),                            # arcsin() function
             ("^(?i)\\bACOS\\b", "FUNCTION", "ID", "UPPER"),                            # arccos() function
             ("^(?i)\\bATAN\\b", "FUNCTION", "ID", "UPPER"),                            # arctan() function
             ("^(?i)\\bSINH\\b", "FUNCTION", "ID", "UPPER"),                            # sinh() function
             ("^(?i)\\bCOSH\\b", "FUNCTION", "ID", "UPPER"),                            # cosh() function
             ("^(?i)\\bTANH\\b", "FUNCTION", "ID", "UPPER"),                            # tanh() function
             ("^(?i)\\bSQRT\\b", "FUNCTION", "ID", "UPPER"),                            # sqrt() function
             ("^(?i)\\bCEIL\\b", "FUNCTION", "ID", "UPPER"),                            # ceil() function
             ("^(?i)\\bSIGN\\b", "FUNCTION", "ID", "UPPER"),                            # sign() function
             ("^(?i)\\bRAND\b", "FUNCTION", "ID", "UPPER"),                             # rand() function
             ("^(?i)\\bATN2\b", "FUNCTION", "ID", "UPPER"),                             # atn2() function
             ("^(?i)\\bSIN\\b", "FUNCTION", "ID", "UPPER"),                             # sin() function
             ("^(?i)\\bCOS\\b", "FUNCTION", "ID", "UPPER"),                             # cos() function
             ("^(?i)\\bTAN\\b", "FUNCTION", "ID", "UPPER"),                             # tan() function
             ("^(?i)\\bEXP\\b", "FUNCTION", "ID", "UPPER"),                             # exp() function
             ("^(?i)\\bLOG\\b", "FUNCTION", "ID", "UPPER"),                             # log() function
             ("^(?i)\\bABS\\b", "FUNCTION", "ID", "UPPER"),                             # abs() function
             ("^(?i)\\bCOT\b", "FUNCTION", "ID", "UPPER"),                              # cot() function
             ("^(?i)\\bLN\\b", "FUNCTION", "ID", "UPPER"),                              # ln() function
             ("^(?i)\\bMOD\b", "FUNCTION", "ID", "UPPER"),                              # mod() function
             ("^(?i)\\bPI\b", "FUNCTION", "ID", "UPPER"),                               # pigreco() function

             # STRINGS FUNCTIONS
             ("^(?i)\\bDATALENGTH\\b", "FUNCTION", "ID", "UPPER"),                      # dataLength() function
             ("^(?i)\\bDIFFERENCE\\b", "FUNCTION", "ID", "UPPER"),                      # difference() function
             ("^(?i)\\bCHARINDEX\\b", "FUNCTION", "ID", "UPPER"),                       # charIndex() function
             ("^(?i)\\bCONCAT_WS\\b", "FUNCTION", "ID", "UPPER"),                       # concatWS() function
             ("^(?i)\\bQUOTENAME\\b", "FUNCTION", "ID", "UPPER"),                       # quoteName() function
             ("^(?i)\\bREPLICATE\\b", "FUNCTION", "ID", "UPPER"),                       # replicate() function
             ("^(?i)\\bSUBSTRING\\b", "FUNCTION", "ID", "UPPER"),                       # substring() function
             ("^(?i)\\bTRANSLATE\\b", "FUNCTION", "ID", "UPPER"),                       # translate() function
             ("^(?i)\\bPATINDEX\\b", "FUNCTION", "ID", "UPPER"),                        # patIndex() function
             ("^(?i)\\bUNICODE\\b", "FUNCTION", "ID", "UPPER"),                         # unicode() function
             ("^(?i)\\bREVERSE\\b", "FUNCTION", "ID", "UPPER"),                         # reverse() function
             ("^(?i)\\bSOUNDEX\\b", "FUNCTION", "ID", "UPPER"),                         # soundEX() function
             ("^(?i)\\bSOUNDEX\\b", "FUNCTION", "ID", "UPPER"),                         # soundEX() function
             ("^(?i)\\bREPLACE\\b", "FUNCTION", "ID", "UPPER"),                         # replace() function
             ("^(?i)\\bINITCAP\\b", "FUNCTION", "ID", "UPPER"),                         # initcap() function
             ("^(?i)\\bCONCAT\\b", "FUNCTION", "ID", "UPPER"),                          # concat() function
             ("^(?i)\\bSUBSTR\\b", "FUNCTION", "ID", "UPPER"),                          # substr() function
             ("^(?i)\\bLENGTH\\b", "FUNCTION", "ID", "UPPER"),                          # length() function
             ("^(?i)\\bFORMAT\\b", "FUNCTION", "ID", "UPPER"),                          # format() function
             ("^(?i)\\bNCHAR\\b", "FUNCTION", "ID", "UPPER"),                           # nChar() function
             #("^(?i)\\bRIGHT\\b", "FUNCTION", "ID", "UPPER"),                          # right() function
             ("^(?i)\\bSPACE\\b", "FUNCTION", "ID", "UPPER"),                           # space() function
             ("^(?i)\\bSTUFF\\b", "FUNCTION", "ID", "UPPER"),                           # stuff() function
             ("^(?i)\\bLOWER\\b", "FUNCTION", "ID", "UPPER"),                           # lower() function
             ("^(?i)\\bUPPER\\b", "FUNCTION", "ID", "UPPER"),                           # upper() function
             ("^(?i)\\bLTRIM\\b", "FUNCTION", "ID", "UPPER"),                           # ltrim() function
             ("^(?i)\\bRTRIM\\b", "FUNCTION", "ID", "UPPER"),                           # rtrim() function
             ("^(?i)\\bINSTR\\b", "FUNCTION", "ID", "UPPER"),                           # instr() function
             ("^(?i)\\bASCII\\b", "FUNCTION", "ID", "UPPER"),                           # ascii() function
             ("^(?i)\\bLPAD\\b", "FUNCTION", "ID", "UPPER"),                            # lpad() function
             ("^(?i)\\bRPAD\\b", "FUNCTION", "ID", "UPPER"),                            # rpad() function
             ("^(?i)\\bCHAR\\b", "FUNCTION", "ID", "UPPER"),                            # char() function
             ("^(?i)\\bTRIM\\b", "FUNCTION", "ID", "UPPER"),                            # trim() function
             #("^(?i)\\bLEFT\\b", "FUNCTION", "ID", "UPPER"),                           # left() function
             ("^(?i)\\bSTR\\b", "FUNCTION", "ID", "UPPER"),                             # str() function
             ("^(?i)\\bLEN\\b", "FUNCTION", "ID", "UPPER"),                             # len() function

             # GROUP FUNCTIONS
             ("^(?i)\\bVARIANCE\\b", "FUNCTION", "ID", "UPPER"),                        # variance() function
             ("^(?i)\\bSTDDEV\\b", "FUNCTION", "ID", "UPPER"),                          # stddev() function
             ("^(?i)\\bMEDIAN\\b", "FUNCTION", "ID", "UPPER"),                          # median() function
             ("^(?i)\\bCOUNT\\b", "FUNCTION", "ID", "UPPER"),                           # count() function
             ("^(?i)\\bCORR\\b", "FUNCTION", "ID", "UPPER"),                            # corr() function             
             ("^(?i)\\bAVG\\b", "FUNCTION", "ID", "UPPER"),                             # avg() function
             ("^(?i)\\bMAX\\b", "FUNCTION", "ID", "UPPER"),                             # max() function
             ("^(?i)\\bMIN\\b", "FUNCTION", "ID", "UPPER"),                             # min() function
             ("^(?i)\\bSUM\\b", "FUNCTION", "ID", "UPPER"),                             # sum() function

             # DATE AND TIME FUNCTIONS
             ("^(?i)\\bCURRENT_TIMESTAMP\\b", "FUNCTION", "ID", "UPPER"),               # currentTimestamp() function
             ("^(?i)\\bMONTHS_BETWEEN\\b", "FUNCTION", "ID", "UPPER"),                  # monthsBetween() function
             ("^(?i)\\bDATEFROMPARTS\\b", "FUNCTION", "ID", "UPPER"),                   # dateFromParts() function
             ("^(?i)\\bSYSDATETIME\\b", "FUNCTION", "ID", "UPPER"),                     # sysDateTime() function
             ("^(?i)\\bGETUTCDATE\\b", "FUNCTION", "ID", "UPPER"),                      # getUTCdate() function
             ("^(?i)\\bADD_MONTHS\\b", "FUNCTION", "ID", "UPPER"),                      # addMonths() function
             ("^(?i)\\bDATEDIFF\\b", "FUNCTION", "ID", "UPPER"),                        # dateDiff() function
             ("^(?i)\\bDATENAME\\b", "FUNCTION", "ID", "UPPER"),                        # dateName() function
             ("^(?i)\\bDATEPART\\b", "FUNCTION", "ID", "UPPER"),                        # datePart() function
             ("^(?i)\\bLAST_DAY\\b", "FUNCTION", "ID", "UPPER"),                        # lastDay() function
             ("^(?i)\\bNEW_TIME\\b", "FUNCTION", "ID", "UPPER"),                        # newTime() function
             ("^(?i)\\bNEXT_DAY\\b", "FUNCTION", "ID", "UPPER"),                        # nextDay() function
             ("^(?i)\\bGREATEST\\b", "FUNCTION", "ID", "UPPER"),                        # greatest() function
             ("^(?i)\\bSYSDATE\\b", "FUNCTION", "ID", "UPPER"),                         # sysDate() function
             ("^(?i)\\bDATEADD\\b", "FUNCTION", "ID", "UPPER"),                         # dateAdd() function
             ("^(?i)\\bGETDATE\\b", "FUNCTION", "ID", "UPPER"),                         # getDate() function
             ("^(?i)\\bISDATE\\b", "FUNCTION", "ID", "UPPER"),                          # isDate() function
             ("^(?i)\\bMONTH\\b", "FUNCTION", "ID", "UPPER"),                           # month() function
             ("^(?i)\\bLEAST\\b", "FUNCTION", "ID", "UPPER"),                           # least() function
             ("^(?i)\\bYEAR\\b", "FUNCTION", "ID", "UPPER"),                            # year() function
             ("^(?i)\\bDAY\\b", "FUNCTION", "ID", "UPPER"),                             # day() function

             # CONVERTION FUNCTIONS
             ("^(?i)\\bTO_CHAR\\b", "FUNCTION", "ID", "UPPER"),                         # toChar() function
             ("^(?i)\\bTO_DATE\\b", "FUNCTION", "ID", "UPPER"),                         # toDate() function
             ("^(?i)\\bCONVERT\\b", "FUNCTION", "ID", "UPPER"),                         # convert() function
             ("^(?i)\\bCAST\\b", "FUNCTION", "ID", "UPPER"),                            # cast() function

             # OTHER FUNCTIONS
             ("^(?i)\\bSESSIONPROPERTY\\b", "FUNCTION", "ID", "UPPER"),                 # sessionProperty() function
             ("^(?i)\\bSESSION_USER\\b", "FUNCTION", "ID", "UPPER"),                    # sessionUser() function
             ("^(?i)\\bCURRENT_USER\\b", "FUNCTION", "ID", "UPPER"),                    # currentUser() function
             ("^(?i)\\bSYSTEM_USER\\b", "FUNCTION", "ID", "UPPER"),                     # systemUser() function
             ("^(?i)\\bISNUMERIC\\b", "FUNCTION", "ID", "UPPER"),                       # isNumeric() function
             ("^(?i)\\bUSER_NAME\\b", "FUNCTION", "ID", "UPPER"),                       # userName() function
             ("^(?i)\\bCOALESCE\\b", "FUNCTION", "ID", "UPPER"),                        # coalesce() function
             ("^(?i)\\bISNULL\\b", "FUNCTION", "ID", "UPPER"),                          # isNull() function
             ("^(?i)\\bNULLIF\\b", "FUNCTION", "ID", "UPPER"),                          # nullIf() function
             ("^(?i)\\bIIF\\b", "FUNCTION", "ID", "UPPER"),                             # iif() function
              
             # STRINGS
             ("^\'[^']*\'", "STRING", "LITERAL", None),                                 # literal single quote string

             # IDENTIFIERS
             ("^(?(?=\()\(\w+(?(?=\.).\w+|)\)|\w+(?(?=\.).\w+|))", "FIELDNAME", "ID", "LOWER"),          # fieldname with/without alias table surrounded by optional round parenthesis (es: alias.fieldname)
             ]

class MyTokenizer():

    def __init__(self): self.Position = 0

    def initialize(self, string):

        self.String = string
        self.Position = 0

    def getNextToken(self):
        
        if not self.Position < len(self.String): return None

        string = self.String[self.Position:]

        for Regex in RegexList:

            result = self.isMatch(Regex, string)

            if not result: continue

            if not Regex[1]: return self.getNextToken()     # skip token

            return {"type" : Regex[1], "value" : result, "category" : Regex[2], "format" : Regex[3]}

        raise EX.MySyntaxException(f"Nessun Token ha riconosciuto la stringa '{string}'")

    def isMatch(self, regex, string):

        result = re.search(regex[0], string)

        if not result: return None

        self.Position += len(result.group())

        return result.group()
        