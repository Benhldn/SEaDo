## Ticket Management System
## The reason for the project:

This is a ticket management tool for a university course where students should be able to create and edit tickets however only admin (lecturers) can reslove tickets after they review it. Admins need to be created and defined outside of the application as there is no way currently to upgrade a user from regular user to admin.





# To run locally:
1.  { python3 -m venv .venv }
2.  { source .venv/bin/activate }
3.  { python3 -m pip install -r requirements.txt }
4.  { export FLASK_APP=src/ }
5.  { flask run }

WARNING: ENSURE YOU ARE IN THE ROOT WHEN RUNNING STEP 5

# Testing
I have manual tested my application.
Evidence of this can be found in task 1 of the assignment doc.

Unit tests have been written and if you wish to run them, paste:
python -m unittest discover

# Running as admin:
If you would like to login as admin to test the delete feature, the credentials are:

Email: admin@email.com
Password: Admin

## Webiste URL:
https://ticket-management-benh.onrender.com/




