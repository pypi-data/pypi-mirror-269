import requests

def hello_world():
    return "Hello, world!"

def save(data_to_send):
    try:
        # Send a POST request to the specified URL with the data
        response = requests.post('http://localhost:5000/application.service/update-active-user-cost', json=data_to_send)
        
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


 