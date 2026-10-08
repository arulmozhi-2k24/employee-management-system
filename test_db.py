import os
import oracledb
from dotenv import load_dotenv

load_dotenv()

connection = oracledb.connect(
    user=os.getenv("employee_app"),
    password=os.getenv(" EmployeeApp123"),
    dsn=os.getenv("ORACLE_DSN")
)

print("Oracle Database Connected Successfully!")

connection.close()