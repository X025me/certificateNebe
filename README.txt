1. install your virtual machine with Python version 3.8.12
2. after activating run "pip install -r requirement.txt" found inside app directory 
3. properly adjust database credentials inside '/app/__init__.py' file

4. run the following commands in order at the terminal 
    a. export FLASK_APP=app 
    b. flask db init
    c. flask db migrate
    d. flask db upgrade 
    NOTE:- If any error happens during the init or migrations process it means your database
             connection is not properly configured
4.import the pole.xlsx file in the project to mssql db 
    NOTE: make sure the attributes are exactly like in the __init__.py Workers class

