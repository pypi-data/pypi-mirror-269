"""
Hello everyone, I am Prashant Bhatt, Class XII D of DPS Haldwani, batch 2024-25.
I made this game the odd eve game, a digitised version of hand cricket.
So I invite you all to this wonderful game of OddEve. So enjoy.
This is version 1.1.1 dated 20 April 2024 under MIT License
"""
ODDEVE_PICS = ["""
           .-.
           | |
           | |
           | |
    _.-.-.-| | 
   ; \\( \\    |
   |\\_)\\ \\   | 
   |    ) \\  |
   |   (    / 
    \\______/ """, """
       .-.
       | |    / )
       | |   / /
       | |  / /
    _.-| |_/ / 
   ; \\( \\    |
   |\\_)\\ \\   | 
   |    ) \\  |
   |   (    / 
    \\______/ """, """
      _.-.
    _| | | 
   | | | | 
   | | | | _ 
   | i ' i\\_|
   |      (_ |
   |      _| |
   |     ;   | 
   |        /
    \\______/ """, """
   .-.-.-.-.
   | | | | |
   | | | | |    
   | | | | |
   | | | | |
   |  ( \\  \\
   |   \\ \\  | 
   |    ) \\ |
   |   (   / 
    \\_____/ """, """
      _.-._
    _| | | |
   | | | | |
   | | | | |  __
   | i ' i | / /
   |       |/ /
   |       ' /
   |      ;  | 
   |        /
    \\______/ """, """
    _
   ( (
    \\=\\ 
   __\\_`-\\
  (____))( \\---
  (____)) _
   (____))
    (__))___/--- """
]

import random,time

def chance():
    """
    Simulates a toss by asking the user for their preference (odd or even)
    and then randomly choosing a number between 1 and 6 for the program.

    Returns:
        True if the user wins the toss (odd + program_number is even), False otherwise.
    """
    print("Here is the toss. Let's go!!!. Choose 'odd' or 'eve(even)'\n")
    time.sleep(1)
    user_oe=isplayerchance("odd","eve","o","e")
    prog=random.randint(1,6)
    user_tn=validnum()
    pic(user_tn, "your")
    pic(prog, "my")
    tot=prog+user_tn
    if not user_oe:
        if tot%2!=0:
            print("You won the toss.")
            return True
        else:
            print("I have won the toss")
            return False
    else:
        if tot%2==0:
            print("You have won the toss")
            return True
        else:
            print("I have won the toss")
            return False

def SuperOver():
    """
  Simulates a Super Over when both players are tied in Odd Even Cricket.

  This function plays an additional 6 "balls" with the following rules:
      - Batsman cannot get out during the Super Over.
      - Runs are added to the batsman's score for each turn.
      - Player batting first plays all 6 balls and sets a target.
      - Player batting second needs to score 1 run more than the target to win.
  """
    print("\nIt's a tie! Going to Super Over...")

  # Player batting first
    player_score = 0
    for i in range(6):
        print("Your turn:")
        player_number = validnum()
        print("Now my turn (bowling).")  # Simulate bowling for clarity
        program_number = random.randint(1, 6)
        pic(player_number, "Your")
        pic(program_number, "my")
        if player_number != program_number:
            player_score += player_number
            print(f"Your score: {player_score}")
        else:
            player_score += 0
            print(f"Your score: {player_score}")

  # Program batting second
    target_score = player_score + 1  # Program needs 1 more than Player's score
    program_score = 0
    for i in range(6):
        print(f"\nMy turn (target: {target_score}):")
        program_number = random.randint(1, 6)
        print("Now your turn (bowling).")  # Simulate bowling for clarity
        player_number = validnum()
        pic(player_number, "Your")
        pic(program_number, "my")
        if player_number != program_number:
            program_score += program_number
            print(f"My score: {program_score}")
            if program_score >= target_score:
                break   # Exit loop if Player 2 reaches or surpasses the target
        else:
            program_score += 0
            print(f"My score: {program_score}")

  # Determine winner based on scores
    if program_score > player_score:
        print(f"Sorry, User! I have won the Super Over and the match! My final score: {program_score}. Your final score: {player_score}. Better luck next time.")
    elif player_score > program_score:
        print(f"Congratulations! User! You won the Super Over and the match! Your final score: {player_score}. My final score: {program_score}. Keep it up. ")
    else:
        print("It's a tie even in the Super Over! We need another Super Over!")
    # Call SuperOver again for another tie-breaker
        SuperOver()
        
