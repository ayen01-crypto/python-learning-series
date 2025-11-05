"""
Mini Project: Personal Finance Calculator

A comprehensive tool to track income, expenses, and calculate savings.
Demonstrates variables, data types, operators, and user input handling.
"""

# ============================================
# Personal Finance Calculator
# ============================================

def main():
    """Main finance calculator function."""
    
    # Display header
    print("=" * 70)
    print("💰  PERSONAL FINANCE CALCULATOR  💰".center(70))
    print("=" * 70)
    print()
    
    # Get user's financial information
    print("📊 Let's calculate your monthly financial summary!\n")
    
    # Income section
    print("💵 INCOME")
    print("-" * 40)
    salary = float(input("Monthly salary: $"))
    freelance = float(input("Freelance income: $"))
    other_income = float(input("Other income: $"))
    
    total_income = salary + freelance + other_income
    
    # Expenses section
    print("\n💳 EXPENSES")
    print("-" * 40)
    rent = float(input("Rent/Mortgage: $"))
    utilities = float(input("Utilities (electricity, water, etc.): $"))
    groceries = float(input("Groceries: $"))
    transportation = float(input("Transportation: $"))
    entertainment = float(input("Entertainment: $"))
    other_expenses = float(input("Other expenses: $"))
    
    total_expenses = rent + utilities + groceries + transportation + entertainment + other_expenses
    
    # Calculate savings
    monthly_savings = total_income - total_expenses
    savings_rate = (monthly_savings / total_income * 100) if total_income > 0 else 0
    
    # Display results
    print("\n" + "=" * 70)
    print("📈  FINANCIAL SUMMARY  📈".center(70))
    print("=" * 70)
    print()
    
    # Income breakdown
    print("💵 INCOME BREAKDOWN")
    print("-" * 70)
    print(f"  Salary:              ${salary:>12,.2f}")
    print(f"  Freelance:           ${freelance:>12,.2f}")
    print(f"  Other:               ${other_income:>12,.2f}")
    print(f"  {'-' * 40:>53}")
    print(f"  Total Income:        ${total_income:>12,.2f}")
    print()
    
    # Expense breakdown
    print("💳 EXPENSE BREAKDOWN")
    print("-" * 70)
    print(f"  Rent/Mortgage:       ${rent:>12,.2f}  ({rent/total_income*100:>5.1f}%)")
    print(f"  Utilities:           ${utilities:>12,.2f}  ({utilities/total_income*100:>5.1f}%)")
    print(f"  Groceries:           ${groceries:>12,.2f}  ({groceries/total_income*100:>5.1f}%)")
    print(f"  Transportation:      ${transportation:>12,.2f}  ({transportation/total_income*100:>5.1f}%)")
    print(f"  Entertainment:       ${entertainment:>12,.2f}  ({entertainment/total_income*100:>5.1f}%)")
    print(f"  Other:               ${other_expenses:>12,.2f}  ({other_expenses/total_income*100:>5.1f}%)")
    print(f"  {'-' * 40:>53}")
    print(f"  Total Expenses:      ${total_expenses:>12,.2f}")
    print()
    
    # Savings summary
    print("💰 SAVINGS SUMMARY")
    print("-" * 70)
    print(f"  Monthly Savings:     ${monthly_savings:>12,.2f}")
    print(f"  Savings Rate:        {savings_rate:>12.1f}%")
    print()
    
    # Projections
    yearly_savings = monthly_savings * 12
    five_year_savings = yearly_savings * 5
    
    print("📊 PROJECTIONS")
    print("-" * 70)
    print(f"  Yearly Savings:      ${yearly_savings:>12,.2f}")
    print(f"  5-Year Savings:      ${five_year_savings:>12,.2f}")
    print()
    
    # Financial advice
    print("💡 FINANCIAL ADVICE")
    print("-" * 70)
    
    if savings_rate >= 20:
        print("  ✅ Excellent! You're saving over 20% of your income.")
        print("  Keep up the great work!")
    elif savings_rate >= 10:
        print("  👍 Good job! You're saving 10-20% of your income.")
        print("  Try to increase this to 20% for better financial health.")
    elif savings_rate > 0:
        print("  ⚠️  Your savings rate is below 10%.")
        print("  Consider reducing expenses or increasing income.")
    else:
        print("  🚨 Warning! You're spending more than you earn.")
        print("  Immediate action needed to reduce expenses!")
    
    print()
    
    # Biggest expense category
    expenses_dict = {
        'Rent/Mortgage': rent,
        'Utilities': utilities,
        'Groceries': groceries,
        'Transportation': transportation,
        'Entertainment': entertainment,
        'Other': other_expenses
    }
    
    biggest_expense = max(expenses_dict.keys(), key=lambda k: expenses_dict[k])
    biggest_amount = expenses_dict[biggest_expense]
    
    print(f"  📌 Biggest expense: {biggest_expense} (${biggest_amount:,.2f})")
    print()
    
    # Savings goal calculator
    print("=" * 70)
    print("🎯  SAVINGS GOAL CALCULATOR  🎯".center(70))
    print("=" * 70)
    print()
    
    goal_amount = float(input("Enter your savings goal: $"))
    
    if monthly_savings > 0:
        months_to_goal = goal_amount / monthly_savings
        years_to_goal = months_to_goal / 12
        
        print(f"\n✨ To save ${goal_amount:,.2f}:")
        print(f"   It will take {int(months_to_goal)} months ({years_to_goal:.1f} years)")
        print(f"   at your current savings rate.")
    else:
        print(f"\n❌ Cannot reach goal with current savings rate.")
        print(f"   You need to save at least ${goal_amount/12:,.2f} per month")
        print(f"   to reach your goal in 1 year.")
    
    print()
    print("=" * 70)
    print("Thank you for using the Personal Finance Calculator! 💰")
    print("=" * 70)


