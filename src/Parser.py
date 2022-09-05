def testSyntax(tokenDict):

    commandStructures = {
        "jumpFunc": 1,
        "jumpToFunc": 2,
        "veerFunc": 1,
        "lookFunc": 1,
        "dropFunc": 1,
        "grabFunc": 1,
        "getFunc": 1,
        "freeFunc": 1,
        "popFunc": 1,
    }

    commandList = commandStructures.keys()

    parameterList = ["northCompass", "eastCompass", "southCompass", "westCompass", "rightDirection", "leftDirection", "aroundDirection", "frontDirection", "backDirection", "DeclarativeState_", "num", "walkFunc", "jumpFunc", "grabFunc", "popFunc", "freeFunc", "dropFunc"]


    conditionalStructures = {
        "condFacing": 1,
        "condValid": 2,
        "condWalk": 2,
    }

    conditionalList = ["condFacing", "condValid", "condWalk", "not"]


    #comprobar iniciación y fin programa
    startEndTokensErrorMessages = testStartEndToken(tokenDict)
    
    #comprobar apertura y cierre llaves y parentesis
    bracketParenthesisErrorMessages, bracketPairs, parenthesisPairs, conditionalPairs, procedurePairs = testBracketsAndParenthesis(tokenDict)

    #comprobar comandos
    commandErrorMessages = testCommands(tokenDict, commandList, commandStructures, parameterList)
    
    #comprobar variables funciones y parámetros
    variablesProceduresParametersErrorMessages = testVariablesAndFunctions(tokenDict, parameterList)

    #comprobar condicionales
    conditionalErrors = testConditionals(tokenDict, conditionalList, conditionalStructures, parameterList)

    #comprobar loops
    loopErrorMessages = testLoops(tokenDict, conditionalList, conditionalStructures, parameterList)

    return bracketParenthesisErrorMessages + commandErrorMessages + variablesProceduresParametersErrorMessages + conditionalErrors + loopErrorMessages



def testStartEndToken(tokenDict):
    
    errorMessages = []
    tokenList = tokenDict["tokens"]
    tokenTuples = tokenDict["tokenTuples"]

    startToken  = tokenList[0]
    endToken = tokenList[len(tokenList)-1]

    startDuplicates = tokenList.count("startProgram")
    endDuplicates = tokenList.count("endProgram")

    #detectar que el primer token sea el inico programa
    if(startToken != "startProgram"):
        startTokenPos = tokenList.index("startProgram")
        tupleError = tokenTuples[startTokenPos]
        
        errorMessages.append(f"Syntax: declaración inicion programa (ln:{tupleError[2]}, col:{tupleError[1]})")

    #detectar que el último token sea el fin del programa
    if(endToken != "endProgram"):
        endTokenPos = tokenList.index("endProgram")
        tupleError = tokenTuples[endTokenPos]
        
        errorMessages.append(f"Syntax: declaración final programa (ln:{tupleError[2]}, col:{tupleError[1]})")

    #detectar que haya token de inicion de programa
    if(startDuplicates == 0):
        errorMessages.append("Syntax: declaración inicion programa no existente")

    #detectar que haya token de final de programa
    if(endDuplicates == 0):
        errorMessages.append("Syntax: declaración final programa no existente")
    
    #detectar que no hayan duplicados de token inicio de programa
    if(startDuplicates > 1):
        for i in tokenList:
            if(tokenList[i] == "startProgram"):
                tupleError = tokenTuples[i]

                errorMessages.append(f"Syntax: Múltiples declaraciones inicio programa (ln:{tupleError[2]}, col:{tupleError[1]})")
    
    #detectar que no hayan duplicados de token fin de programa
    if(endDuplicates > 1):
        for i in tokenList:
            if(tokenList[i] == "endProgram"):
                tupleError = tokenTuples[i]

                errorMessages.append(f"Syntax: Múltiples declaraciones final programa (ln:{tupleError[2]}, col:{tupleError[1]})")
    
    return(errorMessages)

