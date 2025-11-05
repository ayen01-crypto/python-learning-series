"""
Weather Tracker Program
This program demonstrates the use of variables to track weather data.
"""

def main():
    """Main function to track weather information."""
    print("Weather Tracker")
    print("-" * 15)
    
    # Collect weather data using variables
    city = "New York"
    day1_temp = 75.5
    day2_temp = 78.2
    day3_temp = 73.8
    day4_temp = 80.1
    day5_temp = 77.6
    
    # Store weather conditions
    day1_condition = "Sunny"
    day2_condition = "Partly Cloudy"
    day3_condition = "Rainy"
    day4_condition = "Sunny"
    day5_condition = "Cloudy"
    
    # Calculate statistics
    average_temp = (day1_temp + day2_temp + day3_temp + day4_temp + day5_temp) / 5
    highest_temp = max(day1_temp, day2_temp, day3_temp, day4_temp, day5_temp)
    lowest_temp = min(day1_temp, day2_temp, day3_temp, day4_temp, day5_temp)
    
    # Display weather report
    print(f"Weather Report for {city}")
    print("=" * 30)
    print(f"Day 1: {day1_temp}°F - {day1_condition}")
    print(f"Day 2: {day2_temp}°F - {day2_condition}")
    print(f"Day 3: {day3_temp}°F - {day3_condition}")
    print(f"Day 4: {day4_temp}°F - {day4_condition}")
    print(f"Day 5: {day5_temp}°F - {day5_condition}")
    
    print("\nStatistics:")
    print("-" * 15)
    print(f"Average Temperature: {average_temp:.1f}°F")
    print(f"Highest Temperature: {highest_temp}°F")
    print(f"Lowest Temperature: {lowest_temp}°F")
    
    # Demonstrate variable reassignment
    print("\nUpdating forecast...")
    day6_temp = 82.3
    day6_condition = "Sunny"
    
    # Update average with new day
    new_average = (day1_temp + day2_temp + day3_temp + day4_temp + day5_temp + day6_temp) / 6
    print(f"Day 6: {day6_temp}°F - {day6_condition}")
    print(f"New Average Temperature: {new_average:.1f}°F")
    
    # Demonstrate string formatting with variables
    forecast_message = f"The weather in {city} has been variable this week, with temperatures ranging from {lowest_temp}°F to {highest_temp}°F."
    print(f"\nForecast Summary: {forecast_message}")

if __name__ == "__main__":
    main()