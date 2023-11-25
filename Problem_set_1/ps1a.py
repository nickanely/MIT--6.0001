current_savings = 0
annual_salary = int(input("enter your annual salary: "))
portion_saved = float(input("enter your portion: "))
total_cost = int(input("what is value of your dream house: "))

portion_down_payment = total_cost * 0.25
r = 0.04

i = 0
while current_savings < portion_down_payment:
    current_savings += portion_saved * annual_salary / 12 + (current_savings * r / 12)
    i += 1
print(i)
