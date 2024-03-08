import re
import sys

from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguegamefinder
from nba_api.stats.library.parameters import Season
from nba_api.stats.library.parameters import SeasonType
from nba_api.stats.endpoints import playbyplay

TEAM_ABBREVIATION = sys.argv[1]
if len(sys.argv) > 2:
    NUMBER_OF_GAMES = int(sys.argv[2])
else:
    NUMBER_OF_GAMES = 5

nba_teams = teams.get_teams()

team = [team for team in nba_teams if team['abbreviation'] == TEAM_ABBREVIATION][0]
team_id =team['id']



gamefinder = leaguegamefinder.LeagueGameFinder(team_id_nullable=team_id,
                            season_nullable=Season.default,
                            season_type_nullable=SeasonType.regular)  

games_dict = gamefinder.get_normalized_dict()
games = games_dict['LeagueGameFinderResults']


player_dict = {}

def get_first_three(game_id):
    plays = playbyplay.PlayByPlay(game_id).get_normalized_dict()['PlayByPlay']

    for play in plays:
        description = play['HOMEDESCRIPTION'] if play['HOMEDESCRIPTION'] else play['VISITORDESCRIPTION']
        if description is not None:
            if "3PT " in description and "MISS" not in description:
                player = description.split(" ")[0]
                print(description)
                return player

for i in range(0,NUMBER_OF_GAMES):
    game = games[i]
    game_id = game['GAME_ID']
    game_matchup = game['MATCHUP']

    player = get_first_three(game_id)

    if player in player_dict:
        player_dict[player] += 1
    else:
        player_dict[player] = 1
sorted_dict = dict(sorted(player_dict.items(), key=lambda item: item[1], reverse=True))
print(sorted_dict)


