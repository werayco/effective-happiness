import pandas as pd
from autogluon.tabular import TabularPredictor
import seaborn as sns

model = TabularPredictor.load('./ag-lightgbm-only (1)', require_py_version_match=False)
history = pd.read_csv("./final_dataset (2).csv")
history = history[["MatchDate", "HomeTeam", "AwayTeam", "FT_Home_Score", "FT_Away_Score", "FTResult"]]

class SportPredictor:
    def __init__(self,HomeTeam, AwayTeam, MatchDate):
        self.HomeTeam = HomeTeam
        self.AwayTeam = AwayTeam
        self.MatchDate = MatchDate

    def to_dataframe(self) -> pd.DataFrame:
        """This returns a data"""
        data = pd.DataFrame({"HomeTeam":[self.HomeTeam], "AwayTeam":[self.AwayTeam],
                             "MatchDate":[self.MatchDate]})
        data["MatchDate"] = pd.to_datetime(data["MatchDate"])
        data["DayOfWeek"] = data["MatchDate"].dt.dayofweek
        data["Month"] = data["MatchDate"].dt.month
        df = data[["HomeTeam", "AwayTeam", "DayOfWeek","Month"]]
        return df
    
    @property
    def predict(self):
        try:      
            dataframe = self.to_dataframe()
            result = model.predict(dataframe).values
            if result:
                if result == "A":
                    return self.AwayTeam
                elif result == "H":
                    return self.HomeTeam
                else:
                    return "Draw"
            else:
                return "The Model isn't responding"
        except Exception as e:
            return f"An error occured, {e}"
        
    @property
    def get_homeTeam_past_data(self):
        homeTeamData = history[(history.HomeTeam == self.HomeTeam) | (history.AwayTeam == self.HomeTeam)]
        home_wins = homeTeamData[homeTeamData['FTResult'] == 'H']
        total_game = len(homeTeamData)
        wins = len(home_wins)
        game_score: str = f"{wins} out of {total_game} wins. Which Means {self.HomeTeam} lost {total_game - wins}. Having a winning rate of {round(wins/total_game)}%"
        return homeTeamData, game_score
    @property
    def get_awayTeam_past_data(self):
        awayTeamData = history[(history.HomeTeam == self.AwayTeam) | (history.AwayTeam == self.AwayTeam)]
        away_wins = awayTeamData[awayTeamData['FTResult'] == 'H']
        total_game = len(awayTeamData)
        wins = len(away_wins)
        game_score: str = f"{wins} out of {total_game} wins. Which Means {self.AwayTeam} lost {total_game - wins}. Having a winning rate of {round(wins/total_game)}%"
        return awayTeamData, game_score
    @property
    def histogram_homeTeam(self):
        pass

