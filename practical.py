import re
identifiers = '[_a-zA-Z][_a-zA-Z0-9]*'
integers = '[0-9][0-9]*'
float1 = '\d+\.\d*'
float2 = '\.\d+'
operations = {'=':'assign_op', '+':'add_op', '-':'sub_op', '*':'mul_op', '/':'div_op', '%':'mod_op', '\'':'single_quotes', '"':'double_quotes', '(':'left_paranthesis',')':'right_paranthesis', ';':'delimiter','{':'left_curly','}':'right_curly', '>':"GREATER_THAN", '<':"LESS_THAN", "!":"EXCLAMATION", ":":"EACH"}
keywords = {'double':'DOUBLE_CODE','float':'FLOAT_CODE','int':"INT_CODE",'break':"BREAK_CODE",'else':'ELSE_CODE','for':'FOR_CODE','switch':'SWITCH_CODE','void':'VOID_CODE','case':'CASE_CODE','default':'DEFAULT_CODE','char':'CHAR_CODE','do':'DO_CODE','if':'IF_CODE','return':'RETURN_CODE','static':'STATIC_CODE','while':'WHILE_CODE', 'main':'MAIN_CODE', 'forEach':'FOREACH_CODE'}
delimiter = ';'
ArrayParse = []
temp=''

#<factor> --> identifier | float | int
#<term> --> <factor>| <term> / factor | <term> * <factor> | <term> % <factor> 
#<expression> -->  <term> | <expression> + <term> | <expression> - <term> 
#<bool> --> <expression> ( '<=' | '>=' | '<' | '>' |'==' | '!=' ) <expression>
#<stmt> -->  <do_while_stmt> | <while_stmt> |<if_stmt>| <for_stmt> | <forEach_stmt> | <switch_stmt>| <assignment >|<return_stmt>|<block>


#<switch_stmt> --> switch'{'{case <expression>: <stmt>} [default : <stmt>] '}'
#<foreach_stmt> --> foreach'('<variable> ':' <expression> ')'<stmt> 
#<for_stmt> --> for(<expression>; <expression>; <expression>)<statement> 
##<while_stmt> --> while '(' <bool> ')' <statement>
#<do_while_stmt> --> do <statement> while '(' <bool> ')'
#<block> --> '{' (' ' | <stmt>) '}'
#<if_stmt> --> if'('<bool> |<expression>')' <stmt> [else <stmt>] 
#<assignment > - IDENTIFIER ‘=’ <expression>
#<return_stmt> --> return <expression




##have program read file
with open('testfile.txt','r') as file:
    while True:
        newChar = file.read(1)
        if newChar=="":
            break
        token = newChar
        #set variable identifiers to contain identifiers 
        identifier = re.fullmatch(identifiers, newChar)
        if identifier:
            val='IDENTIFIER'
        #set variable integer to contain integers 
        integer = re.fullmatch(integers, newChar)
        #set variable floats to contain floats
        floats = re.fullmatch(float1, newChar)
        if integer:
            val='INTEGER'
        if newChar == ".":
            while newChar!='':
                ##reading the next character
                nextChar = file.read(1)
                if nextChar == "":
                    break
                #check if next character is empty    
                if nextChar == " ":
                    break
                temp_char = token + nextChar
                #sets . floats to "decimal" floats like .7
                decimalFloat = re.fullmatch(float2, temp_char)
                if decimalFloat:
                    token = temp_char
                    val = "FLOAT" 
                if nextChar in operations.keys():
                    temp = operations[nextChar]  
                else:
                    break
        if newChar!="" and newChar in operations.keys():
            val = operations[newChar]
            ArrayParse.append((newChar, val))              
        while newChar!='' and identifier: 
            nextChar = file.read(1)
            if nextChar == "":
                break
            if nextChar == " ":
                break
            temp_char = token + nextChar
            identifier = re.fullmatch(identifiers, temp_char)
            if identifier:
                token = temp_char
                val="IDENTIFIER"
            if nextChar in operations.keys():
                temp = operations[nextChar]   
        while nextChar!='' and integer or floats:
            nextChar = file.read(1)
            if nextChar == "":
                break
            if nextChar == " ":
                break
            temp_char = token + nextChar
            integer = re.fullmatch(integers, temp_char)
            floats = re.fullmatch(float1, temp_char)
            if floats:
                token = temp_char
                val = "FLOAT"
            elif integer:
                token = temp_char
                val="INTEGER"
            if nextChar in operations.keys():
                val_temp = operations[nextChar]
        
        if val == "IDENTIFIER" or val == "INTEGER" or val=="FLOAT" and token != " " and token != "\n":
            if token != " ":
                ArrayParse.append((token,val))
            token=''
            val=""
        if temp and nextChar != " " and nextChar != "\n":
            ArrayParse.append((nextChar, temp))
            temp=''
        token=''
        val=""
        if newChar=="":
            break 
            #checks if identifier is a keyword, if it is then it will replace identifier with keyword.
