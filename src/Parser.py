from errno import ESTALE
from inspect import Parameter
from lib2to3.pgen2 import token
from multiprocessing.resource_sharer import stop


def testSyntax(tokenDict):
    #comprobar iniciación y fin programa
    startEndTokensErrorMessages = testStartEndToken(tokenDict)
    
    #comprobar declaración variables
    variableInitializerErrorMessages = testVariables(tokenDict)

    #comprobar declaración funciones

    #comprobar apertura y cierre llaves

    #comprobar apertura y cierre parentesis

    #comprobar comandos


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
    parametersInitializations = {}

    procCorpPairs = []


    for i in range(0,len(tokenList)):
        token = tokenList[i]

        if token == "PROC":

            j = i + 1
            
            while(tokenList[j] == "space"):
                j += 1

            if tokenList[j][0:17] == "DeclarativeState_":
                tokenPos = tokenTuples[j]

                functionInitializations[tokenList[j][17:]] = {
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

                        if(tokenList[k][0:17] == "DeclarativeState_"):
                            paraName = tokenList[k][17:]
                            paraLine = tokenTuples[k][2]
                            paraCol = tokenTuples[k][1]

                            if not(parametersInitializations.has_key(paraName)):
                                parametersInitializations[paraName] = (paraLine, paraCol)
                            else:
                                errorMessages.append(f"Syntax: Error de multiples parámetos iguales (ln:{paraLine}, col:{paraCol})")

                        k += 1

                        while(tokenList[k] == "space"):
                            k += 1

                        if(tokenList[k] == "rightParenthesis"):
                            stopFlag = True
                        
                        elif(tokenList[k][0:17] == "rightParenthesis")




                    
                else:
                    tupleError = tokenTuples[j+1]

                    errorMessages.append(f"Syntax: Error de estructura de función (ln:{tupleError[2]}, col:{tupleError[1]})")



            else:
                tupleError = tokenTuples[j]

                errorMessages.append(f"Syntax: Error al declarar nombre función (ln:{tupleError[2]}, col:{tupleError[1]})")

    else:
                tupleError = tokenTuples[j]

                errorMessages.append(f"Syntax: Error al declarar nombre función (ln:{tupleError[2]}, col:{tupleError[1]})")



def testKeys(tokenDict):

    errorMessages = []
    tokenTuples = tokenDict["tokenTuples"]

    for i in range(0,len(tokenTuples)):
        token = tokenTuples[i][0]
        tokenCol = tokenTuples[i][1]
        tokenLn = tokenTuples[i][2]

        if token == "":

            pos = 


def testParentesis(tokenDict):

    errorMessages = []
    tokenTuples = tokenDict["tokenTuples"]

    for i in range(0,len(tokenTuples)):
        token = tokenTuples[i][0]
        tokenCol = tokenTuples[i][1]
        tokenLn = tokenTuples[i][2]

        markedPar = []

        if token == "leftParenthesis":

            RParenthesis = False

            for j in range(0,len(tokenTuples)):

                if (tokenTuples[j][0] == "rightParenthesis") and (tokenTuples[j][2] == tokenLn):

                    RParenthesis = True
                    RPLn = tokenTuples[j][2]
                    RPCol = tokenTuples[j][1]
        
            if not(RParenthesis):

                errorMessages.append(f"Syntax: Error de cierre de paréntesis (ln:{tokenLn}, col:{tokenCol})")

            if RParenthesis and (RPCol < tokenCol):

                errorMessages.append(f"Syntax: Error de cierre de paréntesis (ln:{RPLn}, col:{tokenTuples[j][1]})")

            if RParenthesis and (RPCol > tokenCol):

                if (RPLn,RPCol) in markedPar:

                    errorMessages.append(f"Syntax: Error de cierre de paréntesis (ln:{tokenLn}, col:{tokenCol})")
                
                else:

                    markedPar.append((RPLn,RPCol))

        elif (token == "rightParenthesis") and ((tokenCol,tokenLn) not in markedPar):

                errorMessages.append(f"Syntax: Error de cierre de paréntesis (ln:{tokenLn}, col:{tokenCol})")








                
