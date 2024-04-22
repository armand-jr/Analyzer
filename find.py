import sys

# Ensure that the script is run with a file argument
if len(sys.argv) < 2:
    print("Usage: python script.py <filename>")
    sys.exit(1)

filename = sys.argv[1]

try:
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()  # Remove any leading/trailing whitespace
            if line.startswith(':61:'):
                # Extract everything after ':86:'
                description = line[4:].strip()
                print(description)
            
            if line.startswith(':86:'):
                #Extract and store transaction description
                name = line[4:].strip()
                print(name)
                

except FileNotFoundError:
    print(f"Error: File not found '{filename}'")
except Exception as e:
    print(f"An error occurred: {e}")

""" 
def parse_mt940(filename):
    transactions = []  # to store transaction details

    with open(filename, 'r') as file:
        lines = file.readlines()

    current_transaction = {}
    for line in lines:
        line = line.strip()  # Remove any leading/trailing whitespace

        if line.startswith(':86:'):
            # Extract everything after ':86:'
            description = line[4:].strip()
            current_transaction['Description'] = description

        if line.startswith(':62F:'):
            # Extract the amount after 'EUR'
            amount_pos = line.find('EUR')
            if amount_pos != -1:
                # Get the amount by finding the next space after 'EUR'
                amount = line[amount_pos+3:].strip()
                current_transaction['Amount'] = amount
                # Save the transaction and prepare for the next
                transactions.append(current_transaction)
                current_transaction = {}  # Reset for next transaction

    return transactions

# Example usage

transactions = parse_mt940(filename)
for transaction in transactions:
    print(transaction)

"""