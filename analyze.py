import sys
import json
import datetime

#keywords
incassos = [ 'incassobureau', 'incasso bureau', 'groot & evers', 'van der Velde en van Hal', 
            'ultimoo', 'flanderijn ', 'collactivebmk', 'bierens ', 'avi ', 'syncasso', 'straetus', 'ggn ', 
            'vesting', 'debtt ', 'Gerechtsdeurwaarder', 'deurwaarder', 'korenhof', 'kbkp', 'collect4u', 'actis', 'derdenbeslag', 
            'invorderings', ' bru ', 'hoist', ' bvcm', 'coeo incasso', 'intrum', 'alektum', 'hafkamp', 'atradius', 
            'lavg', 'intocash', 'intojuristen', 'steghuis', 'janssen & janssen', 'lindorff', 'credios', 'credifix', 'in-kas',
            'cannock ','zuidweg ', 'debtco', 'jongerius', 'bazuin & partners', 'agin pranger', 'nl81abna0447354663', 'de schout ', 'caminada ',
            'Nationale Grote Club', 'trust krediet beheer', 'bvcm', 'Geerlings + Hofstede', 'debt recovery', 'debt collection agency', 'yards ', ' tkb', 'vd+p', 'call2collect',
            'juristo', 'inkassier', 'medicas bv', 'betaling dossier', 'infoscore collection', 'koning & de raadt', 'betalingsregeling', 'graydon incasso', 'rezeev',
            'juresta']
loterijen = ['toto igaming', 'casino', 'loterij', 'unibet', 'bitvavo', 'crypto', 'poker', 'coinbase', ' trekking', 'uab alternative payments', 'retrust ou', 
             'bet365', 'fpo nederland', 'fairplay', 'joi gaming', 'play north limited', 'skrill', 'pokerstars', 'bwin ', 'betfair', 
             'fair game software kft', 'damagi marketing solutions', 'kansino', 'revoapps', 'lotterie','pokerstars', 'lottery']
financierders = ['youlend', 'yl limited', 'trustly', 'qredits', 'qred', 'floryn', 'online payment platform', 'collin crowdfund',
                  'swishfund', 'funding circle', 'findio', 'new10', 'dutchfinance', ' regeling', 'bondora', 'bedrijfslening', 
                  'yl iv limited', 'yeaz', 'nordiska', 'trustly group', 'capitalbox', 'rabobank zakelijk financieren']

policy = ['coffeeshop']

# check for correct usage
if len(sys.argv) < 2:
    print("Usage: python3 script.py <filename> (<account_holder>)")
    sys.exit(1)

filename = sys.argv[1]
current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
yearago = datetime.datetime.now() - datetime.timedelta(days=366)

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



        #transactions = data.get('transactions', [])
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


                if 'belastingdienst' in name and amount < 0:
                    if transaction_id not in processed_id:
                        processed_id.add(transaction_id)
                        bd_uit += amount
                        print(f"{amount:.0f} --- BD uitgave - {date}")
                        duplicate_bd = {}
                        if amount in duplicate_bd:
                            counter_bd += 1


                if 'belastingdienst' in name and 'teruggaaf' in description:
                    if transaction_id not in processed_id:
                        processed_id.add(transaction_id)
                        bd_terug += amount
                        print(f"{amount:.0f} --- BD teruggave - {date}") 


                #print(search_text)
                if len(sys.argv) == 3:
                    account_holder = sys.argv[2]   
                    if account_holder.lower() or "priverekening" in name:
                        prive_sum += amount
                        #print(f"{amount:.0f} --- Account holder: {account_holder} (Prive) {transaction_id}")      


                for keyword in financierders:
                    if keyword.lower() in search_text and amount > 0:
                        #check duplicates
                        if transaction_id not in processed_id:
                            processed_id.add(transaction_id)
                            fin_sum += amount
                    if keyword.lower() in search_text and amount < 0:
                        #check duplicates
                        if transaction_id not in processed_id:
                            processed_id.add(transaction_id)
                            pay_fin += amount
                            print(f"{amount:.0f} --- {keyword} (Financiering) - {date} ")
  
                for keyword in incassos:
                    if keyword.lower() in search_text and  'centraal justitieel incassobureau' not in search_text:
                        #check duplicates
                        if transaction_id not in processed_id:
                            incasso_sum += amount
                            processed_id.add(transaction_id)
                            print(f"{amount:.0f} --- {keyword} (Incasso) - {date}")

                # Check for loterijen keywords
                for keyword in loterijen:
                    if keyword.lower() in search_text:
                        #check duplicates
                        if transaction_id not in processed_id:
                            processed_id.add(transaction_id)
                            loterijen_sum += amount
                            print(f"{amount:.0f} --- {keyword} (Loterij) - {date} ")
        
        print("\n")
        print(f"incasso: {incasso_sum:.0f}")
        print(f"loterijen: {loterijen_sum:.0f}")
        print(f"prive: {prive_sum:.0f}")
        print(f"financierders: {fin_sum:.0f}")
        print(f"betalingen aan financierders: {pay_fin:.0f}")
        print(f"belastingdienst teruggave: {bd_terug:.0f}")
        print(f"belastingdienst uitgaven: {bd_uit:.0f}")
        print(counter_bd)
        print("\n")



except FileNotFoundError:
    print(f"Error: File not found '{filename}'")