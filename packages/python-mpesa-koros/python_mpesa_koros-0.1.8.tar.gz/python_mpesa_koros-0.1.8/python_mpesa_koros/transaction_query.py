import requests
import os
from dotenv import load_dotenv
from access_token import AccessToken
load_dotenv()
from utils import generate_security_credential

class TransactionQuery:
	def __init__(self):
		if os.getenv('MPESA_ENV') == "1":
			self.trans_status_url=os.getenv('MPESA_LIVE_TRANSACTION_QUERY_URL')
			self.initiator=os.getenv('MPESA_LIVE_INITIATOR')
			self.party_a=os.getenv('MPESA_LIVE_TRANSACTION_QUERY_PARTY_A')
			self.result_url=os.getenv('MPESA_LIVE_TRANSACTION_QUERY_RESULT_URL')
			self.queue_timeout_url=os.getenv('MPESA_LIVE_TRANSACTION_QUERY_QUEUE_TIMEOUT_URL')
			self.remarks=os.getenv('MPESA_LIVE_TRANSACTION_QUERY_REMARKS')
			self.password=os.getenv('MPESA_LIVE_PASSWORD')
			self.command_id=os.getenv('MPESA_LIVE_TRANSACTION_QUERY_COMMAND_ID')
			self.identifier_type = os.getenv('MPESA_LIVE_TRANSACTION_QUERY_IDENTIFIER_TYPE')
		else:
			self.trans_status_url=os.getenv('MPESA_TEST_TRANSACTION_QUERY_URL')
			self.initiator=os.getenv('MPESA_TEST_INITIATOR')
			self.party_a=os.getenv('MPESA_TEST_TRANSACTION_QUERY_PARTY_A')
			self.result_url=os.getenv('MPESA_TEST_TRANSACTION_QUERY_RESULT_URL')
			self.queue_timeout_url=os.getenv('MPESA_TEST_TRANSACTION_QUERY_QUEUE_TIMEOUT_URL')
			self.remarks=os.getenv('MPESA_TEST_TRANSACTION_QUERY_REMARKS')
			self.password=os.getenv('MPESA_TEST_PASSWORD')
			self.command_id=os.getenv('MPESA_TEST_TRANSACTION_QUERY_COMMAND_ID')
			self.identifier_type = os.getenv('MPESA_TEST_TRANSACTION_QUERY_IDENTIFIER_TYPE')

		self.security_credential=generate_security_credential(self.password)

	def transaction_query(self,transaction_code,remarks="",occassion = ""):
		if occassion == "":
			occassion = "OK"
		if remarks == "":
			remarks = "Transaction status query for "+transaction_code
		token = AccessToken()
		access_token=token.get_access_token()
		
		headers = {
		  'Content-Type': 'application/json',
		  "Authorization": "Bearer %s" % access_token
		}

		payload = {
		    "Initiator": self.initiator,
		    "SecurityCredential": self.security_credential,
		    "CommandID": "TransactionStatusQuery",
		    "TransactionID": transaction_code,
		    "PartyA": self.party_a,
		    "IdentifierType": self.identifier_type,
		    "ResultURL": self.result_url,
		    "QueueTimeOutURL": self.queue_timeout_url,
		    "Remarks": remarks,
		    "Occassion": occassion,
		 }

		r = requests.post(self.trans_status_url, json=payload, headers=headers)
		json_response = r.json()
		print(json_response)
		return json_response

	def extract_response_details(self, data):
		sender=data['Result']['ResultParameters']['ResultParameter'][1]['Value']
		split_sender = sender.split('-')
		phone = split_sender[0]
		name = split_sender[1]
		receiver=data['Result']['ResultParameters']['ResultParameter'][0]['Value']
		timestamp=data['Result']['ResultParameters']['ResultParameter'][3]['Value']
		amount=data['Result']['ResultParameters']['ResultParameter'][10]['Value']
		ConversationID=data['Result']['ConversationID']
		OriginatorConversationID=data['Result']['OriginatorConversationID']
		ResultCode=data['Result']['ResultCode']
		TransactionID=data['Result']['TransactionID']
		ReceiptNo=data['Result']['ResultParameters']['ResultParameter'][12]['Value']
		decoded_data = {
			'sender_phone': phone,
			'sender_name' : name,
			'receiver' : receiver,
			'timestamp': timestamp,
			'amount': amount,
			'ConversationID': ConversationID,
			'OriginatorConversationID' : OriginatorConversationID,
			'ResultCode' :ResultCode,
			'TransactionID' : TransactionID,
			'ReceiptNo' : ReceiptNo
		}
		return decoded_data
	    
