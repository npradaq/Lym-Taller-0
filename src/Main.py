import Lexer
import Parser

def testFile():
    fileName = input("Ingrese el nombre del archivo que desea comprobar (en la carpeta ./data): ")
    openedFile = open(f"./data/{fileName}", "r")

    testReturn = True

    characters = []

    for line in openedFile:
        for character in line:
            characters.append(character)

    tokenDict = Lexer.tokenCreator(characters)
    errors = Parser.testSyntax(tokenDict)

    if len(errors) > 0:
        testReturn = False
        for error in errors:
            print(error)

    else:
        testReturn = True
        print("No se encontraron errores en el código")


    openedFile.close()

    return testReturn

    
testFile()