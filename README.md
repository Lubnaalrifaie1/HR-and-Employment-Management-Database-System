# Human-Resources-and-Employment-Management-Database-System
Conceptualized, designed, and executed a cutting-edge web-based employee management system with a focus on two integral components: employee payroll management and employee performance management.

## Introduction / System Overview:
This project revolves around designing and implementing an employee management system web application composed of two sub-components: employee payroll management and employee performance management. These sub-components and the system as whole assist organizations and companies in the processes of evaluating and tracking employee performance relative to a particular product or project and performing payroll-related activities (i.e., calculation of gross wages, deductions, net pay, and generating the pay stub). 
**To accommodate the time constraint imposed on this project, certain assumptions regarding the scope of the system's functionalities were made:**
- The performance of each employee is evaluated per project/product.
- KPIs will be based on the project/product type.
- Each employee will be paid bi-monthly.
- The payment cycle date is fixed and common for all employees in the organization. This assumption is valid as it reflects general accounting principles.
- Each employee will have a fixed wage.
## User Experience / User Interface:
To utilize the system's functionalities, users will have to initially register an organization in the web application and create departments. Following the latter, the superuser (the user who created the organization) can invite other users (i.e., employees) to join newly created departments. Certain departments, as well as users with the appropriate access level,
can create projects, set payroll details, and enter performance appraisal results into the system via forms in the web application. Additionally, the employees can also download their pay stubs or their appraisal results as a PDF.

# **Entities:**
To provide and support the functionalities discussed above, the employee
management system will be composed of the following entities:
1. Organisation: (Strong)
- Creating an organisation entity is the entry point to our system. It will contain
basic details about the organisation, such as the business registration and
payment cycle information. The attributes of this entity, such as the
payroll/payment cycle date, are important for the payroll management
functionalities as they determine when and how much each employee will
be paid.
2. Employee (Weak)
- This entity contains information about each employee of an organisation,
including the bank and wage details. This information will be available for
the employee themselves to be accessed when necessary.
3. Bank: (Weak)
- This entity contains the bank details (e.g., branch number, account number, and
bank name) of each employee. Although this entity is not accessed by any
other entity, its information is used in the computation and entry of records
into the payroll entity.
4. Payroll: (Weak)
- This entity consists of details such as the hours worked by an employee, their
gross pay, and any applicable deductions required for calculating their net
pay and generating the pay stub. The latter is made possible by this entity's
relationship with the employee and organisation entity.
5. Project_Performance: (Weak)
- Whenever an employee in the organisation has their performance evaluated,
the results are stored in this entity. This entity is dependent on information
from the employee and project entity. Users can access information from
this entity by viewing their performance results/evaluation.
6. Project: (Weak)
- This entity contains unique information about each product/project that is
being undertaken by the organisation and its employees. Additionally,
the evaluation of employees' performance is done using key performance
indicators (“KPIs”) relative to the product/projects category. It aids in
managing expectations from which employee appraisals will be entered
into the performance table according to each project or product ID.
7. Department: (Weak)
- This entity contains information regarding the different departments within the
organization, the number of employees per department, as well the
description, budget, and access scope of each department. Employees'
access levels are based on the department entity they are associated with.
8. Addressbook: (Weak)
- This entity contains information about the employee, and organizatin
address details. This includes various attributes such as their street, city,
province, etc.
9. Appraisal: (Weak)
- This entity contains information about the appraised project. The attributes
include, the organization, project, the appraiser and the employee who is
appraised.

# **Relationships:**
1. Employee → Department
a. A department can manage multiple employees.
b. One employee will be managed by one department (1:N relationship)
2. Employee → Position
a. An employee can have one position
b. Multiple Employees can have the same Position (1:N relationship)
3. Employee → Bank
a. Each employee has one bank ID
b. A single bank ID will belong to one employee (1:1 relationship).
4. Employee → Payroll
a. Each employee will be submitted to one payroll
b. One payroll will be submitted by one employee (1:1 relationship)
5. Employee → Project_Performance
a. Each employee can have multiple records in the performance entity (1:N
relationship)
b. One performance record can only belong to one employee ID (1:1
relationship)
6. Project_Performance→ Project
a. Each project will have multiple performance reports (one per employee) (1:N
relationship)
b. Each performance entity record will have one project associated with it.
Performance → Employee (1:1 relationship)
7. Organization → Payroll
a. Each organisation will be part of one payroll.
b. One payroll will be part of a single organisation (1:1 relationship)
8. Department → Project
a. One department controls many projects.
b. Many projects can be controlled by one department (1:N relationship)
