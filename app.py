import streamlit as st
from PIL import Image, ImageOps, ImageDraw
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

# Function for main menu
def main_menu(username):
    # Check if the file exists
    img_path = r"C:/Users/god/OneDrive/Desktop/project/attendence/logo.jpeg"
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

    st.write(f"Welcome, {username}!")

    # Display buttons for different options
    if st.button("STUDENT INFO"):
        st.write("Displaying Student Info...")
        # Add content or functionality for Student Info here
    if st.button("ATTENDENCE"):
        st.write("Displaying Attendance...")
        # Add content or functionality for Attendance here

# Streamlit UI
def main():
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
                # Once logged in, call the main menu with the username
                main_menu(username)
            else:
                st.sidebar.error("Invalid username or password. Please try again.")
                logger.warning("Invalid login attempt for user %s", username)

    # Call the sidebar
    sidebar()

if __name__ == "__main__":
    main()


