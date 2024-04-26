import requests
def compilePHP(apiKey,clientId,code):
    url = 'https://api.codegyan.in/v1/compiler/compile'
    data = {
        'lang': 'php',
        'code': code
    }
    headers = {
        'Content-Type': 'application/json',
        'APIKey': apiKey,
        'ClientID': clientId
    }
    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return response.text