for i in range(len(ArrayParse)):
    if ArrayParse[i][1] == 'IDENTIFIER':
        if ArrayParse[i][0] in keywords.keys():
            temp_var = list([ArrayParse[i][0],keywords[ArrayParse[i][0]]])
            ArrayParse[i] = tuple(temp_var)
i = 0
      
while i < len(ArrayParse):
    if ArrayParse[i][0] == "=" and ArrayParse[i+1][0] == "=":
        ArrayParse.pop(i+1)
        ArrayParse[i] = ("==", 'EQUALITY_OPERATOR')
    else:
        i +=1
i = 0
 
while i < len(ArrayParse):
    if ArrayParse[i][0] == ">" and ArrayParse[i+1][0] == "=":
        ArrayParse.pop(i+1)
        ArrayParse[i] = (">=", 'GREAT_EQUAL')
    else:
        i +=1
i = 0
while i < len(ArrayParse):
    if ArrayParse[i][0] == "<" and ArrayParse[i+1][0] == "=":
        ArrayParse.pop(i+1)
        ArrayParse[i] = ("<=", 'LESS_EQUAL')
    else:
        i +=1
i = 0
while i < len(ArrayParse):
    if ArrayParse[i][0] == "!" and ArrayParse[i+1][0] == "=":
        ArrayParse.pop(i+1)
        ArrayParse[i] = ("!=", 'NOT_EQUAL')
    else:
        i +=1
for i in ArrayParse:
    print(i)

###########portion to check syntax/RDA#####

# function to take everything and put them into lexumes 
def lex():
    global nextToken
    if ArrayParse:
        val = ArrayParse.pop(0)
        val = val[1]
        nextToken = val
        print(nextToken)
    else:
        nextToken = None

def stmt():
    lex()
    if nextToken == 'INT_CODE' or nextToken == 'FLOAT_CODE' or nextToken == 'DOUBLE_CODE' or nextToken=='IDENTIFIER':
        assignment_stmt()
    elif nextToken == 'WHILE_CODE':
        while_stmt()
    elif nextToken == 'FOR_CODE':
        for_stmt()
    elif nextToken == 'IF_CODE':
        if_stmt()
    elif nextToken == 'RETURN_CODE':
        return_stmt()
    elif nextToken == 'FOREACH_CODE':
        forEach_stmt()
    elif nextToken == 'DO_CODE':
        do_while_stmt()
    elif nextToken == 'SWITCH_CODE':
        switch_stmt()    
    elif nextToken == 'left_curly':
        block()
def block():
    print("Start <block>")
    if nextToken != 'left_curly':
        error()
    while nextToken != 'right_curly' and ArrayParse:
        stmt()
    if nextToken == 'right_curly':
        print("END <block>")
    else:
        error()
        
 
def assignment_stmt():
    print('Enter <assign statement>')
    if nextToken == 'INT_CODE' or nextToken == 'FLOAT_CODE' or nextToken=='DOUBLE_CODE':
        lex()
        if nextToken != 'IDENTIFIER':
            error()
        lex()
        if nextToken == 'assign_op':
            lex()
            expr()
            if nextToken != 'delimiter':
                error()
            print('End <assignement statement>')
        elif nextToken == "delimiter":
            print('END <assignment statement>')
        else:
            error()
    elif nextToken == 'IDENTIFIER':
        lex()
        if nextToken == 'assign_op':
            lex()
            expr()
            if nextToken != 'delimiter':
                error()
            print('End <assignement statement>')
        else:
            error()

    else:
        error()

def expr():
    print("Enter <expr>")
    term()
    while (nextToken == 'add_op' or nextToken == 'sub_op'):
        lex()
        term()
    print("Exit <expr>")
    
def term():
    print("Enter <term>")
    factor()

    while(nextToken == 'mult_op' or nextToken == 'div_op' or nextToken == 'mod_op'):
        lex()
        factor()
    print("Exit <term>")
    

