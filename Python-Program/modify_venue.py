import mysql.connector

def is_venue_id_valid(connection, venue_id):
    try:
        cursor = connection.cursor()

        # Check if the event_id exists in the database
        query = "SELECT COUNT(*) FROM venue WHERE Venue_id = %s"
        cursor.execute(query, (venue_id,))
        count = cursor.fetchone()[0]

        return count > 0

    except mysql.connector.Error as err:
        print(f"Error checking Venue ID: {err}")
        return False

# Function to add a venue *WORKS*
def add(connection, venue_data):
    try:
        cursor = connection.cursor()

        query = "SELECT MAX(Venue_id) FROM venue"
        cursor.execute(query)
        max_venue_id = cursor.fetchone()[0]

        if max_venue_id is None:
            # If the table is empty, start with venue_id 1
            new_venue_id = 1
        else:
            new_venue_id = max_venue_id + 1

        # Insert new venue into the database
        query = "INSERT INTO venue (Venue_id, Venue_name, Venue_capacity, Venue_amenities, Venue_availability) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (new_venue_id, *venue_data))
        connection.commit()
        print()
        print("Venue added successfully.")

    except mysql.connector.Error as err:
        connection.rollback()
        print()
        print(f"Error adding venue: {err}")

# Function to delete a venue by ID *WORKS*
def delete(connection, venue_id):
    try:
        cursor = connection.cursor()

        # Check if the venue_id exists
        if not is_venue_id_valid(connection, venue_id):
            print("Venue ID does not exist.")
            return

        # Delete venue from the database
        query = "DELETE FROM venue WHERE Venue_id = %s"
        cursor.execute(query, (venue_id,))
        connection.commit()
        print("Venue deleted successfully.")

    except mysql.connector.Error as err:
        connection.rollback()
        print(f"Error deleting venue: {err}")

# Function to modify a venue by ID *WORKS*
def modify(connection, venue_id, venue_data):
    try:
        cursor = connection.cursor()

        # Check if the venue_id exists
        if not is_venue_id_valid(connection, venue_id):
            print("Venue ID does not exist.")
            return

        # Update venue in the database
        query = "UPDATE venue SET Venue_name = %s, Venue_capacity = %s, Venue_amenities = %s, Venue_availability = %s WHERE Venue_id = %s"
        cursor.execute(query, (*venue_data, venue_id))
        connection.commit()
        print("Venue modified successfully.")

    except mysql.connector.Error as err:
        connection.rollback()
        print(f"Error modifying venue: {err}")

# Function to lookup a venue by ID *WORKS*
def lookup(connection, venue_id):
    try:
        cursor = connection.cursor()

        # Fetch venue information by ID
        query = "SELECT * FROM venue WHERE Venue_id = %s"
        cursor.execute(query, (venue_id,))
        venue = cursor.fetchone()

        if venue:
            print(f"Venue ID: {venue[0]}")
            print(f"Venue Name: {venue[1]}")
            print(f"Venue Capacity: {venue[2]}")
            print(f"Venue Amenities: {venue[3]}")
            print(f"Venue Availability: {venue[4]}")
            print("\n")
        else:
            print("Venue not found.")

    except mysql.connector.Error as err:
        print(f"Error retrieving venue information: {err}")
