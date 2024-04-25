import requests
import os
from dotenv import load_dotenv
from access_token import AccessToken
from utils import generate_security_credential

class BusinessToCustomer:
	def __init__(self):
		if os.getenv('MPESA_ENV') == "1":
			self.business_to_customer_url=os.getenv('MPESA_LIVE_B2C_URL')
			self.initiator=os.getenv('MPESA_LIVE_INITIATOR')
			self.party_a=os.getenv('MPESA_LIVE_TRANSACTION_QUERY_PARTY_A')
			self.party_b=os.getenv('MPESA_LIVE_B2C_PARTY_B')
			self.result_url=os.getenv('MPESA_LIVE_B2C_RESULT_URL')
			self.queue_timeout_url=os.getenv('MPESA_LIVE_B2C_QUEUE_TIMEOUT_URL')
			self.command_id=os.getenv('MPESA_LIVE_B2C_COMMAND_ID')
			self.password=os.getenv('MPESA_LIVE_PASSWORD')
			
		else:
			self.business_to_customer_url=os.getenv('MPESA_TEST_B2C_URL')
			self.initiator=os.getenv('MPESA_TEST_INITIATOR')
			self.party_a=os.getenv('MPESA_TEST_TRANSACTION_QUERY_PARTY_A')
			self.party_b=os.getenv('MPESA_TEST_B2C_PARTY_B')
			self.result_url=os.getenv('MPESA_TEST_B2C_RESULT_URL')
			self.queue_timeout_url=os.getenv('MPESA_TEST_B2C_QUEUE_TIMEOUT_URL')
			self.command_id=os.getenv('MPESA_TEST_B2C_COMMAND_ID')
			self.password=os.getenv('MPESA_TEST_PASSWORD')

		self.security_credential=generate_security_credential(self.password)


	def business_to_customer(self,phone_number,amount, remarks = "",occasion=""):
		token = AccessToken()
		access_token=token.get_access_token()

		if occasion == "":
			occasion = "Ok"

		if remarks == "":
			remarks = "Payment of "+self.amount +" to customer"
		
		headers = {
		  'Content-Type': 'application/json',
		  "Authorization": "Bearer %s" % access_token
		}

		payload = {
		    "Initiator": self.initiator,
		    "SecurityCredential": self.security_credential,
		    "CommandID": self.command_id,
		    "PartyA": self.party_a,
		    "PartyB": phone_number,
		    "Amount": amount,
		    "ResultURL": self.result_url,
		    "QueueTimeOutURL": self.queue_timeout_url,
		    "Remarks": remarks,
		    "Occassion": occasion,
		}

		r = requests.post(self.business_to_customer_url, json=payload, headers=headers)
		json_response = r.json()
		print(json_response)
		return json_response

	def extract_response_details(self, data):
		receiver=data['Result']['ResultParameters']['ResultParameter'][4]['Value']
		split_receiver = receiver.split('-')
		phone = split_receiver[0]
		name = split_receiver[1]
		timestamp=data['Result']['ResultParameters']['ResultParameter'][5]['Value']
		amount=data['Result']['ResultParameters']['ResultParameter'][0]['Value']
		ConversationID=data['Result']['ConversationID']
		OriginatorConversationID=data['Result']['OriginatorConversationID']
		ResultCode=data['Result']['ResultCode']
		TransactionID=data['Result']['TransactionID']
		ReceiptNo=data['Result']['ResultParameters']['ResultParameter'][1]['Value']
		decoded_data = {
			'receiver_phone': phone,
			'receiver_name' : name,
			'timestamp': timestamp,
			'amount': amount,
			'ConversationID': ConversationID,
			'OriginatorConversationID' : OriginatorConversationID,
			'ResultCode' :ResultCode,
			'TransactionID' : TransactionID,
			'ReceiptNo' : ReceiptNo
		}
		return decoded_data
	    