def testBracketsAndParenthesis(tokenDict):

    errorMessages = []
    tokenList = tokenDict["tokens"]
    tokenTuples = tokenDict["tokenTuples"]

    stackOpenBrackets = []
    queueCloseBrackets = []

    stackOpenParenthesis = []
    queueCloseParenthesis = []

    stackOpenConditionals = []
    queueCloseConditionals = []

    stackOpenProcedures = []
    queueCloseProcedures = []

    bracketPairs = []
    parenthesisPairs = []
    conditionalPairs = []
    procedurePairs = []

    #añadir a las pilas las posiciones de los tokens
    for index in range(0, len(tokenList)):
        token = tokenList[index]
        tokenPosition = (tokenTuples[2], tokenTuples[1])

        if token == "leftBracket":
            stackOpenBrackets.append(tokenPosition)
        elif token == "rightBracket":
            queueCloseBrackets.append(tokenPosition)
        
        elif token == "leftParenthesis":
            stackOpenParenthesis.append(tokenPosition)
        elif token == "rightParenthesis":
            queueCloseParenthesis.append(tokenPosition)
        
        elif token == "startIf":
            stackOpenConditionals.append(tokenPosition)
        elif token == "endIf":
            queueCloseConditionals.append(tokenPosition)
        
        elif token == "startProc":
            stackOpenProcedures.append(tokenPosition)
        elif token == "endProc":
            queueCloseProcedures.append(tokenPosition)
        
    while(len(stackOpenBrackets) != 0 and len(queueCloseBrackets) != 0):
        openBracket = stackOpenBrackets.pop(-1)
        closeBracket = queueCloseBrackets.pop(0)

        bracketPairs.append((openBracket, closeBracket))

    if (len(stackOpenBrackets) > 0):
        for bracketPosition in stackOpenBrackets:

            errorMessages.append(f"Syntax: Llave de apertura no tiene llave de cerrado (ln: {bracketPosition[0]}, col: {bracketPosition[1]})")

    if (len(queueCloseBrackets) > 0):
        for bracketPosition in queueCloseBrackets:

            errorMessages.append(f"Syntax: Llave de cerrado no tiene llave de apertura (ln: {bracketPosition[0]}, col: {bracketPosition[1]})")

    
    
    while(len(stackOpenParenthesis) != 0 and len(queueCloseParenthesis) != 0):
        openParenthesis = stackOpenParenthesis.pop(-1)
        closeParenthesis = queueCloseParenthesis.pop(0)

        parenthesisPairs.append((openParenthesis, closeParenthesis))

    if (len(stackOpenParenthesis) > 0):
        for parenthesisPosition in stackOpenParenthesis:

            errorMessages.append(f"Syntax: Paréntesis de apertura no tiene paréntesis de cerrado (ln: {parenthesisPosition[0]}, col: {parenthesisPosition[1]})")

    if (len(queueCloseBrackets) > 0):
        for parenthesisPosition in queueCloseParenthesis:

            errorMessages.append(f"Syntax: Paréntesis de cerrado no tiene paréntesis de apertura (ln: {parenthesisPosition[0]}, col: {parenthesisPosition[1]})")

    
    
    while(len(stackOpenConditionals) != 0 and len(queueCloseConditionals) != 0):
        openConditional = stackOpenConditionals.pop(-1)
        closeConditional = queueCloseConditionals.pop(0)

        conditionalPairs.append((openConditional, closeConditional))

    if (len(stackOpenConditionals) > 0):
        for conditionalPosition in stackOpenConditionals:

            errorMessages.append(f"Syntax: Condicional de apertura no tiene condicional de cerrado (ln: {conditionalPosition[0]}, col: {conditionalPosition[1]})")

    if (len(queueCloseConditionals) > 0):
        for consitionalPosition in queueCloseConditionals:

            errorMessages.append(f"Syntax: Condicional de cerrado no tiene condicional de apertura (ln: {consitionalPosition[0]}, col: {consitionalPosition[1]})")

    
    
    while(len(stackOpenProcedures) != 0 and len(queueCloseProcedures) != 0):
        openProcedure = stackOpenProcedures.pop(-1)
        closeProcedure = queueCloseProcedures.pop(0)

        procedurePairs.append((openProcedure, closeProcedure))

    if (len(stackOpenProcedures) > 0):
        for procedurePosition in stackOpenProcedures:

            errorMessages.append(f"Syntax: Inicio de procedimiento no tiene fin de procedimiento (ln: {procedurePosition[0]}, col: {procedurePosition[1]})")

    if (len(queueCloseProcedures) > 0):
        for procedurePosition in queueCloseProcedures:

            errorMessages.append(f"Syntax: Fin de procedimiento no tiene inicio (ln: {procedurePosition[0]}, col: {procedurePosition[1]})")



    return (errorMessages, bracketPairs, parenthesisPairs, conditionalPairs, procedurePairs)

def testCommands(tokenDict, commandList, commandStructures, parameterList):

    errorMessages = []
    tokenList = tokenDict["tokens"]
    tokenTuples = tokenDict["tokenTuples"]

    for index in range(0, len(tokenList)):
        originalToken = tokenList[index]
        originalTokenPosition = (tokenTuples[index][2], tokenTuples[index][1])

        if originalToken in commandList:
            variableIndex = index + 1
            variableToken = tokenList[variableIndex]
            if variableIndex < len(tokenList):
                variableToken = tokenList[variableIndex]
            errorRaised = False
            parameterCount = 0

            if variableToken != "leftParenthesis":
                errorMessages.append(f"Syntax: error con estructura de comando (ln: {originalTokenPosition[0]}, col: {originalTokenPosition[1]})")
                errorRaised = True

            else:
                stopFlag = False

                while(not(stopFlag) and variableIndex < len(tokenList)):
                    variableIndex += 1
                    if variableIndex < len(tokenList):
                        variableToken = tokenList[variableIndex]

                    while((variableToken == "space" or variableToken == "nextLine") and variableIndex < len(tokenList)):
                        variableIndex += 1
                        if variableIndex < len(tokenList):
                            variableToken = tokenList[variableIndex]

                    if ((variableToken in parameterList) or (variableToken[0:17] in parameterList) or (variableToken[0:3]) in parameterList):
                        
                        parameterCount += 1

                        variableIndex += 1
                        if variableIndex < len(tokenList):
                            variableToken = tokenList[variableIndex]

                        while(variableToken == "space" and variableIndex < len(tokenList)):
                            variableIndex += 1
                            if variableIndex < len(tokenList):
                                variableToken = tokenList[variableIndex]

                        if (variableToken == "rightParenthesis"):
                            stopFlag = True
                        
                        elif(variableToken == "comma"):
                            continue

                        else: 

                            errorMessages.append(f"Syntax: error estructura de comando (ln: {originalTokenPosition[0]}, col: {originalTokenPosition[1]}))")

                            stopFlag = True
                            errorRaised = True
                    
                    else:
                        errorMessages.append(f"Syntax: error tipo de parametro ingresado (ln: {originalTokenPosition[0]}, col: {originalTokenPosition[1]}))")

                        stopFlag = True
                        errorRaised = True

                if not(errorRaised):
                    variableIndex += 1
                    if variableIndex < len(tokenList):
                        variableToken = tokenList[variableIndex]

                    while((variableToken == "space" or variableToken == "nextLine") and variableIndex < len(tokenList)):
                        variableIndex += 1
                        if variableIndex < len(tokenList):
                            variableToken = tokenList[variableIndex]

                    if variableToken == "semiColon" or variableToken == "rightBracket":
                        continue
                    else:
                        errorMessages.append(f"Syntax: No se ha terminado la declaración del comando correctamente (ln: {originalTokenPosition[0]}, col: {originalTokenPosition[1]})")


            if not(errorRaised):
                if originalToken == "walkFunc":
                    if not(parameterCount == 1 or parameterCount == 2):
                        errorMessages.append(f"Syntax: Numero de parámetros no acuerda con los que recibe el comando (ln: {originalTokenPosition[0]}, col: {originalTokenPosition[1]})")
                
                else:
                    numPrameters = commandStructures[originalToken]

                    if parameterCount != numPrameters:
                        errorMessages.append(f"Syntax: Numero de parámetros no acuerda con los que recibe el comando (ln: {originalTokenPosition[0]}, col: {originalTokenPosition[1]})")

    return errorMessages

