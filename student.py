import streamlit as st
from pymongo import MongoClient
import bcrypt

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client["evaluation_system"]
students_collection = db["students"]

# Function to add a new student
def signup_student(email, password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    students_collection.insert_one({"email": email, "password": hashed_password})

# Function to validate login credentials
def login_student(email, password):
    # Fetch the student record
    student = db.students.find_one({"email": email})
    # Compare plain-text password
    if student and student["password"] == password:
        return True
    return False


# Student Page
def student_page():
    st.title("Student Login/Signup")

    # Tabs for Login and Signup
    choice = st.radio("Select an option:", ["Login", "Signup"])

    if choice == "Signup":
        st.subheader("Signup as a Student")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Signup"):
            if email and password:
                signup_student(email, password)
                st.success("Signup successful! Please log in.")
            else:
                st.error("Please fill in all fields.")

    elif choice == "Login":
        st.subheader("Login as a Student")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if login_student(email, password):
                st.success("Login successful!")
                student_dashboard()
            else:
                st.error("Invalid email or password.")

# Student Dashboard
def student_dashboard():
    st.title("Student Dashboard")
    st.write("Welcome to the Student Dashboard!")

    st.subheader("View Marks and Feedback")
    student_id = st.text_input("Enter your Student ID")
    if st.button("View"):
        student = db.students.find_one({"id": student_id})
        if student:
            st.write(f"Marks: {student.get('marks', 'N/A')}")
            st.write(f"Feedback: {student.get('feedback', 'N/A')}")
        else:
            st.error("No records found for the given Student ID.")
