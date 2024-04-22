class RentCalculator:
    def __init__(self, first_month_rent, subsequent_month_rent, num_of_months):
        self.first_month_rent = first_month_rent
        self.subsequent_month_rent = subsequent_month_rent
        self.num_of_months = num_of_months

    def calculate_rent(self):
        total_rent = 0
        deposit = self.first_month_rent
        for month in range(1, self.num_of_months + 1):
            if month == 1:
                total_rent += self.first_month_rent
            else:
                total_rent += self.subsequent_month_rent
            total_rent += deposit
        return total_rent


class PropertyTaxCalculator:
    def __init__(self, assessed_value, tax_rate):
        self.assessed_value = assessed_value
        self.tax_rate = tax_rate

    def calculate_property_tax(self):
        tax_rate_decimal = self.tax_rate / 100.0
        property_tax = self.assessed_value * tax_rate_decimal
        return property_tax
        
