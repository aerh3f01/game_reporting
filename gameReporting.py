from flask import Flask, jsonify
from datetime import timezone, datetime
import json

app = Flask(__name__)

# Load games data from JSON file
with open('games_data.json') as f:
    gamesData = json.load(f)

# Convert epoch to datetime
def epochDateTime(epochTime):
    commentTime = datetime.fromtimestamp(epochTime, tz = timezone.utc)
    return commentTime

# A route to return selected game data by game_id
@app.route('/games/<int:game_id>', methods=['GET'])
def fetchGame(game_id):
    game = next((game for game in gamesData['games'] if game['game_id'] == game_id), None)
    if game:
        for comment in game['comments']:
            try:
                # Some errors with converting the comment time to int
                # So a try/except block is used to catch the error
                comment['dateCreated'] = epochDateTime(int(comment['dateCreated']))
            except:
                pass
        return jsonify(game)
    else:
        return jsonify({"error": "Game not found"}), 404
    
# A route to return all games report data
@app.route('/games/report', methods=['GET'])
def fetchReport():
    usersComments = {}
    gameLikes = {}
    totalLikes = 0

    for game in gamesData['games']:
        # Track total likes for the game
        gameLikes[game['title']] = game['likes']
        totalLikes += game['likes']
        
        # Track user comments
        for comment in game['comments']:
            user = comment['user']
            if user in usersComments:
                usersComments[user] += 1
            else:
                usersComments[user] = 1

    # Find the user with the most comments
    userMostComments = max(usersComments, key=usersComments.get)

    # Find the game with the highest total likes
    highestRatedGame = max(gameLikes, key=gameLikes.get)

    # Calculate average likes per game
    avgLikesPerGame = round(totalLikes / len(gamesData['games']))


    ''' 
    The average likes per game example doesnt work in the sence that all games have 100 likes
    If it wants the average likes of the comments per game then it would just require
    to iterate through the comments instead of the games.
    This is the same concept for the highest rated game as well.
    '''


    report = {
        "user_with_most_comments": userMostComments,
        "highest_rated_game": highestRatedGame,
        "average_likes_per_game": avgLikesPerGame
    }
    
    return jsonify(report)

if __name__ == '__main__':
    app.run(debug=True, port=8080)
