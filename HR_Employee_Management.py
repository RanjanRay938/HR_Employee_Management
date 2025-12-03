"""
HR Employee Management System
Features:
- Three employee types using inheritance: FullTime, PartTime, Intern
- Polymorphic calculate_salary() method implemented differently for each type
- Employee details stored as dictionaries inside each object and in a central registry
- Bonus rules applied differently per employee type
- Save and load employee records to/from CSV for persistence

"""

import csv
import os
from datetime import date


class Employee:
    """Base class for all employees.

    - Stores employee attributes in a dictionary `self.data` for easy serialization.
    - Provides an interface method calculate_salary() to be overridden by subclasses.
    """

    def __init__(self, emp_id, name, join_date, role='Employee'):
        # Core data dictionary that will contain all employee attributes
        self.data = {
            'emp_id': emp_id,
            'name': name,
            'join_date': join_date,  # YYYY-MM-DD string or date object
            'role': role
        }

    def calculate_salary(self):
        """Placeholder -- overridden by subclasses. Returns numeric salary amount."""
        raise NotImplementedError('Subclasses must implement calculate_salary()')

    def years_of_service(self):
        """Compute years of service (integer) from join_date to today."""
        jd = self.data['join_date']
        if isinstance(jd, str):
            y, m, d = jd.split('-')
            jd = date(int(y), int(m), int(d))
        today = date.today()
        return today.year - jd.year - ((today.month, today.day) < (jd.month, jd.day))

    def to_dict(self):
        """Return the data dictionary for saving/inspection. Subclasses may add keys."""
        return dict(self.data)


