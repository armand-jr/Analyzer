import sys

if len(sys.argv) < 2:
    print("Usage: python3 find.py <filename>")
    sys.exit(1)

incassos = ['casso']

filename = sys.argv[1]

try:
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()  # Remove whitespace
            if line.startswith(':61:'):
                if 'C' in line:
                    parts = line.split('C')
                    transaction_type = '+'
                if 'D' in line:
                    parts = line.split('D')
                    transaction_type = '-'
                
                if len(parts) > 1:
                    # Extract the amount
                    amount_part = parts[1]
                    amount = amount_part.split('N')[0].strip()
                    print(f"{transaction_type}{amount.strip()}")
                    
            
            
            if line.startswith(':86:'):
                #Extract and store transaction description
                name = line[5:].strip()
                print(name)
            

except FileNotFoundError:
    print(f"Error: File not found '{filename}'")
except Exception as e:
    print(f"An error occurred: {e}")
