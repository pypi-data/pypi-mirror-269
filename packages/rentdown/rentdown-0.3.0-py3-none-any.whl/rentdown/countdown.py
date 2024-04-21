from datetime import datetime, timedelta

class RentCounter:
    def __init__(self, pay_date, end_date):
        self.pay_date = pay_date
        self.end_date = end_date

    def calculate_remaining_time(self):
        """
        Calculate the remaining time until the rent payment deadline.

        Returns:
            timedelta: The remaining time until the payment deadline.
        """
        time_remaining = self.end_date - self.pay_date
        
        if time_remaining.days < 0:
            next_pay_date = self.pay_date.replace(year=self.pay_date.year + 1)
            time_remaining = self.end_date - next_pay_date
        return time_remaining