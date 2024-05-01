import mysql.connector

def is_attendee_id_valid(connection, attendee_id):
    try:
        cursor = connection.cursor()

        # Check if the attendee_id exists in the database
        query = "SELECT COUNT(*) FROM attendee WHERE Attendee_id = %s"
        cursor.execute(query, (attendee_id,))
        count = cursor.fetchone()[0]

        return count > 0

    except mysql.connector.Error as err:
        print(f"Error checking Attendee ID: {err}")
        return False

# Function to add a attendee *WORKS*
def add(connection, attendee_data):
    try:
        cursor = connection.cursor()

        query = "SELECT MAX(Attendee_id) FROM attendee"
        cursor.execute(query)
        max_attendee_id = cursor.fetchone()[0]

        if max_attendee_id is None:
            # If the table is empty, start with attendee_id 1
            new_attendee_id = 1
        else:
            new_attendee_id = max_attendee_id + 1

        # Insert new speaker into the database
        query = "INSERT INTO attendee (Attendee_id, Attendee_vendor_name, Attendee_website) VALUES (%s, %s, %s)"
        cursor.execute(query, (new_attendee_id, *attendee_data))
        connection.commit()
        print()
        print("Attendee added successfully.")

    except mysql.connector.Error as err:
        connection.rollback()
        print()
        print(f"Error adding Attendee: {err}")

# Function to delete a attendee by ID *WORKS*
def delete(connection, attendee_id):
    try:
        cursor = connection.cursor()

        # Check if the attendee_id exists
        if not is_attendee_id_valid(connection, attendee_id):
            print("Attendee ID does not exist.")
            return

        # Delete attendee from the database
        query = "DELETE FROM attendee WHERE Attendee_id = %s"
        cursor.execute(query, (attendee_id,))
        connection.commit()
        print("Attendee deleted successfully.")

    except mysql.connector.Error as err:
        connection.rollback()
        print(f"Error deleting attendee: {err}")

# Function to modify a attendee by ID *WORKS*
def modify(connection, attendee_id, attendee_data):
    try:
        cursor = connection.cursor()

        # Check if the attendee_id exists
        if not is_attendee_id_valid(connection, attendee_id):
            print("Attendee ID does not exist.")
            return

        # Update attendee in the database
        query = "UPDATE attendee SET Attendee_vendor_name = %s, Attendee_website = %s WHERE Attendee_id = %s"
        cursor.execute(query, (*attendee_data, attendee_id))
        connection.commit()
        print("Attendee modified successfully.")

    except mysql.connector.Error as err:
        connection.rollback()
        print(f"Error modifying attendee: {err}")

# Function to lookup a attendee by ID *WORKS*
def lookup(connection, attendee_id):
    try:
        cursor = connection.cursor()

        # Fetch attendee information by ID
        query = "SELECT * FROM attendee WHERE Attendee_id = %s"
        cursor.execute(query, (attendee_id,))
        attendee = cursor.fetchone()

        if attendee:
            print(f"Attendee ID: {attendee[0]}")
            print(f"Attendee Vednor: {attendee[1]}")
            print(f"Attendee Website: {attendee[2]}")

            print("\n")
        else:
            print("Attendee not found.")

    except mysql.connector.Error as err:
        print(f"Error retrieving attendee information: {err}")
