# For large queries

TOP_PERFORMERS = """
SELECT 'Department Top Performers' AS category, department.dept_name AS department, 
       CONCAT(employee.emp_firstName, ' ', employee.emp_lastName) AS employee_name, 
       performance.KPI_Achieved
FROM employee
INNER JOIN department ON employee.department_id = department.department_id
INNER JOIN performance ON employee.employee_id = performance.appraised_id
WHERE performance.date_Achieved >= '2022-01-01'
GROUP BY department.dept_name, employee.employee_id
HAVING performance.KPI_Achieved >= AVG(performance.KPI_Achieved)
UNION
SELECT 'Top Performers' AS category, 'N/A' AS department, 
       CONCAT(employee.emp_firstName, ' ', employee.emp_lastName) AS employee_name, 
       performance.KPI_Achieved
FROM employee
INNER JOIN performance ON employee.employee_id = performance.appraised_id
WHERE performance.date_Achieved >= '2022-01-01'
GROUP BY employee.employee_id
HAVING performance.KPI_Achieved >= AVG(performance.KPI_Achieved)
ORDER BY KPI_Achieved DESC;
"""


NUM_PROJ_DEP = """
SELECT department.dept_name AS department, COUNT(project.project_id) AS num_projects
FROM department
LEFT JOIN employee ON employee.department_id = department.department_id
LEFT JOIN project ON project.project_id = employee.employee_id
GROUP BY department.dept_name

UNION

SELECT 'Total' AS department, COUNT(project.project_id) AS num_projects
FROM project;
"""


MONEY_TO_INSTITUE = """
SELECT bank.institute_number, COUNT(transactions.transaction_id) AS num_transactions, SUM(transactions.net_pay) AS total_net_pay
FROM bank
LEFT JOIN employee ON employee.bank_id = bank.bank_id
LEFT JOIN transactions ON transactions.employee_id = employee.employee_id
GROUP BY bank.institute_number

UNION

SELECT bank.institute_number, 0 AS num_transactions, 0 AS total_net_pay
FROM bank
WHERE bank.bank_id NOT IN (SELECT DISTINCT bank_id FROM transactions);
"""

LB_1 = """
SELECT bank.institute_number, COUNT(transactions.transaction_id) AS num_transactions, SUM(transactions.net_pay) AS total_net_pay
FROM bank
LEFT JOIN employee ON employee.bank_id = bank.bank_id
LEFT JOIN transactions ON transactions.employee_id = employee.employee_id
GROUP BY bank.institute_number

MINUS

SELECT bank.institute_number, COUNT(transactions.transaction_id) AS num_transactions, SUM(transactions.net_pay) AS total_net_pay
FROM bank
JOIN transactions ON transactions.bank_id = bank.bank_id
GROUP BY bank.institute_number;
"""

LB_2 = """
SELECT employee_id, first_name, last_name
FROM employees
MINUS
SELECT employee_id, first_name, last_name
FROM bonus
JOIN employees ON employee_id = employees.id;
"""
