from database import get_connection


try:
    connection = get_connection()

    print("Database connection successful!")

    cursor = connection.cursor()

    cursor.execute("SELECT USER FROM DUAL")

    result = cursor.fetchone()

    print("Connected User:", result[0])

    cursor.close()
    connection.close()

except Exception as e:
    print("Database connection failed!")
    print("Error:", e)