# ============================================
# Bonus: Simple Budget Planner
# ============================================

def budget_planner():
    """
    Alternative version: Budget planning with the 50/30/20 rule.
    50% Needs, 30% Wants, 20% Savings
    """
    
    print("=" * 70)
    print("📋  50/30/20 BUDGET PLANNER  📋".center(70))
    print("=" * 70)
    print()
    print("The 50/30/20 rule suggests:")
    print("  • 50% for Needs (rent, utilities, groceries)")
    print("  • 30% for Wants (entertainment, dining out)")
    print("  • 20% for Savings and debt repayment")
    print()
    
    monthly_income = float(input("Enter your monthly after-tax income: $"))
    
    # Calculate recommended budget
    needs_budget = monthly_income * 0.50
    wants_budget = monthly_income * 0.30
    savings_budget = monthly_income * 0.20
    
    print("\n" + "=" * 70)
    print("RECOMMENDED BUDGET".center(70))
    print("=" * 70)
    print()
    print(f"  💼 Needs (50%):      ${needs_budget:>12,.2f}")
    print(f"  🎉 Wants (30%):      ${wants_budget:>12,.2f}")
    print(f"  💰 Savings (20%):    ${savings_budget:>12,.2f}")
    print()
    print("=" * 70)
    
    # Get actual spending
    print("\nNow enter your ACTUAL spending:\n")
    actual_needs = float(input("Actual spending on Needs: $"))
    actual_wants = float(input("Actual spending on Wants: $"))
    actual_savings = float(input("Actual Savings: $"))
    
    print("\n" + "=" * 70)
    print("COMPARISON".center(70))
    print("=" * 70)
    print()
    
    # Needs comparison
    needs_diff = actual_needs - needs_budget
    needs_status = "❌ Over" if needs_diff > 0 else "✅ Under"
    print(f"  Needs:    {needs_status} by ${abs(needs_diff):,.2f}")
    
    # Wants comparison
    wants_diff = actual_wants - wants_budget
    wants_status = "❌ Over" if wants_diff > 0 else "✅ Under"
    print(f"  Wants:    {wants_status} by ${abs(wants_diff):,.2f}")
    
    # Savings comparison
    savings_diff = actual_savings - savings_budget
    savings_status = "✅ Above" if savings_diff >= 0 else "❌ Below"
    print(f"  Savings:  {savings_status} by ${abs(savings_diff):,.2f}")
    
    print()
    print("=" * 70)


# ============================================
# Run the program
# ============================================

if __name__ == "__main__":
    # Run the main calculator
    main()
    
    # Option to run budget planner
    print("\n")
    use_planner = input("Would you like to try the 50/30/20 Budget Planner? (yes/no): ")
    
    if use_planner.lower() in ['yes', 'y']:
        print("\n" * 2)
        budget_planner()
    
    print("\n💡 Remember: Track your finances regularly for better control!")
    print("Happy budgeting! 🐍\n")
