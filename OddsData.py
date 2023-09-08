import requests

class OddsData:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://api.the-odds-api.com/v4'
        
    def get_sports(self):
        url = f'{self.base_url}/sports'
        params = {'api_key': self.api_key}
        response = requests.get(url, params=params)
        return response.json()
    
    def get_odds(self, sport_key, regions, markets):
        url = f'{self.base_url}/sports/{sport_key}/odds'
        params = {
            'api_key': self.api_key,
            'regions': regions,
            'markets': markets
        }
        response = requests.get(url, params=params)
        return response.json()

# Usage
API_KEY = '45779c083e2ad88fbea92c4a2e2b0f89'
odds_data = OddsData(API_KEY)

sport_key = 'americanfootball_nfl'
regions = 'us'
markets = 'spreads'
odds = odds_data.get_odds(sport_key, regions, markets)
print('Number of events:', len(odds))
print(odds)