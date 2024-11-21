import streamlit as st
from teacher import teacher_page
from student import student_page

def main():
    st.title("Welcome to the Evaluation System")

    st.write("Please choose an option:")
    choice = st.radio("Login as:", ["Teacher", "Student"])

    if choice == "Teacher":
        teacher_page()
    elif choice == "Student":
        student_page()

if __name__ == "__main__":
    main()
