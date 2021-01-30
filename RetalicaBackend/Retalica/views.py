from django.http import HttpResponse
from django.http import JsonResponse
import praw
import json
import logging
import math

logger = logging.getLogger(__name__)

# This should be expanded as much as text editing allows
# However, if this becomes much larger, we need to increase efficiency here
companyListFull = open('Fortune500.txt', 'r')
companyListShort = open('Fortune500_condensed.txt', 'r')
companyListSymbol = open('Fortune500_symbols.txt', 'r')
fullCompanyArray = [""] * 500
shortCompanyArray = [""] * 500
symbolArray = [""] * 500
companyFrequency = [0] * 500

index = 0
shortLine = companyListShort.readline()
while shortLine != '':
    shortLine = shortLine.replace('\n', '').lstrip().rstrip().lower()
    shortCompanyArray[index] = shortLine
    shortLine = companyListShort.readline()
    index += 1

index = 0
fullLine = companyListFull.readline()
while fullLine != '':
    fullLine = fullLine.replace('\n', '').lstrip().rstrip()
    fullCompanyArray[index] = fullLine
    fullLine = companyListFull.readline()
    index += 1

index = 0
symbolLine = companyListSymbol.readline()
while symbolLine != '':
    symbolLine = symbolLine.replace('\n', '')
    symbolArray[index] = symbolLine
    symbolLine = companyListSymbol.readline()
    index += 1

def topStocks(reddit):

    reddit = praw.Reddit(
        user_agent="Retalica Stock Popularity Analysis",
        client_id="oylqrww5RDa-RQ",
        client_secret="JOM9pkVc3g6aufzohc1mDDP1EOEBhw"
    )

    # Needs several performance improvements here
    for submission in reddit.subreddit("wallstreetbets").hot(limit=500):
        for index in range(0, 500):
            matchCaseTitle = submission.title.lower()
            currentCompany = shortCompanyArray[index]
            currentSymbol = symbolArray[index].lower()
            if matchCaseTitle.find(currentCompany) != -1 or (len(currentSymbol) > 3 and matchCaseTitle.find(currentSymbol) != -1):
                companyFrequency[index] += 1

    # 6th listing is ignored, just overwrites itself 
        # Used to prevent index going out of bounds
    topFiveNames = ["", "", "", "", ""]
    topFiveSymbols = ["", "", "", "", ""]
    topFiveValues = [-1, -1, -1, -1, -1]

    for index in range(0, 500):
        currentCompany = fullCompanyArray[index]
        currentSymbol = symbolArray[index]
        count = companyFrequency[index]
        
        for j in range(0, 5):
            # Current approach favors earlier loaded stock in ties (since ties aren't grounds for removal
            # Future work could hold other details to break ties
            if count > topFiveValues[j]:
                # Push all lower elements (including i) down one, then insert at i
                for k in range(3, j-1, -1):
                    topFiveNames[k + 1] = topFiveNames[k]
                    topFiveSymbols[k + 1] = topFiveSymbols[k]
                    topFiveValues[k + 1] = topFiveValues[k]
                topFiveNames[j] = currentCompany
                topFiveSymbols[j] = currentSymbol
                topFiveValues[j] = count
                break

    return JsonResponse(
        {
            "first": {
                "name": topFiveNames[0],
                "symbol": topFiveSymbols[0].rstrim().lstrip(),
                "ocurrences": topFiveValues[0],
            },
            "second": {
                "name": topFiveNames[1],
                "symbol": topFiveSymbols[1].rstrim().lstrip(),
                "ocurrences": topFiveValues[1],
            },
            "third": {
                "name": topFiveNames[2],
                "symbol": topFiveSymbols[2].rstrim().lstrip(),
                "ocurrences": topFiveValues[2],
            },
            "fourth": {
                "name": topFiveNames[3],
                "symbol": topFiveSymbols[3].rstrim().lstrip(),
                "ocurrences": topFiveValues[3],
            },
            "fifth": {
                "name": topFiveNames[4],
                "symbol": topFiveSymbols[4].rstrim().lstrip(),
                "ocurrences": topFiveValues[4],
            },
        }
    )
    # Other ways to improve hits:
         # Also try with stock abbreviations

def searchStock(request):
    # Other methods of sorting
    # .hot(), .controversial(), .new(), .rising(), .top(time_filter: str = 'all')
    
    json_data = None
    # stock = ''
    stock = 'gamestop' # For testing
    num_submissions = 0
    upvote_weighted_comments = 0
    upvote_ratio_sum = 0

    comments = 0
    log_comments = 0

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
    stockAlternative = ""

    for index in range(0, 500):
        if(fullCompanyArray[index].find(stock) != -1):
            stockAlternative = symbolArray[index]
            break
        elif(symbolArray[index].find(stock) != -1):
            stockAlternative = shortCompanyArray[index]
            break

    reddit = praw.Reddit(
        user_agent="Retalica Stock Popularity Analysis",
        client_id="oylqrww5RDa-RQ",
        client_secret="JOM9pkVc3g6aufzohc1mDDP1EOEBhw"
    )

    for submission in reddit.subreddit("wallstreetbets").hot(limit=500):
        matchCaseTitle = submission.title.lower()
        # Search for either stock or symbol, as long as it's enough characters to consider
        if (len(stock) >= 3 and matchCaseTitle.find(stock) != -1) or (len(stockAlternative) >= 3 and matchCaseTitle.find(stockAlternative) != -1):
            num_submissions += 1
            upvote_ratio_sum += submission.upvote_ratio
            upvote_weighted_comments += submission.upvote_ratio * submission.num_comments
            comments += submission.num_comments

    math.log(comments)
    comment_ave = upvote_ratio_sum / num_submissions
    popularity = math.log(comments * comment_ave) * num_submissions
    popularity2 = math.log(upvote_weighted_comments) * num_submissions

    return JsonResponse(
        {
            "submissionCount": num_submissions,
            "num_comments": comments,
            "comment_ave": comment_ave,
            "upvote_weighted_comments": upvote_weighted_comments,
            "popularity_score": popularity,
            "popularity2_score": popularity2,
        }
    )