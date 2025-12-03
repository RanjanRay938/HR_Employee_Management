# HR Employee Management System

A Python-based system for managing employee records in an organization, supporting different employee types (Full-Time, Part-Time, Intern), salary calculations, persistence via CSV, and extensibility for further HR features.

## Features

- **Employee Types via Inheritance**
  - `FullTime`: Monthly salary, annual bonus.
  - `PartTime`: Hourly rate, performance bonus.
  - `Intern`: Fixed stipend, completion allowance.
- **Polymorphic Salary Calculation:** 
  - Each employee type implements its own `calculate_salary()` method.
- **Central Registry:** 
  - All employees managed in `HRSystem`; stored as objects and as serializable dictionaries.
- **Bonus & Allowance Rules:** 
  - Customized per employee category.
- **Persistence Support:** 
  - Save/load employee records to/from CSV for data retention.
- **Extensible Data Model:** 
  - Easy to add more attributes or extend functionality.

## Usage

Clone the repository and run the main Python script:

```bash
python HR_Employee_Management.py
```

If no data file is found, it creates demo employee records and saves them to `employees.csv`.

### Example Output

<img width="1032" height="618" alt="image" src="https://github.com/user-attachments/assets/4642880f-f8aa-4104-a79f-fb77372c66cd" />


## File Structure

- `HR_Employee_Management.py`: Main logic, class definitions, demo code.
- `employees.csv`: CSV file for persistent employee storage (auto-generated).

## Classes Overview

- `Employee` (base): Common data dictionary, years of service, interface for salary calculation.
- `FullTime`: Implements monthly salary, dynamic bonuses based on tenure.
- `PartTime`: Implements hourly pay, bonus for high hours.
- `Intern`: Fixed stipend, optional completion allowance.
- `HRSystem`: Central registry, supports add/remove/list employees, CSV save/load.

## Extending the System

- Add more employee types (subclass `Employee`, implement required logic).
- Modify bonus or allowance calculation rules per organizational policy.
- Integrate with databases, web apps, or HR portals as needed.

## Requirements

- Python 3.x

## License

MIT License

---

**Note:** This is a demonstration and should be adapted to production HR systems with appropriate security and validation for sensitive data.
