from django.http import HttpResponse
from django.http import JsonResponse
import praw
import json
import os

# If we want to include additional subreddits
# subreddits = ["wallstreetbets"]

# Request should be incoming JSON with request for specific stock or top 5
# Pick top 5 most discussed stocks on wallstreetbets currently from list

def topStocks(reddit):
    # This should be expanded as much as text editing allows
    # However, if this becomes much larger, we need to increase efficiency here
    companyListFull = open('Fortune500_condensed.txt', 'r')
    companyListShorthand = open('Fortune500_condensed.txt', 'r')
    mentionCount = {}

    line = companyListShorthand.readline()
    while line != '':
        line = line.replace('\n', '').lstrip().rstrip().lower()
        mentionCount[line] = 0
        line = companyListShorthand.readline()

    reddit = praw.Reddit(
        user_agent="Retalica Stock Popularity Analysis",
        client_id="oylqrww5RDa-RQ",
        client_secret="JOM9pkVc3g6aufzohc1mDDP1EOEBhw"
    )

    # Needs several performance improvements here
    for submission in reddit.subreddit("wallstreetbets").hot(limit=500):
        for company in mentionCount:
            currentCount = mentionCount[company]
            if submission.title.lower().find(company) != -1:
                mentionCount[company] = currentCount + 1

    # 6th listing is ignored, just overwrites itself 
        # Used to prevent index going out of bounds
    topFiveNames = ["", "", "", "", "", ""]
    topFiveValues = [-1, -1, -1, -1, -1, -1]

    for company in mentionCount:
        count = int(mentionCount[company])
        for i in range(0, 5):
            # Current approach favors earlier loaded stock in ties (since ties aren't grounds for removal
            # Future work could hold other details to break ties
            if count > topFiveValues[i]:
                # Push all lower elements (including i) down one, then insert at i
                for j in range(4, i - 1, -1):
                    topFiveValues[j + 1] = topFiveValues[j]
                    topFiveNames[j + 1] = topFiveNames[j]
                topFiveNames[i] = company
                topFiveValues[i] = count
                break

    companyListShorthand.close()
    return JsonResponse(
        {
            "first": {
                "name": topFiveNames[0],
                "ocurrences": topFiveValues[0],
            },
            "second": {
                "name": topFiveNames[1],
                "ocurrences": topFiveValues[1],
            },
            "third": {
                "name": topFiveNames[2],
                "ocurrences": topFiveValues[2],
            },
            "fourth": {
                "name": topFiveNames[3],
                "ocurrences": topFiveValues[3],
            },
            "fifth": {
                "name": topFiveNames[4],
                "ocurrences": topFiveValues[4],
            },
        }
    )

def searchStock(request):
    # Other methods of sorting
    # .hot(), .controversial(), .new(), .rising(), .top(time_filter: str = 'all')
    
    json_data = None
    # stock = ''
    stock = 'gme' # For testing
    found = 0

    # Work on once we get Flutter-Django connection
    # Wildly untested and likely to be completely wrong
    '''
    # TODO: I don't know what request.is_ajax is or does
    # I assume we're using GET, other option being POST
    if request.is_ajax() and request.method == 'GET':
        if request.method == 'GET':
            json_data = json.loads(request.body.decode("utf-8")) # Decode might or might not be necessary
            stock = json_data['stock']
    '''

    stock = stock.lower()

    reddit = praw.Reddit(
        user_agent="Retalica Stock Popularity Analysis",
        client_id="oylqrww5RDa-RQ",
        client_secret="JOM9pkVc3g6aufzohc1mDDP1EOEBhw"
    )

    for submission in reddit.subreddit("wallstreetbets").hot(limit=500):
        if submission.title.lower().find(stock) != -1:
            found += 1

    return JsonResponse(
        {
            "submissionCount": found
        }
    )