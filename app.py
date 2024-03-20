import streamlit as st
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from git import Repo

# List of accesses
access_list = ['JIRA', 'Bitbucket', 'AWS']

def send_email(selected_accesses, name, empId):
    try:
        # setup the parameters of the message
        password = "lbmm hnet ztxj lcqg"
        msg = MIMEMultipart()
        msg['From'] = "dummy@gmail.com"
        msg['To'] = "dummy@gmail.com"
        msg['Subject'] = "Access request"
        message = "Hi team, \nRequesting you to provide the following accesses for :\nName: {}\nEmployee Id: {}".format(name, empId) +"\n" + "\n".join(selected_accesses)
        msg.attach(MIMEText(message, 'plain'))

        # Set up your email server
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(msg['From'], password)

        # Send the email
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        print("Email sent successfully")

    except Exception as e:
        print("Failed to send email")
        print(e)
    finally:
        server.quit()

# Function to clone the repository
def clone_repository(username, password, repo_url, path): 
    try:
        final_repo_url = repo_url.split("https://github.com/", 1)[1]
        remote = f"https://{username}:{password}@github.com/{final_repo_url}"
        Repo.clone_from(remote, path)
        st.success("Repository cloned successfully!")
        # Set session state variable to navigate to the next page
        st.session_state.next_page = "Select Software"
        st.experimental_rerun()
    except Exception as e:
        st.error(f"Error occurred: {e}")

# Define the pages
def welcome_page():
    st.title('Welcome To SetUpSimplified')
    st.subheader('We will help you setup your local development environment in few clicks')
    st.write('Do you have these accesses?')
    for access in access_list:
        st.write(access)
    if st.button('No'):
        st.write('Please visit the Access Page, using the left navigation pane to request these')
        return False
    return True

def access_page():
    st.title('Access Page')
    name = st.text_input('Please provide your name')
    empId = st.text_input('Please provide your emaployee id')
    selected_accesses = []
    for access in access_list:
        if st.checkbox(access):
            selected_accesses.append(access)
    if st.button('Submit'):
        send_email(selected_accesses, name, empId)
        st.write('Email has been sent!')

def clone_repository_page():
    st.title("GitHub Repository Cloner")
    st.header("Clone Repository")
    # Ask for GitHub credentials
    username = st.text_input("GitHub Username")
    password = st.text_input("GitHub Personal Access Token", type="password")
    # Ask for repository URL and path
    repo_url = st.text_input("Repository URL")
    clone_path = st.text_input("Clone Path", value=os.getcwd())
    clone, next = st.columns(2)
    # Button to clone repository
    if clone.button("Clone Repository"):
        if not username or not password:
            st.error("Please provide both username and password.")
        elif not repo_url:
            st.error("Please provide repository URL.")
        elif not clone_path:
            st.error("Please provide clone path.")
        else:
            clone_repository(username, password, repo_url, clone_path)
    if next.button("Install Software"):
        st.session_state.next_page = "Select Software"
        st.experimental_rerun()

def select_software_page():
    st.title("Software Installation")
    st.header("Software Checklist")
    # List of software with checkboxes
    software_list = ["IntellIJ IDEA", "Notepad++"]
    selected_software = {}
    for software in software_list:
        selected_software[software] = st.checkbox(software, value=True)

    cloneRep, install = st.columns(2)
    # Button to submit selected software
    if cloneRep.button("Clone Repository"):
        st.session_state.next_page = "Clone Repository"
        st.experimental_rerun()
    if install.button("Install"):
        selected_software_list = [software for software, selected in selected_software.items() if selected]
        st.success("Selected software: {}".format(selected_software_list))

def repo_and_software_page():
    # Initialize session state variable
    if "next_page" not in st.session_state:
        st.session_state.next_page = "Clone Repository"

    # Navigation logic
    if st.session_state.next_page == "Clone Repository":
        clone_repository_page()
    elif st.session_state.next_page == "Select Software":
        select_software_page()

# Main app
def main():
    st.sidebar.title('Navigation Menu')
    pages = {
        "Welcome Page": welcome_page,
        "Access Request Page": access_page,
        "Repository and Softwares" : repo_and_software_page
    }

    # User selection logic
    selection = st.sidebar.radio("Go to", list(pages.keys()))
    page = pages[selection]

    if page():
        st.sidebar.success('You have all the accesses?')
    else:
        st.sidebar.text('Go to Access Request Page')

    

if __name__ == "__main__":
    main()