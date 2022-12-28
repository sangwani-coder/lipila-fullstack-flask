""" MTN momo api handler"""

from lipila.momo.momo import Momo
from lipila.helpers import apology

import requests
import json
import os

API_KEY = ''

if not os.environ.get("SUB_KEY"):
    raise RuntimeError("SUB_KEY not set")


class MTN(Momo):
    """ class that defines methods to query the mtn momo api"""

    basic = 'Basic NjM1OWNhM2EtN2M1NC00M2I3LWJlN2MtNGRjZDY1NTBmMGE2OmRjNjNjZDNmMjI4ODQwYWJiMDY0ZmY1YTdiYTUyNjNj'
    # Global authentication headers
    def __init__(self):
        self.subscription_key = os.environ.get('SUB_KEY')
        self.x_target_environment = 'sandbox'
        self.content_type = 'application/json'
        self.x_reference_id = ''
        self.api_key = ''
        self.api_token = 'Bearer '

    def get_uuid(self)-> str:
        """
            Format - UUID. Recource ID for the API user to be created.
            UUID version 4 is required.
            return: str - uuid
        """
        url = "https://www.uuidgenerator.net/api/version4"
        payload={}
        headers = {}
        try:
            uuid_response = requests.get(url, headers=headers, data=payload)
            self.x_reference_id = self.x_reference_id + uuid_response.text
            return (uuid_response)
        except requests.exceptions.HTTPError as errh:
            return ("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            return ("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            return ("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            return ("OOps: Something Else",err)
       
    def create_api_user(self)-> str:
        """
            POST
            Used to create an API user in the sandbox target environment.
            Response: - 201 Created
        """
        url = "https://sandbox.momodeveloper.mtn.com/v1_0/apiuser"
        self.get_uuid()

        payload = json.dumps({
            "providerCallbackHost": "https://webhook.site/48b519d0-d2f6-479e-8f51-142aa1267a89"
        })
        headers = {
            'X-Reference-Id': self.x_reference_id,
            'Ocp-Apim-Subscription-Key': self.subscription_key,
            'Content-Type': self.content_type
        }
        try:
            res = requests.request('POST', url, headers=headers, data=payload)
            return res
        except requests.exceptions.HTTPError as errh:
            return ("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            return ("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            return ("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            return ("OOps: Something Else",err)
        

    def get_api_key(self):
        """
            get api key used to provision the sand box
        """
        url = "https://sandbox.momodeveloper.mtn.com/v1_0/apiuser/{}/apikey".format(self.x_reference_id)

        payload={}
        headers = {
            'Ocp-Apim-Subscription-Key': self.subscription_key,
        }
        try:
            response = requests.post(url, headers=headers, data=payload)
            if response.status_code == 201:
                key = response.json()
                self.api_key = self.api_key + key['apiKey']
                return response
            return response

        except requests.exceptions.HTTPError as errh:
            return ("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            return ("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            return ("Timeout Error:", errt)
        
    def get_api_token(self):
        """Generate API token"""
        url = "https://sandbox.momodeveloper.mtn.com/collection/token/"
     
        payload={}
        headers = {
            'Ocp-Apim-Subscription-Key': self.subscription_key,
            'Authorization': self.basic
        }
        try:
            response = requests.post(url, headers=headers, data=payload)
            if response.status_code == 200:
                token = response.json()
                self.api_token = self.api_token + token['access_token']
            return response
        except requests.exceptions.HTTPError as errh:
            return ("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            return ("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            return ("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            return ("OOps: Something Else",err)
        
    def request_to_pay(self, amount, partyId, externalId ):
        """ Request to pay"""
        if len(partyId) != 10 or int(amount) < 20:
            return "error"
             
        if not isinstance(amount, str):
            raise TypeError("Amount must be string great than 100")
        if not isinstance(partyId, str):
            raise TypeError("PartyId must be string with 10 digits")
        if not isinstance(externalId, str):
            raise TypeError("ExternalId must be string")

        try:
            
            url = "https://sandbox.momodeveloper.mtn.com/collection/v1_0/requesttopay"

            payload = json.dumps({
                "amount": amount,
                "currency": 'EUR',
                "externalId": externalId,
                "payer": {
                "partyIdType": "MSISDN",
                "partyId": partyId
                },
                "payerMessage": "Pay to lipila",
                "payeeNote": "Termly Fees"
            })
            headers = {
                'X-Reference-Id': self.x_reference_id,
                'Ocp-Apim-Subscription-Key': self.subscription_key,
                'X-Target-Environment': self.x_target_environment,
                'Authorization': self.api_token,
                'Content-Type': self.content_type
            }

            response = requests.post(url, headers=headers, data=payload)
            return response
        except ValueError:
            return "BAD_REQUEST"
        except TypeError:
            return "BAD_REQUEST"
        