import requests

def verify_bvn(bvn):
    if len(bvn) != 11 or not bvn.isdigit():
        return 'Invalid BVN'
    try:
        res = requests.get(f"https://usimam12.pythonanywhere.com/bvns/{bvn}")
    except:
        return 'Something went wrong.'

    bvn_details = res.json()
    if not bvn_details:
        return 'Invalid BVN'
    
    state = bvn_details.get('state_of_origin')
    if state.lower() != 'borno':
        return 'This program is for indigen of Borno state only!!!'

    return bvn
    

def verify_nin(nin):
    if len(nin) != 11 or not nin.isdigit():
        return 'Invalid NIN'
    try:
        res = requests.get(f"https://usimam12.pythonanywhere.com/nins/{nin}")
    except:
        return 'Something went wrong.'

    nin_details = res.json()
    if not nin_details:
        return 'Invalid NIN'
    
    state = nin_details.get('state_of_origin')
    if state.lower() != 'borno':
        return 'This program is for indigen of Borno state only!!!'

    return nin


def verify_account(bank, account_no):
    if len(bank) != 3 or not bank.isdigit():
        return 'Invalid Bank'
    if len(account_no) != 10 or not account_no.isdigit():
        return 'Invalid Account Number'
    
    try:
        res = requests.get(f"https://usimam12.pythonanywhere.com/accounts/{bank}/{account_no}")
    except:
        return 'Something went wrong.'
    
    account = res.json()
    if not account:
        return 'Invali Account'
    
    return 'Account verified successfully!!!'

