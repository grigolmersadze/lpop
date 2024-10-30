import json
import random
import colorama
import time
import os
from colorama import *

autoplay = False
displayFacts = True

def menu():
    score = displayScore()

    print(Fore.RED + r"""
.____   __________________ __________ 
|    |  \______   \_____  \\______   \
|    |   |     ___//   |   \|     ___/
|    |___|    |   /    |    \    |    
|_______ \____|   \_______  /____|    
        \/                \/          
""" + Fore.RESET)
    print(Fore.YELLOW + "LUCKIEST PERSON ON PLANET GAME - LPOP" + Fore.RESET + Fore.CYAN + " [Highest Score: " + str(score) + "]" + Fore.RESET)
    print("-------------------------------------")
    print("1. PLAY")
    print("2. HOW TO PLAY")
    print("3. SETTINGS")
    print("4. EXIT")

    while True:
        try:
            choice = int(input("Enter your choice: "))
            if choice == 1:
                chooseBoxes()
            elif choice == 2:
                how_to_play()
            elif choice == 3:
                options()
            elif choice == 4:
                exit()
            else:
                print(Fore.RED + "Invalid choice. Please try again." + Fore.RESET)
        except ValueError:
            print(Fore.RED + "Invalid input. Please enter an integer." + Fore.RESET)


def how_to_play():
    print("-------------------------------------")
    print(f"""
    How to play:

    There are 4 boxes to choose from.
    ┌───┐ ┌───┐ ┌───┐ ┌───┐
    │ {Fore.GREEN}1{Fore.RESET} │ │ {Fore.RED}2{Fore.RESET} │ │ {Fore.RED}3{Fore.RESET} │ │ {Fore.RED}4{Fore.RESET} │
    └───┘ └───┘ └───┘ └───┘

    3 of them are {Fore.RED}false{Fore.RESET}, 1 is {Fore.GREEN}true{Fore.RESET}.
    If you choose the correct box, you will advance to the {Fore.CYAN}next level.{Fore.RESET}
    If you choose the wrong box, you will {Fore.RED}lose{Fore.RESET}.
    
    In the end, you will see how lucky you were. (along with comparison facts)

    {Fore.YELLOW}Good luck!{Fore.RESET}
          
    Press {Fore.CYAN}1{Fore.RESET} to go back to the menu.
          """)
    choice = int(input("Enter your choice: "))
    if choice == 1:
        menu()
    else:
        print(Fore.RED + "Invalid choice. Please try again." + Fore.RESET)
        how_to_play()
    
def chooseBoxes():
    print(Fore.CYAN + "[==Choose quantity of boxes (2-6)==]" + Fore.RESET)
    boxQuantity = int(input("Enter your choice: "))
    if boxQuantity >= 2 and boxQuantity <= 6:
        luckyGame(boxQuantity)
    else:
        print(Fore.RED + "Invalid choice. Please try again." + Fore.RESET)
        return chooseBoxes()
    

def options():
    global autoplay, displayFacts
    print("-------------------------------------")
    print(Fore.LIGHTBLUE_EX + "[== SETTINGS ==]" + Fore.RESET)
    print("")
    if autoplay == False:
        print("1. Enable" + Fore.LIGHTMAGENTA_EX + " Autoplay " + Fore.RESET + "(RANDOM)")
    else:
        print("1. Disable" + Fore.LIGHTRED_EX + " Autoplay " + Fore.RESET + "(RANDOM)")

    if displayFacts == True:
        print("2. " + Fore.LIGHTRED_EX + "Disable" + Fore.RESET + " Fact Display")
    else:
        print("2. " + Fore.LIGHTMAGENTA_EX + "Enable" + Fore.RESET + " Fact Display")

    print("3. Type" + Fore.CYAN + " 0 " + Fore.RESET + "to exit options menu...")

    choice = int(input(Fore.BLUE + "Enter your choice: " + Fore.RESET))
    if choice == 1:
        if autoplay == False:
            autoplay = True
            print(Fore.GREEN + "Autoplay enabled." + Fore.RESET)
            menu()
        else:
            autoplay = False
            print(Fore.GREEN + "Autoplay disabled." + Fore.RESET)
            menu()
    elif choice == 2:
        if displayFacts == True:
            displayFacts = False
            print(Fore.GREEN + "Fact display disabled." + Fore.RESET)
            menu()
        else:
            displayFacts = True
            print(Fore.GREEN + "Fact display enabled." + Fore.RESET)
            menu()
    elif choice == 3:
        menu()
    else:
        print(Fore.RED + "Invalid choice. Please try again." + Fore.RESET)
        options()


def autoplayer(boxInt):
    guess = random.randint(1, boxInt)
    time.sleep(2)
    return guess

def checkForLuckFacts(probability_in_x):
    try:
        with open('facts.json', 'r') as f:
            facts = json.load(f)

        if str(probability_in_x) in facts:
            print(Fore.LIGHTMAGENTA_EX + "FACT: Your luck was equivalent to -> " + Fore.RESET + Fore.CYAN + facts[str(probability_in_x)] + Fore.RESET)
        else:
            print("No facts found for this probability.")
    except FileNotFoundError:
        print(Fore.RED + "Error: 'facts.json' file not found." + Fore.RESET)
    except json.JSONDecodeError:
        print(Fore.RED + "Error: 'facts.json' contains invalid JSON." + Fore.RESET)

def luckyGame(boxInt):
    level = 1

    boxes = ""
    for i in range(1, boxInt + 1):
        boxes += str(f"[{i}]")

    while True:
        print(Fore.LIGHTYELLOW_EX + f"\nLevel {level}: " + Fore.RESET + "Choose a box " + boxes + ".")
        
        true_box = random.randint(1, boxInt)

        if autoplay == True:
            guess = autoplayer(boxInt)
        else:
            guess = int(input(Fore.LIGHTBLUE_EX + "Your choice: " + Fore.RESET))
        
        if guess == true_box:
            print(Fore.LIGHTGREEN_EX + "You got lucky! Advancing to the next level." + Fore.RESET)
            level += 1
        elif guess == 0:
            menu()
        elif guess != true_box:
            cumulative_probability = (1/boxInt) ** (level - 1)

            if cumulative_probability > 0:
                probability_in_x = int(1 / cumulative_probability)
            else:
                probability_in_x = float('inf')

            print(Fore.RED + f"\nYou lost at level {level}." + Fore.RESET)
            print(f"Your luck was equivalent to 1 in {probability_in_x}.")
            checkScore(probability_in_x)

            if displayFacts == True:
                checkForLuckFacts(probability_in_x)
            print("-------------------------------------")
            print("""
            """)
            luckyGame(boxInt)
            
        else:
            print(Fore.RED + "Invalid choice. Please try again." + Fore.RESET)
            luckyGame(boxInt)


# High Score Handling

def updateScore(score):
    print(Fore.LIGHTGREEN_EX + "Saving new high score..." + Fore.RESET)
    with open("score.txt", "w") as file:
        file.write(str(score))

def displayScore():
    if not os.path.exists("score.txt") or os.stat("score.txt").st_size == 0:
        return 0
    with open("score.txt", "r") as file:
        score = int(file.read())
        return score

def checkScore(currentScore):
    if os.path.exists("score.txt") and os.stat("score.txt").st_size > 0:
        with open("score.txt", "r") as file:
            try:
                score = int(file.read())
            except ValueError:
                print("Error: Score in the file is not an integer. Resetting to 0.")
                score = 0
    else:
        score = 0

    if score < currentScore:
        updateScore(currentScore)


colorama.init()
menu()
