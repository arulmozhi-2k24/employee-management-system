import oracledb

connection = oracledb.connect(
    user="employee_app",
    password="EmployeeApp123",
    dsn="LAPTOP-P6KSQAQS:1522/WMS"
)

print("Employee App connected to Oracle successfully!")

cursor = connection.cursor()

cursor.execute("SELECT COUNT(*) FROM employees")

count = cursor.fetchone()[0]

print("Total Employees:", count)

cursor.close()
connection.close()