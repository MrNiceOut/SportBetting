class GameData:
    def __init__(self) -> None:
        self.id = ''
        self.key = ''
        self.title = ''
        self.time = None
        self.home = ''
        self.away = ''
        self.book = []
    def addBookmaker(self,book):
        if not isinstance(book,self.Bookmaker):
            raise ValueError("Input is not of type Bookmaker.")
        self.book.append(book)
    class Bookmaker:
        def __init__(self) -> None:
            self.key = ''
            self.title = ''
            self.update = None
            self.markets = []
        def addMarket(self,market):
            if not isinstance(market,self.Markets):
                raise ValueError("Input is not of type Markets.")
            self.markets.append(market)
        class Markets:
            def __init__(self) -> None:
                self.key = ''
                self.update = None
                self.outcomes = []
            def addOutcome(self,outcome):
                if not isinstance(outcome,self.Outcomes):
                    raise ValueError("Input is not of type Outcomes.")
                self.outcomes.append(outcome)    
            class Outcomes: 
                def __init__(self) -> None:
                    self.name = ''
                    self.price = 0
                    self.point = 0

if __name__=="__main__":
    gameData = GameData()

    testJson=[
            {
                "id": "42db668449664943833b5c04a583328a",
                "sport_key": "americanfootball_nfl",
                "sport_title": "NFL",
                "commence_time": "2023-09-08T00:21:00Z",
                "home_team": "Kansas City Chiefs",
                "away_team": "Detroit Lions",
                "bookmakers": [
                    {
                        "key": "fanduel",
                        "title": "FanDuel",
                        "last_update": "2023-08-18T22:58:58Z",
                        "markets": [
                            {
                                "key": "spreads",
                                "last_update": "2023-08-18T22:58:58Z",
                                "outcomes": [
                                    {
                                        "name": "Detroit Lions",
                                        "price": 1.98,
                                        "point": 6.5
                                    },
                                    {
                                        "name": "Kansas City Chiefs",
                                        "price": 1.83,
                                        "point": -6.5
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    print(testJson)