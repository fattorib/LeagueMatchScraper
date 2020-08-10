#Required imports
import requests
import json
import time
import pandas as pd


#Information for Riot API
api_key = "your API key here"
region = "NA1"



#Code for pulling list of summoner IDs

#Function to pull a single page of summoner IDs for given rank and tier
def summ_ID_puller(division,tier,page):
    import pandas as pd
    
    url_pull = "https://{}.api.riotgames.com/lol/league/v4/entries/RANKED_SOLO_5x5/{}/{}?page={}&api_key={}".format(region,division,tier,page,api_key)
    profile_list = requests.get(url_pull).json()
    num_profiles = len(profile_list)
    summID_list = []
    
    for profile in range(0,num_profiles):
        summID_list.append(profile_list[profile]['summonerId'])
        
    df = pd.DataFrame(summID_list,columns = ["Summoner ID"])
    df.to_csv('summID.csv',mode = 'a')


for tier in ["I","II","III","IV"]:
    for page in range(1,20):
        time.sleep(1.5)
        summ_ID_puller("DIAMOND",tier,page)

        
   
#Code for pulling list of account IDs from summoner IDs
summoner_IDs = pd.read_csv("summID.csv")
accountID_list = []

#Function to get the encrypted account ID from summoner ID
def acct_ID_puller(summID):
    url_acct_pull = "https://{}.api.riotgames.com/lol/summoner/v4/summoners/{}?api_key={}".format(region,summID,api_key)
    account_info = requests.get(url_acct_pull).json()
    accountID_list.append(account_info["accountId"])
    

summID_list = summoner_IDs["Summoner ID"]
for summID_idx in range(0,12000):
    time.sleep(1.5)
    if summID_list[summID_idx] == "Summoner ID":
        pass
    
    else:
        try:
            acct_ID_puller(summID_list[summID_idx])
        except KeyError:
            print("keyerror")
            
            
        
df = pd.DataFrame(accountID_list, columns = ["AccountId"])
df.to_csv('accountId.csv',mode = 'a')
print("Done pulling accounts!")


#Step 3: Pulling 5 most recent matches for each player
account_IDs = pd.read_csv("accountId.csv")
account_IDs_list = account_IDs["AccountId"]

#This is the list of MatchIDs we are creating
matchID_list = []

#Logging any errors that occur
pull_errors = []
    
#Function to pull the 5 most recent matches for a given account ID
def match_ID_puller(acctid):    
    url_match_pull = "https://{}.api.riotgames.com/lol/match/v4/matchlists/by-account/{}?queue=420&api_key={}".format(region,acctid,api_key)
    match_history = requests.get(url_match_pull).json()
    for i in range(0,5):        
        try:
            match_id = match_history['matches'][i]['gameId']
            matchID_list.append(match_id)
            
        except KeyError:
            print(match_history)
            print("KeyError occured with account:",acctid) 
            pull_errors.append(match_history)
  


for acct_id in accountID_list:
    time.sleep(1.5)
    if acct_id == "AccountId":
        pass
    else:
        match_ID_puller(acct_id)


df = pd.DataFrame(matchID_list, columns = ["MatchId"])
df.to_csv('MatchId.csv',mode = 'a')
print("Done pulling matchIDs!")

    
    
    
