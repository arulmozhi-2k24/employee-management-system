from flask import Blueprint, render_template, request, redirect, url_for, session
from database import get_connection

main = Blueprint("main", __name__)


# =========================
# HOME
# =========================

@main.route("/")
def home():

    if "username" not in session:
        return redirect(url_for("main.login"))

    return redirect(url_for("main.dashboard"))


# =========================
# LOGIN
# =========================

@main.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT username, password_hash, role
            FROM users
            WHERE username = :username
        """, {
            "username": username
        })

        user = cursor.fetchone()

        cursor.close()
        connection.close()

        if user:

            session["username"] = user[0]
            session["role"] = user[2]

            return redirect(url_for("main.dashboard"))

        return render_template(
            "login.html",
            error="Invalid username or password"
        )

    return render_template("login.html")


# =========================
# LOGOUT
# =========================

@main.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("main.login"))


# =========================
# DASHBOARD
# =========================

@main.route("/dashboard")
def dashboard():

    if "username" not in session:
        return redirect(url_for("main.login"))

    connection = get_connection()
    cursor = connection.cursor()

    # Total employees
    cursor.execute("""
        SELECT COUNT(*)
        FROM employees
    """)

    total_employees = cursor.fetchone()[0]

    # Active employees
    cursor.execute("""
        SELECT COUNT(*)
        FROM employees
        WHERE status = 'ACTIVE'
    """)

    active_employees = cursor.fetchone()[0]

    # Inactive employees
    cursor.execute("""
        SELECT COUNT(*)
        FROM employees
        WHERE status = 'INACTIVE'
    """)

    inactive_employees = cursor.fetchone()[0]

    # Total salary
    cursor.execute("""
        SELECT NVL(SUM(salary), 0)
        FROM employees
    """)

    total_salary = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return render_template(
        "dashboard.html",
        total_employees=total_employees,
        active_employees=active_employees,
        inactive_employees=inactive_employees,
        total_salary=total_salary
    )


# =========================
# EMPLOYEE LIST
# =========================

@main.route("/employees")
def employees():

    if "username" not in session:
        return redirect(url_for("main.login"))

    search = request.args.get("search", "").strip()

    connection = get_connection()
    cursor = connection.cursor()

    if search:

        search_value = f"%{search}%"

        cursor.execute("""
            SELECT
                employee_id,
                first_name,
                last_name,
                email,
                phone,
                department,
                salary,
                joining_date,
                status
            FROM employees
            WHERE
                LOWER(first_name) LIKE LOWER(:search_value)
                OR LOWER(last_name) LIKE LOWER(:search_value)
                OR LOWER(email) LIKE LOWER(:search_value)
                OR LOWER(department) LIKE LOWER(:search_value)
            ORDER BY employee_id
        """, {
            "search_value": search_value
        })

    else:

        cursor.execute("""
            SELECT
                employee_id,
                first_name,
                last_name,
                email,
                phone,
                department,
                salary,
                joining_date,
                status
            FROM employees
            ORDER BY employee_id
        """)

    employees = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "employees.html",
        employees=employees,
        search=search
    )


# =========================
# ADD EMPLOYEE
# =========================

@main.route("/employees/add", methods=["GET", "POST"])
def add_employee():

    if "username" not in session:
        return redirect(url_for("main.login"))

    if request.method == "POST":

        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        phone = request.form["phone"]
        department = request.form["department"]
        salary = request.form["salary"]
        joining_date = request.form["joining_date"]
        status = request.form["status"]

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO employees
            (
                first_name,
                last_name,
                email,
                phone,
                department,
                salary,
                joining_date,
                status
            )
            VALUES
            (
                :first_name,
                :last_name,
                :email,
                :phone,
                :department,
                :salary,
                TO_DATE(:joining_date, 'YYYY-MM-DD'),
                :status
            )
        """, {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone": phone,
            "department": department,
            "salary": salary,
            "joining_date": joining_date,
            "status": status
        })

        connection.commit()

        cursor.close()
        connection.close()

        return redirect(url_for("main.employees"))

    return render_template("add_employee.html")


# =========================
# EDIT EMPLOYEE
# =========================

@main.route(
    "/employees/edit/<int:employee_id>",
    methods=["GET", "POST"]
)
def edit_employee(employee_id):

    if "username" not in session:
        return redirect(url_for("main.login"))

    connection = get_connection()
    cursor = connection.cursor()

    if request.method == "POST":

        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        phone = request.form["phone"]
        department = request.form["department"]
        salary = request.form["salary"]
        joining_date = request.form["joining_date"]
        status = request.form["status"]

        cursor.execute("""
            UPDATE employees
            SET
                first_name = :first_name,
                last_name = :last_name,
                email = :email,
                phone = :phone,
                department = :department,
                salary = :salary,
                joining_date = TO_DATE(:joining_date, 'YYYY-MM-DD'),
                status = :status
            WHERE employee_id = :employee_id
        """, {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone": phone,
            "department": department,
            "salary": salary,
            "joining_date": joining_date,
            "status": status,
            "employee_id": employee_id
        })

        connection.commit()

        cursor.close()
        connection.close()

        return redirect(url_for("main.employees"))

    cursor.execute("""
        SELECT
            employee_id,
            first_name,
            last_name,
            email,
            phone,
            department,
            salary,
            joining_date,
            status
        FROM employees
        WHERE employee_id = :employee_id
    """, {
        "employee_id": employee_id
    })

    employee = cursor.fetchone()

    cursor.close()
    connection.close()

    return render_template(
        "edit_employee.html",
        employee=employee
    )


# =========================
# DELETE EMPLOYEE
# =========================

@main.route("/employees/delete/<int:employee_id>")
def delete_employee(employee_id):

    if "username" not in session:
        return redirect(url_for("main.login"))

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM employees
        WHERE employee_id = :employee_id
    """, {
        "employee_id": employee_id
    })

    connection.commit()

    cursor.close()
    connection.close()

    return redirect(url_for("main.employees"))