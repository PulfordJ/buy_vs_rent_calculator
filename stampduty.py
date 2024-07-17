def calculateSDLT(second_property, property_value):
    rates = [0.00, .05, 0.05, 0.10, 0.12]
    thresholds = [425000, 625000, 925000, 925000, 15000000]
    total_tax = 0
    remaining_taxable = property_value
    if second_property:
        rates = [rate + 0.03 for rate in rates]
    for i in range(len(thresholds) - 1, -1, -1):
        threshold = thresholds[i]
        rate = rates[i]
        if i != 0:
            lower_threshold = thresholds[i - 1]
            if lower_threshold >= remaining_taxable:
                continue
            threshold_taxable = remaining_taxable - lower_threshold
            remaining_taxable = lower_threshold
        else:
            threshold_taxable = remaining_taxable
        threshold_tax = threshold_taxable * rate
        total_tax += threshold_tax
    return total_tax