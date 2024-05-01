import mysql.connector


def validate_venue_capacity(connection, event_tickets_sold, event_id, ticket_quantity):
    try:
        cursor = connection.cursor()

        # Fetch venue_capacity from the venue table using a join with the event table
        query = "SELECT v.Venue_capacity FROM venue v JOIN event e ON v.Venue_id = e.Venue_id WHERE e.Event_id = %s"
        cursor.execute(query, (event_id,))
        venue_capacity = cursor.fetchone()[0]

        # Check if the total ticket quantity does not exceed the venue_capacity
        if ticket_quantity > venue_capacity:
            print("Error: Ticket quantity cannot exceed the venue capacity.")
            return False
        
        if event_tickets_sold >= venue_capacity:
            print("Error: Ticket quantity cannot exceed the venue capacity.")
            return False

        return True


    except mysql.connector.Error as err:
        print(f"Error validating venue capacity: {err}")
        return False

def update_event_tickets_sold(connection, event_id, new_tickets_sold):
    try:
        cursor = connection.cursor()

        # Update the Event_tickets_sold in the event table
        query = "UPDATE event SET Event_tickets_sold = %s WHERE Event_id = %s"
        cursor.execute(query, (new_tickets_sold, event_id))
        connection.commit()
        print("Event tickets sold updated successfully.")

    except mysql.connector.Error as err:
        connection.rollback()
        print(f"Error updating event tickets sold: {err}")

def is_ticket_id_valid(connection, ticket_id):
    try:
        cursor = connection.cursor()

        # Check if the ticket_id exists in the database
        query = "SELECT COUNT(*) FROM ticket WHERE Ticket_id = %s"
        cursor.execute(query, (ticket_id,))
        count = cursor.fetchone()[0]

        return count > 0

    except mysql.connector.Error as err:
        print(f"Error checking Ticket ID: {err}")
        return False

# Function to add a ticket *WORKS*
def add(connection, event_id, attendee_id, ticket_type, ticket_price, ticket_quantity):
    try:
        cursor = connection.cursor()

        query = "SELECT MAX(Ticket_id) FROM ticket"
        cursor.execute(query)
        max_ticket_id = cursor.fetchone()[0]

        if max_ticket_id is None:
            # If the table is empty, start with ticket_id 1
            new_ticket_id = 1
        else:
            new_ticket_id = max_ticket_id + 1
        
        # Fetch Event_tickets_sold for the specified event_id
        query = "SELECT Event_tickets_sold FROM event WHERE Event_id = %s"
        cursor.execute(query, (event_id,))
        event_tickets_sold = cursor.fetchone()
        res = ""
        for i in event_tickets_sold:
            res+=str(i)
        event_tickets_sold = int(res)

        # Validate ticket_quantity against venue_capacity
        if not validate_venue_capacity(connection, event_tickets_sold, event_id, ticket_quantity):
            return

        # Insert new ticket into the database
        query = "INSERT INTO ticket (Ticket_id, Event_id, Attendee_id, Ticket_type, Ticket_price, Ticket_quantity) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (new_ticket_id, event_id, attendee_id, ticket_type, ticket_price, ticket_quantity))
        connection.commit()
        print("Ticket added successfully.")

        # Update Event_tickets_sold in the event table
        query = "SELECT Event_tickets_sold FROM event WHERE Event_id = %s"
        cursor.execute(query, (event_id,))
        event_tickets_sold = cursor.fetchone()[0]

        new_tickets_sold = event_tickets_sold + ticket_quantity
        update_event_tickets_sold(connection, event_id, new_tickets_sold)

    except mysql.connector.Error as err:
        connection.rollback()
        print(f"Error adding ticket: {err}")