def iscompchance(odd,eve): #if comp won the toss
    """
    Stimulates the program decision if it won the toss.

    Args:
        odd: A string displayed as a prompt.
        eve: same as odd.

    Returns: boolean values True, False or integral values 0,1.
    """
    c=random.randint(0,1)
    if c==0:
        print("I will take", eve)
        return 1 
    else:
        print("I will take", odd)
        return 0

def isplayerchance(odd, eve, o, e):#if player won toss
    """
    Same as iscompchance function, except, it is for user.
    """
    print(odd,"or",eve)
    b=input()
    if b.lower().startswith(o):
        return 0
    elif b.lower().startswith(e):
        return 1
    else:
        return isplayerchance(odd, eve, o, e)

def pic(e, my):#print the pics corresponding to the runs
    """
    Prints the runs corresponding to the input given. 
    Gives the hand gesture of the corresponding number.
    
    Args:
        e: an integer representing the prompt by the user or the program.
        my: a string representing the player name.
    """
    print(my,"number is",e,end=" ")
    print(ODDEVE_PICS[e-1])

def validnum(message="Enter your number, between 1 to 6 : "):
    """
  Prompts the user for a valid number and returns it as an integer.

  Args:
      message: A string to display as a prompt to the user.

  Returns:
      An integer representing the valid number entered by the user.
  """
    while True:
        guess = input(message)
        if guess.isdigit() and 1 <= int(guess) <= 6:
            return int(guess)
    else:
        print("Invalid input. Please enter a number between 1 and 6.")

def gamelogic(d, point):#the main gamelogic which runs the game.
    """
  Runs the core game loop of Odd Even Cricket until the user quits.

  Returns: None
    """
    if d:
        print("my chance.")#comp. bat first
        time.sleep(1)
        e=random.randint(1,6)
        print("I have played my chance, Your turn.")
        time.sleep(1)
        f=validnum()
        pic(e, "my")
        pic(f, "your")
        if e==f:#its, out and the chasing starts
            target=point+1
            chase=0
            print(f"Oh, I got out, you need {target} runs to win \nYour batting.")
            while chase<target:#while runs are less than required runs keep going
                time.sleep(1)
                h=validnum()
                print("You have played your chance, my turn.")
                time.sleep(1)
                i=random.randint(1,6)
                pic(i, "my")
                pic(h, "your")
                if h==i:#batsman out before winning
                    if point==chase:#same point superover starts
                        tx=False
                        SuperOver()
                        break
                    else:
                        print(f"Sorry, User! I have won the match! by {point-chase} runs. My final score: {point}. Your final score: {chase}. Better luck next time.")
                        tx=False
                        break
                else:
                    chase+=h
                    print("target is", target)
                    print("Now you need",target-chase,"runs")
                    print("your score is", chase)
                    tx=True
            if tx:    
                print(f"Congratulation, you win, keep it up. My final score: {point}. Your final score: {chase}.")
                
        else:
            point+=e
            print("my score is", point)
            gamelogic(d, point)
            return point
    else:
        print("your chance.")
        time.sleep(1)
        e=validnum()    
        print("You have played your chance, my turn.")
        time.sleep(1)
        f=random.randint(1,6)
        pic(e, "your")
        pic(f, "my")
        if f==e:
            target=point+1
            chase=0
            print("Oh, you got out, I need", target, "runs to win \nMy batting")
            while chase<target:
                time.sleep(1)
                i=random.randint(1,6)
                print("I have played my chance, your turn.")
                time.sleep(1)
                h=validnum()
                pic(i, "my")
                pic(h, "your")
                if h==i:
                    if point==chase:
                        tx=False
                        SuperOver()
                        break
                    else:
                        print(f"Oh, I lost by {point-chase} runs. Congratulation!! Keep it up. My final score is {chase}. Your final score is {point}.")
                        tx=False
                        break
                else:
                    chase+=i
                    print("target is ",target)
                    print("Now I need",target-chase,"runs")
                    print("my score is", chase)
                    tx=True
            if tx:
                print(f"Sorry, User! I have won the match! My final score: {chase}. Your final score: {point}. Better luck next time.")

        else:
            point+=e
            print("your score is", point)
            gamelogic(d, point)
            return point

