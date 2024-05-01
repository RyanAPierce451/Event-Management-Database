import mysql.connector

def is_event_id_valid(connection, event_id):
    try:
        cursor = connection.cursor()

        # Check if the event_id exists in the database
        query = "SELECT COUNT(*) FROM event WHERE Event_id = %s"
        cursor.execute(query, (event_id,))
        count = cursor.fetchone()[0]

        return count > 0

    except mysql.connector.Error as err:
        print(f"Error checking Event ID: {err}")
        return False

# Function to add a event *WORKS*
def add(connection, event_data):
    try:
        cursor = connection.cursor()

        query = "SELECT MAX(Event_id) FROM event"
        cursor.execute(query)
        max_event_id = cursor.fetchone()[0]

        if max_event_id is None:
            # If the table is empty, start with event_id 1
            new_event_id = 1
        else:
            new_event_id = max_event_id + 1

        # Insert new event into the database
        query = "INSERT INTO event (Event_id, Event_title, Event_description, Event_start_datetime, Event_end_datetime, Event_tickets_sold, Venue_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (new_event_id, *event_data))
        connection.commit()
        print()
        print("Event added successfully.")

    except mysql.connector.Error as err:
        connection.rollback()
        print()
        print(f"Error adding event: {err}")

# Function to delete a event by ID *WORKS*
def delete(connection, event_id):
    try:
        cursor = connection.cursor()

        # Check if the event_id exists
        if not is_event_id_valid(connection, event_id):
            print("Event ID does not exist.")
            return

        # Delete event from the database
        query = "DELETE FROM event WHERE Event_id = %s"
        cursor.execute(query, (event_id,))
        connection.commit()
        print("Event deleted successfully.")

    except mysql.connector.Error as err:
        connection.rollback()
        print(f"Error deleting event: {err}")

# Function to modify a event by ID *WORKS*
def modify(connection, event_id, event_data):
    try:
        cursor = connection.cursor()

        # Check if the event_id exists
        if not is_event_id_valid(connection, event_id):
            print("Event ID does not exist.")
            return

        # Update event in the database
        query = "UPDATE event SET Event_title = %s, Event_description = %s, Event_start_datetime = %s, Event_end_datetime = %s, Event_tickets_sold = %s, Venue_id = %s  WHERE Event_id = %s"
        cursor.execute(query, (*event_data, event_id))
        connection.commit()
        print("Event modified successfully.")

    except mysql.connector.Error as err:
        connection.rollback()
        print(f"Error modifying Event: {err}")

# Function to lookup a event by ID *WORKS*
def lookup(connection, event_id):
    try:
        cursor = connection.cursor()

        # Fetch event information by ID
        query = "SELECT * FROM event WHERE Event_id = %s"
        cursor.execute(query, (event_id,))
        event = cursor.fetchone()

        if event:
            print(f"Event ID: {event[0]}")
            print(f"Event Title: {event[1]}")
            print(f"Event Description: {event[2]}")
            print(f"Event Start Date and Time: {event[3]}")
            print(f"Event End Date and Time: {event[4]}")
            print(f"Event Tickets Sold: {event[5]}")
            print(f"Venue ID: {event[6]}")
            print("\n")
        else:
            print("Event not found.")

    except mysql.connector.Error as err:
        print(f"Error retrieving event information: {err}")
