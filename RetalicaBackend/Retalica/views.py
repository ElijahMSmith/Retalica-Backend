from django.http import HttpResponse
from django.http import JsonResponse
import praw
import json

# If we want to include additional subreddits
# subreddits = ["wallstreetbets"]

# Request should be incoming JSON with request for specific stock or top 5
# Will need some way of differentiating
# Search for a top stock
# Top 5 on Reddit currently

# List of string stocks
# What stocks are we looking for and what is an effective method of checking submissions for all these stocks
def topStocks(reddit):
    mentionCount = {}
    # Are there any inputs here from a JSON object? Or just JSON output?

    # Demo hard coded response
    return JsonResponse({"first": "AMZN", "second": "BKNG", "third": "GOOG", "fourth": "GOOGL", "fifth": "ISRG"})
    # Just need the top five, not any specific information about the stock
    # Can get a list of important stocks from somewhere to evaluate

    # TODO:
    # How do we know what to look for? Ask the group

    # .hot(), .controversial(), .new(), .rising(), .top(time_filter: str = 'all') - can be all, day, hour, month, week, year
    #for submission in reddit.subreddit("wallstreetbets").top('hour'):




# Outputs: Integer number of occurences
# Yet to be decided: What subset of submissions are we taking?
def searchStock(request): # stock is a String
    # .hot(), .controversial(), .new(), .rising(), .top(time_filter: str = 'all') - can be all, day, hour, month, week, year
    # Keep track of: Number of title mentions in the past hour
    # Number of upvotes? Total number of upvotes?
        # Probably needs to be whatever our proposed measurement is
    
    
    # Wildly untested and likely to be completely wrong
    json_data = None
    stock = ""
    found = 0

    if request.is_ajax() and request.method == 'GET':
        if request.method == 'GET':
            json_data = json.loads(request.body.decode("utf-8")) # Decode might or might not be necessary
            stock = json_data['stock']

    reddit = praw.Reddit(
        user_agent="Retalica Stock Popularity Analysis",
        client_id="oylqrww5RDa-RQ",
        client_secret="JOM9pkVc3g6aufzohc1mDDP1EOEBhw"
    )

    for submission in reddit.subreddit("wallstreetbets").top('hour'):
        if submission.title.lower().rfind(stock) == True:
            found += 1

    # Demo hard coded response (CONFIRMED THESE JSON RESPONSES WORK, IF THAT'S GOOD ENOUGH FOR FLUTTER)
    return JsonResponse({"submissionCount": found})