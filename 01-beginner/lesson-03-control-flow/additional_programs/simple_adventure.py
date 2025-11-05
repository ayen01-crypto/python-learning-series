"""
Simple Adventure Game
This program demonstrates control flow with nested conditionals and loops.
"""

def main():
    """Main function to run the adventure game."""
    print("Welcome to the Simple Adventure Game!")
    print("You find yourself at the entrance of a mysterious cave.")
    
    # Game state variables
    has_torch = False
    has_treasure = False
    game_over = False
    
    # Main game loop
    while not game_over:
        print("\nWhat would you like to do?")
        print("1. Enter the cave")
        print("2. Look around")
        print("3. Go home")
        
        choice = input("Enter your choice (1-3): ")
        
        if choice == "1":
            print("\nYou enter the dark cave.")
            if has_torch:
                print("With your torch, you can see clearly.")
                print("You discover two paths:")
                print("A. Go left")
                print("B. Go right")
                
                path_choice = input("Which path do you take? (A/B): ").upper()
                
                if path_choice == "A":
                    print("You find a chest filled with gold!")
                    has_treasure = True
                    print("Congratulations! You found the treasure!")
                elif path_choice == "B":
                    print("You encounter a friendly dragon who gives you a magic gem.")
                    print("The dragon says: 'Take this gem for your journey.'")
                else:
                    print("Invalid choice. You stumble and exit the cave.")
            else:
                print("It's too dark to see anything. You should find a light source.")
                
        elif choice == "2":
            print("\nYou look around the area.")
            print("You see:")
            print("- A small cottage")
            print("- A stream")
            print("- Some rocks")
            
            print("\nWhat do you explore?")
            print("A. The cottage")
            print("B. The stream")
            print("C. The rocks")
            
            explore_choice = input("Enter your choice (A/B/C): ").upper()
            
            if explore_choice == "A":
                print("You find a torch inside the cottage!")
                has_torch = True
            elif explore_choice == "B":
                print("You find some pretty stones by the stream.")
            elif explore_choice == "C":
                print("Under a large rock, you find a map!")
                print("The map shows the way to hidden treasure.")
            else:
                print("You decide not to explore anything.")
                
        elif choice == "3":
            print("\nYou decide to go home.")
            if has_treasure:
                print("You return home with the treasure. Well done!")
            else:
                print("You return home safely, but empty-handed.")
            game_over = True
            
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
    
    print("\nThanks for playing the Simple Adventure Game!")

if __name__ == "__main__":
    main()