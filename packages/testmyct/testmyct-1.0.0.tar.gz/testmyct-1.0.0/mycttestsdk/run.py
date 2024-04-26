import requests

def hello_world():
    return "Hello, world!"

def save(data_to_send : any, api_url: any):
    try:
        # Send a POST request to the specified URL with the data
        url = api_url + '/application.service/update-active-user-cost'
        response = requests.post(url, json=data_to_send)
        
        # Check if the request was successful
        response.raise_for_status()
        
        # Extract data from the response
        data = response.json()
        
        # Return the data
        return data
    except requests.exceptions.RequestException as e:
        # If an error occurs during the request, catch it here
        print('Lỗi khi gọi API:', e)
        
        # Rethrow the error
        raise


 