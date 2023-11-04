from D2.METRICSTICS.data_computation.data_analyzer import DataAnalyzer
from D2.METRICSTICS.data_computation.data_statistics import DataStatistics

# Input data as a list
data = []

# Prompt the user to enter data values
while True:
    value = input("Enter a data value (or 'done' to finish): ")
    if value.lower() == 'done':
        break
    try:
        data.append(float(value))
    except ValueError:
        print("Invalid input. Please enter a numeric value.")

# Check if the data list is not empty
if data:
    analyzer = DataAnalyzer(data)
    statistics = DataStatistics(data)

    # Display a menu for the user to select a metric
    while True:
        print("\nChoose a metric to compute:")
        print("1. Mean (μ)")
        print("2. Standard Deviation (σ)")
        print("3. Maximum")
        print("4. Minimum")
        print("5. Count")
        print("6. Total")
        print("7. Mean Absolute Deviation (MAD)")
        print("8. Mode")
        print("9. Exit")

        choice = input("Enter the number of your choice: ")

        if choice == '1':
            print(f"Mean (μ): {analyzer.mean()}")
        elif choice == '2':
            print(f"Standard Deviation (σ): {analyzer.standard_deviation()}")
        elif choice == '3':
            print(f"Maximum: {statistics.maximum()}")
        elif choice == '4':
            print(f"Minimum: {statistics.minimum()}")
        elif choice == '5':
            print(f"Count: {statistics.count()}")
        elif choice == '6':
            print(f"Total: {statistics.total()}")
        elif choice == '7':
            print(f"Mean Absolute Deviation (MAD): {statistics.mean_absolute_deviation()}")
        elif choice == '8':
            mode_values = statistics.mode()
            print(f"Mode: {', '.join(map(str, mode_values))}")
        elif choice == '9':
            break
        else:
            print("Invalid choice. Please select a valid option.")

else:
    print("No data entered. Exiting.")
