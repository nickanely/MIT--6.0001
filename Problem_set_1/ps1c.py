annual_salary = float(input("Enter your starting annual salary: "))
total_cost = 1000000  # Cost of the house
semi_annual_raise = 0.07  # Semiannual raise
r = 0.04  # Annual return on investments
portion_down_payment = total_cost * 0.25  # Down payment required
target_months = 36  # Target number of months to save

# Bisection search
low_rate = 0
high_rate = 10000  # Represented as an integer to handle two decimal places

steps = 0

while True:
    rate = (low_rate + high_rate) / 20000  # Convert back to decimal
    current_savings = 0
    monthly_salary = annual_salary / 12

    for month in range(target_months):
        current_savings += rate * monthly_salary + (current_savings * r / 12)
        if month % 6 == 5:
            monthly_salary *= (1 + semi_annual_raise)

    if abs(current_savings - portion_down_payment) < 100:
        break
    elif current_savings < portion_down_payment:
        low_rate = int(rate * 10000) + 1
    else:
        high_rate = int(rate * 10000) - 1

    steps += 1

if rate < 1:
    print("Best savings rate:", round(rate, 4))
    print("Steps in bisection search:", steps)
else:
    print("It is not possible to save for the down payment in 36 months.")
