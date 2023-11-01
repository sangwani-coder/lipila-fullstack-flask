"""
    test_mtn_momo.py
    Lipila Fee Collection System
    Creator: Sangwani P. Zyambo

    unittests for the mtn_momo function.
"""
from lipila_app.momo.mtn_momo import MTN
import pytest


def test_get_uuid():
    """ Test the method that generates a UUIDv4"""
    mtn = MTN()
    response = mtn.get_uuid()
    assert response.status_code == 200
    assert mtn.x_reference_id != ''

def test_create_api_user():
    """Test the method that creates a sandbox api user"""
    mtn = MTN()
    response = mtn.create_api_user()
    assert response.status_code == 201

def test_get_api_key():
    """Test the method that creates the api key used to provision the sand box"""
    mtn = MTN()
    mtn.create_api_user()
    response = mtn.get_api_key()
    key = response.json()
    assert response.status_code == 201
    assert 'apiKey' in key

def test_get_api_token():
    """Test the method that genertes an API token"""
    mtn = MTN()
    response = mtn.get_api_token()
    token = response.json()
    assert response.status_code == 200
    assert 'access_token' in token

def test_request_to_pay_accepted():
    """ Test the request to pay method
        payment should be accepted
    """
    mtn = MTN()
    mtn.create_api_user() # create api user
    mtn.get_api_key() # create api key
    mtn.get_api_token() # create access token
    response = mtn.request_to_pay('50', '0255669988', '1992')
    assert response.status_code == 202

def test_request_to_pay_raise_value_error():
    """ Test the request to pay method
        should raise a value error    
    """
    mtn = MTN()
    mtn.get_uuid() # get uuidv4
    mtn.create_api_user() # create api user
    mtn.get_api_key() # create api key
    mtn.get_api_token() # create access token
    amount = '500'
    partyId = ''
    externalId = 'tuition'
    val = mtn.request_to_pay(amount, partyId, externalId)
    assert val == 'error'
    vall = mtn.request_to_pay('10', '0969620939', externalId)
    assert vall == 'error'

def test_request_to_pay_raise_type_error():
    """ Test the request to pay method
        should raise a type error
    """
    mtn = MTN()
    mtn.get_uuid() # get uuidv4
    mtn.create_api_user() # create api user
    mtn.get_api_key() # create api key
    mtn.get_api_token() # create access token
    amount = 500
    partyId = '0969620939'
    externalId = 'tuition'
    with pytest.raises(TypeError) as e:
        mtn.request_to_pay(amount, partyId, externalId)
        mtn.request_to_pay(amount, partyId, externalId)
        mtn.request_to_pay('300', 1000, externalId)
        mtn.request_to_pay('300', '0969620939', 2536)
    


