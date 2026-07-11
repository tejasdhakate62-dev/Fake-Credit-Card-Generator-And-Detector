import os
import random
import urllib.request
import json
from datetime import datetime, timedelta
from flask import Flask, request, jsonify

app = Flask(__name__)

def luhn_checksum_valid(card_number: str) -> bool:
    """Validates the card number structure using the Luhn Algorithm."""
    digits = [int(d) for d in card_number]
    checksum = 0
    reverse_digits = digits[::-1]
    for i, digit in enumerate(reverse_digits):
        if i % 2 == 1:
            doubled = digit * 2
            if doubled > 9:
                doubled -= 9
            checksum += doubled
        else:
            checksum += digit
    return checksum % 10 == 0

def calculate_luhn_check_digit(partial: str) -> str:
    """Calculates the correct check digit to make the number Luhn-valid."""
    checksum = 0
    for k, char in enumerate(reversed(partial)):
        digit = int(char)
        if (k + 1) % 2 == 1:
            doubled = digit * 2
            if doubled > 9:
                doubled -= 9
            checksum += doubled
        else:
            checksum += digit
    d = (10 - (checksum % 10)) % 10
    return str(d)

def generate_card_number(network: str) -> str:
    """Generates a valid card number passing Luhn algorithm for a specific network."""
    if network == "Visa":
        prefix = "4"
        length = 16
    elif network == "Mastercard":
        prefix = str(random.choice([51, 52, 53, 54, 55] + list(range(2221, 2721))))
        length = 16
    elif network == "American Express":
        prefix = random.choice(["34", "37"])
        length = 15
    elif network == "Discover":
        prefix = random.choice(["6011", "65"] + [str(x) for x in range(644, 650)])
        length = 16
    elif network == "JCB":
        prefix = str(random.randint(3528, 3589))
        length = 16
    elif network == "Diners Club":
        prefix = random.choice(["36", "38"] + [str(x) for x in range(300, 306)])
        length = 14
    elif network == "RuPay":
        prefix = random.choice(["60", "81", "82", "508"])
        length = 16
    else:
        prefix = "4"
        length = 16
        
    needed = length - len(prefix) - 1
    partial = prefix + "".join(str(random.randint(0, 9)) for _ in range(needed))
    check_digit = calculate_luhn_check_digit(partial)
    return partial + check_digit

def get_random_name_from_api() -> str:
    """Fetches a random name from the RandomUser API, with a local fallback dataset of 10,000+ combinations."""
    try:
        url = "https://randomuser.me/api/?inc=name&nat=us,gb,ca"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=1.5) as response:
            data = json.loads(response.read().decode('utf-8'))
            results = data.get('results', [])
            if results:
                name_info = results[0].get('name', {})
                first = name_info.get('first', '').upper()
                last = name_info.get('last', '').upper()
                if first and last:
                    return f"{first} {last}"
    except Exception:
        pass
    
    # Offline local fallback dataset (100 first names x 100 last names = 10,000 unique combinations)
    first_names = [
        "JOHN", "JANE", "ALEX", "EMILY", "DAVID", "SARAH", "MICHAEL", "JESSICA", "ROBERT", "LISA",
        "JAMES", "MARY", "WILLIAM", "PATRICIA", "RICHARD", "JENNIFER", "JOSEPH", "ELIZABETH", "THOMAS", "LINDA",
        "CHARLES", "BARBARA", "CHRISTOPHER", "SUSAN", "DANIEL", "MARGARET", "MATTHEW", "DOROTHY", "ANTHONY", 
        "MARK", "NANCY", "DONALD", "KAREN", "STEVEN", "BETTY", "PAUL", "HELEN", "ANDREW", "SANDRA",
        "JOSHUA", "DONNA", "KENNETH", "CAROL", "KEVIN", "RUTH", "BRIAN", "SHARON", "GEORGE", "MICHELLE",
        "TIMOTHY", "LAURA", "RONALD", "EDWARD", "KIMBERLY", "JASON", "DEBORAH", "JEFFREY", 
        "RYAN", "SHIRLEY", "JACOB", "CYNTHIA", "GARY", "ANGELA", "NICHOLAS", "MELISSA", "ERIC", "BRENDA",
        "JONATHAN", "AMY", "STEPHEN", "ANNA", "LARRY", "REBECCA", "JUSTIN", "VIRGINIA", "SCOTT", "KATHLEEN",
        "BRANDON", "PAMELA", "FRANK", "MARTHA", "BENJAMIN", "DEBRA", "GREGORY", "AMANDA", "SAMUEL", "STEPHANIE",
        "RAYMOND", "CAROLYN", "PATRICK", "CHRISTINE", "ALEXANDER", "MARIE", "JACK", "JANET", "DENNIS", "CATHERINE"
    ]
    last_names = [
        "SMITH", "DOE", "JOHNSON", "WILLIAMS", "BROWN", "JONES", "GARCIA", "MILLER", "DAVIS", "RODRIGUEZ",
        "MARTINEZ", "HERNANDEZ", "LOPEZ", "GONZALEZ", "WILSON", "ANDERSON", "THOMAS", "TAYLOR", "MOORE", "JACKSON",
        "MARTIN", "LEE", "PEREZ", "THOMPSON", "WHITE", "HARRIS", "SANCHEZ", "CLARK", "RAMIREZ", "LEWIS",
        "ROBINSON", "WALKER", "YOUNG", "ALLEN", "KING", "WRIGHT", "SCOTT", "TORRES", "NGUYEN", "HILL",
        "FLORES", "GREEN", "ADAMS", "NELSON", "BAKER", "HALL", "RIVERA", "CAMPBELL", "MITCHELL", "CARTER",
        "ROBERTS", "GOMEZ", "PHILLIPS", "EVANS", "TURNER", "DIAZ", "PARKER", "CRUZ", "EDWARDS", "COLLINS",
        "REYES", "STEWART", "MORRIS", "MORALES", "MURPHY", "COOK", "ROGERS", "GUTIERREZ", "ORTIZ", "MORGAN",
        "COOPER", "PETERSON", "BAILEY", "REED", "KELLY", "HOWARD", "RAMOS", "KIM", "COX", "WARD",
        "RICHARDSON", "WATSON", "BROOKS", "CHAVEZ", "WOOD", "BENNETT", "GRAY", "MENDOZA", "RUIZ",
        "HUGHES", "PRICE", "ALVAREZ", "CASTILLO", "SANDERS", "PATEL", "MYERS", "LONG", "ROSS", "FOSTER"
    ]
    return f"{random.choice(first_names)} {random.choice(last_names)}"

