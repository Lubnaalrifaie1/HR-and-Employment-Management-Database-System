from db import database
import queries
# A component that handles the applications system (using the database component)
# TODO: finish methods marked by TODO (and modularize more if time permits)
# TODO: ADD ORG_ID TO TRANSACTIONS AND FILTER BY THAT
# TODO: Filter project and payroll by organization ID
# TODO: Filter bank details by org_id

def derive(values:dict): 
    return '=%s,'.join(values.keys())+'=%s', list(values.values())

# Employee object (Could be the parent for different employee types?)
class organization: # Could be the parent object for differnet organization types etc.
    def __init__(self, db_handler:database, name, values=[]):   
        self.db_handler:database = db_handler
        self.values = values
        self.name = name
        self.org_id = -1 # set after either loading, or creating

        if len(self.values)>0: # Since values were provided, enter the organization into the DB (via the db_handler)
            try:
                sql_command = f'INSERT INTO organizations(org_name,org_address,org_desc,org_netWorth,payment_cycle) VALUES(%s,%s,%s,%s,%s);'
                if not self.db_handler.insert(sql_command,values): raise Exception("Unable to insert values into the database.") # If insert function was not successful, raise an exception to alert the user
            except Exception as e: print("Failed to create the organization: ", e) # For handling all other exceptions/errors
        
        # find the location of the newly created (or existing) organization from the list of tuples and load the organizations details (incl. org_id)
        organizations = self.db_handler.viewEntries("organizations", output=True)
        location = [row[2] for row in organizations].index(self.name)
        self.values = organizations[location]

        # Store organization related data as variables 
        self.org_id = self.values[0]
        self.address = self.values[3]
        self.description = self.values[4]
        self.balance = self.values[5]
        self.payroll_due = self.values[6]
        return
    
    # Admin (organization operations)
    def reset_organization_variables(self): # Used internally after updates to the organization to change the instances variables
        values = self.db_handler.fetch(f'SELECT * FROM organizations WHERE organization_id={self.org_id}',output=True)[0]
        self.name = values[2]
        self.address = values[3]
        self.description = values[4]
        self.balance = values[5]
        self.payroll_due = values[6]
        return
    
    def update_organization(self, values:dict={}):
        if len(values)<=0: # get values from user and load them into the dict
            MENU = "\t1. Update Name\n\t2. Update Address\n\t3. Update Description\n\t4. Update Balance\n\t5. Exit/Back"
            choice = 0
            while choice!=5:
                print(MENU)
                choice = int(input("Please enter your selection: "))
                if choice==5: print("Exiting update organization menu.")
                if choice==1: values['org_name'] = input("Please enter the new name: ")
                if choice==2: values['org_address'] = input("Please enter the new address: ")
                if choice==3: values['org_desc'] = input("Please enter the new description: ")
                if choice==4: values['org_netWorth'] = input("Please enter the new net worth: ")

        # Derive the SQL command and use the insert/update function from the DB handler
        if len(values)>0:
            sql_section,values = derive(values)
            sql = f'UPDATE organizations SET {sql_section} WHERE organization_id={self.org_id}'
            if self.db_handler.insert(sql, values): print("Updated the current organization.")
            self.reset_organization_variables() # Reset the organization variables after the change so they are in sync with the DB
        
        return
    
    def remove_organization(self): # TODO Ensures cascade requirements are met (all details related to this org needs to be deleted)
        # Remove current organization and clear memory if required
        return

    # Department (completed)
    def view_departments(self):
        print("\tID Name Budget Description")
        for department in self.db_handler.fetch(f'SELECT * FROM {self.db_handler.name}.department WHERE organization_id={self.org_id};', output=True): print(f'\t{department[0]}. {department[2]} {department[4]} {department[3]}')
        return

    def add_department(self, values=[]):
        if len(values)<=0:
            name = input("\tName: ")
            description = input("\tDescription: ")
            budget = float(input("\tBudget: "))
            values = [name,description,budget, None, self.org_id]
        if self.db_handler.insert("INSERT INTO department(dept_name,dept_desc,dept_budget,manager_id,organization_id) VALUES (%s,%s,%s,%s,%s);",values): print("Created Department!")
        return
    
    def update_department(self, department_id=None, values:dict={}): 

        # Get department ID if it was not provided by the user (required for both user cases)
        if department_id==None:
            department_id = int(input("Please enter the department ID: "))

        if len(values)<=0: 
            MENU = "\t1. Update Manager\n\t2. Update Balance\n\t3. Exit/Back"
            choice = 0
            while choice!=3:
                print(MENU)
                choice = int(input("Please enter your selection: "))
                if choice==3: print("Exiting update department menu.")
                if choice==1: values["manager_id"] = int(input("Please enter the manager's employee ID: "))
                if choice==2: values["dept_budget"] = float(input("Please enter a new balance: "))

        # Derive the SQL command and use the insert/update function from the DB handler
        if len(values)>0:
            sql_section,values = derive(values)
            sql = f'UPDATE department SET {sql_section} WHERE department_id={department_id}'
            if self.db_handler.insert(sql, values): print("Updated the selected department.")

        return

    def remove_department(self,id=None):
        if id==None:
            id = int(input("Please enter the department (ID) you want to remove: "))
        if self.db_handler.delete(f'DELETE FROM department WHERE department_id={id}'): print("Removed project from table.")
        return

    # Project (completed)
    def view_projects(self):
        print("\tID Name Description")
        for project in self.db_handler.viewEntries("project", output=True): print(f'\t{project[0]}. {project[2]} {project[3]}')
        return

    def add_project(self, values=[]): 
        if len(values)<=0:
            name = input("\tName: ")
            description = input("\tDescription: ")
            date_created = input("\tDate Created: ")
            KPI_goal = input("\tKPI Goal: ")
            values = [name, description, date_created, KPI_goal]
        sql = "INSERT INTO project(prj_name,prj_desc,prj_date_created,KPI_goal) VALUES (%s,%s,%s,%s)"
        if self.db_handler.insert(sql,values): print("Created the project!")
        return
    
    def update_project(self, prj_id=None, values={}):
        if prj_id==None:
            prj_id = int(input("Please enter the project ID: "))
        
        if len(values)<=0: # If no values were provided, get them from the user via CLI
            MENU = "\t1. Update Name\n\t2. Update Description\n\t3. Update KPI Goal\n\t4. Exit/Back"
            update_project_choice = 0
            while update_project_choice!=4:
                print(MENU)
                update_project_choice = int(input("Please enter your selection: "))
                if update_project_choice==4: print("Exiting update project menu.")
                elif update_project_choice==1: values['prj_name'] = input("Please enter the new name: ")
                elif update_project_choice==2: values['prj_desc'] = input("Please enter the new description: ")
                elif update_project_choice==3: values['KPI_goal'] = input("Please enter the new KPI Goal: ")

        # Derive the SQL command and use the insert/update function from the DB handler
        if len(values)>0:
            sql_section,values = derive(values)
            sql = f'UPDATE project SET {sql_section} WHERE project_id={prj_id}'
            if self.db_handler.insert(sql, values): print("Updated the selected project.")

        return
    
    def remove_project(self, id=None):
        if id==None:
            id = int(input("Please enter the project (ID) you want to remove: "))
        if self.db_handler.delete(f'DELETE FROM project WHERE project_id={id}'): print("Removed project from table.")
        return

    # Payroll
    def view_payroll(self):
        print("\tID Date       bankID NetPay") # Filter by organization (to only show current organization's trasnactions) <- TODO: Need to update DB schema
        for row in self.db_handler.viewEntries("transactions", output=True): print(f'\t{row[0]}. {row[1]} {row[8]} {row[7]}') 
        return
    
    def add_payroll(self, values=[]):
        if len(values)<=0:
            print("Please enter the following information:")
            transaction_date = input("\tTransaction date: ")
            wage = input("\tWage: ")
            EI_pay = input("\tEI Pay: ")
            vacation_pay = input("\tVacation Pay: ")
            bonus_pay = input("\tBonus Pay: ")
            net_pay = input("\tNet Pay: ")
            employee_id = int(input("Employee ID: "))
            bank_id=int(input("Bank ID: "))
            values = [transaction_date, wage, EI_pay, vacation_pay, bonus_pay, net_pay, employee_id, bank_id]
        sql = "INSERT INTO transactions (transaction_date, wage, EI_pay, vacation_pay, bonus_pay, net_pay, employee_id, bank_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        if self.db_handler.insert(sql,values): print("Added the payroll!")
        return

    def edit_payroll(self): # TODO
        return

    def remove_payroll(self, id=None):
        if id==None: id=int(input("Please enter the payroll ID: "))
        if self.db_handler.delete(f'DELETE FROM transactions WHERE transaction_id={id}'): print("Removed payroll transaction from table.")
        return

    def run_payroll(self): # TODO Making Employee Payments (uses add payroll function to add transactions to the transactions table)
        return

    # Bank Details
    def view_bank(self): 
        print("\tID Account Number")
        for row in self.db_handler.viewEntries("bank", output=True): print(f'\t{row[0]}. {row[4]}')
        return

    def add_bank(self, values=[]): 
        if len(values)<=0:
            print("Please enter the following information:")
            institute_number = input("\tInstitute Number: ")
            transit_number = input("\tTransit Number: ")
            account_number = input("\tAccount Number: ")
            values = [institute_number, transit_number, account_number]
        sql = "INSERT INTO bank (institute_number, transit_number, account_number) VALUES (%s,%s,%s)"
        if self.db_handler.insert(sql,values): print("Added the bank!")
        return
    
    def update_bank(self): # TODO
        return

    def remove_bank(self, id=None):
        if id==None: id=int(input("Please enter the bank ID: "))
        if self.db_handler.delete(f'DELETE FROM bank WHERE bank_id={id}'): print("Removed entry from bank table.")
        return

    # HR (Employeee Management)
    def view_employees(self):
        print("\tID Firstname Lastname")
        for employee in self.db_handler.fetch(f'SELECT * FROM {self.db_handler.name}.employee WHERE organization_id={self.org_id};', output=True): print(f'\t{employee[0]}. {employee[2]} {employee[3]}')
        return

    def add_employee(self, values=[]): 
        if len(values)<=0: # ask for UI only if values are not provided as parameters
            # Get required inputs
            firstname = input("\tFirstname: ")
            lastname = input("\tLastname: ")
            address = input("\tAddress: ")
            phone = input("\tPhone: ")
            username = input("\tUsername: ")
            email = input("\tEmail: ")
            password = input("\tPassword: ")
            emp_type = input("\tType (full_time|part_time): ")

            # Get optional (and conditional) inputs
            if emp_type=="full_time":
                salary = input("\tSalary: ")
                hourly_wage = None
            else:
                hourly_wage = input("\tHourly Wage: ")
                salary = None
            
            department_id = int(input("\tDepartment ID: "))
            bank_id = input("\tBank ID (optional): ")
            bank_id = int(bank_id) if bank_id!="" else None

            # create list of values (required for SQL command/db handler func.)
            values = [firstname, lastname, address, phone, username, email, password, emp_type, hourly_wage, salary,self.org_id, department_id, bank_id]
        
        # insert employee to database
        if self.db_handler.insert("INSERT INTO employee(emp_firstName,emp_lastName, emp_address, emp_phone, emp_username,emp_email, emp_password,emp_type,emp_hourlyWage,emp_salary,organization_id,department_id,bank_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", values): print("Created Employee!")
        return

    def update_employee(self,values:dict={}): # TODO 
        # either take inputs as a dictionary or print the menu and get the values
        # update based on query created with values.keys() or by input from UI
        return

    def remove_employee(self, id=None):
        if id==None:
            id = int(input("Please enter the employee (ID) you want to remove: "))
        if self.db_handler.delete(f'DELETE FROM employee WHERE employee_id={id}'): print("Removed employee from table.")
        return
    
    # HR (Performance Evaluation)
    def view_evaluations(self):
        print("ID Date                 Notes    Appraised ID")
        for row in self.db_handler.viewEntries("performance", output=True): print(f'{row[0]}. {row[1]} {row[2]} {row[6]}')
        return

    def add_evaluation(self, values=[]):
        if len(values)<=0:
            print("Please enter the following information:")
            perf_notes = input("\Perf. Notes: ")
            date_Achieved = input("\tDate Achieved: ")
            KPI_Achieved = input("\tKPI Achieved: ")
            appraiser_id = input("\tAppraiser ID: ")
            appraised_id = input("\tAppraised ID: ")
            project_id = input("\tProject ID: ")
            values = [perf_notes, date_Achieved, KPI_Achieved,appraiser_id,appraised_id,project_id]
        sql = "INSERT INTO performance (perf_notes,date_Achieved,KPI_Achieved,appraiser_id,appraised_id,project_id) VALUES (%s,%s,%s,%s,%s,%s)"
        if self.db_handler.insert(sql,values): print("Added the evaluation!") 
        return

    def update_evaluation(self): # TODO
        return
    
    def remove_evaluation(self, id=None):
        if id==None:
            id = int(input("Please enter the performance ID you want to remove: "))
        if self.db_handler.delete(f'DELETE FROM performance WHERE performance_id={id}'): print("Removed selected evaluation from performance table.")
        return

    # Special Queries
    def view_managerial(self):
        print("List of employees with managerial status:")
        print("\tFull Name")
        sql = "select distinct emp_firstName, emp_lastName from employee where exists (select * from department where employee.employee_id = department.manager_id);"
        for row in self.db_handler.fetch(sql, output=True): print(f'\t{row[0]} {row[1]}')
        return

    def count_working_in_progress(self):
        sql = "select count(distinct appraised_id) from performance where exists (select * from employee where employee.employee_id = performance.appraised_id and perf_notes= 'in progress');"
        print(f'\tNumber of employees working in projects that are currently in progress: {self.db_handler.fetch(sql, output=True)[0][0]}')
        return

    def multiple_evals(self):
        sql = "select emp_firstName, count(performance.performance_id) as NoOfEvaluations from performance inner join employee on performance.appraised_id = employee.employee_id group by emp_firstName having count(performance.performance_id)>1;"
        rows = self.db_handler.fetch(sql, output=True)
        if len(rows)==0: print("No employee fits the criteria.")
        else: 
            print("First Name Count")
            for row in rows: print(f'\t{row[0]} {row[1]}')
        return
    
    def top_performers(self):
        print("\tCategory Department Employee Name KPI Achieved")
        for row in self.db_handler.fetch(queries.TOP_PERFORMERS, output=True): print(f'\t{row[0]} {row[1]} {row[2]} {row[3]}')
        return
    
    def proj_per_dep(self):
        print("\tDepartment Num Projects")
        for row in self.db_handler.fetch(queries.NUM_PROJ_DEP, output=True): print(f'\t{row[0]} {row[1]}')
        return
    
    def transactions_summary(self):
        print("\tInstitue# #Transactions Total Paid")
        for row in self.db_handler.fetch(queries.MONEY_TO_INSTITUE, output=True): print(f'\t{row[0]} {row[1]} {row[2]}')
        return

    # Special Queries (Lubna)
    def special_1(self):
        try: 
            for row in self.db_handler.fetch(queries.LB_1, output=True): print(f'\t{row[0]} {row[1]} {row[2]}')
        except: print("Failed to generate results. Please try again later.")
        return
    
    def special_2(self):
        try: 
            for row in self.db_handler.fetch(queries.LB_2, output=True): print(f'\t{row[0]} {row[1]} {row[2]}')
        except: print("Failed to generate results. Please try again later.")
        return

    # Misc.
    def __str__(self):
        return f'\tName: {self.name}\n\tAddress: {self.address}\n\tDesc: {self.description}\n\tBalance: {self.balance}\n\tPayroll: {self.payroll_due}'
