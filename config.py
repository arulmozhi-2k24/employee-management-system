import os
from dotenv import load_dotenv

load_dotenv()

ORACLE_USER = os.getenv("employee_app")
ORACLE_PASSWORD = os.getenv("EmployeeApp123")
ORACLE_DSN = os.getenv("ORACLE_DSN")