def generate_mock_card_details(network: str) -> dict:
    """Generates mock, valid card details (number, name, expiry, CVV)."""
    card_number = generate_card_number(network)
    name = get_random_name_from_api()
    
    now = datetime.now()
    months_add = random.randint(24, 60)
    expiry_date = now + timedelta(days=months_add * 30)
    expiry = expiry_date.strftime("%m/%y")
    
    cvv_len = 4 if network == "American Express" else 3
    cvv = "".join(str(random.randint(0, 9)) for _ in range(cvv_len))
    
    return {
        "card_number": card_number,
        "cardholder_name": name,
        "expiry": expiry,
        "cvv": cvv,
        "network": network
    }

def verify_card_details(card_number: str) -> dict:
    """
    Performs verification on card length, network rules, and math architecture.
    """
    length = len(card_number)
    if not card_number.isdigit():
        return {"status": "fake", "message": "❌ INVALID: Input must contain numbers only."}
    
    # Identify network and length constraints
    network = None
    is_length_valid = False
    
    if card_number.startswith('4'):
        network = "Visa"
        is_length_valid = length in [13, 16, 19]
    elif card_number.startswith(('34', '37')):
        network = "American Express"
        is_length_valid = (length == 15)
    elif card_number.startswith(('51', '52', '53', '54', '55')) or (2221 <= int(card_number[:4]) <= 2720 if len(card_number) >= 4 and card_number[:4].isdigit() else False):
        network = "Mastercard"
        is_length_valid = (length == 16)
    elif card_number.startswith(('6011', '65')) or (622126 <= int(card_number[:6]) <= 622925 if len(card_number) >= 6 and card_number[:6].isdigit() else False) or card_number.startswith(('644', '645', '646', '647', '648', '649')):
        network = "Discover"
        is_length_valid = length in [16, 19]
    elif len(card_number) >= 4 and (3528 <= int(card_number[:4]) <= 3589 if card_number[:4].isdigit() else False):
        network = "JCB"
        is_length_valid = 16 <= length <= 19
    elif card_number.startswith(('36', '38', '309')) or (len(card_number) >= 3 and (300 <= int(card_number[:3]) <= 305 if card_number[:3].isdigit() else False)):
        network = "Diners Club"
        is_length_valid = 14 <= length <= 19
    elif card_number.startswith(('60', '81', '82')) or (len(card_number) >= 4 and (6521 <= int(card_number[:4]) <= 6522 if card_number[:4].isdigit() else False)) or card_number.startswith('508'):
        network = "RuPay"
        is_length_valid = (length == 16)
    else:
        return {"status": "fake", "message": "❌ FAKE: Unrecognized routing profile / fake network prefix."}

    if not is_length_valid:
        return {"status": "fake", "message": f"❌ FAKE: Invalid layout. A real {network} card cannot be {length} digits long."}

    if not luhn_checksum_valid(card_number):
        return {"status": "fake", "message": f"❌ FAKE: Failed structural validation. This {network} pattern is mathematically impossible."}

    return {
        "status": "valid", 
        "message": f"✅ VERIFIED: Structurally sound {network} card profile.",
        "network": network
    }

@app.route('/')
def home():
    """Serves the main frontend page."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(base_dir, 'templates', 'index.html')
    
    if os.path.exists(html_path):
        with open(html_path, 'r', encoding='utf-8') as file:
            return file.read()
    else:
        return """
        <div style="font-family:sans-serif; padding:20px; color:#dc2626;">
            <h3>Error: Could not find index.html</h3>
            <p>Please ensure your file is inside the 'templates' folder and named exactly 'index.html'.</p>
        </div>
        """

@app.route('/validate', methods=['POST'])
def validate():
    data = request.get_json() or {}
    raw_card_number = data.get('card_number', '')
    
    clean_number = raw_card_number.replace(" ", "").replace("-", "")
    result = verify_card_details(clean_number)
    return jsonify(result)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json() or {}
    network = data.get('network', 'Visa')
    
    valid_networks = ["Visa", "Mastercard", "American Express", "Discover", "JCB", "Diners Club", "RuPay"]
    if network not in valid_networks:
        network = "Visa"
        
    result = generate_mock_card_details(network)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)