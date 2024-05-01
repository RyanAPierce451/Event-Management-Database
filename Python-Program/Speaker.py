import mysql.connector
import modify_speaker as modS

def connect_to_database():
    host = 'IP-Address'
    user = 'root'
    password = 'ADD-password'
    database = 'event_managment'

    # Establish the connection
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to the database: {err}")
        return None

def fetch_speaker_information(connection):
    try:
        cursor = connection.cursor()

        # Fetch speaker information
        query = "SELECT * FROM speaker"
        cursor.execute(query)
        speakers = cursor.fetchall()

        return speakers

    except mysql.connector.Error as err:
        print(f"Error retrieving speaker information: {err}")
        return []

def display_speaker_information(connection):
    speaker = fetch_speaker_information(connection)

    # Display speaker information
    for speaker in speaker:
        speaker_id, session_id, speaker_first_name, speaker_last_name, speaker_bio, speaker_email, speaker_phone = speaker

        print(f"Speaker ID: {speaker_id}")
        print(f"Session ID: {session_id}")
        print(f"Speaker First Name: {speaker_first_name}")
        print(f"Speaker Last Name: {speaker_last_name}")
        print(f"Speaker Bio: {speaker_bio}")
        print(f"Speaker Email: {speaker_email}")
        print(f"Speaker Phone: {speaker_phone}")
        print("\n")

def main():

    connection = connect_to_database()
    if not connection:
        return

    while True:
        print("\nSelect an option:")
        print("1. Display All Speakers")
        print("2. Speaker ID Lookup")
        print("3. Add Speaker")
        print("4. Delete Speaker")
        print("5. Modify Speaker")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
             display_speaker_information(connection)
        elif choice == '2':
             speaker_id = int(input('Enter Speaker ID: '))
             print()
             modS.lookup(connection, speaker_id)
        elif choice == '3':
             speaker_data = (
                int(input("Enter Session ID: ")),
                input("Enter Speaker's First Name: "),
                input("Enter Speaker's Last Name: "),
                input("Enter Speaker's Biography: "),
                input("Enter Speaker's Email: "),
                input("Enter Speaker's Phone: "),
            )
             modS.add(connection, speaker_data)
        elif choice == '4':
             speaker_id = int(input('Enter Speaker ID: '))
             print()
             modS.delete(connection, speaker_id)
        elif choice == '5':
             speaker_id = int(input('Enter Speaker ID: '))
             speaker_data = (
                int(input("Enter Session ID: ")),
                input("Enter Speaker's First Name: "),
                input("Enter Speaker's Last Name: "),
                input("Enter Speaker's Biography: "),
                input("Enter Speaker's Email: "),
                input("Enter Speaker's Phone: "),
            )
             print()
             modS.modify(connection, speaker_id, speaker_data)
             
        elif choice == '0':
             print("Exiting the Database Explorer.")
             break
        else:
             print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()