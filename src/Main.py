import Lexer
import Parser

file = open("./data/test.txt", "r")

characters = []

for line in file:
    for character in line:
        characters.append(character)

tokenDict = Lexer.tokenCreator(characters)
tokenList = tokenDict["tokens"]

#for i in characters:
#    print(i)

for i in tokenList:
    print(i)


file.close()