# League of Legends Match Scraper

# About
This is code for scraping Diamond League of Legends matches using Riot Games API. The final dataset can be found [here](https://www.kaggle.com/benfattori/league-of-legends-diamond-games-first-15-minutes). This data is meant to be used for training a model to predict the outcome of a match using the first 15 minutes of data (WIP).

# How data is collected
## Part 1: Getting a collection of games played
All data was scraped manually using Riot Games API, specifically Match V4. Unfortunately, their is no one API to collect only Diamond Ranked matches. Instead, we need to do the following:

1. First, we use the League-V4 API to source a list of encrypted in-game ID's for 12 000 Diamond players (25% from each tier).
2. Next, we use the Account-V1 API to convert these in-games ID's to encrypted account ID's. Doing this allows us to query these players accounts to get their recently played matches.
3. After we have our collection of Account IDs, we use the Match V4 API to source the 5 most recently played matches for each of these accounts. When sourcing these accounts, we make sure to filter by game type to ensure we are only pulling ranked matches (WHY?)

We now have a collection of around 60 000 Diamond ranked matches! Occasionally, the Riot API will encounter unexpected server errors, therefore, we aim to collect more matches than we think we need to account for this. 

## Part 2: Getting match data
With our collection of match IDs, we now once again use Match V4 to get a "snapshot" of the match at the 10 and 15 minute mark respectively. Calling the timeline portion of the Match V4 API returns JSON giving us a snapshot of the match at 1 minute intervals. With this snapshot we do the following:
1. First, check the length of the match. The average Diamond game is 29 minutes in length. However, there are matches that can be a lot shorter (on the order of 5 minutes) due to teams giving up or surrending. Any match less than 15 minutes is dropped for our queries. 
2. For each player, we get their individual stats and add them to the team's total.
3. For each frame, we have a collection of match events that occur. Iterate through each of these to get the important ones and record them.

Matches are scraped in batches of 5000 to allow us to distribute the scraping over multiple API keys (but don't tell Riot).