def factor():
    print("Enter <factor>")
    if (nextToken == 'IDENTIFIER' or nextToken == 'INTEGER' or nextToken == 'FLOAT'):
        lex()

    elif nextToken == 'left_paranthesis':
        lex()
        expr()
        if nextToken == 'right_paranthesis':
            lex()
        else:
            error()
    else:
        error()
    print("Exit <factor>")




def bool_expr():
    print("Enter <bool_expr>")
    expr()
    if nextToken == "EQUALITY_OPERATOR" or nextToken == "NOT_EQUAL" or nextToken == "GREAT_EQUAL" or nextToken =="LESS_EQUAL" or nextToken == "GREATER_THAN" or nextToken == "LESS_THAN":
        lex()
        expr()
    else:
        error()
    print("End <bool_expr>")
    


def error():
    print("There is an error, try again.")
    exit()



def if_stmt():
    print("Enter <IF STMT>")
    if (nextToken != 'IF_CODE'):
        error()
    else:
        lex()
        if (nextToken != 'left_paranthesis'):
            error()
        else:
            lex()
            bool_expr()
            if nextToken != 'right_paranthesis':
                error()
            else:
                stmt()
                lex()
                if nextToken == 'ELSE_CODE':
                    print("ENTER <ELSE STMT>")
                    stmt()
                    print("EXIT <ELSE STMT>")
    print("End <IF STMT>")
def for_stmt():
    print("Enter <FOR STATMENT>")
    if nextToken != 'FOR_CODE':
        error()
    lex()
    if nextToken!='left_paranthesis':
        error()
    while nextToken != 'delimiter' and ArrayParse:
        lex()
    if nextToken != 'delimiter':
        error()
    lex()
    while nextToken != 'delimiter' and ArrayParse:
        lex()
    if nextToken != 'delimiter':
        error()
    while nextToken != 'right_paranthesis' and ArrayParse:
        lex()
    if nextToken != 'right_paranthesis':
        error()
    stmt()
    print("End <for statement>") 
def forEach_stmt():
    print("Enter <forEach statement>")
    if nextToken != "FOREACH_CODE":
        error()
    lex()
    if nextToken != 'left_paranthesis':
        error()
    lex()
    if nextToken != 'IDENTIFIER':
        error()
    lex()
    if nextToken != 'EACH':
        error()
    lex()
    if nextToken != 'IDENTIFIER':
        error()
    lex()
    if nextToken != 'right_paranthesis':
        error()
    else:
        stmt()
    print('End <forEach statement>')
def while_stmt():
    print('Enter <while statement>')
    if nextToken != 'WHILE_CODE':
        error()
    else:
        lex()
        if nextToken != 'left_paranthesis':
            error()
        else:
            lex()
            bool_expr()
            if nextToken != 'right_paranthesis':
                error()
            else:
                stmt()
    print("End <while statement>")
def switch_stmt():
    print('Enter <switch statement>')
    if nextToken != 'SWITCH_CODE':
        error()
    else:
        lex()
        if nextToken != 'left_paranthesis':
            error()
        lex()
        if nextToken != 'right_paranthesis':
            error()
        lex()
        if nextToken != 'left_curly':
            error()
        lex()
        if nextToken == 'CASE_CODE' or nextToken == 'DEFAULT_CODE':
            stmt()
        else:
            if nextToken != 'right_curly':
                error()
        print('End <switch statement>')
def return_stmt():
    print("Enter <Return statement>")
    if nextToken != 'RETURN_CODE':
        error()
    lex()
    expr()
    print('End <return statement>')
def do_while_stmt():
    print('Enter <Do While Statement>')
    if nextToken != 'DO_CODE':
        error()
    stmt()
    lex()
    if nextToken != "WHILE_CODE":
        error()
    lex()
    if nextToken != "left_paranthesis":
        error()
    lex()
    bool_expr()
    if nextToken != 'right_paranthesis':
        error()
    lex()
    if nextToken != 'delimiter':
        error()
    print("End <Do While Statement>")
def checkSyntax():
    print('START <Syntax Check: Program>')
    lex()
    if nextToken != 'VOID_CODE':
        error()
    lex()
    if nextToken != 'MAIN_CODE':
        error()
    lex()
    if nextToken != 'left_paranthesis':
        error()
    lex()
    if nextToken != 'right_paranthesis':
        error()
    else:
        stmt()
    print('END <Syntax Check: Program >')                 

#check syntax of file       
checkSyntax()
