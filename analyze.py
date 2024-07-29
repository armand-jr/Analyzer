import sys
import json
import datetime
from collections import Counter, defaultdict


#keywords
incassos = ['incassobureau', 'incasso bureau', 'groot & evers', 'van der Velde en van Hal', 'graydon incasso',
            'ultimoo', 'flanderijn ', 'collactivebmk', 'bierens ', ' avi ', 'syncasso', 'straetus', 'ggn mastering', 
            'vesting', 'debtt ', 'Gerechtsdeurwaarder', 'deurwaarder', 'korenhof', 'kbkp', 'collect4u', 'actis', 'derdenbeslag', 
            'invorderings', 'bru incasso', 'hoist', ' bvcm', 'coeo incasso', 'intrum', 'alektum', 'hafkamp', 'atradius collections', 
            'lavg', 'intocash', 'intojuristen', 'steghuis', 'janssen & janssen', 'lindorff', 'credios', 'credifix', 'in-kas',
            'cannock','zuidweg ', 'debtco', 'jongerius', 'bazuin & partners', 'agin pranger', 'agin nederland', 'nl81abna0447354663', 'de schout ', 'caminada ',
            'Nationale Grote Club', 'trust krediet beheer', 'bvcm', 'Geerlings + Hofstede', 'debt recovery', 'debt collection agency', 'yards ', ' tkb', 'vd+p', 'call2collect',
            'juristo', 'inkassier', 'medicas bv', 'betaling dossier', 'infoscore collection', 'koning & de raadt', 'rezeev',
            'juresta', 'perfect incasso', 'dbo finance', 'credifixx', 'of london', 'bos incasso', 'ikinkbekman', 'bcde faktuur', 'plaggemars incasso', 'e legal', 'e-legal', 'dicore',
            'abc incasso', 'centraal invorderings bureau', 'invorderingbureau']
loterijen = ['toto igaming', 'casino', 'loterij', 'unibet', 'bitvavo', 'crypto', 'poker', 'coinbase', ' trekking', 'uab alternative payments', 'retrust ou', 
             'bet365', 'fpo nederland', 'fairplay', 'joi gaming', 'play north limited', 'skrill', 'pokerstars', 'bwin ', 'betfair', 
             'fair game software kft', 'damagi marketing solutions', 'kansino', 'revoapps', 'lotterie','pokerstars', 'lottery', 'vof brouwer en keet', 'merkur casino',
             'fair play casino', 'kraken ', 'google play store by globalcollect', '711 bv', 'optdeck service limited']
financierders = ['youlend', 'yl limited', 'qeld', 'qredits', 'qred ', 'floryn', 'mkb krediet nederland', 'mollie capital', 'collin crowdfund',
                  'swishfund', 'funding circle', 'findio', 'new10', 'dutchfinance', ' regeling', 'bondora', 'capital circle b.v.',
                  'yl iv limited', 'yeaz', 'nordiska', 'capitalbox', 'rabobank zakelijk financieren', 'opr-finance', 'bedrijfslening', 'crowdfund', 'european merchant finance',
                  'geldvoorelkaar', 'betalingsregeling']
policy = ['coffeeshop']

# check for correct usage
if len(sys.argv) < 2:
    print("Usage: python3 script.py <filename> (<account_holder>)")
    sys.exit(1)

filename = sys.argv[1]
current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
yearago = datetime.datetime.now() - datetime.timedelta(days=370)

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
        count_storno = 0
        storno_amount = 0
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
                    doublename = name + original_name
                    search_text = f"{description} {name} {original_name}"
                    storno_desc = f"{description} {name}"
                    storneringen.append((storno_desc, amount))
                     


                # Belasting dienst uitgaven
                if 'belastingdienst' in name and amount < 0:
                    if transaction_id not in processed_id:
                        processed_id.add(transaction_id)
                        bd_uit += amount
                        #print (f"{amount:.0f} --- BD uitgave - {date}")
                        if amount in duplicate_bd:
                            #and date > (datetime.datetime.now() - datetime.timedelta(days=90)).strftime('%Y-%m-%d')
                            duplicate_bd[amount] += 1
                        else:
                            duplicate_bd[amount] = 1
                        


                # BD teruggaven
                if 'belastingdienst' in name and 'teruggaaf'  or 'teveelbet' in description:
                    if transaction_id not in processed_id:
                        processed_id.add(transaction_id)
                        bd_terug += amount
                        #print(f"{amount:.0f} --- BD teruggave - {date}") 


                #print(search_text)
                if len(sys.argv) == 3:
                    account_holder = sys.argv[2]
                    if account_holder.lower()  in doublename:
                        if transaction_id not in processed_id and date > yearago.strftime('%Y-%m-%d'):
                            prive_sum += amount
                            processed_id.add(transaction_id)
                        # "priverekening" mist nog


                for keyword in financierders:
                    if keyword.lower() in search_text and amount > 0:
                        #check duplicates
                        if transaction_id not in processed_id:
                            processed_id.add(transaction_id)
                            fin_sum += amount
                            print(f"{amount} --- {keyword} (+ Financiering) - {date} ")
                    if keyword.lower() in search_text and amount < 0:
                        #check duplicates
                        if transaction_id not in processed_id:
                            processed_id.add(transaction_id)
                            pay_fin += amount
                            print(f"{amount} --- {keyword} (- Financiering) - {date} ")
  

                for keyword in incassos:
                    if keyword.lower() in search_text and  'centraal justitieel incassobureau' not in search_text:
                        #check duplicates
                        if transaction_id not in processed_id and amount < 0:
                            incasso_sum += amount
                            processed_id.add(transaction_id)
                            print(f"{amount:.0f} --- {keyword} (Incasso) - {date}")

                # Check for loterijen keywords
                for keyword in loterijen:
                    if keyword.lower() in search_text:
                        #check duplicates
                        if transaction_id not in processed_id and amount < 0:
                            processed_id.add(transaction_id)
                            loterijen_sum += amount
                            print(f"{amount:.0f} --- {keyword} (Loterij) - {date} ")
        
                #check for stornos 


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

        for amount, count in duplicate_bd.items():
            if count > 2 and amount < -70: 
                print(f"{amount} --- BD uitgave - {count} keer")
            elif amount in [-500, -1000, -1500, -2000, -2500, -3000, -3500, -4000, -4500, -5000, -5500, -6000, -6500, -7000, -7500, -8000, -10000, -15000, -20000, -25000, -30000]:
                print(f"{amount} --- BD uitgave - {count} keer")
        print("\n")
        print(" --- Storneringen --- ")
        print(count_storno)


except FileNotFoundError:
    print(f"Error: File not found '{filename}'")
