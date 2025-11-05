"""
Mini Project: Text-Based Adventure Game

An interactive story game where your choices determine the outcome.
Demonstrates control flow, conditionals, loops, and user input.
"""

import random
import time


# ============================================
# Game Functions
# ============================================

def print_slow(text, delay=0.03):
    """Print text with typewriter effect."""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()


def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(text.center(70))
    print("=" * 70 + "\n")


def get_choice(options):
    """
    Get player's choice from a list of options.
    Returns the choice number (1-indexed).
    """
    while True:
        try:
            choice = int(input("\nYour choice (number): "))
            if 1 <= choice <= len(options):
                return choice
            else:
                print(f"❌ Please enter a number between 1 and {len(options)}")
        except ValueError:
            print("❌ Please enter a valid number")


# ============================================
# Game Scenes
# ============================================

def intro():
    """Introduction scene."""
    print_header("🗡️  THE MYSTERIOUS CAVE  🗡️")
    
    print_slow("You are a brave adventurer seeking treasure in the legendary Cave of Wonders.")
    time.sleep(0.5)
    print_slow("Armed with only a torch and your wit, you stand at the cave entrance...")
    time.sleep(0.5)
    print()
    
    name = input("What is your name, adventurer? ")
    print_slow(f"\nWelcome, {name}! Your adventure begins now...\n")
    time.sleep(1)
    
    return name


def scene_entrance(player_name):
    """Cave entrance scene."""
    print_header("📍 CAVE ENTRANCE")
    
    print_slow("You enter the dark cave. Your torch flickers, casting dancing shadows on the walls.")
    print_slow("Ahead, you see three tunnels:")
    print()
    
    print("1. 🌟 A bright tunnel with golden light")
    print("2. 💧 A damp tunnel with the sound of dripping water")
    print("3. 🌪️  A windy tunnel with cold air rushing out")
    
    choice = get_choice([1, 2, 3])
    
    if choice == 1:
        return scene_golden_tunnel(player_name)
    elif choice == 2:
        return scene_water_tunnel(player_name)
    else:
        return scene_windy_tunnel(player_name)


def scene_golden_tunnel(player_name):
    """Golden tunnel scene."""
    print_header("🌟 GOLDEN TUNNEL")
    
    print_slow("You follow the golden light deeper into the cave...")
    time.sleep(0.5)
    print_slow("The tunnel opens into a magnificent chamber filled with treasure!")
    print_slow("But wait! A DRAGON is sleeping on the pile of gold! 🐉")
    print()
    
    print("What do you do?")
    print("1. 🤫 Try to sneak past the dragon")
    print("2. ⚔️  Challenge the dragon to battle")
    print("3. 🎵 Sing a lullaby to keep it asleep")
    print("4. 🏃 Run away quietly")
    
    choice = get_choice([1, 2, 3, 4])
    
    if choice == 1:
        # Sneak attempt - random outcome
        luck = random.randint(1, 100)
        if luck > 50:
            print_slow("\n✅ You successfully sneak past the dragon and grab some treasure!")
            return "victory"
        else:
            print_slow("\n❌ The dragon wakes up! You barely escape with your life!")
            return "escape"
    
    elif choice == 2:
        print_slow("\n❌ The dragon wakes up and defeats you easily. Game Over!")
        return "defeat"
    
    elif choice == 3:
        print_slow("\n✅ Your lullaby works! The dragon stays asleep.")
        print_slow("You collect treasure and leave safely!")
        return "victory"
    
    else:
        print_slow("\n🏃 You wisely retreat. Better safe than sorry!")
        return "retreat"


def scene_water_tunnel(player_name):
    """Water tunnel scene."""
    print_header("💧 WATER TUNNEL")
    
    print_slow("You wade through the damp tunnel, water dripping from the ceiling...")
    time.sleep(0.5)
    print_slow("You discover an underground lake with a mysterious island in the center.")
    print_slow("On the island, you see a glowing chest! 💎")
    print()
    
    print("How will you reach the island?")
    print("1. 🏊 Swim across the lake")
    print("2. 🚶 Look for a way around")
    print("3. 🧱 Build a raft from nearby debris")
    
    choice = get_choice([1, 2, 3])
    
    if choice == 1:
        print_slow("\n❌ The water is freezing cold! You turn back.")
        return "retreat"
    
    elif choice == 2:
        print_slow("\n✅ You find stepping stones hidden beneath the water!")
        print_slow("You reach the island safely and claim the treasure!")
        return "victory"
    
    else:
        print_slow("\n✅ You build a sturdy raft and paddle to the island.")
        print_slow("The chest contains ancient gold coins!")
        return "victory"


