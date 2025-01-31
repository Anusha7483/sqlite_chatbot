from flask import Flask, render_template, request, jsonify
import sqlite3
import re


app = Flask(__name__)

# Function to process natural language queries
def process_query(user_query):
    conn = sqlite3.connect("chat_assistant.db")
    cursor = conn.cursor()

    user_query = user_query.lower().strip()
    response = "Sorry, I didn't understand that query."

    # Extract relevant information using regex patterns
    hired_after_match = re.search(r"hired after(?: the)?\s+(\d{4}-\d{2}-\d{2})", user_query)

    employees_match = re.search(r"employees(?: in| of| from| for)?(?: the)?\s+(\w+)(?: department)?", user_query)
    manager_match = re.search(r"manager of(?: the)?\s+(\w+)(?: department)?", user_query)
    salary_match = re.search(r"total salary expense for(?: the)?\s+(\w+)(?: department)?", user_query)

    all_departments_match = re.search(r"show all departments", user_query)
    all_employees_match = re.search(r"show all employees", user_query)
    employee_details_match = re.search(r"details of employee (\w+)", user_query)
    highest_salary_match = re.search(r"highest salary(?: in| for)?\s+([\w&\-\s]+)", user_query)
    lowest_salary_match = re.search(r"lowest salary(?: in| for)?\s+([\w&\-\s]+)", user_query)
    average_salary_match = re.search(r"average salary(?: in| for)?\s+([\w&\-\s]+)", user_query)

    
    #list all employees after specific date
    if  hired_after_match:

    
        
        hire_date = hired_after_match.group(1).strip()
        print(f"Extracted Date: '{hire_date}'")  # Debugging

        cursor.execute("SELECT Name FROM Employees WHERE DATE(Hire_Date) > DATE(?)", (hire_date,))
        result = cursor.fetchall()
        response = f"Employees hired after {hire_date}: " + ", ".join(row[0] for row in result) if result else "No employees hired after that date."

    # 2️. Show Department Manager
    elif manager_match:
        department = manager_match.group(1).strip()
        print(f"Extracted Department: '{department}'")  # Debugging

        cursor.execute("SELECT Manager FROM Departments WHERE LOWER(Name) = LOWER(?)", (department,))
        result = cursor.fetchone()
        response = f"The manager of {department.capitalize()} department is {result[0]}" if result else "Department not found."

    # 1.Show Employees in a Department
    elif employees_match:
        department = employees_match.group(1).strip()
        print(f"Extracted Department: '{department}'")  # Debugging

        cursor.execute("SELECT Name FROM Employees WHERE LOWER(Department) = LOWER(?)", (department,))
        result = cursor.fetchall()
        response = f"Employees in {department.capitalize()} department: " + ", ".join(row[0] for row in result) if result else "No employees found in that department."


    # 4️. Get Total Salary Expense for a Department
    elif salary_match:
        department = salary_match.group(1).strip()
        print(f"Extracted Department: '{department}'")  # Debugging

        cursor.execute("SELECT SUM(Salary) FROM Employees WHERE LOWER(Department) = LOWER(?)", (department,))
        result = cursor.fetchone()
        response = f"Total salary expense for {department.capitalize()} department: rs {result[0]}" if result[0] else "Departments not found."

    # 5️.Show All Departments
    elif all_departments_match:
        print("Fetching all departments...")  # Debugging

        cursor.execute("SELECT Name FROM Departments")
        result = cursor.fetchall()
        response = "Available departments: " + ", ".join(row[0] for row in result) if result else "No departments found."

    # 6️.Show All Employees
    elif all_employees_match:
        print("Fetching all employees...")  # Debugging

        cursor.execute("SELECT Name FROM Employees")
        result = cursor.fetchall()
        response = "List of employees: " + ", ".join(row[0] for row in result) if result else "No employees found."

    # 7️.Get Employee Details
    elif employee_details_match:
        employee_name = employee_details_match.group(1).strip()
        print(f"Extracted Employee: '{employee_name}'")  # Debugging

        cursor.execute("SELECT Name, Department, Salary, Hire_Date FROM Employees WHERE LOWER(Name) = LOWER(?)", (employee_name,))
        result = cursor.fetchone()
        response = f"Details of {employee_name.capitalize()}: Department - {result[1]}, Salary - ${result[2]}, Hired on {result[3]}" if result else "Employee not found."

    # 8️.Get Highest Salary in a Department
    elif highest_salary_match:
        department = highest_salary_match.group(1).strip()
        print(f"Extracted Department: '{department}'")  # Debugging

        cursor.execute("SELECT Name, MAX(Salary) FROM Employees WHERE LOWER(Department) = LOWER(?)", (department,))
        result = cursor.fetchone()
        response = f"Highest salary in {department.capitalize()}: {result[0]} with rs {result[1]}" if result[0] else "Department not found or no salary data."

    # 9️. Get Lowest Salary in a Department
    elif lowest_salary_match:
        department = lowest_salary_match.group(1).strip()
        print(f"Extracted Department: '{department}'")  # Debugging

        cursor.execute("SELECT Name, MIN(Salary) FROM Employees WHERE LOWER(Department) = LOWER(?)", (department,))
        result = cursor.fetchone()
        response = f"Lowest salary in {department.capitalize()}: {result[0]} with rs:{result[1]}" if result[0] else "Department not found or no salary data."

    # 10. Get Average Salary in a Department
    elif average_salary_match:
        department = average_salary_match.group(1).strip()
        print(f"Extracted Department: '{department}'")  # Debugging

        cursor.execute("SELECT AVG(Salary) FROM Employees WHERE LOWER(Department) = LOWER(?)", (department,))
        result = cursor.fetchone()
        response = f"Average salary in {department.capitalize()}: rs:{round(result[0], 2)}" if result[0] else "Department not found or no salary data."

    conn.close()
    return response


# Home Route
@app.route("/")
def home():
    return render_template("index.html")


# API Route for Chat
@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json["query"]
    response = process_query(user_input)
    return jsonify({"response": response})


if __name__ == "__main__":
    app.run(debug=True)
