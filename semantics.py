"""

Input: A text file where each line has a token and the corresponding lexeme
Output: True if and only if no syntax errors and no semantics errors; otherwise 
        returns error
        
"""
import sys

symTable = {}  # empty dictionary/hash-map
iNextToken = 0
tokenStream = []
lexemeStream = []
executeIf = True


def main():
    # declare globals
    global tokenStream
    global lexemeStream
    global iNextToken
    global executeIf

    # get the filename
    filename = input("Please type in a filename: ")

    # Read in the file to fill in token and lexeme streams
    infile = open(filename, "r")
    myStr = infile.read()  # a string of the whole file
    myList = myStr.split()  # splits the string into tokens and lexemes
    tokenStream = myList[0::2]  # list of tokens (even elements from myList)
    lexemeStream = myList[1::2]  # list of lexemes (odd elements from myList)

    # Start at the start symbol Program
    result = program()

    if iNextToken < len(tokenStream):
        error()


def program():
    # declare globals
    global tokenStream
    global lexemeStream
    global iNextToken
    global symTable

    if iNextToken < len(tokenStream) and (tokenStream[iNextToken] == "type"):
        iNextToken += 1  # consume the 'type'

    if iNextToken < len(tokenStream) and (tokenStream[iNextToken] == "main"):
        iNextToken += 1  # consume the 'main'

    if iNextToken < len(tokenStream) and (tokenStream[iNextToken] == "("):
        iNextToken += 1  # consume the '('

    if iNextToken < len(tokenStream) and (tokenStream[iNextToken] == ")"):
        iNextToken += 1  # consume the ')'

    if iNextToken < len(tokenStream) and (tokenStream[iNextToken] == "{"):
        iNextToken += 1  # consume the '{'
    else:
        # if any of the above 5 tokens are not present in this order
        # then, not syntactically correct; prematurely call error
        error()

    declarations()  # consume the declarations

    statements()  # consume the statements

    # if this isn't present, need to call error, as the iNextToken < len
    # won't catch it in the main function

    if iNextToken < len(tokenStream) and (tokenStream[iNextToken] == "}"):
        iNextToken += 1  # consume the '}'

    else:
        error()


def declarations():
    # declare globals
    global tokenStream
    global lexemeStream
    global iNextToken

    # check if the current token starts a declaration, keeping in mind that 
    # declarations start with 'type'; if that's the case then keep looking for
    # more declarations
    while iNextToken < len(tokenStream) and \
            tokenStream[iNextToken] == "type":
        declaration()


def declaration():
    # declare globals
    global tokenStream
    global lexemeStream
    global iNextToken
    global symTable

    # consume 'type'
    if iNextToken < len(tokenStream) and (tokenStream[iNextToken] == "type"):
        iNextToken += 1

    # consume 'id'
    if iNextToken < len(tokenStream) and (tokenStream[iNextToken] == "id"):
        # get name and type of variable
        vName = lexemeStream[iNextToken]
        vType = lexemeStream[iNextToken - 1]
        iNextToken += 1

        # if a variable with that name doesn't exist, put it in the symTable
        if vName not in symTable.keys():
            symTable[vName] = [vType, None]
        # otherwise, there is a duplicate declaration; call duplicate error
        else:
            dupError()

    # while there are still more ids to follow (indicated by a comma)
    while iNextToken < len(tokenStream) and (tokenStream[iNextToken] == ","):
        iNextToken += 1  # consume the comma

        if iNextToken < len(tokenStream) and (tokenStream[iNextToken] == "id"):
            # get name and type of variable
            vName = lexemeStream[iNextToken]
            # use vType from before ;)

            # if a variable with that name doesn't exist, put it in the symTable
            if vName not in symTable.keys():
                symTable[vName] = [vType, None]
                iNextToken += 1
                # otherwise, there is a duplicate declaration
            else:
                dupError()

    # consume the following semi-colon
    if iNextToken < len(tokenStream) and tokenStream[iNextToken] == ";":
        iNextToken += 1


def statements():
    # declare globals
    global tokenStream
    global lexemeStream
    global iNextToken
    global executeIf

    # while there are are more statements left; excecute
    # look if there are more statements left by looking for "print", "if", 
    # "while", "return", or "id"
    while iNextToken < len(tokenStream) and ( \
                    tokenStream[iNextToken] == "print" or \
                    tokenStream[iNextToken] == "if" or \
                    tokenStream[iNextToken] == "while" or \
                    tokenStream[iNextToken] == "return" or \
                    tokenStream[iNextToken] == "id"):
        executeIf = True
        statement()


