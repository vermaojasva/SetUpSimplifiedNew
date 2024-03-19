import streamlit as st
import os
from git import Repo


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


def main():

    # Initialize session state variable
    if "next_page" not in st.session_state:
        st.session_state.next_page = "Clone Repository"

    # Navigation logic
    if st.session_state.next_page == "Clone Repository":
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
    elif st.session_state.next_page == "Select Software":
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


if __name__ == "__main__":
    main()
