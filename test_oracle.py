import oracledb

connection = oracledb.connect(
    user="employee_app",
    password="EmployeeApp123",
    dsn="LAPTOP-P6KSQAQS:1522/WMS"
)

print("Oracle Database Connected Successfully!")

connection.close()