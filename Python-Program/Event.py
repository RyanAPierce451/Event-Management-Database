import mysql.connector
import modify_event as modE

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

def fetch_event_information(connection):
    try:
        cursor = connection.cursor()

        # Fetch event information
        query = "SELECT * FROM event"
        cursor.execute(query)
        events = cursor.fetchall()

        return events

    except mysql.connector.Error as err:
        print(f"Error retrieving event information: {err}")
        return []

def display_event_information(connection):
    events = fetch_event_information(connection)

    # Display event information
    for event in events:
        event_id, event_title, event_description, event_start_datetime, event_end_datetime, event_tickets_sold, venue_id = event

        print(f"Event ID: {event_id}")
        print(f"Event Title: {event_title}")
        print(f"Event Description: {event_description}")
        print(f"Event Start Date and Time: {event_start_datetime}")
        print(f"Event End Date and Time: {event_end_datetime}")
        print(f"Event Tickets Sold: {event_tickets_sold}")
        print(f"Venue ID: {venue_id}")
        print("\n")

def main():

    connection = connect_to_database()
    if not connection:
        return

    while True:
        print("\nSelect an option:")
        print("1. Display All Events")
        print("2. Event ID Lookup")
        print("3. Add Event")
        print("4. Delete Event")
        print("5. Modify Event")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
             display_event_information(connection)
        elif choice == '2':
             event_id = int(input('Enter Event ID: '))
             print()
             modE.lookup(connection, event_id)
        elif choice == '3':
             event_data = (
                input("Enter Event Title: "),
                input("Enter Event Description: "),
                input("** MUST BE EXACT FORMAT: YYYY-MM-DD HH:MM:SS\n**Time is based on Military Time**\nEnter Event Start Date & Time: "),
                input("** MUST BE EXACT FORMAT: YYYY-MM-DD HH:MM:SS\n**Time is based on Military Time**\nEnter Event End Date & Time: "),
                int(input("Enter Tickets Sold: ")),
                int(input("Enter Venue ID: ")),
            )
             modE.add(connection, event_data)
        elif choice == '4':
             event_id = int(input('Enter Event ID: '))
             print()
             modE.delete(connection, event_id)
        elif choice == '5':
             event_id = int(input('Enter Event ID: '))
             event_data = (
                input("Enter Event Title: "),
                input("Enter Event Description: "),
                input("** MUST BE EXACT FORMAT: YYYY-MM-DD HH:MM:SS\n**Time is based on Military Time**\nEnter Event Start Date & Time: "),
                input("** MUST BE EXACT FORMAT: YYYY-MM-DD HH:MM:SS\n**Time is based on Military Time**\nEnter Event End Date & Time: "),
                int(input("Enter Tickets Sold: ")),
                int(input("Enter Venue ID: ")),
            )
             print()
             modE.modify(connection, event_id, event_data)
             
        elif choice == '0':
             print("Exiting the Database Explorer.")
             break
        else:
             print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()