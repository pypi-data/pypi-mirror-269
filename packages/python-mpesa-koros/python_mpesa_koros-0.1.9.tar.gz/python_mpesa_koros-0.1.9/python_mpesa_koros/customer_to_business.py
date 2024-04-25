import base64
import datetime
import requests
import os

from dotenv import load_dotenv
from .access_token import AccessToken
load_dotenv()


class CustomerToBusiness:	
	def stk_push(self,amount, phone,bill_reference,transaction_description =""):
		if transaction_description == "":
			transaction_description = "Payment REquest for Bill Reference "+bill_reference
		time = datetime.datetime.now()
		timestamp = time.strftime('%Y%m%d%H%M%S')
		if os.getenv('MPESA_ENV_1') == "1":
			api_url = os.getenv('MPESA_LIVE_CUSTOMER_TO_BUSINESS_URL')
			data = os.getenv('MPESA_LIVE_BUSINESS_SHORTCODE') + os.getenv('MPESA_LIVE_PASSKEY') + timestamp
			callback_url = os.getenv('MPESA_LIVE_CALLBACK_URL')
			busines_shortcode = os.getenv('MPESA_LIVE_BUSINESS_SHORTCODE')
		else:
			api_url = os.getenv('MPESA_TEST_CUSTOMER_TO_BUSINESS_URL')
			data = os.getenv('MPESA_TEST_BUSINESS_SHORTCODE') + os.getenv('MPESA_TEST_PASSKEY') + timestamp
			callback_url = os.getenv('MPESA_TEST_CALLBACK_URL')
			busines_shortcode = os.getenv('MPESA_TEST_BUSINESS_SHORTCODE')
		encoded_string = base64.b64encode(data.encode())
		password = encoded_string.decode('utf-8')
		token = AccessToken()
		access_token=token.get_access_token()
		headers = {"Authorization": "Bearer %s" % access_token }
		request = {
            "BusinessShortCode": busines_shortcode,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": busines_shortcode,
            "PhoneNumber": phone,
            "CallBackURL": callback_url,
            "AccountReference": bill_reference,
            "TransactionDesc": transaction_description
        }
		response = requests.post(api_url, json = request, headers=headers)
		json_response = response.json()
		print(json_response)
		return (json_response)
	    
