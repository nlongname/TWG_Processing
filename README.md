# TWG_processing
Project to gather and analyze data around a forum-based Werewolf Game (aka Mafia). https://en.wikipedia.org/wiki/Mafia_(party_game)  
Current functions:  
* parsing current and former names and correlating with post and profile IDs  
* recognize votes (indicated by bolded text)  
* utilize fuzzy logic to interpret nicknames in votes and assign them to a player  
* train a sentiment analysis model based on historical wolf/human posts to identify wolves  
In progress:  
* make sentiment_analysis more modular  
* set up a system to more easily apply the model to lists of posts using above  