def testConditionals(tokenDict, conditionalList, conditionalStructures, parameterList):
    
    errorMessages = []
    tokenList = tokenDict["tokens"]
    tokenTuples = tokenDict["tokenTuples"]

    for index in range(0, len(tokenList)):
        originalToken = tokenList[index]
        originalTokenPosition = (tokenTuples[index][2], tokenTuples[index][1])

        if originalToken == "startIf":
            variableIndex = index + 1
            variableToken = tokenList[variableIndex]
            if variableIndex < len(tokenList):
                variableToken = tokenList[variableIndex]
            errorRaised = False
            parameterCount = 0
            

            while(variableToken == "space" and variableIndex < len(tokenList)):
                variableIndex += 1
                if variableIndex < len(tokenList):
                    variableToken = tokenList[variableIndex]
  
            if variableToken != "leftParenthesis":
                errorMessages.append(f"Syntax: error con estructura de condicional (ln: {originalTokenPosition[0]}, col: {originalTokenPosition[1]})")
                errorRaised = True

            else:
                stopFlag = False

            
                variableIndex += 1
                if variableIndex < len(tokenList):
                    variableToken = tokenList[variableIndex]

                while(variableToken == "space" and variableIndex < len(tokenList)):
                    variableIndex += 1
                    if variableIndex < len(tokenList):
                        variableToken = tokenList[variableIndex]

                if(variableToken in conditionalList):
                    notCounter = 0

                    if variableToken == "not":

                        stopNotLoop = True

                        while(stopNotLoop):

                            variableIndex += 1
                            if variableIndex < len(tokenList):
                                variableToken = tokenList[variableIndex]
                            
                            if variableToken != "leftParenthesis":
                                errorMessages.append(f"Syntax: error con estructura de condicional (ln: {originalTokenPosition[0]}, col: {originalTokenPosition[1]})")
                                errorRaised = True
                                stopNotLoop = False

                            else:
                                while(variableToken == "space" and variableIndex < len(tokenList)):
                                    variableIndex += 1
                                    if variableIndex < len(tokenList):
                                        variableToken = tokenList[variableIndex]

                                if((variableToken in conditionalList) and variableToken != "not"):
                                    stopNotLoop = False
                                    conditionalNumParameters = conditionalStructures[variableToken]

                                else:
                                    notCounter += 1

                        variableIndex += 1
                        if variableIndex < len(tokenList):
                            variableToken = tokenList[variableIndex]
                            
                        if variableToken != "leftParenthesis":
                            errorMessages.append(f"Syntax: error con estructura de condicional (ln: {originalTokenPosition[0]}, col: {originalTokenPosition[1]})")
                            errorRaised = True

                        else:
                            variableIndex += 1
                            if variableIndex < len(tokenList):
                                variableToken = tokenList[variableIndex]



                    else:
                        conditionalNumParameters = conditionalStructures[variableToken]

                        variableIndex += 1
                        if variableIndex < len(tokenList):
                            variableToken = tokenList[variableIndex]
                            
                        if variableToken != "leftParenthesis":
                            errorMessages.append(f"Syntax: error con estructura de condicional (ln: {originalTokenPosition[0]}, col: {originalTokenPosition[1]})")
                            errorRaised = True

                        else:
                            variableIndex += 1
                            if variableIndex < len(tokenList):
                                variableToken = tokenList[variableIndex]

                    parameterCountStopFlag = False

                    while(not(parameterCountStopFlag) and variableIndex < len(tokenList)):

                        while((variableToken == "space") and variableIndex < len(tokenList)):
                            variableIndex += 1
                            if variableIndex < len(tokenList):
                                variableToken = tokenList[variableIndex]

                        if((variableToken in parameterList) or (variableToken[0:17] in parameterList) or (variableToken[0:3]) in parameterList):
                            
                            parameterCount += 1

                            variableIndex += 1
                            if variableIndex < len(tokenList):
                                variableToken = tokenList[variableIndex]

                            while(variableToken == "space" and variableIndex < len(tokenList)):
                                variableIndex += 1
                                if variableIndex < len(tokenList):
                                    variableToken = tokenList[variableIndex]

                            if (variableToken == "rightParenthesis"):
                                parameterCountStopFlag = True
                            
                            elif(variableToken == "comma"):
                                variableIndex += 1
                                if variableIndex < len(tokenList):
                                    variableToken = tokenList[variableIndex]
                                continue

                            else: 

                                errorMessages.append(f"Syntax: error estructura de condicional (ln: {originalTokenPosition[0]}, col: {originalTokenPosition[1]}))")

                                parameterCountStopFlag = True
                                errorRaised = True
                        
                        else:
                            errorMessages.append(f"Syntax: error tipo de parametro ingresado (ln: {originalTokenPosition[0]}, col: {originalTokenPosition[1]}))")

                            parameterCountStopFlag = True
                            errorRaised = True

                            variableIndex += 1
                            if variableIndex < len(tokenList):
                                variableToken = tokenList[variableIndex]

                            while(variableToken == "space" and variableIndex < len(tokenList)):
                                variableIndex += 1
                                if variableIndex < len(tokenList):
                                    variableToken = tokenList[variableIndex]

                if not(errorRaised):
                    if parameterCount != conditionalNumParameters:
                        errorMessages.append(f"Syntax: Numero de parámetros no acuerda con los que recibe la condición (ln: {originalTokenPosition[0]}, col: {originalTokenPosition[1]})")

                    else:
                        stopNotLoop = True
                        while(notCounter > 0 and stopNotLoop):
                            variableIndex += 1
                            if variableIndex < len(tokenList):
                                variableToken = tokenList[variableIndex]

                            while(variableToken == "space" and variableIndex < len(tokenList)):
                                variableIndex += 1
                                if variableIndex < len(tokenList):
                                    variableToken = tokenList[variableIndex]

                            if variableToken != "leftParenthesis":
                                errorMessages.append(f"Syntax: error con estructura de condicional (ln: {originalTokenPosition[0]}, col: {originalTokenPosition[1]})")
                                stopNotLoop = False
                            else:
                                notCounter -= 1

                        variableIndex += 1
                        if variableIndex < len(tokenList):
                            variableToken = tokenList[variableIndex]

                        while((variableToken == "space") and variableIndex < len(tokenList)):
                            variableIndex += 1
                            if variableIndex < len(tokenList):
                                variableToken = tokenList[variableIndex]

                        if variableToken != "rightParenthesis":
                            errorMessages.append(f"Syntax: Error con estructura de condicional (ln: {originalTokenPosition[0]}, col: {originalTokenPosition[1]})")

                        else:

                            variableIndex += 1
                            if variableIndex < len(tokenList):
                                variableToken = tokenList[variableIndex]

                            while((variableToken == "space" or variableToken == "nextLine") and variableIndex < len(tokenList)):
                                variableIndex += 1
                                if variableIndex < len(tokenList):
                                    variableToken = tokenList[variableIndex]

                            if variableToken != "leftBracket":
                                errorMessages.append(f"Syntax: Error con estructura de condicional (ln: {originalTokenPosition[0]}, col: {originalTokenPosition[1]})")

                            else:
                                variableIndex += 1
                                if variableIndex < len(tokenList):
                                    variableToken = tokenList[variableIndex]
                                openBracketCounter = 1
                                stopFlag = True

                                while((stopFlag) and variableIndex < len(tokenList)):
                                    variableIndex += 1
                                    if variableIndex < len(tokenList):
                                        variableToken = tokenList[variableIndex]

                                    if variableToken == "endIf":
                                        errorMessages.append(f"Syntax: Error con estructura de condicional (ln: {originalTokenPosition[0]}, col: {originalTokenPosition[1]})")

                                    elif variableToken == "leftBracket":
                                        openBracketCounter += 1

                                    elif variableToken == "rightBracket":
                                        openBracketCounter -= 1

                                    if openBracketCounter == 0:
                                        stopFlag = False
                                
                                variableIndex += 1
                                if variableIndex < len(tokenList):
                                    variableToken = tokenList[variableIndex]

                                while((variableToken == "space" or variableToken == "nextLine") and variableIndex < len(tokenList)):
                                    variableIndex += 1
                                    if variableIndex < len(tokenList):
                                        variableToken = tokenList[variableIndex]

                                if variableToken == "elseIf":
                                    variableIndex += 1
                                    if variableIndex < len(tokenList):
                                        variableToken = tokenList[variableIndex]

                                    while((variableToken == "space" or variableToken == "nextLine") and variableIndex < len(tokenList)):
                                        variableIndex += 1
                                        if variableIndex < len(tokenList):
                                            variableToken = tokenList[variableIndex]

                                    if variableToken != "leftBracket":
                                        errorMessages.append(f"Syntax: Error con estructura de condicional (ln: {originalTokenPosition[0]}, col: {originalTokenPosition[1]})")

                                    else:
                                        variableIndex += 1
                                        if variableIndex < len(tokenList):
                                            variableToken = tokenList[variableIndex]

                                        while((variableToken == "rightBracket") and variableIndex < len(tokenList)):
                                            variableIndex += 1
                                            if variableIndex < len(tokenList):
                                                variableToken = tokenList[variableIndex]

                                            if variableToken == "endIf":
                                                errorMessages.append(f"Syntax: Error con estructura de condicional (ln: {originalTokenPosition[0]}, col: {originalTokenPosition[1]})")

                                    variableIndex += 1
                                    if variableIndex < len(tokenList):
                                        variableToken = tokenList[variableIndex]

                                while((variableToken == "space" or variableToken == "nextLine") and variableIndex < len(tokenList)):
                                    variableIndex += 1
                                    if variableIndex < len(tokenList):
                                        variableToken = tokenList[variableIndex]

                                if variableToken != "endIf":
                                    errorMessages.append(f"Syntax: Error con estructura de condicional (ln: {originalTokenPosition[0]}, col: {originalTokenPosition[1]})")


                else:
                    errorMessages.append(f"Syntax: Error con estructura de condicional (ln: {originalTokenPosition[0]}, col: {originalTokenPosition[1]})")
                    errorRaised = True

    return errorMessages

