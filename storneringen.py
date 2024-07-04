import sys
import json
import datetime
from collections import Counter, defaultdict

# [Your existing keywords lists remain unchanged]

# check for correct usage
if len(sys.argv) < 2:
    print("Usage: python3 script.py <filename> (<account_holder>)")
    sys.exit(1)

filename = sys.argv[1]
current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
yearago = datetime.datetime.now() - datetime.timedelta(days=370)

def process_storneringen(storneringen):
    storno_count = defaultdict(int)
    storno_sum = defaultdict(float)
    
    for desc, amount in storneringen:
        storno_count[desc] += 1
        storno_sum[desc] += amount
    
    duplicates = {desc: (count, storno_sum[desc]) for desc, count in storno_count.items() if count > 1}
    return duplicates

try:
    with open(filename, 'r') as file:
        data = json.load(file)
        incasso_sum = 0
        loterijen_sum = 0
        fin_sum = 0
        pay_fin = 0
        prive_sum = 0
        bd_uit = 0
        bd_terug = 0
        counter_bd = 0
        processed_id = set()
        duplicate_bd = {}
        storneringen = []

        transactions = data.get('transactions', [])
        for account in data['accounts']:
            for transaction in account['transactions']:
                date = transaction.get('transactionDate', '').split('T')[0]
                transaction_id = transaction.get('id', '')

                if date > yearago.strftime('%Y-%m-%d'):
                    amount = transaction.get('amount', 0)
                    description = transaction.get('description', '').lower()
                    beneficiary = transaction.get('beneficiary', {})
                    name = beneficiary.get('name', '').lower()
                    original_name = beneficiary.get('originalName', '').lower()
                    date = transaction.get('transactionDate', '').split('T')[0]
                    search_text = f"{description} {name} {original_name}"
                    storno_desc = f"{description} {name}"
                    storneringen.append((storno_desc, amount))

                    # [Your existing transaction processing logic remains here]

        # Process storneringen
        storno_results = process_storneringen(storneringen)

        print("\n")
        print(f"incasso: {incasso_sum:.0f}")
        print(f"loterijen: {loterijen_sum:.0f}")
        print(f"prive: {prive_sum:.0f}")
        print(f"financierders: {fin_sum:.0f}")
        print(f"betalingen aan financierders: {pay_fin:.0f}")
        print(f"belastingdienst teruggave: {bd_terug:.0f}")
        print(f"belastingdienst uitgaven: {bd_uit:.0f}")
        print(counter_bd)
        print("\n --- Duplicates --- \n")
        print(duplicate_bd.items())

        for amount, count in duplicate_bd.items():
            if count > 1 and amount < -70: 
                print(f"{amount} --- BD uitgave - {count} keer")
            elif amount in [-500, -1000, -1500, -2000, -2500, -3000, -3500, -4000, -4500, -5000, -5500, -6000, -6500, -7000, -7500, -8000, -10000, -15000, -20000, -25000, -30000]:
                print(f"{amount} --- BD uitgave - {count} keer")
        
        print("\n --- Storneringen --- ")
        

        total_duplicate_amount = sum(amount for _, amount in storno_results.values())
        print(f"\nTotal amount of all duplicates: {total_duplicate_amount:.2f}")

except FileNotFoundError:
    print(f"Error: File not found '{filename}'")