import mysql.connector
import modify_venue as modV

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

def fetch_venue_information(connection):
    try:
        cursor = connection.cursor()

        # Fetch venue information
        query = "SELECT * FROM venue"
        cursor.execute(query)
        venues = cursor.fetchall()

        return venues

    except mysql.connector.Error as err:
        print(f"Error retrieving venue information: {err}")
        return []

def display_venue_information():
    connection = connect_to_database()

    if not connection:
        return

    venues = fetch_venue_information(connection)

    connection.close()
    print("Connection to the database closed.")

    # Display venue information
    for venue in venues:
        venue_id, venue_name, venue_capacity, venue_amenities, venue_availability = venue
        print(f"Venue ID: {venue_id}")
        print(f"Venue Name: {venue_name}")
        print(f"Venue Capacity: {venue_capacity}")
        print(f"Venue Amenities: {venue_amenities}")
        print(f"Venue Availability: {venue_availability}")
        print("\n")

def main():

    connection = connect_to_database()
    if not connection:
        return

    while True:
        print("\nSelect an option:")
        print("1. Display All Venues")
        print("2. Venue ID Lookup")
        print("3. Add Venue")
        print("4. Delete Venue")
        print("5. Modify Venue")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
             display_venue_information()
        elif choice == '2':
             venue_id = int(input('Enter Venue ID: '))
             print()
             modV.lookup(connection, venue_id)
        elif choice == '3':
             
             venue_data = (
                input("Enter Venue Name: "),
                int(input("Enter Venue Capacity: ")),
                input("Enter Venue Amenities: "),
                input("Enter Venue Availability: ")
            )
             modV.add(connection, venue_data)
        elif choice == '4':
             venue_id = int(input('Enter Venue ID: '))
             print()
             modV.delete(connection, venue_id)
        elif choice == '5':
             venue_id = int(input('Enter Venue ID: '))
             venue_data = (
                input("Enter Venue Name: "),
                int(input("Enter Venue Capacity: ")),
                input("Enter Venue Amenities: "),
                input("Enter Venue Availability: ")
            )
             print()
             modV.modify(connection, venue_id, venue_data)
             
        elif choice == '0':
             print("Exiting the Database Explorer.")
             break
        else:
             print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()