def rules():
    """
  Prints a detailed explanation of the rules of Odd Even hand Cricket.
    """
    print("\nWelcome to Odd Even Cricket!")
    print("\n**Gameplay:**")
    print(
        "- The game is played between two players: you and the program."
        "\n- Players take turns 'batting' and 'bowling' using finger gestures representing numbers between 1 and 6."
        "\n- To 'bat', a player chooses a number and reveals it with a finger gesture."
        "\n- To 'bowl', a player chooses a number and reveals it with a finger gesture."
        "\n- The batsman scores points equal to their chosen number during their turn."
        "\n- The batsman gets 'out' if their chosen number matches the bowler's number."
        "\n- You have only one wicket. i.e you can get out only one time."
    )

    print("\n**Winning Conditions:**")
    print(
        "- The player batting second, has to reach the target set by player batting first. If he succeed he win, else player batting first wins."
        "\n- If both players have the same score after their turns are exhausted, a Super Over is triggered."
        "\n- Target is +1 run made by player batting first."
    )

    print("\n**Super Over:**")
    print(
        "- A Super Over consists of 6 additional 'balls' for each player."
        "\n- The batsman cannot get out during the Super Over, but score don't get added if same both throws same number."
        "\n-  - If you bat first:"
        "\n      - You play all 6 balls and set a target score."
        "\n      - The program needs to score 1 run more than your score to win."
        "\n  - If the program bats first:"
        "\n      - It plays all 6 balls and sets a target score."
        "\n      - You need to score exactly or more then the target score to win, i.e. +1 run than the program score to win."
    )

    print("\n**Toss:**")
    print(
        "- A coin toss is simulated to determine who bats first."
        "\n- If you win the toss, you can choose to bat or bowl first."
        "\n- If the program wins the toss, it randomly decides whether to bat or bowl first."
    )

    print("\n**Program Decisions:**")
    print(
        "- The program randomly chooses a number between 1 and 6 when bowling/batting."
        "\n- The program randomly decides whether to bat or bowl first if it wins the toss."
    )

    print("\n**User Interaction:**")
    print(
        "- You will be prompted to enter your chosen number and confirm your preference (bat or bowl) if you win the toss."
        "\n- You can quit the game by entering 'q' after a match."
    )

    print("\n**Additional Notes:**")
    print(
        "- This program uses ASCII art representations of hand gestures to simulate the game."
        "\n- Scores for both players will be displayed throughout the game."
    )

    print("\nReady to play? Let's go!")
    
def game():#below is the preview image of the game.
    """
    The main gaim loop of the odd eve game
    """
    print("""
          __      __  __        __    ___  __       __   __   __       __         __
    |  | |   |   |   |  | |\\/| |       |  |  |     |  | |  \\ |  \\   / |   \\    / |
    |  | |-- |   |   |  | |  | |--     |  |  |     |  | |  | |  |  /  |--  \\  /  |--
    |/\\| |__ |__ |__ |__| |  | |__     |  |__|     |__| |__; |__; /   |__   \\/   |__
    """)
    v=input("Want to know about rules, if yes press y, else press any key to continue.\n")
    if v.lower().startswith("y"):
        rules()
    while True:#game starts.
        point=0
        d=chance()
        if not d:
            k=iscompchance("bowling", "batting")
            gamelogic(k, point)
        else:
            k=isplayerchance("batting","bowling","bat","bowl")
            gamelogic(k, point)

        q=input("To quit press q else press enter key: ")
        if q.lower().startswith("q"):
            break

game()
