import private
from db import database
from system import organization

# Connection Constants
HOST = private.HOST
USERNAME = "admin"
PASSWORD = private.PASSWORD
NAME = "cp363"
# UI Constants (TODO: make this unique to the organization (e.x. create organization, view employees etc)) <- Harri: Working on this
MENU = "Options:\n\t1. View all tables\n\t2. View tables entries\n\t3.Insert into table\n\t4. Exit"

# Testing Constants
SAMPLE_INSERT_VALUES = "INSERT INTO organizations(org_name,org_address,org_desc,org_netWorth,payment_cycle) VALUES(%s,%s,%s,%s,%s)"
SAMPLE_INSERT_VALUES = ['Dons','Random Street 21','Mid burger spot','100000000.0','2023-03-22']

# A connection is established and a cursor is created when the database handler object is initialized
db_handler = database(host=HOST, username=USERNAME, password=PASSWORD, name=NAME)

# Menu Constant Strings
ROOT_MENU = "Root Menu:\n1. Update Organization\n2. Create Organization\n3. Exit"
ORG_ROOT_MENU = "1. Manage Organization\n2. Manage Departments\n3. Manage Projects\n4. Manage Employees\n5. Manage Payroll\n6. Manage Bank\n7. Manage Performance\n8. Special Queries\n9. Exit/Back"
ORG_MENU = "1. Update Organization\n2. Delete Organization\n3. Exit/Back"
DEP_MENU = "1. View Departments\n2. Add Department\n3. Update Department\n4. Remove Department\n5. Exit/Back"
PROJ_MENU = "1. View Projects\n2. Add Project\n3. Update Project\n4. Remove Project\n5. Exit/Back"
EMP_MENU = "1. View Employees\n2. Add Employee\n3. Update Employee\n4. Remove Employee\n5. Exit/Back"
PAY_MENU = "1. View Payroll Entries\n2. Run Payroll\n3. Add Payroll Entry\n4. Edit Payroll Entry\n5. Remove Payroll Entry\n6. Exit/Back"
BANK_MENU = "1. View Bank Info\n2. Add Bank Info\n3. Edit Bank Info\n4. Remove Bank Info\n5. Exit/Back"
PERF_MENU = "1. View Evaluations\n2. Add Evaluation\n3. Remove Evaluation\n4. Exit/Back" # TODO: Create menu for performance and handle performance entries
SPEC_MENU = "1. View Managerial Employees\n2. Count of employees working on projects\n3. Employees with multiple evaluations\n4. Top Performers\n5. Projects By Departments\n6. Transactions Summary\n7. Exit/Back"

