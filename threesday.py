import sys

from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguegamefinder
from nba_api.stats.library.parameters import Season
from nba_api.stats.library.parameters import SeasonType
from nba_api.stats.endpoints import playbyplayv2

TEAM_ABBREVIATION = sys.argv[1]
if len(sys.argv) > 2:
    NUMBER_OF_GAMES = int(sys.argv[2])
else:
    NUMBER_OF_GAMES = 5

if len(sys.argv) > 3:
    NUM_TO_GRAB = int(sys.argv[3])
else:
    NUM_TO_GRAB = 1

nba_teams = teams.get_teams()

team = [team for team in nba_teams if team["abbreviation"] == TEAM_ABBREVIATION][0]
team_id = team["id"]


gamefinder = leaguegamefinder.LeagueGameFinder(
    team_id_nullable=team_id,
    season_nullable=Season.default,
    season_type_nullable=SeasonType.regular,
)

games_dict = gamefinder.get_normalized_dict()
games = games_dict["LeagueGameFinderResults"]


player_dict = {}
team_dict = {}


def get_first_three(game_id, num_to_grab):
    plays = playbyplayv2.PlayByPlayV2(game_id).get_normalized_dict()["PlayByPlay"]
    players = []
    teams = []
    for play in plays:
        description = (
            play["HOMEDESCRIPTION"]
            if play["HOMEDESCRIPTION"]
            else play["VISITORDESCRIPTION"]
        )
        if description is not None:
            if "3PT " in description and "MISS" not in description:
                player = play["PLAYER1_NAME"]
                team = play["PLAYER1_TEAM_ABBREVIATION"]
                print(description)
                players.append(player)
                teams.append(team)
                if len(players) == num_to_grab:
                    return players, teams
    return players, teams


for i in range(0, NUMBER_OF_GAMES):
    game = games[i]
    game_id = game["GAME_ID"]
    game_matchup = game["MATCHUP"]

    players, teams = get_first_three(game_id, NUM_TO_GRAB)

    for player in players:
        if player in player_dict:
            player_dict[player] += 1
        else:
            player_dict[player] = 1
    for team in teams:
        if team in team_dict:
            team_dict[team] += 1
        else:
            team_dict[team] = 1

players_sorted = dict(
    sorted(player_dict.items(), key=lambda item: item[1], reverse=True)
)
print(players_sorted)

teams_sorted = dict(sorted(team_dict.items(), key=lambda item: item[1], reverse=True))
print(teams_sorted)
