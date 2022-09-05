def tokenCreator(characterList):

    #declaracion token y lista tokens

    tokenDict = {
        "tokens":[],
        "tokenTuples": []
    }
    
    tokenMaker = ""
    returnToken = ""

    numLine = 1
    numChar = 0

    for char in characterList:
        """
        Comprobar tokens unicos-
        se comprueban los tokens unicos y, si ya habia un token haciendose, se termina el token anterior
        
        Llaves: { , }
        Parentesis: (, )
        igual: =
        punto y coma: ;
        coma: ,
        espacio: " "
        salto de linea: \n
        """

        #cambio de linea
        if(char == "\n"):
            startNumChar = numChar - len(tokenMaker)

            returnToken = checkToken(tokenMaker)
            if returnToken != "":
                tokenDict["tokenTuples"].append((returnToken, startNumChar, numLine))
                tokenDict["tokens"].append(returnToken)

            returnToken = "nextLine"
            tokenDict["tokenTuples"].append((returnToken, numChar, numLine))
            tokenDict["tokens"].append(returnToken)

            numLine += 1
            numChar = 0

            tokenMaker = ""
        
        #espacio
        elif(char == ' '):
            startNumChar = numChar - len(tokenMaker)

            returnToken = checkToken(tokenMaker)
            if returnToken != "":
                tokenDict["tokenTuples"].append((returnToken, startNumChar, numLine))
                tokenDict["tokens"].append(returnToken)

            returnToken = "space"
            tokenDict["tokenTuples"].append((returnToken, numChar, numLine))
            tokenDict["tokens"].append(returnToken)

            tokenMaker = ""

        #coma
        elif(char == ","):
            startNumChar = numChar - len(tokenMaker)

            returnToken = checkToken(tokenMaker)
            if returnToken != "":
                tokenDict["tokenTuples"].append((returnToken, startNumChar, numLine))
                tokenDict["tokens"].append(returnToken)

            returnToken = "comma"
            tokenDict["tokenTuples"].append((returnToken, numChar, numLine))
            tokenDict["tokens"].append(returnToken)

            tokenMaker = ""

        #Llave izquierda
        elif(char == "{"):
            startNumChar = numChar - len(tokenMaker)

            returnToken = checkToken(tokenMaker)
            if returnToken != "":
                tokenDict["tokenTuples"].append((returnToken, startNumChar, numLine))
                tokenDict["tokens"].append(returnToken)

            returnToken = "leftBracket"
            tokenDict["tokenTuples"].append((returnToken, numChar, numLine))
            tokenDict["tokens"].append(returnToken)

            tokenMaker = ""

        #Llave derecha
        elif(char == "}"):
            startNumChar = numChar - len(tokenMaker)

            returnToken = checkToken(tokenMaker)
            if returnToken != "":
                tokenDict["tokenTuples"].append((returnToken, startNumChar, numLine))
                tokenDict["tokens"].append(returnToken)

            returnToken = "rightBracket"
            tokenDict["tokenTuples"].append((returnToken, numChar, numLine))
            tokenDict["tokens"].append(returnToken)

            tokenMaker = ""

        #Parentesis izquierdo
        elif(char == "("):
            startNumChar = numChar - len(tokenMaker)

            returnToken = checkToken(tokenMaker)
            if returnToken != "":
                tokenDict["tokenTuples"].append((returnToken, startNumChar, numLine))
                tokenDict["tokens"].append(returnToken)

            returnToken = "leftParenthesis"
            tokenDict["tokenTuples"].append((returnToken, numChar, numLine))
            tokenDict["tokens"].append(returnToken)

            tokenMaker = ""

        #Parentesis derecho
        elif(char == ")"):
            startNumChar = numChar - len(tokenMaker)

            returnToken = checkToken(tokenMaker)
            if returnToken != "":
                tokenDict["tokenTuples"].append((returnToken, startNumChar, numLine))
                tokenDict["tokens"].append(returnToken)
            
            returnToken = "rightParenthesis"
            tokenDict["tokenTuples"].append((returnToken, numChar, numLine))
            tokenDict["tokens"].append(returnToken)

            tokenMaker = ""
   
        #Simbolo Igual
        elif(char == "="):
            startNumChar = numChar - len(tokenMaker)

            returnToken = checkToken(tokenMaker)
            if returnToken != "":
                tokenDict["tokenTuples"].append((returnToken, startNumChar, numLine))
                tokenDict["tokens"].append(returnToken)
            
            returnToken = "equals"
            tokenDict["tokenTuples"].append((returnToken, numChar, numLine))
            tokenDict["tokens"].append(returnToken)

            tokenMaker = ""

        elif(char == ";"):
            startNumChar = numChar - len(tokenMaker)

            returnToken = checkToken(tokenMaker)
            if returnToken != "":
                tokenDict["tokenTuples"].append((returnToken, startNumChar, numLine))
                tokenDict["tokens"].append(returnToken)

            returnToken = "semiColon"
            tokenDict["tokenTuples"].append((returnToken, numChar, numLine))
            tokenDict["tokens"].append(returnToken)

            tokenMaker = ""
        
        else:
            tokenMaker = tokenMaker + char
        
        numChar += 1

    startNumChar = numChar - len(tokenMaker)
    returnToken = checkToken(tokenMaker)
    tokenDict["tokenTuples"].append((returnToken, startNumChar, numLine))
    tokenDict["tokens"].append(returnToken)

    return tokenDict

