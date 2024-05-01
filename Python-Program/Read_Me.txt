Database Explorer
The Database_explorer is a Python program designed to explore and interact with a recreated database. The database is re-created using Python files that represent individual tables such as Attendee, Event, Venue, etc.

Getting Started
To get started with the Database_explorer program, follow the instructions below:

Step 1: Recreate the Database
Make sure you have all the necessary Python files representing the tables (Attendee.py, Event.py, Venue.py, etc.) that collectively constitute the database. Each of these Python files should include a function called connect_to_database().

Step 2: Configure Database Connection
In order to connect to the re-created database, you need to provide four variables with the appropriate information. These variables are:

host: The host address where the database is hosted. For example, "localhost" if the database is on your local machine, or a specific IP address if hosted elsewhere.
user: The username to access the database.
password: The password associated with the provided username.
database: The name of the database you want to connect to.
Ensure that the values of these variables match the information of the re-created database.

Step 3: Update Python Files
After configuring the database connection variables, you need to update all Python files that contain the connect_to_database() function. Change the values of these variables in each file to match the new information of the re-created database.

Usage
Once you have completed the setup steps above, you can run the Database_explorer program, which will now successfully connect to the re-created database using the provided information.