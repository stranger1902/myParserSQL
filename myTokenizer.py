import myException as EX
import regex as re

RegexList = [
             # COMMENTS
             ("^\/\*[\s\S]*?\*\/", None, "COMMENT"),                           # multi lines comment
             ("^\-\-.*", None, "COMMENT"),                                     # single line comment

            # NUMBERS
             ("^((\d+(\.\d*)?)|(\.\d+))", "NUMBER", "LITERAL"),                # literal number (integer and float both)
            
             # OPERATORS
             ("^[\<\>\=][\=\>]?", "RELATIONAL_OPERATOR", "OPERATOR"),          # relational operator
             ("^[\+\-]", "ADDITIVE_OPERATOR", "OPERATOR"),                     # plus and minus operator
             ("^[\/]", "SLASH", "OPERATOR"),                                   # slash operator             
             ("^[\*]", "STAR", "LITERAL"),                                     # star operator

             # SYMBOLS
             ("^\)", "CLOSE-ROUND-BRACKET", "SYMBOL"),                         # closed round brackets
             ("^\(", "OPEN-ROUND-BRACKET", "SYMBOL"),                          # opened round brackets
             ("^\;", "SEMICOLON", "SYMBOL"),                                   # semi-colon
             ("^\.", "FULL_STOP", "SYMBOL"),                                   # full-stop
             ("^\,", "COMMA", "SYMBOL"),                                       # comma
             ("^\s+", None, "SYMBOL"),                                         # whitespaces

             # KEYWORDS 
             # La categoria KEYWORDS è messa prima della categoria IDENTIFIERS in modo tale che venga riconosciuta come parole chiave da non poter usare come identificatori
             ("^(?i)\\bDISTINCT\\b", "DISTINCT", "KEYWORD"),                   # distinct keyword
             ("^(?i)\\bGROUP BY\\b", "GROUP_BY", "KEYWORD"),                   # group by keyword
             ("^(?i)\\bORDER BY\\b", "ORDER_BY", "KEYWORD"),                   # order by keyword
             ("^(?i)\\bBETWEEN\\b", "BETWEEN", "KEYWORD"),                     # distinct keyword
             ("^(?i)\\bHAVING\\b", "HAVING", "KEYWORD"),                       # having keyword
             ("^(?i)\\bSELECT\\b", "SELECT", "KEYWORD"),                       # select keyword
             ("^(?i)\\bEXISTS\\b", "EXISTS", "KEYWORD"),                       # exists keyword
             ("^(?i)\\bNOLOCK\\b", "NOLOCK", "KEYWORD"),                       # nolock keyword
             ("^(?i)\\bOUTER\\b", "OUTER", "KEYWORD"),                         # outer keyword
             ("^(?i)\\bINNER\\b", "INNER", "KEYWORD"),                         # inner keyword
             ("^(?i)\\bUNION\\b", "UNION", "KEYWORD"),                         # union keyword
             ("^(?i)\\bWHERE\\b", "WHERE", "KEYWORD"),                         # where keyword
             ("^(?i)\\bRIGHT\\b", "RIGHT", "KEYWORD"),                         # right keyword
             ("^(?i)\\bFROM\\b", "FROM", "KEYWORD"),                           # from keyword
             ("^(?i)\\bJOIN\\b", "JOIN", "KEYWORD"),                           # join keyword
             ("^(?i)\\bLEFT\\b", "LEFT", "KEYWORD"),                           # left keyword
             ("^(?i)\\bELSE\\b", "ELSE", "KEYWORD"),                           # else keyword
             ("^(?i)\\bCASE\\b", "CASE", "KEYWORD"),                           # case keyword
             ("^(?i)\\bWHEN\\b", "WHEN", "KEYWORD"),                           # when keyword
             ("^(?i)\\bTHEN\\b", "THEN", "KEYWORD"),                           # then keyword
             ("^(?i)\\bDESC\\b", "DESC", "KEYWORD"),                           # desc keyword
             ("^(?i)\\bLIKE\\b", "LIKE", "KEYWORD"),                           # like keyword
             ("^(?i)\\bASC\\b", "ASC", "KEYWORD"),                             # asc keyword
             ("^(?i)\\bEND\\b", "END", "KEYWORD"),                             # end keyword
             ("^(?i)\\bTOP\\b", "TOP", "KEYWORD"),                             # top keyword
             ("^(?i)\\bON\\b", "ON", "KEYWORD"),                               # on keyword
             ("^(?i)\\bAS\\b", "AS", "KEYWORD"),                               # as keyword
             ("^(?i)\\bIN\\b", "IN", "KEYWORD"),                               # in keyword
             ("^(?i)\\bIS\\b", "IS", "KEYWORD"),                               # is keyword

             ("^(?i)\\bNULL\\b", "NULL", "LITERAL"),                           # null keyword

             ("^(?i)\\bAND\\b", "AND", "CONDITION"),                           # and keyword
             ("^(?i)\\bNOT\\b", "NOT", "CONDITION"),                           # not keyword
             ("^(?i)\\bOR\\b", "OR", "CONDITION"),                             # or keyword

             # MATHEMATICAL FUNCTIONS
             ("^(?i)\\bRADIANS\b", "FUNCTION", "ID"),                          # radians() function
             ("^(?i)\\bCEILING\b", "FUNCTION", "ID"),                          # ceiling() function
             ("^(?i)\\bDEGREES\b", "FUNCTION", "ID"),                          # degrees() function
             ("^(?i)\\bROUND\\b", "FUNCTION", "ID"),                           # round() function
             ("^(?i)\\bTRUNC\\b", "FUNCTION", "ID"),                           # trunc() function
             ("^(?i)\\bSQUARE\b", "FUNCTION", "ID"),                           # square() function
             ("^(?i)\\bFLOOR\\b", "FUNCTION", "ID"),                           # floor() function
             ("^(?i)\\bPOWER\\b", "FUNCTION", "ID"),                           # power() function
             ("^(?i)\\bROUND\\b", "FUNCTION", "ID"),                           # round() function
             ("^(?i)\\bTRUNC\\b", "FUNCTION", "ID"),                           # trunc() function
             ("^(?i)\\bLOG10\b", "FUNCTION", "ID"),                            # log10() function
             ("^(?i)\\bASIN\\b", "FUNCTION", "ID"),                            # arcsin() function
             ("^(?i)\\bACOS\\b", "FUNCTION", "ID"),                            # arccos() function
             ("^(?i)\\bATAN\\b", "FUNCTION", "ID"),                            # arctan() function
             ("^(?i)\\bSINH\\b", "FUNCTION", "ID"),                            # sinh() function
             ("^(?i)\\bCOSH\\b", "FUNCTION", "ID"),                            # cosh() function
             ("^(?i)\\bTANH\\b", "FUNCTION", "ID"),                            # tanh() function
             ("^(?i)\\bSQRT\\b", "FUNCTION", "ID"),                            # sqrt() function
             ("^(?i)\\bCEIL\\b", "FUNCTION", "ID"),                            # ceil() function
             ("^(?i)\\bSIGN\\b", "FUNCTION", "ID"),                            # sign() function
             ("^(?i)\\bRAND\b", "FUNCTION", "ID"),                             # rand() function
             ("^(?i)\\bATN2\b", "FUNCTION", "ID"),                             # atn2() function
             ("^(?i)\\bSIN\\b", "FUNCTION", "ID"),                             # sin() function
             ("^(?i)\\bCOS\\b", "FUNCTION", "ID"),                             # cos() function
             ("^(?i)\\bTAN\\b", "FUNCTION", "ID"),                             # tan() function
             ("^(?i)\\bEXP\\b", "FUNCTION", "ID"),                             # exp() function
             ("^(?i)\\bLOG\\b", "FUNCTION", "ID"),                             # log() function
             ("^(?i)\\bABS\\b", "FUNCTION", "ID"),                             # abs() function
             ("^(?i)\\bCOT\b", "FUNCTION", "ID"),                              # cot() function
             ("^(?i)\\bLN\\b", "FUNCTION", "ID"),                              # ln() function
             ("^(?i)\\bMOD\b", "FUNCTION", "ID"),                              # mod() function
             ("^(?i)\\bPI\b", "FUNCTION", "ID"),                               # pigreco() function

             # STRINGS FUNCTIONS
             ("^(?i)\\bDATALENGTH\\b", "FUNCTION", "ID"),                      # dataLength() function
             ("^(?i)\\bDIFFERENCE\\b", "FUNCTION", "ID"),                      # difference() function
             ("^(?i)\\bCHARINDEX\\b", "FUNCTION", "ID"),                       # charIndex() function
             ("^(?i)\\bCONCAT_WS\\b", "FUNCTION", "ID"),                       # concatWS() function
             ("^(?i)\\bQUOTENAME\\b", "FUNCTION", "ID"),                       # quoteName() function
             ("^(?i)\\bREPLICATE\\b", "FUNCTION", "ID"),                       # replicate() function
             ("^(?i)\\bSUBSTRING\\b", "FUNCTION", "ID"),                       # substring() function
             ("^(?i)\\bTRANSLATE\\b", "FUNCTION", "ID"),                       # translate() function
             ("^(?i)\\bPATINDEX\\b", "FUNCTION", "ID"),                        # patIndex() function
             ("^(?i)\\bUNICODE\\b", "FUNCTION", "ID"),                         # unicode() function
             ("^(?i)\\bREVERSE\\b", "FUNCTION", "ID"),                         # reverse() function
             ("^(?i)\\bSOUNDEX\\b", "FUNCTION", "ID"),                         # soundEX() function
             ("^(?i)\\bSOUNDEX\\b", "FUNCTION", "ID"),                         # soundEX() function
             ("^(?i)\\bREPLACE\\b", "FUNCTION", "ID"),                         # replace() function
             ("^(?i)\\bINITCAP\\b", "FUNCTION", "ID"),                         # initcap() function
             ("^(?i)\\bCONCAT\\b", "FUNCTION", "ID"),                          # concat() function
             ("^(?i)\\bSUBSTR\\b", "FUNCTION", "ID"),                          # substr() function
             ("^(?i)\\bLENGTH\\b", "FUNCTION", "ID"),                          # length() function
             ("^(?i)\\bFORMAT\\b", "FUNCTION", "ID"),                          # format() function
             ("^(?i)\\bNCHAR\\b", "FUNCTION", "ID"),                           # nChar() function
             #("^(?i)\\bRIGHT\\b", "FUNCTION", "ID"),                          # right() function
             ("^(?i)\\bSPACE\\b", "FUNCTION", "ID"),                           # space() function
             ("^(?i)\\bSTUFF\\b", "FUNCTION", "ID"),                           # stuff() function
             ("^(?i)\\bLOWER\\b", "FUNCTION", "ID"),                           # lower() function
             ("^(?i)\\bUPPER\\b", "FUNCTION", "ID"),                           # upper() function
             ("^(?i)\\bLTRIM\\b", "FUNCTION", "ID"),                           # ltrim() function
             ("^(?i)\\bRTRIM\\b", "FUNCTION", "ID"),                           # rtrim() function
             ("^(?i)\\bINSTR\\b", "FUNCTION", "ID"),                           # instr() function
             ("^(?i)\\bASCII\\b", "FUNCTION", "ID"),                           # ascii() function
             ("^(?i)\\bLPAD\\b", "FUNCTION", "ID"),                            # lpad() function
             ("^(?i)\\bRPAD\\b", "FUNCTION", "ID"),                            # rpad() function
             ("^(?i)\\bCHAR\\b", "FUNCTION", "ID"),                            # char() function
             ("^(?i)\\bTRIM\\b", "FUNCTION", "ID"),                            # trim() function
             #("^(?i)\\bLEFT\\b", "FUNCTION", "ID"),                           # left() function
             ("^(?i)\\bSTR\\b", "FUNCTION", "ID"),                             # str() function
             ("^(?i)\\bLEN\\b", "FUNCTION", "ID"),                             # len() function

             # GROUP FUNCTIONS
             ("^(?i)\\bVARIANCE\\b", "FUNCTION", "ID"),                        # variance() function
             ("^(?i)\\bSTDDEV\\b", "FUNCTION", "ID"),                          # stddev() function
             ("^(?i)\\bMEDIAN\\b", "FUNCTION", "ID"),                          # median() function
             ("^(?i)\\bCOUNT\\b", "FUNCTION", "ID"),                           # count() function
             ("^(?i)\\bCORR\\b", "FUNCTION", "ID"),                            # corr() function             
             ("^(?i)\\bAVG\\b", "FUNCTION", "ID"),                             # avg() function
             ("^(?i)\\bMAX\\b", "FUNCTION", "ID"),                             # max() function
             ("^(?i)\\bMIN\\b", "FUNCTION", "ID"),                             # min() function
             ("^(?i)\\bSUM\\b", "FUNCTION", "ID"),                             # sum() function

             # DATE AND TIME FUNCTIONS
             ("^(?i)\\bCURRENT_TIMESTAMP\\b", "FUNCTION", "ID"),               # currentTimestamp() function
             ("^(?i)\\bMONTHS_BETWEEN\\b", "FUNCTION", "ID"),                  # monthsBetween() function
             ("^(?i)\\bDATEFROMPARTS\\b", "FUNCTION", "ID"),                   # dateFromParts() function
             ("^(?i)\\bSYSDATETIME\\b", "FUNCTION", "ID"),                     # sysDateTime() function
             ("^(?i)\\bGETUTCDATE\\b", "FUNCTION", "ID"),                      # getUTCdate() function
             ("^(?i)\\bADD_MONTHS\\b", "FUNCTION", "ID"),                      # addMonths() function
             ("^(?i)\\bDATEDIFF\\b", "FUNCTION", "ID"),                        # dateDiff() function
             ("^(?i)\\bDATENAME\\b", "FUNCTION", "ID"),                        # dateName() function
             ("^(?i)\\bDATEPART\\b", "FUNCTION", "ID"),                        # datePart() function
             ("^(?i)\\bLAST_DAY\\b", "FUNCTION", "ID"),                        # lastDay() function
             ("^(?i)\\bNEW_TIME\\b", "FUNCTION", "ID"),                        # newTime() function
             ("^(?i)\\bNEXT_DAY\\b", "FUNCTION", "ID"),                        # nextDay() function
             ("^(?i)\\bGREATEST\\b", "FUNCTION", "ID"),                        # greatest() function
             ("^(?i)\\bSYSDATE\\b", "FUNCTION", "ID"),                         # sysDate() function
             ("^(?i)\\bDATEADD\\b", "FUNCTION", "ID"),                         # dateAdd() function
             ("^(?i)\\bGETDATE\\b", "FUNCTION", "ID"),                         # getDate() function
             ("^(?i)\\bISDATE\\b", "FUNCTION", "ID"),                          # isDate() function
             ("^(?i)\\bMONTH\\b", "FUNCTION", "ID"),                           # month() function
             ("^(?i)\\bLEAST\\b", "FUNCTION", "ID"),                           # least() function
             ("^(?i)\\bYEAR\\b", "FUNCTION", "ID"),                            # year() function
             ("^(?i)\\bDAY\\b", "FUNCTION", "ID"),                             # day() function

             # CONVERTION FUNCTIONS
             ("^(?i)\\bTO_CHAR\\b", "FUNCTION", "ID"),                         # toChar() function
             ("^(?i)\\bTO_DATE\\b", "FUNCTION", "ID"),                         # toDate() function
             ("^(?i)\\bCONVERT\\b", "FUNCTION", "ID"),                         # convert() function
             ("^(?i)\\bCAST\\b", "FUNCTION", "ID"),                            # cast() function

             # OTHER FUNCTIONS
             ("^(?i)\\bSESSIONPROPERTY\\b", "FUNCTION", "ID"),                 # sessionProperty() function
             ("^(?i)\\bSESSION_USER\\b", "FUNCTION", "ID"),                    # sessionUser() function
             ("^(?i)\\bCURRENT_USER\\b", "FUNCTION", "ID"),                    # currentUser() function
             ("^(?i)\\bSYSTEM_USER\\b", "FUNCTION", "ID"),                     # systemUser() function
             ("^(?i)\\bISNUMERIC\\b", "FUNCTION", "ID"),                       # isNumeric() function
             ("^(?i)\\bUSER_NAME\\b", "FUNCTION", "ID"),                       # userName() function
             ("^(?i)\\bCOALESCE\\b", "FUNCTION", "ID"),                        # coalesce() function
             ("^(?i)\\bISNULL\\b", "FUNCTION", "ID"),                          # isNull() function
             ("^(?i)\\bNULLIF\\b", "FUNCTION", "ID"),                          # nullIf() function
             ("^(?i)\\bIIF\\b", "FUNCTION", "ID"),                             # iif() function
              
             # STRINGS
             ("^\'[^']*\'", "STRING", "LITERAL"),                              # literal single quote string

             # IDENTIFIERS
             ("^(?(?=\()\(\w+(?(?=\.).\w+|)\)|\w+(?(?=\.).\w+|))", "FIELDNAME", "ID"),          # fieldname with/without alias table surrounded by optional round parenthesis (es: alias.fieldname)
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

            return {"type" : Regex[1], "value" : result, "category" : Regex[2]}

        raise EX.MySyntaxException(f"Nessun Token ha riconosciuto la stringa '{string}'")

    def isMatch(self, regex, string):

        result = re.search(regex[0], string)

        if not result: return None

        self.Position += len(result.group())

        return result.group()
        