# Function to delete a ticket by ID *WORKS*
def delete(connection, ticket_id):
    try:
        cursor = connection.cursor()

        # Fetch ticket quantity for the ticket to be deleted
        query = "SELECT Ticket_quantity, Event_id FROM ticket WHERE Ticket_id = %s"
        cursor.execute(query, (ticket_id,))
        ticket_data = cursor.fetchone()

        if not ticket_data:
            print("Error: Ticket ID not found.")
            return

        ticket_quantity, event_id = ticket_data

        # Delete the ticket from the ticket table
        query = "DELETE FROM ticket WHERE Ticket_id = %s"
        cursor.execute(query, (ticket_id,))
        connection.commit()
        print("Ticket deleted successfully.")

        # Update Event_tickets_sold in the event table
        query = "SELECT Event_tickets_sold FROM event WHERE Event_id = %s"
        cursor.execute(query, (event_id,))
        event_tickets_sold = cursor.fetchone()[0]

        new_tickets_sold = event_tickets_sold - ticket_quantity
        update_event_tickets_sold(connection, event_id, new_tickets_sold)

    except mysql.connector.Error as err:
        connection.rollback()
        print(f"Error deleting ticket: {err}")

# Function to modify a ticket by ID *WORKS*
def modify(connection, ticket_id, event_id, attendee_id, ticket_type, ticket_price, ticket_quantity):
    try:
        cursor = connection.cursor()

        # Check if the ticket_id exists
        if not is_ticket_id_valid(connection, ticket_id):
            print("Ticket ID does not exist.")
            return

        # Fetch Event_tickets_sold for the specified event_id
        query = "SELECT Event_tickets_sold FROM event WHERE Event_id = %s"
        cursor.execute(query, (event_id,))
        event_tickets_sold = cursor.fetchone()
        res = ""
        for i in event_tickets_sold:
            res+=str(i)
        event_tickets_sold = int(res)

        # Fetch current ticket quantity for the ticket to be modified
        query = "SELECT Ticket_quantity, Event_id FROM ticket WHERE Ticket_id = %s"
        cursor.execute(query, (ticket_id,))
        ticket_data = cursor.fetchone()

        if not ticket_data:
            print("Error: Ticket ID not found.")
            return

        current_ticket_quantity, event_id = ticket_data

        # Calculate the net change in ticket quantity
        net_ticket_change = ticket_quantity - current_ticket_quantity

        # Validate ticket_quantity against event_tickets_sold and venue_capacity
        if not validate_venue_capacity(connection, event_tickets_sold, event_id, ticket_quantity):
            return

        # Update ticket in the database
        query = "UPDATE ticket SET Event_id = %s, Attendee_id = %s, Ticket_type = %s, Ticket_price = %s, Ticket_quantity = %s WHERE Ticket_id = %s"
        cursor.execute(query, (event_id, attendee_id, ticket_type, ticket_price, ticket_quantity, ticket_id))
        connection.commit()
        print("Ticket modified successfully.")

        # Update Event_tickets_sold in the event table
        query = "SELECT Event_tickets_sold FROM event WHERE Event_id = %s"
        cursor.execute(query, (event_id,))
        event_tickets_sold = cursor.fetchone()[0]

        new_tickets_sold = event_tickets_sold + net_ticket_change
        update_event_tickets_sold(connection, event_id, new_tickets_sold)

    except mysql.connector.Error as err:
        connection.rollback()
        print(f"Error modifying ticket: {err}")

# Function to lookup a ticket by ID *WORKS*
def lookup(connection, ticket_id):
    try:
        cursor = connection.cursor()

        # Fetch ticket information by ID
        query = "SELECT * FROM ticket WHERE Ticket_id = %s"
        cursor.execute(query, (ticket_id,))
        ticket = cursor.fetchone()

        if ticket:
            print(f"Ticket ID: {ticket[0]}")
            print(f"Event ID: {ticket[1]}")
            print(f"Attendee ID: {ticket[2]}")
            print(f"Ticket Type: {ticket[3]}")
            print(f"Ticket Price: {ticket[4]}")
            print(f"Ticket Quantity: {ticket[5]}")
            print("\n")
        else:
            print("Ticket not found.")

    except mysql.connector.Error as err:
        print(f"Error retrieving ticket information: {err}")
