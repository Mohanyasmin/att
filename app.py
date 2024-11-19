import streamlit as st
from PIL import Image, ImageOps, ImageDraw
import pandas as pd
from datetime import date
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# Define a dictionary of valid users (username: password)
USER_CREDENTIALS = {
    "mohan": "lusu",
    "bala": "manmathan",
    "thzim": "mandakolaru",
}

# Function to check login
def check_login(username, password):
    if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
        return True
    return False

# Function to create a rounded image
def make_rounded_image(img):
    mask = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + img.size, fill=255)
    output = ImageOps.fit(img, img.size, centering=(0.5, 0.5))
    output.putalpha(mask)
    return output

# Generate a filename based on today's date
def get_filename():
    today = date.today().strftime("%Y-%m-%d")
    return f"attendance_{today}.xlsx"

# Initialize the Excel file if it doesn't exist
def initialize_excel_file(filename):
    if not os.path.exists(filename):
        df = pd.DataFrame(columns=["Date", "Name", "Period1", "Period2", "Period3", "Period4", "Period5"])
        df.to_excel(filename, index=False)

# Load attendance data
def load_attendance(filename):
    return pd.read_excel(filename)

# Save attendance data
def save_attendance(data, filename):
    data.to_excel(filename, index=False)

# Function for attendance management
def attendance_management(username):
    st.write("Attendance Management System")

    # Get today's date
    today = date.today()
    filename = get_filename()
    initialize_excel_file(filename)

    # Input for student details
    st.subheader("Mark Attendance")
    name = username  # Use the logged-in username
    period1 = st.selectbox("Select Status for Period 1", ["Present", "Absent", "Leave"], key="period1")
    period2 = st.selectbox("Select Status for Period 2", ["Present", "Absent", "Leave"], key="period2")
    period3 = st.selectbox("Select Status for Period 3", ["Present", "Absent", "Leave"], key="period3")
    period4 = st.selectbox("Select Status for Period 4", ["Present", "Absent", "Leave"], key="period4")
    period5 = st.selectbox("Select Status for Period 5", ["Present", "Absent", "Leave"], key="period5")

    # Button to add attendance
    if st.button("Submit Attendance"):
        # Load existing data
        attendance_data = load_attendance(filename)
        # Append the new record
        new_entry = pd.DataFrame({
            "Date": [today], 
            "Name": [name], 
            "Period1": [period1], 
            "Period2": [period2], 
            "Period3": [period3], 
            "Period4": [period4], 
            "Period5": [period5]
        })
        attendance_data = pd.concat([attendance_data, new_entry], ignore_index=True)
        # Save updated data
        save_attendance(attendance_data, filename)
        st.success(f"Attendance marked for {name}")

    # Display attendance data
    st.subheader("Attendance Records")
    attendance_data = load_attendance(filename)
    st.dataframe(attendance_data)

    # Restrict download functionality to "mohan" user
    st.subheader("Download Attendance")
    download_username = st.text_input("Enter Username to Download")
    download_password = st.text_input("Enter Password", type="password")
    if download_username in USER_CREDENTIALS and USER_CREDENTIALS[download_username] == download_password:
        if st.button("Download Excel File"):
            with open(filename, "rb") as file:
                st.download_button(
                    label="Download",
                    data=file,
                    file_name=filename,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
    else:
        st.warning("Only  'admin' can download the attendance file.")

# Function for main menu
def main_menu(username):
    # Check if the file exists
    img_path = 'logo.jpeg'  # Use relative path
    if os.path.exists(img_path):
        img = Image.open(img_path)
        img = img.resize((150, 150))  # Resize the image to a smaller size
        img = make_rounded_image(img)  # Make the image rounded
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(img, caption="BCA DATA SCIENCE", use_column_width=True)
        logger.info("Profile image loaded successfully")
    else:
        st.error("Image file not found")
        logger.error("Image file not found at path: %s", img_path)

    st.title(f"Welcome, {username}!")

    # Display buttons for different options in a single line
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("STUDENT INFO"):
            st.write("Displaying Student Info...")
            # Add content or functionality for Student Info here
    with col2:
        if st.button("ATTENDANCE"):
            st.session_state.page = "ATTENDANCE"
    with col3:
        if st.button("CLASS INFO"):
            st.write("Displaying Class Info...")
            # Add content or functionality for Class Info here

# Streamlit UI
def main():
    # Initialize session state
    if "page" not in st.session_state:
        st.session_state.page = "MAIN_MENU"
    if "username" not in st.session_state:
        st.session_state.username = ""

    # Function for sidebar content
    def sidebar():
        logger.info("Loading sidebar content")

        # Sidebar login form
        st.sidebar.title("STUDENT LOGIN")
        username = st.sidebar.text_input("Username").lower()
        password = st.sidebar.text_input("Password", type="password")

        if st.sidebar.button("Login"):
            if check_login(username, password):
                st.sidebar.success(f"Welcome, {username}!")
                st.sidebar.write("You are successfully logged in.")
                logger.info("User %s logged in successfully", username)
                st.session_state.username = username
                st.session_state.page = "MAIN_MENU"
            else:
                st.sidebar.error("Invalid username or password. Please try again.")
                logger.warning("Invalid login attempt for user %s", username)

    # Call the sidebar
    sidebar()

    # Show the correct page based on the state
    if st.session_state.page == "MAIN_MENU":
        main_menu(st.session_state.username)
    elif st.session_state.page == "ATTENDANCE":
        attendance_management(st.session_state.username)

if __name__ == "__main__":
    main()


