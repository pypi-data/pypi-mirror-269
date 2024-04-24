class SalaryConverter:
    def __init__(self, annual_salary):
        self.annual_salary = annual_salary

    def convert_to_monthly(self):
        return self.annual_salary / 12