class FullTime(Employee):
    """Full-time employee with fixed monthly salary and annual bonus rules."""

    def __init__(self, emp_id, name, join_date, monthly_salary, role='Full-Time'):
        super().__init__(emp_id, name, join_date, role)
        # Store type-specific data in the dictionary
        self.data.update({
            'monthly_salary': monthly_salary,
            'bonus_percent': 0.05  # base 5% annual bonus
        })

    def calculate_salary(self, months=1, apply_bonus=False):
        """Calculate salary for a given number of months.

        - months: number of months to pay (default 1)
        - apply_bonus: if True, apply annual bonus pro-rated by years_of_service and company rules

        Bonus rules implemented here (example):
        - Base bonus percent stored in data['bonus_percent'] (5%)
        - For each full 3 years of service, add +1% to bonus, capped at +5% extra
        - Final bonus applies once when apply_bonus=True and is added to the total pay as a lump sum
        """
        base = self.data['monthly_salary'] * months

        if apply_bonus:
            years = self.years_of_service()
            extra = min((years // 3) * 0.01, 0.05)  # up to +5%
            bonus_rate = self.data['bonus_percent'] + extra
            bonus_amount = base * bonus_rate
            return round(base + bonus_amount, 2)

        return round(base, 2)


class PartTime(Employee):
    """Part-time employee paid hourly, may receive a small bonus based on hours worked."""

    def __init__(self, emp_id, name, join_date, hourly_rate, role='Part-Time'):
        super().__init__(emp_id, name, join_date, role)
        self.data.update({
            'hourly_rate': hourly_rate,
            'monthly_hours': 0  # will be set when calculating
        })

    def calculate_salary(self, hours_worked, apply_bonus=False):
        """Calculate pay based on hours worked.

        Bonus rules (example):
        - If hours_worked >= 80 in a month, give a performance bonus of 2% of earned pay.
        - If apply_bonus is True, include that bonus.
        """
        base = self.data['hourly_rate'] * hours_worked
        bonus_amount = 0
        if apply_bonus and hours_worked >= 80:
            bonus_amount = base * 0.02
        # store last computed hours for record
        self.data['monthly_hours'] = hours_worked
        return round(base + bonus_amount, 2)


class Intern(Employee):
    """Intern with a fixed stipend and no bonus, but may get a completion allowance."""

    def __init__(self, emp_id, name, join_date, stipend, role='Intern'):
        super().__init__(emp_id, name, join_date, role)
        self.data.update({
            'stipend': stipend,
            'completed': False  # track completion status
        })

    def calculate_salary(self, apply_completion_allowance=False):
        """Return stipend. If completed and apply_completion_allowance=True, add a small allowance."""
        base = self.data['stipend']
        allowance = 0
        if apply_completion_allowance and self.data.get('completed', False):
            allowance = 0.10 * base  # 10% completion allowance
        return round(base + allowance, 2)


class HRSystem:
    """Manages a registry of employees and supports persistence.

    - Stores employees in a dict keyed by emp_id, values are Employee objects.
    - Can save/load employee *data dictionaries* to CSV for persistence.
    """

    def __init__(self, storage_file='employees.csv'):
        self.employees = {}
        self.storage_file = storage_file
        self._load_from_file()

    def add_employee(self, employee_obj):
        """Add an Employee object to the registry. Overwrites if emp_id exists."""
        emp_id = employee_obj.data['emp_id']
        self.employees[emp_id] = employee_obj

    def remove_employee(self, emp_id):
        """Remove employee by id if present."""
        if emp_id in self.employees:
            del self.employees[emp_id]

    def get_employee(self, emp_id):
        return self.employees.get(emp_id)

    def list_employees(self):
        """Return list of data dictionaries for all employees."""
        return [emp.to_dict() for emp in self.employees.values()]

    def save_to_file(self):
        """Save the current registry to CSV using the dictionaries returned by to_dict().

        Note: We write a superset of keys to accommodate different employee types.
        """
        if not self.employees:
            return
        # Collect all keys
        all_keys = set()
        rows = []
        for emp in self.employees.values():
            d = emp.to_dict()
            all_keys.update(d.keys())
            rows.append(d)
        all_keys = sorted(all_keys)

        with open(self.storage_file, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=all_keys)
            writer.writeheader()
            for r in rows:
                writer.writerow(r)

    def _load_from_file(self):
        """Attempt to load employees from CSV and create Employee objects.

        This loader uses the 'role' field to decide which concrete subclass to instantiate.
        If file missing or malformed, we silently start empty.
        """
        if not os.path.exists(self.storage_file):
            return
        try:
            with open(self.storage_file, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    role = row.get('role', '')
                    emp_id = row.get('emp_id')
                    name = row.get('name')
                    join_date = row.get('join_date')
                    if role == 'Full-Time':
                        monthly_salary = float(row.get('monthly_salary', 0) or 0)
                        emp = FullTime(emp_id, name, join_date, monthly_salary)
                    elif role == 'Part-Time':
                        hourly = float(row.get('hourly_rate', 0) or 0)
                        emp = PartTime(emp_id, name, join_date, hourly)
                        # if monthly_hours present, restore it
                        mh = row.get('monthly_hours')
                        if mh:
                            emp.data['monthly_hours'] = float(mh)
                    elif role == 'Intern':
                        stipend = float(row.get('stipend', 0) or 0)
                        emp = Intern(emp_id, name, join_date, stipend)
                        if row.get('completed') in ('True', 'true', '1'):
                            emp.data['completed'] = True
                    else:
                        # unknown role -> generic Employee record
                        emp = Employee(emp_id, name, join_date, role=role)
                    # Update any extra fields from CSV into data dict
                    for k, v in row.items():
                        if k in ('emp_id', 'name', 'join_date', 'role'):
                            continue
                        # try to convert numeric fields
                        if v is None or v == '':
                            continue
                        try:
                            if '.' in v:
                                num = float(v)
                                emp.data[k] = num
                            else:
                                num = int(v)
                                emp.data[k] = num
                        except Exception:
                            emp.data[k] = v
                    self.employees[emp_id] = emp
        except Exception:
            # If loading fails, we don't want the whole program to crash — start fresh.
            self.employees = {}


# Example usage (this runs when file is executed directly)
if __name__ == '__main__':
    hr = HRSystem()

    # Example: if storage had nothing, add some demo employees
    if not hr.employees:
        e1 = FullTime('FT001', 'Alice kumar', '2018-06-15', monthly_salary=80000)
        e2 = PartTime('PT101', 'Bikash Singh', '2022-01-10', hourly_rate=500)
        e3 = Intern('IN900', 'Charu Rai', '2024-07-01', stipend=15000)
        e3.data['completed'] = True  # mark intern completed

        hr.add_employee(e1)
        hr.add_employee(e2)
        hr.add_employee(e3)
        hr.save_to_file()

    # Demonstrate polymorphic salary calculations
    print('\nEmployee Salaries (examples)')
    for emp in hr.employees.values():
        role = emp.data.get('role')
        print('-' * 40)
        print(f"ID: {emp.data.get('emp_id')} | Name: {emp.data.get('name')} | Role: {role}")
        if isinstance(emp, FullTime):
            print('Monthly pay (no bonus):', emp.calculate_salary())
            print('Yearly lump (3 months + bonus):', emp.calculate_salary(months=3, apply_bonus=True))
        elif isinstance(emp, PartTime):
            print('Pay for 90 hours (with possible bonus):', emp.calculate_salary(hours_worked=90, apply_bonus=True))
        elif isinstance(emp, Intern):
            print('Stipend:', emp.calculate_salary())
            print('Stipend with completion allowance:', emp.calculate_salary(apply_completion_allowance=True))
        else:
            print('Generic employee — no salary calculation available')

    print('\nSaved employee records to', hr.storage_file)
