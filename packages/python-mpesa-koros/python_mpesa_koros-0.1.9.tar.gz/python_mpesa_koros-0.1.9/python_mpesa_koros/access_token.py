import requests
import os
from dotenv import load_dotenv
load_dotenv()

class AccessToken:
	def __init__(self):
		if os.getenv('MPESA_ENV') == "1":
			self.consumer_key=os.getenv('MPESA_LIVE_CONSUMER_KEY')
			self.consumer_secret=os.getenv('MPESA_LIVE_CONSUMER_SECRET')
			self.token_url=os.getenv('MPESA_LIVE_TOKEN_URL')
		else:
			self.consumer_key=os.getenv('MPESA_TEST_CONSUMER_KEY')
			self.consumer_secret=os.getenv('MPESA_TEST_CONSUMER_SECRET')
			self.token_url=os.getenv('MPESA_TEST_TOKEN_URL')

	def get_access_token(self):
		access_token=None
		r = requests.get(self.token_url, auth=requests.auth.HTTPBasicAuth(self.consumer_key, self.consumer_secret))
		status_code=r.status_code
		json_response = r.json()
		print(json_response)
		if 'access_token' in json_response:
			access_token = json_response['access_token']
		return access_token
	    
