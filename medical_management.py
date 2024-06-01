from pymongo import MongoClient
from bson.objectid import ObjectId

# Initialize MongoDB Client
client = MongoClient('mongodb://localhost:27017/')
db = client['medical_management']
patients_collection = db['patients']

# Function to create a new patient record
def create_patient(name, age, medical_history):
    patient = {
        "name": name,
        "age": age,
        "medical_history": medical_history
    }
    result = patients_collection.insert_one(patient)
    print(f"Patient created with ID: {result.inserted_id}")

# Function to read patient records
def read_patients():
    patients = patients_collection.find()
    for patient in patients:
        print(patient)

# Function to update a patient record by ID
def update_patient(patient_id, name=None, age=None, medical_history=None):
    update_fields = {}
    if name:
        update_fields['name'] = name
    if age:
        update_fields['age'] = age
    if medical_history:
        update_fields['medical_history'] = medical_history

    result = patients_collection.update_one(
        {"_id": ObjectId(patient_id)},
        {"$set": update_fields}
    )
    if result.matched_count > 0:
        print(f"Patient with ID {patient_id} updated.")
    else:
        print(f"No patient found with ID {patient_id}.")

# Function to delete a patient record by ID
def delete_patient(patient_id):
    result = patients_collection.delete_one({"_id": ObjectId(patient_id)})
    if result.deleted_count > 0:
        print(f"Patient with ID {patient_id} deleted.")
    else: 
        print(f"No patient found with ID {patient_id}.")

# Main function to demonstrate CRUD operations
if __name__ == "__main__":
    while True:
        print("\nMedical Management System")
        print("1. Create Patient")
        print("2. Read Patients")
        print("3. Update Patient")
        print("4. Delete Patient")
        print("5. Exit")

        choice = input("Enter your choice: ")
        
        if choice == '1':
            name = input("Enter patient's name: ")
            age = int(input("Enter patient's age: "))
            medical_history = input("Enter patient's medical history: ")
            create_patient(name, age, medical_history)
        elif choice == '2':
            read_patients()
        elif choice == '3':
            patient_id = input("Enter patient ID to update: ")
            name = input("Enter new name (leave blank to keep unchanged): ")
            age = input("Enter new age (leave blank to keep unchanged): ")
            medical_history = input("Enter new medical history (leave blank to keep unchanged): ")
            update_patient(patient_id, name if name else None, int(age) if age else None, medical_history if medical_history else None)
        elif choice == '4':
            patient_id = input("Enter patient ID to delete: ")
            delete_patient(patient_id)
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")
