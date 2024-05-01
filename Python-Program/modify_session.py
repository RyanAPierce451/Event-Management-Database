import mysql.connector

def is_session_id_valid(connection, session_id):
    try:
        cursor = connection.cursor()

        # Check if the session_id exists in the database
        query = "SELECT COUNT(*) FROM session WHERE Session_id = %s"
        cursor.execute(query, (session_id,))
        count = cursor.fetchone()[0]

        return count > 0

    except mysql.connector.Error as err:
        print(f"Error checking Session ID: {err}")
        return False

# Function to add a sesion *WORKS*
def add(connection, session_data):
    try:
        cursor = connection.cursor()

        query = "SELECT MAX(Session_id) FROM session"
        cursor.execute(query)
        max_session_id = cursor.fetchone()[0]

        if max_session_id is None:
            # If the table is empty, start with session_id 1
            new_session_id = 1
        else:
            new_session_id = max_session_id + 1

        # Insert new session into the database
        query = "INSERT INTO session (Session_id, Event_id, Session_title, Session_description, Session_start_datetime, Session_end_datetime) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (new_session_id, *session_data))
        connection.commit()
        print()
        print("Session added successfully.")

    except mysql.connector.Error as err:
        connection.rollback()
        print()
        print(f"Error adding session: {err}")

# Function to delete a session by ID *WORKS*
def delete(connection, session_id):
    try:
        cursor = connection.cursor()

        # Check if the session_id exists
        if not is_session_id_valid(connection, session_id):
            print("Session ID does not exist.")
            return

        # Delete session from the database
        query = "DELETE FROM session WHERE Session_id = %s"
        cursor.execute(query, (session_id,))
        connection.commit()
        print("Session deleted successfully.")

    except mysql.connector.Error as err:
        connection.rollback()
        print(f"Error deleting session: {err}")

# Function to modify a session by ID *WORKS*
def modify(connection, session_id, session_data):
    try:
        cursor = connection.cursor()

        # Check if the session_id exists
        if not is_session_id_valid(connection, session_id):
            print("Session ID does not exist.")
            return

        # Update session in the database
        query = "UPDATE session SET Event_id = %s, Session_title = %s, Session_description = %s, Session_start_datetime = %s, Session_end_datetime = %s WHERE Session_id = %s"
        cursor.execute(query, (*session_data, session_id))
        connection.commit()
        print("Session modified successfully.")

    except mysql.connector.Error as err:
        connection.rollback()
        print(f"Error modifying Session: {err}")

# Function to lookup a session by ID *WORKS*
def lookup(connection, session_id):
    try:
        cursor = connection.cursor()

        # Fetch session information by ID
        query = "SELECT * FROM session WHERE Session_id = %s"
        cursor.execute(query, (session_id,))
        session = cursor.fetchone()

        if session:
            print(f"Session ID: {session[0]}")
            print(f"Event ID: {session[1]}")
            print(f"Session Title: {session[2]}")
            print(f"Session Description: {session[3]}")
            print(f"Session Start Date and Time: {session[4]}")
            print(f"Session End Date and Time: {session[5]}")
            print("\n")
        else:
            print("Session not found.")

    except mysql.connector.Error as err:
        print(f"Error retrieving session information: {err}")
