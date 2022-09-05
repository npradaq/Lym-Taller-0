def testVariables(tokenDict):
    errorMessages = []
    tokenList = tokenDict["tokens"]
    tokenTuples = tokenDict["tokenTuples"]

    variablesInitializations = {}
    variablesInstances = {}

    #comprobar qué variables se han inicializado, y donde
    for i in range(0,len(tokenList)):
        token = tokenList[i]
        tokenDeclarative = token[0:17]
        if(token == "variableInitializer"):
            errorFlag = False
            endFlag = False
            j = i + 1
            while(not(errorFlag or endFlag)):
                declarative = tokenList[j+1][0:17]
                variableName = tokenList[j+1][17:]
                variablePos = tokenTuples[j+1]


                #revisar spacio
                if tokenList[j] != "space":
                    tupleError = tokenTuples[j]

                    errorMessages.append(f"Syntax: declaración de variable (ln:{tupleError[2]}, col:{tupleError[1]})")
                
                #revisar declaración variable
                if (declarative != "DeclarativeState_"):
                    tupleError = tokenTuples[j+1]

                    errorMessages.append(f"Syntax: declaración de variable (ln:{tupleError[2]}, col:{tupleError[1]})")

                #revisar punto y coma
                if(tokenList[j+2] != "semiColon"):
                    if tokenList[j+2] != "comma":
                        tupleError = tokenTuples[j+2]

                        errorMessages.append(f"Syntax: declaración de variable (ln:{tupleError[2]}, col:{tupleError[1]})")
                    
                    else:
                        j = j + 3

                if not(variablesInitializations.has_key(variableName)):
                    variablesInitializations[variableName] = (variablePos[2], variablePos[1])
                else:
                    errorMessages.append("Syntax: Múltiples declaraciones de variable")

                    endFlag = True

                if(tokenList[j] == "nextLine" or tokenList[j+1] == "nextLine" or tokenList[j+2] == "nextLine"):
                    endFlag = True

        if(tokenDeclarative == "DeclarativeState_"):
            tokenPos = tokenTuples[i]
            tokenVariableName = token[17:]

            if(variablesInstances.has_key(tokenVariableName)):
                variablesInstances[tokenVariableName].append((tokenPos[2], tokenPos[1]))
            else:
                variablesInstances[tokenVariableName] = [(tokenPos[2], tokenPos[1])]

    #Comprobar si una variable se inicia después de ser inicializada
    """
    toca arreglar esta parte tomando en cuenta variables en parametros y funciones
    """

    for key in variablesInstances:
        instances = variablesInstances[key]

        if(variablesInitializations.has_key(key)):
            initial = variablesInitializations[key]
            initialLine = initial[1]
            initialCol = initial[2]

            for inst in instances:
                instLine = inst[1]
                instCol = inst[2]

                if initialLine > initialLine:
                    errorMessages.append(f"Syntax: variable no declarada (ln:{instLine}, col:{instCol})")

                if initialCol > initialLine:
                    errorMessages.append(f"Syntax: variable no declarada (ln:{instLine}, col:{instCol})")


    return errorMessages

def testFunctions(tokenDict):
    errorMessages = []
    tokenList = tokenDict["tokens"]
    tokenTuples = tokenDict["tokenTuples"]

    """
    nombreFuncion = {
        "parameters": []
        "line":
        "col": 
    }
    """
    functionInitializations = {}
    funtionInstances = {}
    parametersInstances = {}
    parametersInitializations = []

    procCorpPairs = []


    for i in range(0,len(tokenList)):
        token = tokenList[i]

        if token == "PROC":

            j = i + 1
            
            while(tokenList[j] == "space"):
                j += 1

            if tokenList[j][0:17] == "DeclarativeState_":
                tokenPos = tokenTuples[j]
                funcName = tokenList[j][17:]

                functionInitializations[funcName] = {
                   "parameters": [],
                    "line": tokenPos[2],
                    "col": tokenPos[1],
                }

                if(tokenList[j + 1] == "leftParenthesis"):
                    k = j + 2

                    stopFlag = False
                    while(not(stopFlag)):
                        while(tokenList[k] == "space"):
                            k += 1

                        paraName = tokenList[k][17:]
                        paraLine = tokenTuples[k][2]
                        paraCol = tokenTuples[k][1]

                        if(tokenList[k][0:17] == "DeclarativeState_"):
                            parametersInitializations.append((paraName,paraLine, paraCol))
                            functionInitializations[funcName]["parameters"].append(paraName)

                        else: 
                            errorMessages.append(f"Syntax: Error de declración de parámetos (ln:{paraLine}, col:{paraCol})")

                        k += 1

                        while(tokenList[k] == "space"):
                            k += 1

                        if(tokenList[k] == "rightParenthesis"):
                            stopFlag = True
                        
                        elif(tokenList[k] == "comma"):
                            continue

                        else:
                            errorTuple = tokenTuples[k]

                            errorMessages.append(f"Syntax: Error de construcción de parámetos en la función (ln:{errorTuple[2]}, col:{errorTuple[1]})")

                            stopFlag = True

                    k += 1

                    while(tokenList[k] == "space" or tokenList[k] == "nextLine"):
                        k += 1

                    if tokenList[k] != "leftBracket":
                        errorMessages.append(f"Syntax: Error de apertura bloque (ln:{tupleError[2]}, col:{tupleError[1]})")

                    else:
                        #Inicio análisis Bloque
                        startBlock = k
                        k += 1
                        

                        while(tokenList[k] != "rightBracket" and k < len(tokenList)):
                            k += 1

                        if token[k] == "rightBracket":

                        else:
                            errorMessages.append
                    
                else:
                    tupleError = tokenTuples[j+1]

                    errorMessages.append(f"Syntax: Error de estructura de función (ln:{tupleError[2]}, col:{tupleError[1]})")

            else:
                tupleError = tokenTuples[j]

                errorMessages.append(f"Syntax: Error al declarar nombre función (ln:{tupleError[2]}, col:{tupleError[1]})")

    else:
                tupleError = tokenTuples[j]

                errorMessages.append(f"Syntax: Error al declarar nombre función (ln:{tupleError[2]}, col:{tupleError[1]})")

def checkFunctionBlock(tokenDict, startBlock, endBlock, )           
