import requests

def get_with_token(url, token):
    """
    Send a GET request using the Bearer token.

    Parameters:
        url: URL of the request
        token: user's token
    
    Return value:
        requests.Response: response object
    """
    headers = {
        'Authorization':f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    return response


def patch_with_token(url, token, data):
    """
    Send a PATCH request using the Bearer token.

    Parameters:
        url: URL of the request
        token: user's token
        data: data to be sent
    
    Return value:
        requests.Response: response object
    """
    headers = {
        'Authorization':f"Bearer {token}",
        'Content-Type': 'application/json'
    }

    requestData = {
        "bodies" : [
            data
        ]
    }

    print( requestData )

    response = requests.patch(url, headers=headers, json=requestData)
    return response

def post_with_token(url, token, data):
    """
    Send a POST request using the Bearer token.

    Parameters:
        url: URL of the request
        token: user's token
        data: data to be sent
    
    Return value:
        requests.Response: response object
    """
    headers = {
        'Authorization':f"Bearer {token}",
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, json=data)

    return response

def delete_with_token(url, token):
    """
    Send a DELETE request using the Bearer token.

    Parameters:
        url: URL of the request
        token: user's token

    Return value:
        requests.Response: response object
    """
    headers = {
        'Authorization':f"Bearer {token}",
        'Content-Type': 'application/json'
    }
    response = requests.delete(url, headers=headers)
    return response


