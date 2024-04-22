def calculate_rent(first_month_rent, subsequent_month_rent, num_of_months):
    total_rent = 0
    deposit = first_month_rent
    for month in range(1, num_of_months + 1):
        if month == 1:
            total_rent += first_month_rent
        else:
            total_rent += subsequent_month_rent
    total_rent += deposit
    return total_rent