def statement():
    # declare globals
    global tokenStream
    global lexemeStream
    global iNextToken

    # only want to check one statement at a time, so use conditional
    # if it is 

    # check if it is an assignment statement
    if tokenStream[iNextToken] == "id":
        assignment()
    # check if print statement
    elif tokenStream[iNextToken] == "print":
        printStatement()
    # check if if statement
    elif tokenStream[iNextToken] == "if":
        ifStatement()
    # check if while statement
    elif tokenStream[iNextToken] == "while":
        whileStatement()
    # check if return statement
    elif tokenStream[iNextToken] == "return":
        returnStatement()

    # if it is not a statement, don't consume the token


def printStatement():
    # declare globals
    global tokenStream
    global lexemeStream
    global iNextToken
    global symTable
    global executeIf

    # consume the 'print' token
    if iNextToken < len(tokenStream) and tokenStream[iNextToken] == "print":
        iNextToken += 1

    # print out the expression
    printToken = iNextToken

    # check the expression statement to ensure that it is syntactically correct
    expression()

    # shouldn't print if it is nested in a false if statement
    # iterate through the tokens in the expression
    while (tokenStream[printToken] != ";" and executeIf):
        # if the current lexeme is in the symTable, then we want to print out
        # the value associated with it
        if lexemeStream[printToken] in symTable.keys():
            print(symTable[lexemeStream[printToken]][1])
            # otherwise, just print the lexeme
        else:
            print(lexemeStream[printToken], end=" ")

        printToken += 1

        # consume the semicolon
    if iNextToken < len(tokenStream) and \
            tokenStream[iNextToken] == ";":
        iNextToken += 1


def ifStatement():
    # declare globals
    global tokenStream
    global lexemeStream
    global iNextToken
    global executeIf

    # consume the 'if' token
    if iNextToken < len(tokenStream) and \
            tokenStream[iNextToken] == "if":
        iNextToken += 1

        # consume the '('
    if iNextToken < len(tokenStream) and \
            tokenStream[iNextToken] == "(":
        iNextToken += 1

        # check for an expresion
    # check to see if whatever is in the if statement should be evaluated
    executeIf = expression() and executeIf
    # keep the boolean for this statement in case of nested statements
    nonNonested = executeIf

    # consume the ')'
    if iNextToken < len(tokenStream) and \
            tokenStream[iNextToken] == ")":
        iNextToken += 1

    # check for a statement
    statement()

    # 
    executeIf = nonNested

    # check to see if there is an else; if so, there's another statement
    if iNextToken < len(tokenStream) and \
            tokenStream[iNextToken] == "else":
        iNextToken += 1  # consume the 'else' token

        # ensure that statements will be executed only if the if was not
        # executed
        executeIf = not executeIf

        # check the next statement
        statement()


def whileStatement():
    # declare globals
    global tokenStream
    global lexemeStream
    global iNextToken

    # consume the 'while' token
    if iNextToken < len(tokenStream) and \
            tokenStream[iNextToken] == "while":
        iNextToken += 1
        # consume the '('
    if iNextToken < len(tokenStream) and \
            tokenStream[iNextToken] == "(":
        iNextToken += 1

        # check the expression
    expression()

    # consume the ')'
    if iNextToken < len(tokenStream) and \
            tokenStream[iNextToken] == ")":
        iNextToken += 1

    # check the statement
    statement()


def returnStatement():
    # declare globals
    global tokenStream
    global lexemeStream
    global iNextToken

    # consume the "return" token
    if iNextToken < len(tokenStream) and \
            tokenStream[iNextToken] == "return":
        iNextToken += 1

        # check the expression
    expression()

    # consume the semicolon
    if iNextToken < len(tokenStream) and \
            tokenStream[iNextToken] == ";":
        iNextToken += 1
    else:
        error()


