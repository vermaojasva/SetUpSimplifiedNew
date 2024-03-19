import streamlit as st
import smtplib

# List of accesses
access_list = ['JIRA', 'Bitbucket', 'AWS']

def send_email(selected_accesses):
    # Set up your email server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("your-email@gmail.com", "your-password")

    # Compose the email
    msg = "User has selected the following accesses:\n\n" + "\n".join(selected_accesses)
    # server.sendmail("your-email@gmail.com", "recipient-email@gmail.com", msg)
    server.quit()

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
    selected_accesses = []
    for access in access_list:
        if st.checkbox(access):
            selected_accesses.append(access)
    if st.button('Submit'):
        send_email(selected_accesses)
        st.write('Email has been sent!')

# Main app
def main():
    st.sidebar.title('Navigation')
    pages = {
        "Welcome Page": welcome_page,
        "Access Page": access_page
    }

    # User selection logic
    selection = st.sidebar.radio("Go to", list(pages.keys()))
    page = pages[selection]

    if page():
        st.sidebar.success('You have all the accesses?')
    else:
        st.sidebar.text('Go to Access Page')

if __name__ == "__main__":
    main()