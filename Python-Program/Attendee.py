import mysql.connector
import modify_attendee as modA

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

def fetch_attendee_information(connection):
    try:
        cursor = connection.cursor()

        # Fetch attendee information
        query = "SELECT * FROM attendee"
        cursor.execute(query)
        attendees = cursor.fetchall()

        return attendees

    except mysql.connector.Error as err:
        print(f"Error retrieving attendee information: {err}")
        return []

def display_attendee_information(connection):
    attendee = fetch_attendee_information(connection)

    # Display attendee information
    for attendee in attendee:
        attendee_id, attendee_vendor_name, attendee_website = attendee

        print(f"Attendee ID: {attendee_id}")
        print(f"Attendee Vendor: {attendee_vendor_name}")
        print(f"Attendee Website: {attendee_website}")
        print("\n")

def main():

    connection = connect_to_database()
    if not connection:
        return

    while True:
        print("\nSelect an option:")
        print("1. Display All Attendee")
        print("2. Attendee ID Lookup")
        print("3. Add Attendee")
        print("4. Delete Attendee")
        print("5. Modify Attendee")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
             display_attendee_information(connection)
        elif choice == '2':
             attendee_id = int(input('Enter Attendee ID: '))
             print()
             modA.lookup(connection, attendee_id)
        elif choice == '3':
             attendee_data = (
                input("Enter Attendee Vendor: "),
                input("Enter Atetndee Website: "),
            )
             modA.add(connection, attendee_data)
        elif choice == '4':
             attendee_id = int(input('Enter Attendee ID: '))
             print()
             modA.delete(connection, attendee_id)
        elif choice == '5':
             attendee_id = int(input('Enter Attendee ID: '))
             attendee_data = (
                input("Enter Attendee Vendor: "),
                input("Enter Atetndee Website: "),
            )
             print()
             modA.modify(connection, attendee_id, attendee_data)
             
        elif choice == '0':
             print("Exiting the Database Explorer.")
             break
        else:
             print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()