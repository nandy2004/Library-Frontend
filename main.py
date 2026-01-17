import streamlit as st
import requests

base_url="https://library-backend-nu.vercel.app"

st.header("Nandy's Library")
st.text("Welcome to Nandy's Library." \
        "Here you can find different types of books with their respective categories."\
        "find the book of your choice and collect it"\
        "Don't forget to return the book. Thank You for choosing 'Nandy's Library'")
st.divider()

#-----------------------------------THIS IS FOR BOOKS---------------------------------------
#------------GET METHOD -1

with st.expander("Welcome to Books Section",expanded=True):
    st.text("Click 'BOOKS' to get the list of books.")
    
    btn = st.button('BOOKS', type='primary', use_container_width=False)
    if btn:
        tabs=st.tabs(['Books'])
        with tabs[0]:
            res=requests.get(base_url + '/books')
            Books=res.json()
            st.data_editor(Books)
#------------GET METHOD -2
    
    st.text("Click 'GET_BOOK' to the details of a specific id.")
    get_book = st.button("GET_BOOK", type='primary')

    if get_book:
        @st.dialog("Get_book_by_id")
        def Get_book():
            with st.form("get_book_by_id"):
                book_id = st.text_input("Enter Book ID")
                confirm = st.form_submit_button("confirm")
                if confirm:
                    if book_id.strip()=="":
                        st.warning("Please enter a book id")
                    else:
                        tabs=st.tabs(['Books'])
                        with tabs[0]:
                            res = requests.get(f"{base_url}/books/{book_id}")
                            Books=res.json()
                            st.data_editor(Books,use_container_width=True)
        Get_book()


#---------------------------------------------THIS IS FOR USERS-----------------------------------

with st.expander("Welcome to Users Section",expanded=True):
#----------------GET METHOD-1
    st.text("Click here to get the list of users.")
    btn = st.button('USERS',type='primary',use_container_width=False)
    if btn:
        tabs=st.tabs(['USERS'])
        with tabs[0]:
            res=requests.get(base_url+'/users')
            Users=res.json()
            st.data_editor(Users)

#----------------GET METHOD -2
    st.text("Click 'GET_USER' to get the details of a specific id.")
    get_user = st.button("GET_USER", type='primary')

    if get_user:
        @st.dialog("Get_user_by_id")
        def Get_user():
            with st.form("get_user_by_id"):
                user_id = st.text_input("Enter ID")
                confirm = st.form_submit_button("confirm")
                if confirm:
                    if user_id.strip()=="":
                        st.warning("Please enter a user id")
                    else:
                        tabs=st.tabs(['Users'])
                        with tabs[0]:
                            res = requests.get(f"{base_url}/users/{user_id}")
                            Users=res.json()
                            st.data_editor(Users,use_container_width=True)
        Get_user()

#---------------POST METHOD
    st.text("Click 'ADD_USER' to add a User to the library")
    if st.button("ADD_USER",type='primary'):
    #dialog box
        @st.dialog('Add a new User')
        def Add_user():
            with st.form("add_user_form"):
                id=st.text_input('Enter ID')
                user_name=st.text_input('Enter User Name')
                user_id=st.text_input('Enter User ID')
                book_collected=st.radio("Book collected or not",["yes","No"],horizontal=True)
                book_returned=st.radio("Book returned or not",["yes","no"],horizontal=True)
                book_name=st.text_input("Name of Book")
            
                submit=st.form_submit_button("Submit")
                if submit:
                    payload={"id": int(id),
                    "user_name": user_name,
                    "user_id": int(user_id),
                    "book_collected": book_collected,
                    "book_returned": book_returned,
                    "book_name": book_name}
                    res = requests.post(f"{base_url}/users/addnewuser",json=payload)
                    response = res.json()
             
                    if response["status"] == "failed":
                        st.error(response["message"])   # user ID already exists

                    else:
                        st.success(response["message"])
                        st.toast("user added successfully")
                        
    # Open dialog
        Add_user()
#----------------PUT METHOD
    st.text("Click 'UPDATE_USER' to update a user details")
    #button to open dialog box
    if st.button('UPDATE_USER',type='primary'):
    #dialogbox
        @st.dialog('Update a user')
        def Update_user():
            with st.form("Update_user_form"):
                id=st.text_input("Enter user id to update",key='id_input')
                user_name=st.text_input("give the user name",key="Update_user_name")
                user_id=st.text_input("give the user id",key="Update_user_id")
                book_collected=st.radio("Book Collected or not",["yes","no"],key="Update_book_collected")
                book_returned=st.radio("Book returned or not",["yes","no"],key="Update_book_returned")
                book_name=st.text_input("Book name is",key="Update_book_name")
                submit=st.form_submit_button("confirm update")
                if submit:
                    if id.strip()=="":
                        st.warning("Please enter id to update a user")
                    else:
                        payload={"user_name":user_name,"user_id":user_id,"book_collected":book_collected,"book_returned":book_returned,"book_name":book_name}
                        res = requests.put(f"{base_url}/users/updateuserdetails/{id}", json=payload)
                        if res.status_code in [200, 204]:
                            st.success("User updated successfully!")
                        else:
                            st.error(f"Failed to update user! Status code: {res.status_code}")
                            st.write(res.text)
    #open dialog
        Update_user()

#------------DELETE METHOD

    st.text("Click 'DELETE_USER' to delete a book")
    #button for delete dialog box
    if st.button("DELETE_USER",type='primary'):
        @st.dialog("Delete User")
        def delete_user():
            with st.form("Delete_a_user"):
                user_id=st.text_input("Enter user ID to delete")
                confirm=st.form_submit_button("Confirm Delete")
                if confirm:
                    if user_id.strip() == "":
                        st.warning("Please enter a valid user ID")
                    else:
                        res = requests.delete(f"{base_url}/users/deleteauser/{user_id}")
                        if res.status_code in [200, 204]:
                            st.success("user deleted successfully!")
                        else:
                            st.error(f"Failed to delete user! Status code: {res.status_code}")
                            st.write(res.text)

        delete_user()

#ISSUE A BOOK

with st.expander("COLLECT A BOOK FROM LIBRARY",expanded=True):
    st.subheader("Issue a Book")

    if st.button("ISSUE BOOK", type="primary"):

        @st.dialog("Issue a Book")
        def issue_book():
            with st.form("issue_book_form"):
                book_id = st.text_input("Enter Book ID")
                user_id = st.text_input("Enter User ID")

                submit = st.form_submit_button("Confirm Issue")

                if submit:
                    payload = {
                        "book_id": book_id,
                        "user_id": user_id
                    }

                    res = requests.post(
                        f"{base_url}/books/selectbooktocollect",
                        json=payload
                    )

                    response = res.json()

                    if response["status"] == "success":
                        st.success(response["message"])
                    else:
                        st.error(response["message"])

        issue_book()

# COLLECT A BOOK
with st.expander("RETURN A BOOK TO LIBRARY",expanded=True):
    st.subheader("Return a Book")

    if st.button("RETURN BOOK", type="primary"):

        @st.dialog("Return a Book")
        def return_book():
            with st.form("return_book_form"):
                book_id = st.text_input("Enter Book ID")
                user_id = st.text_input("Enter User ID")

                submit = st.form_submit_button("Confirm Return")

                if submit:
                    payload = {
                        "book_id": book_id,
                        "user_id": user_id
                    }

                    res = requests.post(
                        f"{base_url}/books/returnabook",
                        json=payload
                    )

                    response = res.json()

                    if response["status"] == "success":
                        st.success(response["message"])
                    else:
                        st.error(response["message"])

        return_book()


    
    



    
