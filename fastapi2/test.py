#to check what data is actually being sent to the server in JSON format

import requests

def main():
    #url = "http://localhost:8000/transactions/"
    url = "http://127.0.0.1:8000/transactions/"
    res = requests.get(url)
    print(res.json())

if __name__ == "__main__":
    main()