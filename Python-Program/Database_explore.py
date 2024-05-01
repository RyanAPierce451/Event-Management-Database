import mysql.connector
import Venue as venue
import Event as event
import Session as session
import Speaker as speaker
import Ticket as ticket
import Attendee as attendee

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
        print("Connected to the database.")
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to the database: {err}")
        return None

def main():
    print("Welcome to the Event Managment Database Explorer!")

    while True:
        print("\nSelect an option:")
        print("1. Explore Venue Information")
        print("2. Explore Event Information")
        print("3. Explore Session Information")
        print("4. Explore Speaker Information")
        print("5. Explore Ticket Information")
        print("6. Explore Attendee Information")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            venue.main()
        elif choice == '2':
            event.main()
        elif choice == '3':
            session.main()
        elif choice == '4':
            speaker.main()
        elif choice == '5':
            ticket.main()
        elif choice == '6':
            attendee.main()
        elif choice == '0':
            print("Exiting the Database Explorer.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