root_choice = 0 
while root_choice!=3:
    print(f'\n{ROOT_MENU}')
    root_choice = int(input("Please enter your selection: "))
    
    # Handle menu options and exit the program
    if root_choice==3: print("Exiting the program.")
    elif root_choice==1: # Load existing organization
        print("Organizations:")
        for org in db_handler.viewEntries("organizations",output=True): print(f'\t{org[2]}')
        org_name = input("Please enter a organization name:")
        org_obj = organization(db_handler,org_name)
    elif root_choice==2:  # Create a new organization
        # get values for creating the organization and create the required organization
        print("Please enter the following details for creating the organization")
        org_name = input("\tName: ")
        org_address = input("\tAddress: ")
        org_description = input("\tDescription: ")
        org_balance = float(input("\tBalance:"))
        org_payroll = input("\tPayroll Due:")
        org_obj = organization(db_handler,org_name, [org_name,org_address,org_description,org_balance,org_payroll])
    
    # Enter organiztion menu (if user did not select exit)
    if root_choice!=3:
        # Section of code related to handling the organization related functions
        print('\nHandling the following organization:')
        print(org_obj)

        # Entering organizations function menu loop
        org_choice = 0
        while org_choice!=9:
            print(f'\n{ORG_ROOT_MENU}')
            org_choice = int(input("Please enter your selection: "))

            if org_choice==9: print("Exiting the organization")
            
            # Handling Organization Related Function
            elif org_choice==1:
                org_root_choice = 0
                while org_root_choice!=3:
                    print(f'\n{ORG_MENU}')
                    org_root_choice = int(input("Please enter your selection: "))
                    if org_root_choice==3: print("Exiting the organization menu.")
                    elif org_root_choice==1: org_obj.update_organization({})

            # Handling Department Related Functions
            elif org_choice==2: 
                dep_choice = 0
                while dep_choice!=5:
                    print(f'\n{DEP_MENU}')
                    dep_choice = int(input("Please enter your selection: "))
                    if dep_choice==5: print("Exiting the department menu.")
                    elif dep_choice==1: org_obj.view_departments()
                    elif dep_choice==2: org_obj.add_department()
                    elif dep_choice==3: org_obj.update_department(None,{})
                    elif dep_choice==4: org_obj.remove_department()

            # Handling Project Related Functions
            elif org_choice==3:
                prj_choice = 0
                while prj_choice!=5:
                    print(f'\n{PROJ_MENU}')
                    prj_choice = int(input("Please enter your selection: "))
                    if prj_choice==5: print("Exiting the project menu.")
                    elif prj_choice==1: org_obj.view_projects()
                    elif prj_choice==2: org_obj.add_project()
                    elif prj_choice==3: org_obj.update_project(None,{})
                    elif prj_choice==4: org_obj.remove_project(None)

            # Handling Employee Related Functions
            elif org_choice==4:
                emp_choice = 0
                while emp_choice!=5:
                    print(f'\n{EMP_MENU}')
                    emp_choice=int(input("Please enter your selection: "))
                    if emp_choice==5: print("Exiting the employee menu.")
                    elif emp_choice==1: org_obj.view_employees()
                    elif emp_choice==2: org_obj.add_employee()
                    elif emp_choice==3: org_obj.update_employee()
                    elif emp_choice==4: org_obj.add_employee()

            # Handling Payroll Related Functions
            elif org_choice==5:
                payroll_choice = 0
                while payroll_choice!=6:
                    print(f'\n{PAY_MENU}')
                    payroll_choice=int(input("Please enter your selection: "))
                    if payroll_choice==6: print("Exiting the employee menu.")
                    elif payroll_choice==1: org_obj.view_payroll() 
                    elif payroll_choice==3: org_obj.add_payroll()
                    elif payroll_choice==5: org_obj.remove_payroll()

            # Handling Bank Related Functions
            elif org_choice==6:
                bank_choice = 0
                while bank_choice!=5:
                    print(f'\n{BANK_MENU}')
                    bank_choice=int(input("Please enter your selection: "))
                    if bank_choice==5: print("Exiting the employee menu.")
                    elif bank_choice==1: org_obj.view_bank()
                    elif bank_choice==2: org_obj.add_bank()
                    elif bank_choice==4: org_obj.remove_bank()

            # Handling Performance Evaluation Related Functions
            elif org_choice==7:
                perf_choice = 0
                while perf_choice!=4:
                    print(f'\n{PERF_MENU}')
                    perf_choice=int(input("Please enter your selection: "))
                    if perf_choice==4: print("Exiting the performance menu.")
                    elif perf_choice==1: org_obj.view_evaluations()
                    elif perf_choice==2: org_obj.add_evaluation()
                    elif perf_choice==3: org_obj.remove_evaluation()

            # Handling special queries
            elif org_choice==8:
                spec_choice = 0
                while spec_choice!=7:
                    print(f'\n{SPEC_MENU}')
                    spec_choice=int(input("Please enter your selection: "))
                    if spec_choice==7: print("Exiting the special menu.")
                    elif spec_choice==1: org_obj.view_managerial()
                    elif spec_choice==2: org_obj.count_working_in_progress()
                    elif spec_choice==3: org_obj.multiple_evals()
                    elif spec_choice==4: org_obj.top_performers()
                    elif spec_choice==5: org_obj.proj_per_dep()
                    elif spec_choice==6: org_obj.transactions_summary()

db_handler.exit()
