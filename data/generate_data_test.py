import csv  # CSV file operations
import random  # Generating random values
import uuid  # Generate unique flight IDs
from datetime import datetime, timedelta  # Date and time operations

# List of IATA airport codes
IATA_CODES = ["LAX", "JFK", "SFO", "ORD", "DFW", "MIA", "SEA", "ATL", "DEN", "PHX"] 

# Function to generate random flight data
def generate_flight_data(num_rows):
    """
    Generates a list of flight data dictionaries with random values.
    
    Parameters:
    num_rows (int): Number of rows of flight data to generate.
    
    Returns:
    list: A list of dictionaries representing flight data.
    """
    data = []  # Initialize an empty list to store the generated flight data

    # Loop to generate each flight's data
    for _ in range(num_rows):
        # Generate a random flight ID
        flight_id = str(uuid.uuid4())[:8]

        # Randomly choose departure and arrival airports
        departure_airport = random.choice(IATA_CODES)
        arrival_airport = random.choice([code for code in IATA_CODES if code != departure_airport])

        # Randomly generate a future departure timestamp
        departure_timestamp = datetime.now() + timedelta(days=random.randint(0, 30), hours=random.randint(0, 23))

        # Random flight duration between 2 and 16 hours
        flight_duration = timedelta(hours=random.randint(2, 16))

        arrival_timestamp = departure_timestamp + flight_duration

        # 20% chance of a delay
        delay_time = random.randint(0, 300) if random.random() < 0.2 else 0 

        # Randomly decide if the flight is canceled (10% chance)
        cancelation = 1 if random.random() < 0.1 else 0  

        # Number of passengers between 150 and 300
        passengers = random.randint(150, 300)  

        # Dictionary with the generated flight data to the list
        data.append({
            'flight_id': flight_id,
            'departure_airport': departure_airport,
            'arrival_airport': arrival_airport,
            'departure_timestamp': departure_timestamp.strftime("%Y-%m-%dT%H:%M:%S"),  
            'arrival_timestamp': arrival_timestamp.strftime("%Y-%m-%dT%H:%M:%S"),  
            'delay_time': delay_time,
            'cancelation': cancelation,
            'passengers': passengers
        })

    return data  # Return the generated flight data list

# Save the flight data to a CSV file
def save_to_csv(filename, data):
    """
    Saves a list of dictionaries (flight data) to a CSV file.
    
    Parameters:
    filename (str): Name of the CSV file to save the data.
    data (list): List of dictionaries containing flight data.
    """
    with open(filename, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=data[0].keys())
        dict_writer.writeheader()  # Write the headers (column names)
        dict_writer.writerows(data)  # Write the rows of flight data

if __name__ == '__main__':
    num_rows = 10000  

    flight_data = generate_flight_data(num_rows)

    output_file = "flight_data_test.csv"  

    # Save the generated flight data to a CSV file
    save_to_csv(output_file, flight_data)

    print(f"Generated {num_rows} rows of flight data and saved to {output_file}")
