# TODO: Develop a console-based Rock Paper Scissors Lizard Spock game in Python 

# Game should be modular, allowing for easy updates or rule changes 

# Implement game rules: 

# - Scissors decapitate lizard 

# - Scissors cuts paper 

# - Paper covers rock 

# - Rock crushes lizard 

# - Lizard poisons Spock 

# - Spock smashes scissors 

# - Lizard eats paper 

# - Paper disproves Spock 

# - Spock vaporizes rock 

# - Rock crushes scissors 

# Include user input for selecting options and display game results 

 

import random 

 

# Define global variables 

# Define dictionary of game options 

game_options = { 

    1: "rock", 

    2: "paper", 

    3: "scissors", 

    4: "lizard", 

    5: "spock" 

} 

 

# Define dictionary of game rules 

game_rules = { 

    "rock": ["scissors", "lizard"], 

    "paper": ["rock", "spock"], 

    "scissors": ["paper", "lizard"], 

    "lizard": ["spock", "paper"], 

    "spock": ["rock", "scissors"] 

} 

 

# Define dictionary of game results 

game_results = { 

    "win": "You win!", 

    "lose": "You lose!", 

    "tie": "It's a tie!" 

} 

 

# Define function to get user input 
def get_user_input():
    prompt = "Enter your choice (number or name): "
    while True:
        user_input = input(prompt).strip()
        if not user_input:
            print("Invalid input. Please try again.")
            continue

        # Accept numeric selection
        if user_input.isdigit():
            choice_num = int(user_input)
            if choice_num in game_options:
                return game_options[choice_num]
            else:
                print("Invalid selection number. Please try again.")
                continue

        # Accept name (case-insensitive)
        user_choice = user_input.lower()
        if user_choice in game_options.values():
            return user_choice

        print("Invalid input. Please try again.")

 

# Define function to get computer input 

def get_computer_input(): 

    # Get computer input 

    computer_input = random.choice(list(game_options.values())) 

    # Return computer input 

    return computer_input 

 

# Define function to determine game results 

def get_game_results(user_input, computer_input): 

    # Determine game results 

    if user_input == computer_input: 

        game_result = game_results["tie"] 

    elif computer_input in game_rules[user_input]: 

        game_result = game_results["win"] 

    else: 

        game_result = game_results["lose"] 

    # Return game results 

    return game_result 

 

# Define function to display game results 

def display_game_results(game_result): 

    # Display game results 

    print(game_result) 

 

# Define main function 

def main(): 

    # Display welcome message 
    print("Welcome to Rock Paper Scissors Lizard Spock!") 

    # Display game options 
    print("Game options:") 
    for key, value in game_options.items(): 
        print(f"{key} - {value}") 

    # Get user input 
    user_input = get_user_input() 

    # Get computer input 
    computer_input = get_computer_input() 

    # Show computer's selection
    print(f"Computer chose: {computer_input}") 

    # Determine game results 
    game_result = get_game_results(user_input, computer_input) 

    # Display game results 
    display_game_results(game_result) 

# Call main function 

main() 

