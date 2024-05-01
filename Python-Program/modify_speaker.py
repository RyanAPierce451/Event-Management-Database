import mysql.connector

def is_speaker_id_valid(connection, speaker_id):
    try:
        cursor = connection.cursor()

        # Check if the speaker_id exists in the database
        query = "SELECT COUNT(*) FROM speaker WHERE Speaker_id = %s"
        cursor.execute(query, (speaker_id,))
        count = cursor.fetchone()[0]

        return count > 0

    except mysql.connector.Error as err:
        print(f"Error checking Speaker ID: {err}")
        return False

# Function to add a speaker *WORKS*
def add(connection, speaker_data):
    try:
        cursor = connection.cursor()

        query = "SELECT MAX(Speaker_id) FROM speaker"
        cursor.execute(query)
        max_speaker_id = cursor.fetchone()[0]

        if max_speaker_id is None:
            # If the table is empty, start with speaker_id 1
            new_speaker_id = 1
        else:
            new_speaker_id = max_speaker_id + 1

        # Insert new speaker into the database
        query = "INSERT INTO speaker (Speaker_id, Session_id, Speaker_first_name, Speaker_last_name, Speaker_bio, Speaker_email, Speaker_phone) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (new_speaker_id, *speaker_data))
        connection.commit()
        print()
        print("Speaker added successfully.")

    except mysql.connector.Error as err:
        connection.rollback()
        print()
        print(f"Error adding Speaker: {err}")

# Function to delete a speaker by ID *WORKS*
def delete(connection, speaker_id):
    try:
        cursor = connection.cursor()

        # Check if the speaker_id exists
        if not is_speaker_id_valid(connection, speaker_id):
            print("Speaker ID does not exist.")
            return

        # Delete speaker from the database
        query = "DELETE FROM speaker WHERE Speaker_id = %s"
        cursor.execute(query, (speaker_id,))
        connection.commit()
        print("Speaker deleted successfully.")

    except mysql.connector.Error as err:
        connection.rollback()
        print(f"Error deleting speaker: {err}")

# Function to modify a speaker by ID *WORKS*
def modify(connection, speaker_id, speaker_data):
    try:
        cursor = connection.cursor()

        # Check if the session_id exists
        if not is_speaker_id_valid(connection, speaker_id):
            print("Session ID does not exist.")
            return

        # Update session in the database
        query = "UPDATE speaker SET Session_id = %s, Speaker_first_name = %s, Speaker_last_name = %s, Speaker_bio = %s, Speaker_email = %s, Speaker_phone = %s WHERE Speaker_id = %s"
        cursor.execute(query, (*speaker_data, speaker_id))
        connection.commit()
        print("Speaker modified successfully.")

    except mysql.connector.Error as err:
        connection.rollback()
        print(f"Error modifying speaker: {err}")

# Function to lookup a speaker by ID *WORKS*
def lookup(connection, speaker_id):
    try:
        cursor = connection.cursor()

        # Fetch speaker information by ID
        query = "SELECT * FROM speaker WHERE Speaker_id = %s"
        cursor.execute(query, (speaker_id,))
        speaker = cursor.fetchone()

        if speaker:
            print(f"Speaker ID: {speaker[0]}")
            print(f"Session ID: {speaker[1]}")
            print(f"Speaker First Name: {speaker[2]}")
            print(f"Speaker Last Name: {speaker[3]}")
            print(f"Speaker Bio: {speaker[4]}")
            print(f"Speaker Email: {speaker[5]}")
            print(f"Speaker Phone: {speaker[6]}")
            print("\n")
        else:
            print("Speaker not found.")

    except mysql.connector.Error as err:
        print(f"Error retrieving speaker information: {err}")