def checkToken(stringToken):

    returnToken = ""

    #inicio Programa
    if(stringToken == "PROG"):
        returnToken = "startProgram"

    #fin Programa
    elif(stringToken == "GORP"):
        returnToken = "endProgram"

    #inicio Procedimiento
    elif(stringToken == "PROC"):
        returnToken = "startProc"

    #fin Procedimiento
    elif(stringToken == "CORP"):
        returnToken = "endProc"

    #brujula:
    #north
    #east
    #south
    #west
    elif(stringToken == "North" or stringToken == "north"):
        returnToken = "northCompass"

    elif(stringToken == "East" or stringToken == "east"):
        returnToken = "eastCompass"

    elif(stringToken == "South" or stringToken == "south"):
        returnToken = "southCompass"

    elif(stringToken == "West" or stringToken == "west"):
        returnToken = "westCompass"

    #direcciones:
    #right
    #left
    #around
    #front
    #back

    elif(stringToken == "right"):
        returnToken = "rightDirection"

    elif(stringToken == "left"):
        returnToken = "leftDirection"

    elif(stringToken == "around"):
        returnToken = "aroundDirection"

    elif(stringToken == "front"):
        returnToken = "frontDirection"

    elif(stringToken == "back"):
        returnToken = "backDirection"

    #walk
    elif(stringToken == "walk"):
        returnToken = "walkFunc"

    #jump
    elif(stringToken == "jump"):
        returnToken = "jumpFunc"

    #jumpTo
    elif(stringToken == "jumpTo"):
        returnToken = "jumpToFunc"

    #veer
    elif(stringToken == "veer"):
        returnToken = "veerFunc"

    #look
    elif(stringToken == "look"):
        returnToken = "lookFunc"

    #drop
    elif(stringToken == "drop"):
        returnToken = "dropFunc"

    #grab
    elif(stringToken == "grab"):
        returnToken = "grabFunc"

    #get
    elif(stringToken == "get"):
        returnToken = "getFunc"

    #free
    elif(stringToken == "free"):
        returnToken = "freeFunc"

    #pop
    elif(stringToken == "pop"):
        returnToken = "popFunc"

    #inicio if
    elif(stringToken == "if"):
        returnToken = "startIf"

    #fin if
    elif(stringToken == "fi"):
        returnToken = "endIf"

    #else
    elif(stringToken == "else"):
        returnToken = "elseIf"

    #while
    elif(stringToken == "while"):
        returnToken = "whileLoop"

    #inicio do
    elif(stringToken == "do"):
        returnToken = "startDo"

    #fin do
    elif(stringToken == "od"):
        returnToken = "endDo"

    #inicio repeatTimes
    elif(stringToken == "repeatTimes"):
        returnToken = "startRepeat"

    #fin repeatTime
    elif(stringToken == "per"):
        returnToken = "endRepeat"

    #Condicionales:
    #isfacing
    #isValid
    #drop
    #canWalk
    elif(stringToken == "isfacing"):
        returnToken = "condFacing"

    elif(stringToken == "isValid"):
        returnToken = "condValid"

    elif(stringToken == "canWalk"):
        returnToken = "condWalk"
    
    #not

    elif(stringToken == "not"):
        returnToken = "not"

    #declarar variable
    elif(stringToken == "VAR"):
        returnToken = "variableInitializer"

    #Numero
    elif(checkInt(stringToken)):
        returnToken = f"num({stringToken})"

    #vacio
    elif(stringToken == " " or stringToken == "'" or stringToken == ""):
        returnToken = ""
    
    #variable//funcion

    else:
        returnToken = "DeclarativeState_" + stringToken


    return returnToken

def checkInt(str):
    try:
        int(str)
        return True
    except ValueError:
        return False