def assignment():
    # declare globals
    global tokenStream
    global lexemeStream
    global iNextToken
    global symTable
    global executeIf

    # check the id
    if iNextToken < len(tokenStream) and \
            (tokenStream[iNextToken] == "id"):
        # check if its in our symTable
        varName = lexemeStream[iNextToken]
        if varName not in symTable.keys():
            decError()  # if not, call a declaration error
        else:
            # it is in the symTable
            iNextToken += 1

            # check the assignOp
    if iNextToken < len(tokenStream) and \
            (tokenStream[iNextToken] == "assignOp"):
        iNextToken += 1
        value = expression()

    # consume the semicolon
    if iNextToken < len(tokenStream) and \
            tokenStream[iNextToken] == ";":
        iNextToken += 1

        # check for type errors
        # if type of variable not equal to the value type
        if type(value) is bool:
            vType = "bool"
        elif type(value) is float:
            vType = "float"
        elif type(value) is int:
            vType = "int"
        elif type(value) is str:
            vType = "char"

        if symTable[varName][0] != vType:

            # check to see if widening variable scope; only case allowed is if
            # the variable is a float, and the assigned value is an integer
            if symTable[varName][0] == "float":
                if vType == "int":

                    # if this is nested in a false if statement, should not
                    # execute
                    if executeIf:
                        symTable[varName][1] = value
            else:
                typeError("assignment", symTable[varName][0], vType)

        elif executeIf:
            symTable[varName][1] = value


def expression():
    # declare globals
    global tokenStream
    global lexemeStream
    global iNextToken

    # check the conjunction
    total = conjunction()

    # check if there are more conjunctions left by looking at the '||' token
    while (iNextToken < len(tokenStream) and tokenStream[iNextToken] == "||"):
        iNextToken += 1  # consume the or token

        # check the next conjunction
        value2 = conjunction()

        # make sure values are comparable
        if type(value1) is not type(value2):
            # only time when different types can be compared is float/int
            if type(value1) is (bool or str) or type(value2) is (bool or str):
                typeError("comparison", type(total), type(value2))

                # reset total
        total = total or value2

    return total


def conjunction():
    # declare globals
    global tokenStream
    global lexemeStream
    global iNextToken

    # check the equality
    total = equality()

    # check for more equalities by looking at the '&&' token
    while (iNextToken < len(tokenStream) and tokenStream[iNextToken] == "&&"):
        iNextToken += 1  # consume the && token

        # check the next equality
        value2 = equality()

        # make sure values are comparable
        if type(value1) is not type(value2):
            # only time when different types can be compared is float/int
            if type(value1) is (bool or str) or type(value2) is (bool or str):
                typeError("comparison", type(value1), type(value2))

        total = total and value2
    return total


def equality():
    # declare globals
    global tokenStream
    global lexemeStream
    global iNextToken

    # check the first relation
    value1 = relation()

    # check if there is another relation
    if (iNextToken < len(tokenStream) and tokenStream[iNextToken] == "equOp"):

        # check the actual equOp
        lexeme = lexemeStream[iNextToken]

        iNextToken += 1  # consume the 'equOp'
        value2 = relation()

        # make sure values are comparable
        if type(value1) is not type(value2):
            # only time when different types can be compared is float/int
            if type(value1) is (bool or str) or type(value2) is (bool or str):
                typeError("comparison", type(value1), type(value2))

        # if it is !=, then return if value1 and value2 not equal
        if lexeme == "!=":
            return value1 != value2
        # otherwise, return if they are equal
        else:
            return value1 == value2

    # if no relation, then just return relation
    return value1


def relation():
    # declare globals
    global tokenStream
    global lexemeStream
    global iNextToken

    # check the first addition
    value1 = addition()

    # check if there is another addition
    if (iNextToken < len(tokenStream) and tokenStream[iNextToken] == "relOp"):
        # grab the relative operator
        lexeme = lexemeStream[iNextToken]

        iNextToken += 1  # consume the 'relOp'
        value2 = addition()

        # make sure values are comparable
        if type(value1) is not type(value2):
            # only time when different types can be compared is float/int
            if type(value1) is (bool or str) or type(value2) is (bool or str):
                typeError("comparison", type(value1), type(value2))

                # return the appropriate conditional
        if lexeme == ">":
            return value1 > value2
        elif lexeme == ">=":
            return value1 >= value2
        elif lexeme == "<":
            return value1 < value2
        elif lexeme == "<=":
            return value1 <= value2

    # if no second value, just return regular value
    return value1


def addition():
    # declare globals
    global tokenStream
    global lexemeStream
    global iNextToken
    global symTable

    # check the first term
    total = term()

    # check if there are more terms by looking for a "addOp"
    while (iNextToken < len(tokenStream) and tokenStream[iNextToken] == "addOp"):
        # grab the addition operator
        lexeme = lexemeStream[iNextToken]
        iNextToken += 1  # consume the "addOp"

        # check the next term
        value2 = term()

        # check to make sure no type error
        # I am making boolean addition and char addition illegal, which would
        # cover the cases of adding a boolean to a float, etc.
        if type(total) is bool or type(value2) is bool or \
                type(total) is str or type(value2) is str:
            typeError("addition", total, value2)

        if lexeme == "+":
            total = total + value2
        else:
            total = total - value2

    return total


