


import pandas as pd
import requests
import json
import time
import numpy as np



#Required for Riot API
api_key = "Your API key here"
region = "NA1"


match_id_df  = pd.read_csv('MatchId.csv')

#Code to get the 15th minute of a given Match. 
def get_match_json(matchid):
    url_pull_match = "https://{}.api.riotgames.com/lol/match/v4/timelines/by-match/{}?api_key={}".format(region,matchid,api_key)
    match_data_all = requests.get(url_pull_match).json()
    
    #Check to make sure match is long enough
    try:
        length_match = match_data_all['frames'][15]
        return match_data_all
    
    except IndexError:
        return ['Match is too short. Skipping.']
        
    

def get_player_stats(match_data,player):
    #Get player information at the fifteenth minute of the game.
    
    player_query = match_data['frames'][15]['participantFrames'][player]    
    player_total_gold = player_query['totalGold']
    player_level = player_query['level']
    player_xp = player_query['xp']
    player_minionsKilled = player_query['minionsKilled']
    player_jungleMinionsKilled = player_query['jungleMinionsKilled']
    
    return (player_total_gold,player_level,player_minionsKilled,
            player_jungleMinionsKilled)
    
    

def get_team_stats(match_data):
    #Get team stats at the fifteenth minute of the game.
    
    blue_team = ['1','2','3','4','5']
    red_team = ['6','7','8','9','10']
    
    #blue team
    blue_total_gold = 0
    blue_minionsKilled = 0
    blue_jungleMinionsKilled = 0
    blue_average_player_level = 0
    
    for player in blue_team:
        (player_total_gold,player_level,player_minionsKilled,
            player_jungleMinionsKilled) = get_player_stats(match_data,player)
    
        blue_total_gold += player_total_gold
        blue_minionsKilled += player_minionsKilled
        blue_jungleMinionsKilled += player_jungleMinionsKilled
        blue_average_player_level += player_level



    #red team
    red_total_gold = 0
    red_minionsKilled = 0
    red_jungleMinionsKilled = 0
    red_average_player_level = 0
    
    
    for player in red_team:
        (player_total_gold,player_level,player_minionsKilled,
            player_jungleMinionsKilled) = get_player_stats(match_data,player)
    
        red_total_gold += player_total_gold
        red_minionsKilled += player_minionsKilled
        red_jungleMinionsKilled += player_jungleMinionsKilled
        red_average_player_level += player_level
    
    return (blue_total_gold,blue_minionsKilled,blue_jungleMinionsKilled,
            blue_average_player_level/5,red_total_gold,red_minionsKilled,red_jungleMinionsKilled,
            red_average_player_level/5)



def get_all_events(match_data):
    #Get all important events at the fifteenth minute of the game.
    
    red_total_champion_kills = 0
    blue_total_champion_kills = 0
    blue_monsters = 0
    blue_dragons = 0
    red_dragons = 0
    red_monsters = 0
    blue_towers_destroyed = 0
    red_towers_destroyed = 0
    
    
    for i in range(0,16):
        all_events = match_data['frames'][i]['events']
        for event in all_events:
            if event['type'] == 'CHAMPION_KILL':
                if event['killerId'] <6:
                    blue_total_champion_kills += 1
                else:
                    red_total_champion_kills += 1
                
            elif event['type'] == 'ELITE_MONSTER_KILL':
                if event['killerId'] <6:
                    if event['monsterType'] == 'Dragon':
                        blue_dragons += 1
                    else:
                        blue_monsters +=1
                        
                else:
                    if event['monsterType'] == 'Dragon':
                        red_dragons += 1
                    else:
                        red_monsters +=1
                
                
            elif event['type'] == 'BUILDING_KILL':
                if event['teamId'] == 100 and event['buildingType'] == 'TOWER_BUILDING':
                    blue_towers_destroyed += 1
                
                elif event['teamId'] == 200 and event['buildingType'] == 'TOWER_BUILDING':
                    red_towers_destroyed += 1
                        
                    
    return (blue_total_champion_kills,blue_monsters,blue_dragons,
            blue_towers_destroyed,red_total_champion_kills,red_monsters,
            red_dragons, red_towers_destroyed)



def get_match_row(matchid):
    #Code to handle querying all information for a given matchID. 
    
    match_row = [matchid]
    
    match_data_all = get_match_json(matchid)
    
    if match_data_all == ['Match is too short. Skipping.']:
        return ['Match is too short. Skipping.']
    
    else:
        (blue_total_gold,blue_minionsKilled,blue_jungleMinionsKilled,
                blue_average_player_level,red_total_gold,red_minionsKilled,red_jungleMinionsKilled,
                red_average_player_level) = get_team_stats(match_data_all)
        
        all_stats = [blue_total_gold,blue_minionsKilled,blue_jungleMinionsKilled,
                blue_average_player_level,red_total_gold,red_minionsKilled,red_jungleMinionsKilled,
                red_average_player_level]
        
        
        (blue_total_champion_kills,blue_monsters,blue_dragons,
                blue_towers_destroyed,red_total_champion_kills,red_monsters,
                red_dragons, red_towers_destroyed) = get_all_events(match_data_all)
        
        all_events = [blue_total_champion_kills,blue_monsters,blue_dragons,
                blue_towers_destroyed,red_total_champion_kills,red_monsters,
                red_dragons,red_towers_destroyed]
        
        
        match_row_data = match_row+all_stats+all_events
        
        return np.array(match_row_data)
    


column_titles = ['matchId','blueGold','blueMinionsKilled','blueJungleMinionsKilled',
           'blueAvgLevel','redGold','redMinionsKilled','redJungleMinionsKilled',
           'redAvgLevel','blueChampKills','blueHeraldKills','blueDragonKills',
           'blueTowersDestroyed','redChampKills','redHeraldKills','redDragonKills',
           'redTowersDestroyed']

match_ids = pd.read_csv('MatchId.csv')

match_ids = match_ids["MatchId"].drop_duplicates()
    

#Working in batches of 5000 
first_batch = match_ids[0:5000]
second_batch = match_ids[50000:10000]
third_batch = match_ids[10000:15000]
fourth_batch = match_ids[15000:20000]
fifth_batch = match_ids[20000:25000]
sixth_batch = match_ids[25000:30000]
seventh_batch = match_ids[30000:35000]
eighth_batch = match_ids[35000:40000]
ninth_batch = match_ids[40000:45000]
tenth_batch = match_ids[45000:]


# all_batches = [seventh_batch,eighth_batch]
all_batches = [first_batch,second_batch,third_batch,fourth_batch,fifth_batch,
               sixth_batch,seventh_batch,eighth_batch,ninth_batch,tenth_batch]


for matchid_batch in all_batches:
    match_data = []
    for match_id in matchid_batch:
        time.sleep(1.5)
        if match_id == 'MatchId':
            pass
        
        else:
            try: 
                match_entry = get_match_row(match_id)
                if match_entry[0] == 'Match is too short. Skipping.':
                    print('Match',match_id,"is too short.")
                    
                else:
                    match_entry = get_match_row(match_id).reshape(1,-1)
                    match_data.append(np.array(match_entry))
                
            except KeyError:
                print("KeyError")
                
    match_data = np.array(match_data)
    match_data.shape = -1,17
    
    
    df = pd.DataFrame(match_data, columns = column_titles)
    df.to_csv('Match_data_timeline.csv',mode = 'a')
    print('Done Batch!')