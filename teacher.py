import streamlit as st
from pymongo import MongoClient
import bcrypt

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client["evaluation_system"]
teachers_collection = db["teachers"]

# Function to add a new teacher
def signup_teacher(email, password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    teachers_collection.insert_one({"email": email, "password": hashed_password})

# Function to validate login credentials
def login_teacher(email, password):
    # Fetch the teacher record
    teacher = db.teachers.find_one({"email": email})
    # Compare plain-text password
    if teacher and teacher["password"] == password:
        return True
    return False


# Teacher Page
def teacher_page():
    st.title("Teacher Login/Signup")

    # Tabs for Login and Signup
    choice = st.radio("Select an option:", ["Login", "Signup"])

    if choice == "Signup":
        st.subheader("Signup as a Teacher")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Signup"):
            if email and password:
                signup_teacher(email, password)
                st.success("Signup successful! Please log in.")
            else:
                st.error("Please fill in all fields.")

    elif choice == "Login":
        st.subheader("Login as a Teacher")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if login_teacher(email, password):
                st.success("Login successful!")
                teacher_dashboard()
            else:
                st.error("Invalid email or password.")

# Teacher Dashboard
def teacher_dashboard():
    st.title("Teacher Dashboard")
    st.write("Welcome to the Teacher Dashboard!")

    # Options for the teacher
    choice = st.radio("Choose an action:", ["Upload and Evaluate Answer Sheet", "Upload Marks and Feedback", "Go Home"])
    
    if choice == "Upload and Evaluate Answer Sheet":
        st.subheader("Upload Student Answer Sheet")
        uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            st.write("Processing the image...")
            # Add code to process the image with Google Cloud Vision API and GPT-4 here.
    
    elif choice == "Upload Marks and Feedback":
        st.subheader("Upload Marks and Feedback")
        student_id = st.text_input("Student ID")
        marks = st.number_input("Marks", min_value=0, max_value=100)
        feedback = st.text_area("Feedback")
        if st.button("Upload"):
            # Save marks and feedback to MongoDB
            db.students.update_one(
                {"id": student_id},
                {"$set": {"marks": marks, "feedback": feedback}},
                upsert=True
            )
            st.success("Marks and feedback uploaded successfully!")

    elif choice == "Go Home":
        st.experimental_rerun()