def term():
    # declare globals
    global tokenStream
    global lexemeStream
    global iNextToken

    # check the first factor
    total = factor()

    # check if there are more factors by looking for a "multOp"
    while (iNextToken < len(tokenStream) and \
           tokenStream[iNextToken] == "multOp"):

        # find the multiplication operator
        lexeme = lexemeStream[iNextToken]
        iNextToken += 1  # consume the "multOp"

        # check the next factor
        value2 = factor()

        # again, preventing type errors. Same logic as the addition function
        if type(total) is bool or type(value2) is bool or \
                type(total) is str or type(value2) is str:
            typeError("multiplication", total, value2)

        # set total equal to the appropriate total, depending on multOp
        # division runs left to right, so this works
        if lexeme == "*":
            total = total * value2
        else:
            total = total / value2
    return total


def factor():
    # declare globals
    global tokenStream
    global lexemeStream
    global iNextToken
    global symTable

    if iNextToken < len(tokenStream) and \
            tokenStream[iNextToken] == "id":

        # check if its in our symTable
        vName = lexemeStream[iNextToken]
        if vName not in symTable.keys():
            decError  # if not, declaration error
        else:
            # it is in the symTable
            iNextToken += 1
            # return the value associated with vName
            if symTable[vName][0] == "intLiteral":
                return int(symTable[vName][1])
            elif symTable[vName][0] == "floatLiteral":
                return float(symTable[vName][1])
            elif symTable[vName][0] == "boolLiteral":
                return bool(symTable[vName][1])
            else:
                return symTable[vName][1]

    # check if the factor is an int, bool, or float
    elif iNextToken < len(tokenStream) and \
            tokenStream[iNextToken] == "intLiteral":

        iNextToken += 1
        return int(lexemeStream[iNextToken - 1])
    elif iNextToken < len(tokenStream) and \
            tokenStream[iNextToken] == "boolLiteral":
        iNextToken += 1
        return bool(lexemeStream[iNextToken - 1])

    elif iNextToken < len(tokenStream) and \
            tokenStream[iNextToken] == "floatLiteral":
        iNextToken += 1
        return float(lexemeStream[iNextToken - 1])

    elif iNextToken < len(tokenStream) and \
            tokenStream[iNextToken] == "charLiteral":
        iNextToken += 1
        return lexemeStream[iNextToken - 1]

        # check if the factor is an expression enclosed by parantheses
    elif iNextToken < len(tokenStream) and tokenStream[iNextToken] == "(":
        iNextToken += 1  # consume the parantheses

        # check if the next token is an expression
        total = expression()

        # consume the ')'
        if (iNextToken < len(tokenStream) and tokenStream[iNextToken] == ")"):
            iNextToken += 1

        return total


def error():
    # declare globals
    global tokenStream
    global lexemeStream
    global iNextToken

    # if there are any tokens left, then point to error location    
    if iNextToken < len(tokenStream):
        print("Syntax Error: Invalid expression. Error location: <", \
              tokenStream[iNextToken], ",", lexemeStream[iNextToken], ">.")

    # if there are no tokens left, it must be expecting more terms
    else:
        print("Syntax Error: Incomplete expression. Expecting more terms.")

    # stop the function from running further
    sys.exit()


def decError():
    # declare globals
    global tokenStream
    global lexemeStream
    global iNextToken

    # print error and stop the function from running further
    print("Semantics Error: Variable", lexemeStream[iNextToken],
          "referenced before declaration.")
    sys.exit()


def dupError():
    # declare globals
    global tokenStream
    global lexemeStream
    global iNextToken

    # print error and stop the function from running any further
    print("Semantics Error: Variable", lexemeStream[iNextToken],
          "is a duplicate of a previously declared variable")
    sys.exit()


def typeError(problem, type1, type2):
    # declare globals
    global tokenStream
    global lexemeStream
    global iNextToken

    # need to pass in the types of the problem children
    print("Type Error at", iNextToken)
    if problem == "assignment":
        print("Assignment of a", type2, "value to a", type1, "variable is",
              "not allowed.")
    elif problem == "addition":
        print("Addition or subtraction between a", type1, "and", type2,
              "is not allowed.")
    elif problem == "multiplication":
        print("Multiplication or division between a", type(type1), "and",
              type(type2), "is not allowed.")
    elif problem == "comparison":
        print("Comparison between a", type1, "and a", type2, "is not allowed")

    sys.exit()


main()
