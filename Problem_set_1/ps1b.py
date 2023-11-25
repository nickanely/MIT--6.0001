annual_salary = int(input("enter your annual salary: "))
portion_saved = float(input("enter your portion: "))
total_cost = int(input("what is value of your dream house: "))
semi_annual_raise = float(input("That is your semiannual salary raise: "))

current_savings = 0
monthly_salary = annual_salary/12
portion_down_payment = total_cost * 0.25
r = 0.04

i = 0
while current_savings < portion_down_payment:
    current_savings += portion_saved * monthly_salary + (current_savings * r /12)
    i+=1
    if i % 6 == 0:
        monthly_salary *= 1 + semi_annual_raise
print(i)