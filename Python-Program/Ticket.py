import mysql.connector
import modify_ticket as modT

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

def fetch_ticket_information(connection):
    try:
        cursor = connection.cursor()

        # Fetch ticket information
        query = "SELECT * FROM ticket"
        cursor.execute(query)
        tickets = cursor.fetchall()

        return tickets

    except mysql.connector.Error as err:
        print(f"Error retrieving ticket information: {err}")
        return []

def display_ticket_information(connection):
    ticket = fetch_ticket_information(connection)

    # Display ticket information
    for ticket in ticket:
        ticket_id, event_id, attendee_id, ticket_type, ticket_price, ticket_quantity = ticket

        print(f"Ticket ID: {ticket_id}")
        print(f"Event ID: {event_id}")
        print(f"Attendee ID: {attendee_id}")
        print(f"Ticket Type: {ticket_type}")
        print(f"Ticket Price: {ticket_price}")
        print(f"Ticket Quantity: {ticket_quantity}")
        print("\n")

def main():

    connection = connect_to_database()
    if not connection:
        return

    while True:
        print("\nSelect an option:")
        print("1. Display All Tickets")
        print("2. Ticket ID Lookup")
        print("3. Add Ticket")
        print("4. Delete Ticket")
        print("5. Modify Ticket")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
             display_ticket_information(connection)
        elif choice == '2':
             ticket_id = int(input('Enter Ticket ID: '))
             print()
             modT.lookup(connection, ticket_id)
        elif choice == '3':
             event_id = int(input("Enter Event ID: "))
             attendee_id = int(input("Enter Attendee ID: "))
             ticket_type = input("Enter Ticket Type: ")
             ticket_price = float(input("**Have Two Decimal Spaces**\n**NO currency symbols*\n*Enter Ticket Price: "))
             ticket_quantity = int(input("Enter Ticket Quantity: "))
             modT.add(connection, event_id, attendee_id, ticket_type, ticket_price, ticket_quantity)
        elif choice == '4':
             ticket_id = int(input('Enter Ticket ID: '))
             print()
             modT.delete(connection, ticket_id)
        elif choice == '5':
             ticket_id = int(input('Enter Ticket ID: '))
             event_id = int(input("Enter Event ID: "))
             attendee_id = int(input("Enter Attendee ID: "))
             ticket_type = input("Enter Ticket Type: ")
             ticket_price = float(input("**Have Two Decimal Spaces**\n**NO currency symbols*\n*Enter Ticket Price: "))
             ticket_quantity = int(input("Enter Ticket Quantity: "))
             print()
             modT.modify(connection, ticket_id, event_id, attendee_id, ticket_type, ticket_price, ticket_quantity)
             5
        elif choice == '0':
             print("Exiting the Database Explorer.")
             break
        else:
             print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()