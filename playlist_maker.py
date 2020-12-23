from urllib.parse import quote
import base64
import json
import sys
import requests
import webbrowser 
class Spotify:
    def __init__(self, client_id, client_secret, username=""):
        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.get_meta()
        self.authenticate()
    def authenticate(self):
        url = "https://accounts.spotify.com/authorize"
        url += "?response_type=code"
        url += "&client_id=" + quote(self.client_id)
        url += "&scope=" + quote("user-library-read")
        url += "&redirect_uri=" + quote("http://localhost:3000/callback")
        webbrowser.open(url)
        self.authorization_code = input("Enter auth code from url: ")
        if not self.authorization_code:
            print("Could not authenticate")
            sys.exit()
        else:
            print(self.authorization_code)
            token_url = "https://accounts.spotify.com/api/token?client_id"
            params = {"grant_type": "authorization_code", "code": self.authorization_code, "redirect_uri": "http://localhost:3000/callback"}
            auth_str = bytes("{}:{}".format(self.client_id, self.client_secret), "utf-8")
            b64_auth_str = base64.b64encode(auth_str).decode('utf-8')
            response = requests.post(token_url,headers = {"Content-Type": "application/x-www-form-urlencoded", "Authorization": "Basic {}".format(b64_auth_str)}, data = params) 
            response_data = json.loads(response.text)
            if response_data["access_token"]:
                self.access_token = response_data["access_token"]
        self.base_header = {"Authorization": "Bearer {}".format(self.access_token)}
    def request(self, method, url, action, scopes = []):
        if method == "POST":
            pass
        elif method == "GET":
            response = requests.get(url, headers=self.base_header)
            print(json.loads(response.text))
    def get_meta(self):
        pass
        '''
        self.scopes = 
        [
        "ugc-image-upload",
        "user-read-recently-played",
        "user-read-playback-state",
        "user-top-read",
        "app-remote-control",
        "playlist-modify-public",
        "user-modify-playback-state",
        "playlist-modify-private",
        "user-follow-modify",
        "user-read-currently-playing",
        "user-follow-read",
        "user-library-modify",
        "user-read-playback-position",
        "playlist-read-private",
        "user-read-email",
        "user-read-private",
        "user-library-read",
        "playlist-read-collaborative"
        ]
       '''

def main():
  if len(sys.argv) > 1:
    username = sys.argv[1]
  else:
    print(f'Usage: {sys.argv[0]} username ')
    sys.exit()
  spotify = Spotify("6d4450ab6f1b45afa948971e03c10dba","8bf413755af14b07abb381410a1e6ce0", username)
  if spotify.access_token:
    print('Authentication was succesful')
    spotify.request("GET","https://api.spotify.com/v1/me/tracks", "action") 
  else:
    print(f"Cant get token for user: {username}")

if __name__ == '__main__':
  main()
