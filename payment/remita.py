import time
import random
from datetime import datetime

lga_codes = [
    "ABD", "ASU", "BAM", "BYO", 
    "BIU", "CHK", "DAM", "DIK", 
    "GUB", "GZM", "GWZ", "HWL", 
    "JER", "KAG", "KBG", "KDG", 
    "KUK", "KKS", "MAF", "MAG", 
    "MMC", "MAR", "MOB", "MNG", 
    "NGL", "NGZ", "SHN" 
]

# Male Names (Including Christian Names)
male_names = [
    "Abba", "Abdullahi", "Abdulrahman", "Adamu", "Ahmed", "Ali", "Aminu", "Auwal", "Baba", "Bashir",
    "Bello", "Bukar", "Danlami", "Dikko", "Elijah", "Farouk", "Garba", "Goni", "Habib", "Hassan",
    "Hussein", "Ibrahim", "Idris", "Iliyasu", "Isa", "Ismail", "Jafar", "Jibril", "Kabir",
    "Kalli", "Kassim", "Kolo", "Lawal", "Mahmud", "Malam", "Mallam", "Mamman", "Mansur", "Modu",
    "Mohammed", "Muktar", "Mustapha", "Nafiu", "Nuhu", "Rabiu", "Ramalan", "Ramat", "Rashid",
    "Saadu", "Sadiq", "Salihu", "Shehu", "Shuaibu", "Sulaiman", "Sumaila", "Tambari", "Tanimu", "Umar",
    "Usaini", "Usman", "Yakubu", "Yunusa", "Zabiru", "Zakar", "Zanna", "Zubair", "Zubairu", "Babagana",
    "Babayo", "Bura", "Bulama", "Chindo", "Dala", "Dalhatu", "Fannami", "Gambo", "Gwoni", "Inuwa",
    "Kachalla", "Khadir", "Khalil", "Kyari", "Lawalli", "Lawan", "Limamin", "Maina", "Mallamti", "Mamuda",
    "Modibbo", "Mohd", "Muhammad", "Muhammed", "Muhammedu", "Ngarnoma", "Saleh", "Tijjani", "Zakari",
    "Abubakar", "Aliyu", "Ado", "Haruna", "Kasimu", "Alhaji", "Damian", "Galadima", "Jada", "Mudi",
    "Bukar", "Rufa’i", "Malami", "Wada", "Sumonu", "Sa’idu", "Ishaku", "Alhassan", "Abba", "Fannami",
    "Modu", "Bulama", "Birma", "Aji", "Limamin", "Malle", "Mairo", "Maishanu", "Dauda", "Bulus",
    "Daniel", "Simon", "Jacob", "John", "Emmanuel", "Moses", "Peter", "Sunday", "David", "Solomon",
    "Joseph", "Philip", "Joshua", "Barnabas", "Stephen", "Andrew", "Samuel", "Gabriel", "Ibrahim"
]

# Female Names (Including Christian Names)
female_names = [
    "Aisha", "Amina", "Asabe", "Asma'u", "Binta", "Fadimatu", "Falmata", "Fatima", "Fatsuma", "Fiddausi",
    "Hadiza", "Hajarat", "Hauwa", "Hindatu", "Husaina", "Iya", "Jamila", "Jummai", "Kaltum", "Khadeja",
    "Kulu", "Ladi", "Lami", "Lantana", "Laraba", "Maimuna", "Mairo", "Maryam", "Mariya", "Nafisat",
    "Nana", "Nasiya", "Rahama", "Ramatu", "Rashida", "Sa'adiya", "Sadiya", "Sakinah", "Salma", "Sana",
    "Shafa'atu", "Shamsiya", "Suhaila", "Suwaiba", "Taibat", "Talle", "Ummi", "Yagana", "Yalwa",
    "Yarima", "Yasira", "Zainab", "Zaliha", "Zara'u", "Zariya", "Zeyna", "Zulaiha", "Zuwaira", "Aishatu",
    "Balaraba", "Balkisu", "Fatimatu", "Hajara", "Halima", "Halimatu", "Hassana", "Khadijah", "Ladidi",
    "Lariya", "Laraba", "Maijidda", "Mariya", "Maryama", "Nafisa", "Rahama", "Sakinah", "Shafaatu",
    "Umma", "Yagana", "Yalwa", "Yarwa", "Zainaba", "Zulaihat", "Zuwaira", "Barira", "Fateema", "Hafsatu",
    "Inna", "Sadia", "Farida", "Rabi", "Taiba", "Maimu", "Shariatu", "Sumayya", "Zulai", "Asiya",
    "Khadija", "Aminatu", "Bilqis", "Amina", "Hafsat", "Fati", "Zuwaira", "Rahamat", "Gimbiya",
    "Rejoice", "Mary", "Elizabeth", "Ruth", "Esther", "Deborah", "Martha", "Grace", "Lydia", "Mercy",
    "Patience", "Miriam", "Sarah", "Hannah", "Tabitha", "Eunice", "Phoebe", "Priscilla", "Julia", "Veronica"
]

def get_first_name(gender):
    if gender == 'Male':
        return random.choice(male_names)
    return random.choice(female_names)

def get_last_name():
    return random.choice(male_names)

def get_date_of_birth():
    now = time.time()
    sec_per_year = 31_557_600
    a = int(now - sec_per_year * 30)
    b = int(now - sec_per_year * 18)
    dob = datetime.fromtimestamp(
        random.randint(a, b)
    )

    return dob.date()

def get_state_code(identity):
    return 'BO' if not identity.startswith('00') else 'YO'

def get_lga_code():
    return random.choice(lga_codes)

def get_gender():
    return random.choice(
        ['Male', 'Female']
    )

class Remita:
    def get_account_details(self, bvn, bank_code, account_num):
        if account_num.startswith('00'):
            return {
                'status': 'Invalid',
                'message': 'Invalid Account',
                'valid': False,
                'bvn': bvn,
                'accountNumber': account_num,
                'nameOnAccount': None
            }
        
        return {
            'status': 'Valid',
            'message': 'Valid Account',
            'valid': True,
            'bvn': bvn,
            'bankCode': bank_code,
            'accountNumber': account_num,
            'nameOnAccount': get_first_name('Male') + ' ' + get_last_name()
        }

    def get_nin_data(self, nin):
        if len(nin) != 11: return {}
        
        gender = get_gender()

        return {
            'firstName': get_first_name(gender),
            'lastName': get_last_name(),
            'dateOfBirth': get_date_of_birth(),
            'stateOfOriginCode': get_state_code(nin),
            'lgaofOriginCode': get_lga_code(),
            'gender': gender,
        }

    def get_bvn_data(self, bvn):
        return self.get_nin_data(bvn)

remita = Remita()