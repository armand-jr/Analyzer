import sys

#keywords
incassos = ['cjib ', 'incassobureau', 'incasso bureau', ' evers ', 'van der Velde en van Hal', 
            'ultimoo', 'flanderijn ', 'collactivebmk', 'bierens ', 'avi ', 'syncasso', 'straetus', 'ggn ', 
            'vesting', 'debtt', 'Gerechtsdeurwaarder', 'korenhof', 'kbkp', 'collect4u', 'actis', 'derdenbeslag', 
            'invorderings', ' bru ', 'hoist', ' bvcm', 'coeo incasso', 'intrum', 'alektum', 'hafkamp', 'atradius', 
            'lavg', 'intocash', 'intojuristen', 'steghuis', 'janssen en janssen', 'lindorff', 'credios', 'credifix', 'in-kas',
            'cannock','zuidweg', 'debtco', 'jongerius', 'bazuin & partners', 'agin pranger', 'nl81abna0447354663', 'de schout',
            'Nationale Grote Club', 'trust krediet beheer', 'bvcm']
loterijen = ['toto', 'casino', 'loterij', 'unibet', 'bitvavo', 'crypto', 'poker', 'coinbase', 'trekking', 'uab alternative payments', 'retrust ou', 
             'bet365', 'fpo nederland', 'fairplay', 'joi gaming', 'play north limited', 'skrill', 'pokerstars', 'bwin ', 'betfair', 
             'fair game software kft', 'damagi marketing solutions']

# check for correct usage
if len(sys.argv) < 2:
    print("Usage: python3 script.py <filename> (<account_holder>)")
    sys.exit(1)

filename = sys.argv[1]
#account_holder = sys.argv[2]

try:
    with open(filename, 'r') as file:
        transaction_amount = ''
        transaction_type = ''
        collecting_description = False
        description_lines = []
        
        for line in file:
            line = line.strip()
            if line.startswith(':61:'):
                # check if we need to process the previous transaction
                if collecting_description:
                    description = ' '.join(description_lines)
                    # check for keywords
                    for keyword in incassos + loterijen:
                        if keyword in description.lower():
                            print(f"{transaction_type}{transaction_amount} --- Keyword: {keyword}")
                    description_lines = []
                    collecting_description = False

                # process the new transaction
                transaction_type = '+' if 'C' in line else '-'
                parts = line.split('C' if 'C' in line else 'D')
                transaction_amount = parts[1].split(',')[0].strip()
            
            elif line.startswith(':86:'):
                collecting_description = True
                description_lines.append(line[4:].strip())  # start collecting the description from here

            elif collecting_description:
                description_lines.append(line)  # continue collecting the description


        # handle the last transaction in the file
        if collecting_description:
            description = ' '.join(description_lines)
            #print (description)
            for keyword in incassos + loterijen:
                if keyword in description.lower():
                    print(f"{transaction_type}{transaction_amount} -+- Keyword: {keyword}")

except FileNotFoundError:
    print(f"Error: File not found '{filename}'")
except Exception as e:
    print(f"An error occurred: {e}")
