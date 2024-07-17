import matplotlib.pyplot as plt
from calculator import buy_vs_rent_calculator
import pandas as pd
from matplotlib.ticker import ScalarFormatter

# Parameters
home_price = 395000  # Price of the home
down_payment = 80000  # Down payment
mortgage_rate = 0.0515  # Annual mortgage rate
home_insurance = 1200  # Annual home insurance
maintenance_costs = home_price * 0.01  # Annual maintenance costs
initial_rent = 2000  # Initial guess for monthly rent
rent_increase_rate = 0.0376  # Annual rent increase rate
investment_return_rate = 0.06  # Annual investment return rate, nominal (inflation must be included!)
property_price_growth_rate = 0.03  # Annual property price growth rate, nominal (inflation must be included!)
surveyor_fees = 3000  # One-off surveyor fees
ground_rent = 350  # Annual ground rent
service_charge = 3310  # Annual service charge
upfront_mortgage_fees = 999  # One-off upfront mortgage fees
inflation_rate = 0.02
down_payment_liquidation_average_tax=0.2

years = 5  # Number of years to compare

def find_intersection_rent(low, high, tolerance=0.01):
    while high - low > tolerance:
        mid_rent = (low + high) / 2
        result = buy_vs_rent_calculator(home_price, down_payment, mortgage_rate, home_insurance, maintenance_costs,
                                        mid_rent, rent_increase_rate, investment_return_rate, years,
                                        property_price_growth_rate, surveyor_fees, ground_rent, service_charge,
                                        upfront_mortgage_fees, inflation_rate, down_payment_liquidation_average_tax)
        if result["Total Buy Future Value"] > result["Total Rent Future Value"]:
            high = mid_rent
        else:
            low = mid_rent
    return mid_rent, result

# Binary search for the intersection point
low_rent = 0
high_rent = 10000
intersection_rent, final_result = find_intersection_rent(low_rent, high_rent)

# Plotting the results for the intersection rent
years_range = range(1, years + 1)
renting_savings_over_time = []
buying_savings_over_time = []

for year in years_range:
    result = buy_vs_rent_calculator(home_price, down_payment, mortgage_rate, home_insurance, maintenance_costs,
                                    intersection_rent, rent_increase_rate, investment_return_rate, year,
                                    property_price_growth_rate, surveyor_fees, ground_rent, service_charge,
                                    upfront_mortgage_fees, inflation_rate, down_payment_liquidation_average_tax)
    renting_savings_over_time.append(result["Total Rent Future Value"])
    buying_savings_over_time.append(result["Total Buy Future Value"])

# Convert the final result to a pandas DataFrame
df = pd.DataFrame(list(final_result.items()), columns=['Metric', 'Value'])

# Display the DataFrame as a table
print(df)

print(final_result)
print(f"Minimum rent to justify property price given parameters: {intersection_rent}")

# Plotting the results
plt.plot(years_range, renting_savings_over_time, label='Rent')
plt.plot(years_range, buying_savings_over_time, label='Buy')
plt.xlabel('Years')
plt.ylabel('Future Value')
plt.title('Buying vs Renting Future Values Over Time')
plt.legend()
plt.grid(True)



# Highlight the intersection point with a dashed vertical line
intersection_year = None
for i in range(len(years_range)):
    if buying_savings_over_time[i] >= renting_savings_over_time[i]:
        intersection_year = years_range[i]
        break

if intersection_year is not None:
    intersection_value = buying_savings_over_time[intersection_year - 1]
    plt.axvline(x=intersection_year, color='red', linestyle='--')
    plt.scatter(intersection_year, intersection_value, color='red')  # Highlight the intersection point
    plt.annotate(f'Year {intersection_year}', xy=(intersection_year, 0), xycoords='data', fontsize=12,
                 xytext=(30, 0), textcoords='offset points',
                 ha='center', color='red')

# Set y-axis to display whole numbers
plt.gca().yaxis.set_major_formatter(ScalarFormatter())
plt.ticklabel_format(style='plain', axis='y')

plt.show()
