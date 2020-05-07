caseTypes = ["scissor", "rock", "paper"]

# Start of Answer
import random

def GenerateRandomCaseForComputer():
    R = random.randrange(0, 2)
    return caseTypes[R]

def MakeDecision(a,b):
    if (a == "scissor") or (a=="rock") or (a=="paper"):
        if len(a)!=len(b):
            if len(a) == 4:
                if len(b) == 5:
                    return "Computer"
                else:
                    return "User"
            elif len(a) == 5:
                if len(b) == 4:
                    return "User"
                else:
                    return "Computer"
            else:
                if len(b) == 4:
                    return "Computer"
                else:
                    return "User"
        else:
            return "Tie"
    else:
        return -1
# End of Answer

# Below is Execution Example, and can be removed.

userInput = 0
while True:
    userInput = int(input("\nMenu: \n[0] scissor, \n[1] rock, \n[2] paper, \n[3] quit \n\nSelect: "))
    if(userInput != 3):
        valueUser = caseTypes[userInput]
        valueComputer = GenerateRandomCaseForComputer()
        valueDecision = MakeDecision(valueUser, valueComputer)
        print("\nResult: User [{0}] vs Computer [{1}] -> Winner is {2}".format(valueUser, valueComputer, valueDecision))
    else:
        break
