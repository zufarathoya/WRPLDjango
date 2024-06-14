from django.shortcuts import redirect
from midtransclient import Snap
from .models import TopUpHistory, BankAccount
from django.conf import settings

def create_transaction(request, order_dict):
    # gross_amount = request.POST.get('gross_amount')
    # user_id = request.POST.get('user_id')

    # server_key = settings.MIDTRANS_SERVER_KEY
    # client_key = settings.MIDTRANS_CLIENT_KEY

    server_key = 'SB-Mid-server-QzcMURhEak6PYYSzTk_JKR7l'
    client_key = 'SB-Mid-client-j_PTjxciuHB4z3Nu'

    snap = Snap(
        is_production=False,
        # server_key='SB-Mid-server-',
        # client_key='SB-Mid-client-',
        server_key=server_key,
        client_key=client_key,
    )
    # order_id = str(uuid.uuid4()) 

    param = {
        "transaction_details": {
            "order_id": order_dict['order_id'],
            "gross_amount": order_dict['total_price'],
        },
        "credit_card":{
            "secure" : True
        }
    }

    transaction = snap.create_transaction(param)
    print(transaction)
    insert_ = {
        'bank_account': BankAccount.find_one({'user_id':order_dict['user_id']}),
        'transaction_type': 'P',
        'amount': order_dict['total_price'],
        'order_id': order_dict['order_id'],
        'user_id': order_dict['user_id'],
    }
    TopUpHistory.insert_one(insert_)
    return transaction['redirect_url']