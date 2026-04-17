import sqlite3

# Connect to database
conn = sqlite3.connect("vehicle_rental.db")
cursor = conn.cursor()

# Create table
cursor.execute('''
CREATE TABLE IF NOT EXISTS vehicles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    type TEXT,
    price_per_day REAL,
    available INTEGER
)
''')
conn.commit()

# Add vehicle
def add_vehicle():
    name = input("Enter vehicle name: ")
    vtype = input("Enter vehicle type (Car/Bike): ")
    price = float(input("Enter price per day: "))

    cursor.execute("INSERT INTO vehicles (name, type, price_per_day, available) VALUES (?, ?, ?, 1)",
                   (name, vtype, price))
    conn.commit()
    print("Vehicle added successfully!\n")

# View vehicles
def view_vehicles():
    cursor.execute("SELECT * FROM vehicles")
    vehicles = cursor.fetchall()

    print("\n--- Vehicle List ---")
    for v in vehicles:
        status = "Available" if v[4] == 1 else "Rented"
        print(f"ID: {v[0]} | {v[1]} | {v[2]} | ₹{v[3]}/day | {status}")
    print()

# Rent vehicle
def rent_vehicle():
    vid = int(input("Enter vehicle ID to rent: "))

    cursor.execute("SELECT available FROM vehicles WHERE id=?", (vid,))
    result = cursor.fetchone()

    if result and result[0] == 1:
        cursor.execute("UPDATE vehicles SET available=0 WHERE id=?", (vid,))
        conn.commit()
        print("Vehicle rented successfully!\n")
    else:
        print("Vehicle not available!\n")

# Return vehicle
def return_vehicle():
    vid = int(input("Enter vehicle ID to return: "))

    cursor.execute("UPDATE vehicles SET available=1 WHERE id=?", (vid,))
    conn.commit()
    print("Vehicle returned successfully!\n")

# Menu
def menu():
    while True:
        print("===== Vehicle Rental System =====")
        print("1. Add Vehicle")
        print("2. View Vehicles")
        print("3. Rent Vehicle")
        print("4. Return Vehicle")
        print("5. Exit")

        choice = input("Enter choice: ")

        if choice == '1':
            add_vehicle()
        elif choice == '2':
            view_vehicles()
        elif choice == '3':
            rent_vehicle()
        elif choice == '4':
            return_vehicle()
        elif choice == '5':
            break
        else:
            print("Invalid choice!\n")

# Run program
menu()

# Close connection
conn.close()
