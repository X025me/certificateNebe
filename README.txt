1. install your virtual machine with Python version 3.8.12
2. after activating Requirement.txt make sure to adjust the database Connection string to your credentials

3. run the following commands in order
    a. export FLASK_APP=app 
    b. flask db init
    c. flask db migrate
    d. flask db upgrade 
    NOTE:- If any error happens during the init or migrations process it means your database
             connection is not properly configered
4.import the pole.xlsx file in the project to mssql db 
    NOTE: make sure the attribues are exactly like in the __init__.py Workers class


option two
extract the zip file and skip section 1