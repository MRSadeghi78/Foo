# PWP SPRING 2024
# Project Name: Foo
1. Install [Python](https://www.python.org/)
2. Clone the project from github
   ```
   git clone https://github.com/Damonmehrpour/Foo.git
   ```
4. Create virtual environment
   ```
   python -m venv venv
   ```
5. Activate the virtual environment
6. Install the libraries and dependencies
   ```
   pip install -r requirements.txt
   ```
7. Run the project using below command
```
uvicorn main:app
```

# Setting up database
Database setup has been integrated with on startup event of application. If you run the application it will automatically create the necessary tables. 
No extra action is required for setting up database.

# PyLint Checking

Run this command in the project folder or in the project's virtual environment
```
pylint *.py > pylint_report.txt
```

# Testing and Coverage
Run this command in the project folder or in the project's virtual environment
```
pytest -s --cov=.   
```

# Group information
* Student 1. Mahdi Mehrpour Moghadam mmehrpou23@student.oulu.fi
* Student 2. Mohamadreza Sadeghi msadeghi23@student.oulu.fi
* Student 3. Raisul Islam raisul.islam@student.oulu.fi
* Student 4. Nazmul Mahmud nazmul.mahmud@student.oulu.fi



