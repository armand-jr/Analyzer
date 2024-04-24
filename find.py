import sys

if len(sys.argv) < 2:
    print("Usage: python3 find.py <filename>")
    sys.exit(1)

incassos = ['cjib ', 'Flanderijn ', 'Bierens ', 'Avi ', 'Syncasso', 'straetus', 'GGN ', 'Vesting', 'Debtt', 'Gerechtsdeurwaarder', 'korenhof', 'KBKP', 'Collect4u', 'Actis', 'derdenbeslag', 'invorderings', ' BRU ', 'Hoist', ' BVCM', 'coeo incasso', 'intrum', 'alektum']
loterijen = ['Toto', 'casino', 'loterij', 'unibet', 'Bitvavo', 'Crypto', ' bet ', 'poker', 'coinbase']

filename = sys.argv[1]
flag = False


try:
   with open(filename, 'r') as file:
        last_line = ''
        flag = False
        for line in file:
            line = line.strip()  
            if line.startswith(':61:'):
                if 'C' in line:
                    parts = line.split('C')
                    transaction_type = '+'
                if 'D' in line:
                    parts = line.split('D')
                    transaction_type = '-'
                
                if len(parts) > 1:
                    amount_part = parts[1]
                    amount = amount_part.split('N')[0].strip()
                last_line = f"{transaction_type}{amount.strip()}"
                flag = False
            
            if line.lower().startswith(':86:'):
                if any(word.lower() in line.lower() for word in incassos):
                    flag = True
                    name = line[5:].strip()
            
            if line.lower().startswith(':86:'):
                if any(word.lower() in line.lower() for word in loterijen):
                    flag = True
                    name = line[5:].strip()
            
            if flag:
                print(last_line)
                print(f"{name}")
                flag = False

            

except FileNotFoundError:
    print(f"Error: File not found '{filename}'")
except Exception as e:
    print(f"An error occurred: {e}")