from dotenv import load_dotenv
import os
import base64
import requests
import json
import urllib.parse

load_dotenv()
class SpotifyFollowChecker:
    def __init__(self):
        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")
        self.redirect_uri = "http://127.0.0.1:8888/callback"
        self.scope = "user-follow-read"
        
    def get_authorization_url(self):
        values = {
            'client_id': self.client_id,
            'response_type': 'code',
            'redirect_uri': self.redirect_uri,
            'scope': self.scope,
            'show_dialog': 'true'
        }
        
        url = "https://accounts.spotify.com/authorize?" + urllib.parse.urlencode(values)
        return url
    
    def get_access_token(self, authorization_code):
        auth_string = f"{self.client_id}:{self.client_secret}"
        auth_bytes = auth_string.encode("utf-8")
        auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")
        
        url = "https://accounts.spotify.com/api/token"
        headers = {
            "Authorization": f"Basic {auth_base64}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        data = {
            "grant_type": "authorization_code",
            "code": authorization_code,
            "redirect_uri": self.redirect_uri
        }
        
        try:
            response = requests.post(url, headers=headers, data=data)
            response.raise_for_status()
            return response.json()["access_token"]
        except requests.exceptions.RequestException as e:
            print(f"Token alma hatası: {e}")
            return None
    
    def check_if_user_follows(self, access_token, target_user_id):
        url = "https://api.spotify.com/v1/me/following/contains"
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        values = {
            "type": "user",
            "ids": target_user_id
        }
        
        try:
            response = requests.get(url, headers=headers, values=values)
            response.raise_for_status()
            result = response.json()
            return result[0] if result else False
        except requests.exceptions.RequestException as e:
            print(f"API hatası: {e}")
            return False

def is_following_user(user_access_token, target_user_id):
    checker = SpotifyFollowChecker()
    return checker.check_if_user_follows(user_access_token, target_user_id)

def get_user_authorization():
    checker = SpotifyFollowChecker()
    
    print("Spotify Yetkilendirmesi")
    print("=" * 30)
    print("1. Aşağıdaki URL'yi tarayıcınızda açın:")
    print(checker.get_authorization_url())
    print("\n2. Spotify'da giriş yapın ve uygulamayı yetkilendirin")
    print("4. Adres çubuğundaki URL şöyle görünür:")
    print("   http://127.0.0.1:8888/callback?code=AQC4o2KsB...")
    print("5. 'code=' den sonraki kısmı kopyalayın (& işaretine kadar)")
    auth_code = input("\n6. Authorization code'u yapıştırın: ")
    access_token = checker.get_access_token(auth_code)
    
    if access_token:
        print("===Yetkilendirme başarılı!===")
        return access_token
    else:
        print("===Yetkilendirme başarısız!===")
        return None

if __name__ == "__main__":
    print("Spotify Takip Kontrol Uygulaması")
    print("=" * 40)
    access_token = get_user_authorization()
    
    if access_token:
        target_user_id = input("\nSizin takip edip etmediğinizi kontrol edeceğiniz kullanıcının Spotify ID'si: ")
        
        result = is_following_user(access_token, target_user_id)
        print(f"\nSonuç: {result}")
        
        if result:
            print("===Bu kullanıcıyı takip ediyorsunuz===")
        else:
            print("===Bu kullanıcıyı takip etmiyorsunuz===")
    else:

        print(False) 