def testLoops(tokenDict, conditionalList, conditionalStructures, parameterList):
    
    errorMessages = []
    tokenList = tokenDict["tokens"]
    tokenTuples = tokenDict["tokenTuples"]

    for index in range(0, len(tokenList)):
        originalToken = tokenList[index]
        originalTokenPosition = (tokenTuples[index][2], tokenTuples[index][1])


        if(originalToken == "whileLoop"):
            variableIndex = index + 1
            variableToken = tokenList[variableIndex]
            if variableIndex < len(tokenList):
                variableToken = tokenList[variableIndex]
            errorRaised = False
            parameterCount = 0
            

            while(variableToken == "space" and variableIndex < len(tokenList)):
                variableIndex += 1
                if variableIndex < len(tokenList):
                    variableToken = tokenList[variableIndex]

            if variableToken != "leftParenthesis":
                errorMessages.append(f"Syntax: error con estructura de condicional (ln: {originalTokenPosition[0]}, col: {originalTokenPosition[1]})")
                errorRaised = True

            else:
                variableIndex += 1
                if variableIndex < len(tokenList):
                    variableToken = tokenList[variableIndex]

                while(variableToken == "space" and variableIndex < len(tokenList)):
                    variableIndex += 1
                    if variableIndex < len(tokenList):
                        variableToken = tokenList[variableIndex]

                if(variableToken in conditionalList):
                    notCounter = 0

                    if variableToken == "not":

                        stopNotLoop = True

                        while(stopNotLoop):

                            variableIndex += 1
                            if variableIndex < len(tokenList):
                                variableToken = tokenList[variableIndex]
                            
                            if variableToken != "leftParenthesis":
                                errorMessages.append(f"Syntax: error con estructura de condicional (ln: {originalTokenPosition[0]}, col: {originalTokenPosition[1]})")
                                errorRaised = True
                                stopNotLoop = False

                            else:
                                while(variableToken == "space" and variableIndex < len(tokenList)):
                                    variableIndex += 1
                                    if variableIndex < len(tokenList):
                                        variableToken = tokenList[variableIndex]

                                if((variableToken in conditionalList) and variableToken != "not"):
                                    stopNotLoop = False
                                    conditionalNumParameters = conditionalStructures[variableToken]

                                else:
                                    notCounter += 1

                        variableIndex += 1
                        if variableIndex < len(tokenList):
                            variableToken = tokenList[variableIndex]
                            
                        if variableToken != "leftParenthesis":
                            errorMessages.append(f"Syntax: error con estructura de condicional (ln: {originalTokenPosition[0]}, col: {originalTokenPosition[1]})")
                            errorRaised = True

                        else:
                            variableIndex += 1
                            if variableIndex < len(tokenList):
                                variableToken = tokenList[variableIndex]

                    else:
                        conditionalNumParameters = conditionalStructures[variableToken]

                        variableIndex += 1
                        if variableIndex < len(tokenList):
                            variableToken = tokenList[variableIndex]
                            
                        if variableToken != "leftParenthesis":
                            errorMessages.append(f"Syntax: error con estructura de condicional (ln: {originalTokenPosition[0]}, col: {originalTokenPosition[1]})")
                            errorRaised = True

                        else:
                            variableIndex += 1
                            if variableIndex < len(tokenList):
                                variableToken = tokenList[variableIndex]

                    parameterCountStopFlag = False

                    while(not(parameterCountStopFlag) and variableIndex < len(tokenList)):

                        while((variableToken == "space") and variableIndex < len(tokenList)):
                            variableIndex += 1
                            if variableIndex < len(tokenList):
                                variableToken = tokenList[variableIndex]

                        if((variableToken in parameterList) or (variableToken[0:17] in parameterList) or (variableToken[0:3]) in parameterList):
                            
                            parameterCount += 1

                            variableIndex += 1
                            if variableIndex < len(tokenList):
                                variableToken = tokenList[variableIndex]

                            while(variableToken == "space" and variableIndex < len(tokenList)):
                                variableIndex += 1
                                if variableIndex < len(tokenList):
                                    variableToken = tokenList[variableIndex]

                            if (variableToken == "rightParenthesis"):
                                parameterCountStopFlag = True
                            
                            elif(variableToken == "comma"):
                                variableIndex += 1
                                if variableIndex < len(tokenList):
                                    variableToken = tokenList[variableIndex]
                                continue

                            else: 

                                errorMessages.append(f"Syntax: error estructura de condicional (ln: {originalTokenPosition[0]}, col: {originalTokenPosition[1]}))")

                                parameterCountStopFlag = True
                                errorRaised = True
                        
                        else:
                            errorMessages.append(f"Syntax: error tipo de parametro ingresado (ln: {originalTokenPosition[0]}, col: {originalTokenPosition[1]}))")

                            parameterCountStopFlag = True
                            errorRaised = True

                            variableIndex += 1
                            if variableIndex < len(tokenList):
                                variableToken = tokenList[variableIndex]

                            while(variableToken == "space" and variableIndex < len(tokenList)):
                                variableIndex += 1
                                if variableIndex < len(tokenList):
                                    variableToken = tokenList[variableIndex]

                    variableIndex += 1
                    if variableIndex < len(tokenList):
                        variableToken = tokenList[variableIndex]

                    while((variableToken == "space") and variableIndex < len(tokenList)):
                        variableIndex += 1
                        if variableIndex < len(tokenList):
                            variableToken = tokenList[variableIndex]

                    if variableToken != "rightParenthesis":
                        errorMessages.append(f"Syntax: error con estructura de condicional (ln: {originalTokenPosition[0]}, col: {originalTokenPosition[1]})")
                        errorRaised = True



            if not(errorRaised):
                variableIndex += 1
                if variableIndex < len(tokenList):
                    variableToken = tokenList[variableIndex]

                while((variableToken == "space" or variableToken == "nextLine") and variableIndex < len(tokenList)):
                    variableIndex += 1
                    if variableIndex < len(tokenList):
                        variableToken = tokenList[variableIndex]

                if variableToken != "startDo":
                    errorMessages.append(f"Syntax: error con estructura de condicional (ln: {originalTokenPosition[0]}, col: {originalTokenPosition[1]})")
                    errorRaised = True
        
                else:
                    variableIndex += 1
                    if variableIndex < len(tokenList):
                        variableToken = tokenList[variableIndex]

                    while((variableToken == "space" or variableToken == "nextLine") and variableIndex < len(tokenList)):
                        variableIndex += 1
                        if variableIndex < len(tokenList):
                            variableToken = tokenList[variableIndex]

                    if variableToken == "leftBracket":
                        openBracketCounter = 1
                        stopFlag = True

                        while((stopFlag) and variableIndex < len(tokenList)):
                            variableIndex += 1
                            if variableIndex < len(tokenList):
                                variableToken = tokenList[variableIndex]

                            if variableToken == "leftBracket":
                                openBracketCounter += 1

                            elif variableToken == "rightBracket":
                                openBracketCounter -= 1

                            if openBracketCounter == 0:
                                stopFlag = False

                        if not(errorRaised):
                            variableIndex += 1
                            if variableIndex < len(tokenList):
                                variableToken = tokenList[variableIndex]

                            while((variableToken == "space" or variableToken == "nextLine") and variableIndex < len(tokenList)):
                                variableIndex += 1
                                if variableIndex < len(tokenList):
                                    variableToken = tokenList[variableIndex]

                            if variableToken != "endDo":
                                errorMessages.append(f"Syntax: error con el cierre del ciclo (ln: {originalTokenPosition[0]}, col: {originalTokenPosition[1]})")
                                errorRaised = True


                    else:
                        errorMessages.append(f"Syntax: error con estructura del ciclo (ln: {originalTokenPosition[0]}, col: {originalTokenPosition[1]})")
                        errorRaised = True  
        
        elif(originalToken == "startRepeat"):
            variableIndex = index + 1
            if variableIndex < len(tokenList):
                variableToken = tokenList[variableIndex]
            errorRaised = False
            parameterCount = 0
            

            while(variableToken == "space" and variableIndex < len(tokenList)):
                variableIndex += 1
                if variableIndex < len(tokenList):
                    variableToken = tokenList[variableIndex]

            if((variableToken in parameterList) or (variableToken[0:17] in parameterList) or (variableToken[0:3]) in parameterList):

                variableIndex = index + 1
                if variableIndex < len(tokenList):
                    variableToken = tokenList[variableIndex]

                while(variableToken == "space" and variableIndex < len(tokenList)):
                    variableIndex += 1
                    if variableIndex < len(tokenList):
                        variableToken = tokenList[variableIndex]

                if variableToken != "leftBracket":
                    errorMessages.append(f"Syntax: Error con estructura del ciclo (ln: {originalTokenPosition[0]}, col: {originalTokenPosition[1]})")
                    errorRaised = True

                else:
                    variableIndex += 1
                    if variableIndex < len(tokenList):
                        variableToken = tokenList[variableIndex]
                    openBracketCounter = 1
                    stopFlag = True

                    while((stopFlag) and variableIndex < len(tokenList)):
                        variableIndex += 1
                        if variableIndex < len(tokenList):
                            variableToken = tokenList[variableIndex]

                        if variableToken == "leftBracket":
                            openBracketCounter += 1

                        elif variableToken == "rightBracket":
                            openBracketCounter -= 1

                        if openBracketCounter == 0:
                            stopFlag = False

                    variableIndex = index + 1
                    if variableIndex < len(tokenList):
                        variableToken = tokenList[variableIndex]

                    while((variableToken == "space" or variableToken == "nextLine") and variableIndex < len(tokenList)):
                        variableIndex += 1
                        if variableIndex < len(tokenList):
                            variableToken = tokenList[variableIndex]

                    if variableToken != "endRepeat":
                        errorMessages.append(f"Syntax: Error con finalización del ciclo (ln: {originalTokenPosition[0]}, col: {originalTokenPosition[1]})")
                        errorRaised = True

            else:
                errorMessages.append(f"Syntax: Error con estructura del ciclo (ln: {originalTokenPosition[0]}, col: {originalTokenPosition[1]})")
                errorRaised = True

    return errorMessages

