from stampduty import calculateSDLT


def buy_vs_rent_calculator(home_price, down_payment, mortgage_rate, home_insurance, maintenance_costs, rent,
                           rent_increase_rate, investment_return_rate, years, property_price_growth_rate, surveyor_fees,
                           ground_rent, service_charge, upfront_mortgage_fees, inflation_rate):
    # Initial calculations
    loan_amount = home_price - down_payment
    stamp_duty = calculateSDLT(False, home_price)
    one_off_costs = stamp_duty + surveyor_fees
    monthly_mortgage_rate = mortgage_rate / 12

    monthly_mortgage_payment = (loan_amount * monthly_mortgage_rate)

    # Total monthly costs for buying
    monthly_home_insurance = home_insurance / 12
    monthly_maintenance_costs = maintenance_costs / 12
    monthly_ground_rent = ground_rent / 12
    monthly_service_charge = service_charge / 12
    monthly_upfront_mortgage_fees = upfront_mortgage_fees / 12 / 5
    total_monthly_buying_expenses = monthly_home_insurance + monthly_maintenance_costs + monthly_ground_rent + monthly_service_charge
    total_monthly_buying_cost = monthly_mortgage_payment + total_monthly_buying_expenses

    def get_monthly_increase_multiplier(rate):
        return (1 + rate) ** (1 / 12)

    # Monthly multipliers for rent increase and investment return
    monthly_rent_increase_multiplier = get_monthly_increase_multiplier(rent_increase_rate)
    monthly_investment_return_multiplier = get_monthly_increase_multiplier(investment_return_rate)
    monthly_property_price_growth_multiplier = get_monthly_increase_multiplier(property_price_growth_rate)
    monthly_inflation_multipler = get_monthly_increase_multiplier(inflation_rate)

    # Initial total costs and savings
    total_renting_cost = 0
    total_buying_cost = 0
    future_value_rent_savings = 0
    future_value_buy_savings = 0
    future_property_value = home_price

    renting_savings = []
    buying_savings = []

    for month in range(years * 12):
        future_value_buy_savings *= monthly_investment_return_multiplier
        future_value_rent_savings *= monthly_investment_return_multiplier

        future_value_buy_savings += max(rent - total_monthly_buying_cost, 0)
        future_value_rent_savings += max(total_monthly_buying_cost - rent, 0)

        total_renting_cost += rent
        total_buying_cost += total_monthly_buying_cost

        rent *= monthly_rent_increase_multiplier
        future_property_value *= monthly_property_price_growth_multiplier
        total_monthly_buying_cost = monthly_mortgage_payment + total_monthly_buying_expenses * monthly_inflation_multipler

    # Future value of down payment if invested
    future_value_rent_initial_investment = (down_payment + one_off_costs) * (1 + investment_return_rate) ** years

    # Future property value after the given period
    future_property_value_after_years = future_property_value
    real_estate_agent_sell_fee = future_property_value_after_years * 0.03

    # Comparison
    total_rent_option_future_value = future_value_rent_savings + future_value_rent_initial_investment - total_renting_cost
    total_buy_option_future_value = future_value_buy_savings + (
                future_property_value_after_years - loan_amount) - total_buying_cost - one_off_costs - real_estate_agent_sell_fee

    if total_buy_option_future_value < total_rent_option_future_value:
        decision = "Renting is better than buying."
    else:
        decision = "Buying is better than renting."

    return {
        "Total Buying Cost": total_buying_cost,
        "Total Renting Cost": total_renting_cost,
        "Total Buy Future Value": total_buy_option_future_value,
        "Total Rent Future Value": total_rent_option_future_value,
        "Future Value of Investment": future_value_rent_initial_investment,
        "Future Value of Rent Savings": future_value_rent_savings,
        "Future Value of Buy Savings": future_value_buy_savings,
        "Future Property Value": future_property_value_after_years,
        "Current rent price": rent,
        "Monthly mortgage payment": monthly_mortgage_payment,
        "Total Monthly Buying Costs": total_monthly_buying_cost,
        "Difference": abs(total_buy_option_future_value - total_rent_option_future_value),
        "Decision": decision,
    }
