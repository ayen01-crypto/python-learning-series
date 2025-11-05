"""
Mini Project: Interactive Greeting Card Generator

This program creates a personalized greeting card based on user input.
It demonstrates basic Python concepts: input, output, and string manipulation.
"""

# ============================================
# Interactive Greeting Card Generator
# ============================================

def main():
    """Main function to run the greeting card generator."""
    
    # Display welcome banner
    print("=" * 60)
    print("🎉  PERSONALIZED GREETING CARD GENERATOR  🎉".center(60))
    print("=" * 60)
    print()
    
    # Gather user information
    print("Let's create your personalized greeting card!\n")
    
    recipient_name = input("👤 Recipient's name: ")
    occasion = input("🎊 Occasion (e.g., Birthday, Anniversary): ")
    sender_name = input("✍️  Your name: ")
    custom_message = input("💬 Your message: ")
    
    # Generate the greeting card
    print("\n" + "=" * 60)
    print("YOUR PERSONALIZED GREETING CARD".center(60))
    print("=" * 60)
    print()
    
    # Card header
    print("┏" + "━" * 58 + "┓")
    print("┃" + " " * 58 + "┃")
    print("┃" + f"Happy {occasion}!".center(58) + "┃")
    print("┃" + " " * 58 + "┃")
    print("┃" + f"Dear {recipient_name},".center(58) + "┃")
    print("┃" + " " * 58 + "┃")
    
    # Wrap message (simple version)
    if len(custom_message) <= 54:
        print("┃" + f"  {custom_message}".ljust(58) + "┃")
    else:
        # Split into two lines if too long
        mid = len(custom_message) // 2
        line1 = custom_message[:mid]
        line2 = custom_message[mid:]
        print("┃" + f"  {line1}".ljust(58) + "┃")
        print("┃" + f"  {line2}".ljust(58) + "┃")
    
    print("┃" + " " * 58 + "┃")
    print("┃" + f"With love,".rjust(56) + "  ┃")
    print("┃" + f"{sender_name}".rjust(56) + "  ┃")
    print("┃" + " " * 58 + "┃")
    print("┗" + "━" * 58 + "┛")
    print()
    
    # Decorative footer
    print("✨" * 30)
    print()
    print("🎁 Card generated successfully!")
    print("💡 Tip: You can copy and share this card!")
    print()


# ============================================
# Bonus Features (Uncomment to try!)
# ============================================

def colored_card():
    """
    Advanced version with more customization.
    Uncomment this function and call it instead of main() to try it!
    """
    
    print("=" * 60)
    print("🌟  ADVANCED GREETING CARD GENERATOR  🌟".center(60))
    print("=" * 60)
    print()
    
    recipient_name = input("👤 Recipient's name: ")
    occasion = input("🎊 Occasion: ")
    sender_name = input("✍️  Your name: ")
    
    # Choose card style
    print("\n📋 Choose a card style:")
    print("1. Classic")
    print("2. Modern")
    print("3. Minimalist")
    style = input("Enter choice (1-3): ")
    
    custom_message = input("💬 Your message: ")
    
    # Generate based on style
    print("\n" + "=" * 60)
    
    if style == "1":
        # Classic style
        print("╔" + "═" * 58 + "╗")
        print("║" + f" Happy {occasion}! ".center(58) + "║")
        print("╠" + "═" * 58 + "╣")
        print("║" + f" Dear {recipient_name}, ".ljust(58) + "║")
        print("║" + " " * 58 + "║")
        print("║" + f" {custom_message} ".ljust(58) + "║")
        print("║" + " " * 58 + "║")
        print("║" + f" - {sender_name} ".rjust(58) + "║")
        print("╚" + "═" * 58 + "╝")
    
    elif style == "2":
        # Modern style
        print("┌" + "─" * 58 + "┐")
        print("│" + f"🎉 {occasion.upper()} 🎉".center(58) + "│")
        print("├" + "─" * 58 + "┤")
        print("│" + " " * 58 + "│")
        print("│" + f"  @{recipient_name}".ljust(58) + "│")
        print("│" + f"  {custom_message}".ljust(58) + "│")
        print("│" + " " * 58 + "│")
        print("│" + f"  Sent by: {sender_name}".rjust(56) + "  │")
        print("└" + "─" * 58 + "┘")
    
    else:
        # Minimalist style
        print()
        print(f"  {occasion}".upper())
        print("  " + "-" * 50)
        print()
        print(f"  {recipient_name},")
        print()
        print(f"  {custom_message}")
        print()
        print(f"  — {sender_name}")
        print()
    
    print("\n✅ Your card is ready!")


# ============================================
# Run the program
# ============================================

if __name__ == "__main__":
    # Run the basic version
    main()
    
    # Want to try the advanced version?
    # Comment out main() above and uncomment the line below:
    # colored_card()
    
    # Ask if user wants to create another card
    print()
    another = input("Would you like to create another card? (yes/no): ")
    if another.lower() in ['yes', 'y']:
        print("\n" * 2)
        main()
    else:
        print("\n👋 Thank you for using Greeting Card Generator!")
        print("Happy coding! 🐍\n")