def testVariablesAndFunctions(tokenDict, expectedParameterList):
    errorMessages = []
    tokenList = tokenDict["tokens"]
    tokenTuples = tokenDict["tokenTuples"]


    """
    nombre = {
        nombre: ""
        lugar: ()
        instancias: [(),()]

    }
    """
    variableInstances = {}


    """
    nombre = {
        nombre: ""
        lugar: ()
        instancias = [(),()]
        parametros = 0
    }
    """
    functionInstances = {}

    """
    nombre = {
        posicionesInicianles: [(ln, col)]
        posicionesFinales: [(ln,col)]
    }
    
    """
    parametersExpectedPlace = {

    }



    for index in range(0, len(tokenList)):
        originalToken = tokenList[index]
        originalTokenPosition = (tokenTuples[index][2], tokenTuples[index][1])

        if originalToken == "variableInitializer":
            variableIndex = index
            variableToken = tokenList[variableIndex]
            if variableIndex < len(tokenList):
                variableToken = tokenList[variableIndex]
            errorRaised = False
            multipleVarsFlag = True
            
            while(multipleVarsFlag and not(errorRaised)):
                variableIndex += 1
                if variableIndex < len(tokenList):
                    variableToken = tokenList[variableIndex]

                while(variableToken == "space" and variableIndex < len(tokenList)):
                    variableIndex += 1
                    if variableIndex < len(tokenList):
                        variableToken = tokenList[variableIndex]


                if variableToken[0:17] == "DeclarativeState_":

                    variableName = variableToken[17:]

                    if variableName in variableInstances:
                        errorMessages.append(f"Syntax: multiples inicializaciones de la variable (ln: {originalTokenPosition[0]}, col: {originalTokenPosition[1]})")
                        errorRaised = True
                    
                    elif variableName in functionInstances:
                        errorMessages.append(f"Syntax: nombre de variable coincide con nombre de procedimiento(ln: {originalTokenPosition[0]}, col: {originalTokenPosition[1]})")
                        errorRaised = True

                    else:

                        variableInstances[variableName]= {
                            "nombre": variableName,
                            "posición": originalTokenPosition,
                            "instancias": []
                        }

                    
                    if not(errorRaised):
                        variableIndex += 1
                        if variableIndex < len(tokenList):
                            variableToken = tokenList[variableIndex]

                        while(variableToken == "space" and variableIndex < len(tokenList)):
                            variableIndex += 1
                            if variableIndex < len(tokenList):
                                variableToken = tokenList[variableIndex]

                        if variableToken == "semiColon":
                            multipleVarsFlag = False


                        
                        elif variableToken == "comma":
                            continue
                        
                        else:
                            errorMessages.append(f"Syntax: Error con la estructura de declaración de variable(ln: {originalTokenPosition[0]}, col: {originalTokenPosition[1]})")
                            errorRaised = True

                else:
                    errorMessages.append(f"Syntax: Error con la estructura de declaración de variable(ln: {originalTokenPosition[0]}, col: {originalTokenPosition[1]})")
                    errorRaised = True

        elif originalToken == "startProc":
            variableIndex = index + 1
            if variableIndex < len(tokenList):
                variableToken = tokenList[variableIndex]
            errorRaised = False


            while(variableToken == "space" and variableIndex < len(tokenList)):
                variableIndex += 1
                if variableIndex < len(tokenList):
                    variableToken = tokenList[variableIndex]

            if variableToken[0:17] == "DeclarativeState_":

                functionName = variableToken[17:]

                if functionName in variableInstances:
                    errorMessages.append(f"Syntax: nombre de procedimeinto coincide con nombre de variable (ln: {originalTokenPosition[0]}, col: {originalTokenPosition[1]})")
                    errorRaised = True
                
                elif functionName in functionInstances: 
                    errorMessages.append(f"Syntax: Múltiples declaraciones del mismo procedimiento (ln: {originalTokenPosition[0]}, col: {originalTokenPosition[1]})")
                    errorRaised = True

                else:

                    functionInstances[functionName]= {
                        "nombre": functionName,
                        "posición": originalTokenPosition,
                        "instancias": [],
                        "numParametros": 0,
                        "parametros": [],
                        "initialized": False
                    }

                if not(errorRaised):
                    variableIndex += 1
                    if variableIndex < len(tokenList):
                        variableToken = tokenList[variableIndex]

                    if variableToken == "leftParenthesis":
                        parameterDeclarationFlag = True
                        parameterList = []
                        parameterStart = originalTokenPosition
                        parameterEnd = ()

                        while(parameterDeclarationFlag and not(errorRaised)):
                            variableIndex += 1
                            if variableIndex < len(tokenList):
                                variableToken = tokenList[variableIndex]

                            while(variableToken == "space" and variableIndex < len(tokenList)):
                                variableIndex += 1
                                if variableIndex < len(tokenList):
                                    variableToken = tokenList[variableIndex]

                            if variableToken[0:17] == "DeclarativeState_":
                                parameterName = variableToken[17:]
                                if (not(parameterName in functionInstances[functionName])):
                                    functionInstances[functionName]["numParametros"] += 1
                                    functionInstances[functionName]["parametros"].append(parameterName)
                                    parameterList.append(parameterName)

                                    variableIndex += 1
                                    if variableIndex < len(tokenList):
                                        variableToken = tokenList[variableIndex]

                                    while(variableToken == "space" and variableIndex < len(tokenList)):
                                        variableIndex += 1
                                        if variableIndex < len(tokenList):
                                            variableToken = tokenList[variableIndex]

                                    if(variableToken == "rightParenthesis"):
                                        parameterDeclarationFlag = False

                                    elif(variableToken == "comma"):
                                        continue

                                    else:
                                        errorMessages.append(f"Syntax: Error con la declaración de parámetros en el procedimiento (ln: {originalTokenPosition[0]}, col: {originalTokenPosition[1]})")
                                        errorRaised = True

                                        parameterEnd = (tokenTuples[variableIndex][2], tokenTuples[variableIndex][1])


                                else:
                                    errorMessages.append(f"Syntax: Multiples inicializaciones del mismo parámetro (ln: {originalTokenPosition[0]}, col: {originalTokenPosition[1]})")
                                    errorRaised = True
                                    
                                    parameterEnd = (tokenTuples[variableIndex][2], tokenTuples[variableIndex][1])

                            elif variableToken == "rightParenthesis":
                                parameterDeclarationFlag = False

                            else:
                                errorMessages.append(f"se ha ingresado algun objeto incorrecto como parámetro (ln: {originalTokenPosition[0]}, col: {originalTokenPosition[1]})")
                                errorRaised = True

                                parameterEnd = (tokenTuples[variableIndex][2], tokenTuples[variableIndex][1]) 


                        if not(errorRaised):

                            variableIndex += 1
                            if variableIndex < len(tokenList):
                                variableToken = tokenList[variableIndex]

                            while((variableToken == "space" or variableToken == "nextLine") and variableIndex < len(tokenList)):
                                variableIndex += 1
                                if variableIndex < len(tokenList):
                                    variableToken = tokenList[variableIndex]

                            if variableToken != "leftBracket":
                                errorMessages.append(f"Syntax: Error con la estructura de declaración de procedimiento (ln: {originalTokenPosition[0]}, col: {originalTokenPosition[1]})")
                                errorRaised = True

                            else:
                                openBracketCounter = 1

                                while(openBracketCounter > 0 and variableIndex < len(tokenList)):
                                    variableIndex += 1
                                    if variableIndex < len(tokenList):
                                        variableToken = tokenList[variableIndex]
                                    
                                    if variableToken == "leftBracket":
                                        openBracketCounter += 1
                                    
                                    elif variableToken == "rightBracket":
                                        openBracketCounter -= 1

                                    elif variableToken == "endProc":
                                        errorMessages.append(f"Syntax: Error con la terminación del proceso (ln: {originalTokenPosition[0]}, col: {originalTokenPosition[1]})")
                                        errorRaised = True

                                if not(errorRaised):
                                    variableIndex += 1
                                    if variableIndex < len(tokenList):
                                        variableToken = tokenList[variableIndex]

                                    while((variableToken == "space" or variableToken == "nextLine") and variableIndex < len(tokenList)):
                                        variableIndex += 1
                                        if variableIndex < len(tokenList):
                                            variableToken = tokenList[variableIndex]

                                    if variableToken != "endProc":
                                        errorMessages.append(f"Syntax: Error con la terminación del proceso (ln: {originalTokenPosition[0]}, col: {originalTokenPosition[1]})")
                                        errorRaised = True
                                    else:
                                        parameterEnd = (tokenTuples[variableIndex][2], tokenTuples[variableIndex][1])


                    else:
                        errorMessages.append(f"Syntax: Error con la estructura de declaración de procedimiento (ln: {originalTokenPosition[0]}, col: {originalTokenPosition[1]})")
                        errorRaised = True

            else:
                errorMessages.append(f"Syntax: Error con la estructura de declaración de procedimiento(ln: {originalTokenPosition[0]}, col: {originalTokenPosition[1]})")
                errorRaised = True

            if not(errorRaised):

                functionInstances[functionName]["initialized"] == True

                for parameter in parameterList:
                    if not(parameter in parametersExpectedPlace):
                        parametersExpectedPlace[parameter] = {
                            "posicionesInicianles": [originalTokenPosition],
                            "posicionesFinales": [parameterEnd]
                        }

                    else:
                        parametersExpectedPlace[parameter]["posicionesInicianles"].append(originalTokenPosition)
                        parametersExpectedPlace[parameter]["posicionesFinales"].append(parameterEnd)

        elif originalToken[0:17] == "DeclarativeState_":
            stateName = originalToken[17:]

            variableIndex = index + 1
            if variableIndex < len(tokenList):
                variableToken = tokenList[variableIndex]

            if not(stateName in variableInstances or stateName in functionInstances or stateName in parametersExpectedPlace):

                errorMessages.append(f"Syntax: estado no ha sido declarado con ningún tipo (ln: {originalTokenPosition[0]}, col: {originalTokenPosition[1]})")

            else:
                errorRaised = False

                if stateName in variableInstances:
                    errorRaised = False

                elif stateName in functionInstances:

                    functionInfo = functionInstances[stateName]

                    if variableToken != "leftParenthesis":
                        errorMessages.append(f"Syntax: El llamado de procedimiento es incorrecto (ln: {originalTokenPosition[0]}, col: {originalTokenPosition[1]})")
                        errorRaised = True

                    else:
                        parameterCounter = 0
                        countingParameters = True

                        if functionInfo["numParametros"] != 0:

                            while(countingParameters and variableIndex < len(tokenList)):

                                variableIndex += 1
                                if variableIndex < len(tokenList):
                                    variableToken = tokenList[variableIndex]

                                while(variableToken == "space" and variableIndex < len(tokenList)):
                                    variableIndex += 1
                                    if variableIndex < len(tokenList):
                                        variableToken = tokenList[variableIndex]

                                
                                if ((variableToken in expectedParameterList) or (variableToken[0:17] in expectedParameterList) or (variableToken[0:3]) in expectedParameterList):
                                    parameterCounter += 1

                                    variableIndex += 1
                                    if variableIndex < len(tokenList):
                                        variableToken = tokenList[variableIndex]

                                    while(variableToken == "space" and variableIndex < len(tokenList)):
                                        variableIndex += 1
                                        if variableIndex < len(tokenList):
                                            variableToken = tokenList[variableIndex]

                                    if variableToken == "comma":
                                        continue

                                    elif(variableToken == "rightParenthesis"):
                                        countingParameters = False

                                    else:
                                        errorMessages.append(f"Syntax: Error con estructura de llamado de procedimiento (ln: {originalTokenPosition[0]}, col: {originalTokenPosition[1]})")
                                        errorRaised = True


                                else:
                                    errorMessages.append(f"Syntax: se ha ingresado algun objeto incorrecto como parámetro (ln: {originalTokenPosition[0]}, col: {originalTokenPosition[1]})")
                                    errorRaised = True
                                
                        if not(errorRaised):

                            parameterTrueCount = functionInfo["numParametros"]

                            if parameterCounter != parameterTrueCount:
                                errorMessages.append(f"Syntax: el número de parametros ingresados no coincide con el número de parámetros que pide el procedimiento (ln: {originalTokenPosition[0]}, col: {originalTokenPosition[1]})")
                                errorRaised = True

                elif stateName in parametersExpectedPlace:
                    line = originalTokenPosition[0]
                    column = originalTokenPosition[1]

                    startPlaces = parametersExpectedPlace[stateName]["posicionesInicianles"]
                    endPlaces = parametersExpectedPlace[stateName]["posicionesFinales"]

                    inExpectedPlace = False

                    for index in range(0, len(startPlaces)):
                        start = startPlaces[index]
                        startLine, startCol = start
                        end = endPlaces[index]
                        endLine, endCol = end

                        if (line >= startLine and line <= endLine):
                            inExpectedPlace = True
                            break

                    if not(inExpectedPlace):
                        errorMessages.append(f"El parámetro no se encuentra en el lugar designado (ln: {originalTokenPosition[0]}, col: {originalTokenPosition[1]})")

    return(errorMessages)