def scene_windy_tunnel(player_name):
    """Windy tunnel scene."""
    print_header("🌪️  WINDY TUNNEL")
    
    print_slow("The cold wind grows stronger as you proceed...")
    time.sleep(0.5)
    print_slow("You find yourself in a chamber with three magical doors.")
    print_slow("Each door has an inscription:")
    print()
    
    print("1. 🔥 'Through fire and flame' (Red Door)")
    print("2. ❄️  'Frozen in time' (Blue Door)")
    print("3. ⚡ 'Strike like lightning' (Yellow Door)")
    
    choice = get_choice([1, 2, 3])
    
    # Puzzle: The correct answer is the Blue Door (middle way)
    if choice == 1:
        print_slow("\n❌ Flames burst out! You retreat quickly!")
        return "retreat"
    
    elif choice == 2:
        print_slow("\n✅ The door opens to reveal a chamber of ice crystals!")
        print_slow("In the center is a frozen treasure chest.")
        print_slow("You carefully chip away the ice and claim the treasure!")
        return "victory"
    
    else:
        print_slow("\n⚡ Lightning strikes! You're thrown backward!")
        print_slow("Shaken but alive, you decide to leave.")
        return "escape"


def ending(result, player_name):
    """Display ending based on result."""
    print_header("🏁 THE END")
    
    if result == "victory":
        print_slow(f"🎉 Congratulations, {player_name}!")
        print_slow("You have successfully claimed the treasure of the Cave of Wonders!")
        print_slow("Your name will be remembered in legends!")
        print_slow("\n💰 Final Score: 100/100")
    
    elif result == "escape":
        print_slow(f"😅 {player_name}, you escaped with your life!")
        print_slow("Sometimes survival is the greatest victory.")
        print_slow("You live to adventure another day!")
        print_slow("\n💰 Final Score: 60/100")
    
    elif result == "retreat":
        print_slow(f"🚶 {player_name}, you chose caution over treasure.")
        print_slow("Wisdom is knowing when to retreat.")
        print_slow("Perhaps you'll return better prepared!")
        print_slow("\n💰 Final Score: 40/100")
    
    else:  # defeat
        print_slow(f"💀 {player_name}, your adventure ends here...")
        print_slow("But brave adventurers never truly die—they respawn!")
        print_slow("\n💰 Final Score: 20/100")
    
    print()


# ============================================
# Main Game Loop
# ============================================

def play_game():
    """Main game function."""
    
    # Introduction
    player_name = intro()
    
    # Main game
    result = scene_entrance(player_name)
    
    # Ending
    ending(result, player_name)
    
    # Play again?
    return play_again()


def play_again():
    """Ask if player wants to play again."""
    print("\n" + "=" * 70)
    choice = input("Would you like to play again? (yes/no): ").lower()
    return choice in ['yes', 'y']


# ============================================
# Game Statistics (Bonus Feature)
# ============================================

def play_with_stats():
    """Play game with statistics tracking."""
    
    games_played = 0
    victories = 0
    
    print_header("🎮 ADVENTURE GAME - STATS MODE")
    
    keep_playing = True
    
    while keep_playing:
        games_played += 1
        print(f"\n📊 Game #{games_played}")
        
        # Play the game
        player_name = intro()
        result = scene_entrance(player_name)
        
        if result == "victory":
            victories += 1
        
        ending(result, player_name)
        
        # Show stats
        win_rate = (victories / games_played * 100) if games_played > 0 else 0
        print(f"\n📈 Your Stats:")
        print(f"   Games Played: {games_played}")
        print(f"   Victories: {victories}")
        print(f"   Win Rate: {win_rate:.1f}%")
        
        # Play again?
        keep_playing = play_again()
    
    print("\n👋 Thanks for playing! Adventure awaits again soon!")


# ============================================
# Run the game
# ============================================

if __name__ == "__main__":
    # Choose game mode
    print("=" * 70)
    print("🎮 TEXT-BASED ADVENTURE GAME".center(70))
    print("=" * 70)
    print("\nChoose mode:")
    print("1. Normal Mode")
    print("2. Stats Mode (track your performance)")
    
    mode = get_choice([1, 2])
    
    if mode == 1:
        # Normal mode
        keep_playing = True
        while keep_playing:
            keep_playing = play_game()
        
        print("\n👋 Thanks for playing! May your next adventure be legendary!")
    
    else:
        # Stats mode
        play_with_stats()
    
    print("\n" + "=" * 70)
    print("Game created as part of Python Learning Series".center(70))
    print("=" * 70 + "\n")
