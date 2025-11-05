"""
Number Guessing Game
This program demonstrates control flow with loops and conditionals.
"""

import random

def main():
    """Main function to run the number guessing game."""
    print("Welcome to the Number Guessing Game!")
    print("I'm thinking of a number between 1 and 100.")
    
    # Generate a random number between 1 and 100
    secret_number = random.randint(1, 100)
    attempts = 0
    max_attempts = 7
    guess = None  # Initialize guess variable
    
    # Game loop
    while attempts < max_attempts:
        try:
            # Get user's guess
            guess = int(input(f"\nAttempt {attempts + 1}/{max_attempts}. Enter your guess: "))
            attempts += 1
            
            # Check the guess
            if guess < secret_number:
                print("Too low! Try a higher number.")
            elif guess > secret_number:
                print("Too high! Try a lower number.")
            else:
                print(f"Congratulations! You guessed the number {secret_number} in {attempts} attempts!")
                break
                
        except ValueError:
            print("Please enter a valid number.")
            attempts -= 1  # Don't count invalid input as an attempt
    
    # Check if player ran out of attempts
    if attempts >= max_attempts and guess != secret_number:
        print(f"\nSorry, you've run out of attempts. The number was {secret_number}.")
    
    # Ask if player wants to play again
    play_again = input("\nDo you want to play again? (yes/no): ").lower()
    if play_again == "yes":
        main()  # Restart the game
    else:
        print("Thanks for playing!")

if __name__ == "__main__":
    main()