import mysql.connector
import modify_session as modS

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

def fetch_session_information(connection):
    try:
        cursor = connection.cursor()

        # Fetch session information
        query = "SELECT * FROM session"
        cursor.execute(query)
        sessions = cursor.fetchall()

        return sessions

    except mysql.connector.Error as err:
        print(f"Error retrieving session information: {err}")
        return []

def display_session_information(connection):
    sessions = fetch_session_information(connection)

    # Display session information
    for session in sessions:
        session_id, event_id, session_title, session_description, session_start_datetime, session_end_datetime = session

        print(f"Session ID: {session_id}")
        print(f"Event ID: {event_id}")
        print(f"Session Title: {session_title}")
        print(f"Session Description: {session_description}")
        print(f"Session Start Date and Time: {session_start_datetime}")
        print(f"Session End Date and Time: {session_end_datetime}")
        print("\n")

def main():

    connection = connect_to_database()
    if not connection:
        return

    while True:
        print("\nSelect an option:")
        print("1. Display All Sessions")
        print("2. Session ID Lookup")
        print("3. Add Session")
        print("4. Delete Session")
        print("5. Modify Session")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
             display_session_information(connection)
        elif choice == '2':
             session_id = int(input('Enter Session ID: '))
             print()
             modS.lookup(connection, session_id)
        elif choice == '3':
             session_data = (
                int(input("Enter Event ID: ")),
                input("Enter Session Title: "),
                input("Enter Session Description: "),
                input("** MUST BE EXACT FORMAT: YYYY-MM-DD HH:MM:SS\n**Time is based on Military Time**\nEnter Session Start Date and Time: "),
                input("** MUST BE EXACT FORMAT: YYYY-MM-DD HH:MM:SS\n**Time is based on Military Time**\nEnter Session End Date and Time: "),
            )
             modS.add(connection, session_data)
        elif choice == '4':
             session_id = int(input('Enter Session ID: '))
             print()
             modS.delete(connection, session_id)
        elif choice == '5':
             session_id = int(input('Enter Session ID: '))
             session_data = (
                int(input("Enter Event ID: ")),
                input("Enter Session Title: "),
                input("Enter Session Description: "),
                input("** MUST BE EXACT FORMAT: YYYY-MM-DD HH:MM:SS\n**Time is based on Military Time**\nEnter Session Start Date and Time: "),
                input("** MUST BE EXACT FORMAT: YYYY-MM-DD HH:MM:SS\n**Time is based on Military Time**\nEnter Session End Date and Time: "),
            )
             print()
             modS.modify(connection, session_id, session_data)
             
        elif choice == '0':
             print("Exiting the Database Explorer.")
             break
        else:
             print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()