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
        # this is the dataframe that the HomeTeam has Played
        homeTeamData = history[(history.HomeTeam == self.HomeTeam) | (history.AwayTeam == self.HomeTeam)]

        hometeamer = homeTeamData[["HomeTeam","FTResult"]]
        awayteamer=homeTeamData[["AwayTeam","FTResult"]]

        # hometeam in AwayColumn
        homeTeam_win_in_awayCol = awayteamer[(awayteamer.AwayTeam==self.HomeTeam) & (awayteamer.FTResult=="A")]
        # hometeam in homeColumn
        homeTeam_win_in_homeCol = hometeamer[(hometeamer.HomeTeam==self.HomeTeam) & (awayteamer.FTResult=="H")]

        # total wins
        home_wins = len(homeTeam_win_in_awayCol) + len(homeTeam_win_in_homeCol)

        # total matches played
        total_game = len(homeTeamData)

        # response
        game_score: str = f"{self.HomeTeam} wins {home_wins} matches out of {total_game} games, loosing {total_game - home_wins} games. Hence, Having a winning rate of {(home_wins / total_game) * 100:.2f}%"
        return homeTeamData, game_score
    
    @property
    def get_awayTeam_past_data(self):
        awayTeamData = history[(history.HomeTeam == self.AwayTeam) | (history.AwayTeam == self.AwayTeam)]
        hometeamer = awayTeamData[["HomeTeam","FTResult"]]
        awayteamer = awayTeamData[["AwayTeam","FTResult"]]
        
        awayTeam_win_in_awayCol = awayteamer[(awayteamer.AwayTeam==self.AwayTeam) & (awayteamer.FTResult=="A")]
        awayTeam_win_in_homeCol = hometeamer[(hometeamer.HomeTeam==self.AwayTeam) & (awayteamer.FTResult=="H")]

        away_wins = len(awayTeam_win_in_awayCol) + len(awayTeam_win_in_homeCol)
        total_game = len(awayTeamData)

        game_score: str = f"{self.AwayTeam} wins {away_wins} matches out of {total_game} games, loosing {total_game - away_wins} games. Hence, Having a winning rate of {(away_wins / total_game) * 100:.2f}%"
        return awayTeamData, game_score
    @property
    def histogram_homeTeam(self):
        pass

