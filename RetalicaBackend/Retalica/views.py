from django.http import HttpResponse
from django.http import JsonResponse
import praw
import json
import logging
import math

logger = logging.getLogger(__name__)

# Load up company data

# Holds the full stock market listing of the company
companyListFull = open('Fortune500.txt', 'r')
# Holds a shortened version of the name that only includes key phrases
    # Used for comparisons to improve search accuracy
companyListShort = open('Fortune500_condensed.txt', 'r')
# Holds the company's ticker/symbol used to identify their stock
companyListSymbol = open('Fortune500_symbols.txt', 'r')

# Where this data will be loaded to
fullCompanyArray = [""] * 500
shortCompanyArray = [""] * 500
symbolArray = [""] * 500

# Read shortened names to list
index = 0
shortLine = companyListShort.readline()
while shortLine != '':
    shortLine = shortLine.replace('\n', '').lstrip().rstrip().lower()
    shortCompanyArray[index] = shortLine
    shortLine = companyListShort.readline()
    index += 1

# Read full names to list
index = 0
fullLine = companyListFull.readline()
while fullLine != '':
    fullLine = fullLine.replace('\n', '').lstrip().rstrip()
    fullCompanyArray[index] = fullLine
    fullLine = companyListFull.readline()
    index += 1

# Read symbols to list
index = 0
symbolLine = companyListSymbol.readline()
while symbolLine != '':
    symbolLine = symbolLine.replace('\n', '')
    symbolArray[index] = symbolLine
    symbolLine = companyListSymbol.readline()
    index += 1

def topStocks(reddit):

    # Connect to Reddit
    reddit = praw.Reddit(
        user_agent="Retalica Stock Popularity Analysis",
        client_id="oylqrww5RDa-RQ",
        client_secret="JOM9pkVc3g6aufzohc1mDDP1EOEBhw"
    )

    companyFrequency = [0] * 500

    # Holds important data for calculating our popularity metric
    # Each index is consistent per company for all lists used (including loaded above)
    upvote_ratio_sum = [0] * 500
    sum_comments = [0] * 500
    popularity = [0] * 500

    # Initial empty state of arrays storing data for top 10 popular top stocks
    # As we go through additional companies, they will slot in their ranking and the rest slide down as needed
    # Over time, this will sort into the corrent top 10 stocks
    topFiveNames = ["", "", "", "", "", "", "", "", "", ""]
    topFiveSymbols = ["", "", "", "", "", "", "", "", "", ""]
    topFiveValues = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
    topFivePops = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1]

    # For each post in r/wallstreetbets under hot (500 max retrieved),
    for submission in reddit.subreddit("wallstreetbets").hot(limit=500):
        # Check each if each company's short-form name appears in the title (case insensitive)
        for index in range(0, 500):
            matchCaseTitle = " " + submission.title.lower() + " "
            currentCompany = shortCompanyArray[index]
            currentSymbol = symbolArray[index].lower()
            # We check length here because we don't want to compare symbols that are one character like 'A',
                # which could appear in a title as a legitimate English word.
            #debugFail = 1/0
            if matchCaseTitle.find(currentCompany) != -1 or (len(currentSymbol) > 3 and matchCaseTitle.find(currentSymbol) != -1):
                # If so, note we found another matching submission and store popularity data
                companyFrequency[index] += 1
                upvote_ratio_sum[index] += submission.upvote_ratio
                sum_comments[index] += submission.num_comments


    # Calculate popularity metric for each company
    for index in range(0, 500):
        # If not mentioned in any post, avoid zero division and simply set to 0
        if companyFrequency[index] == 0 or sum_comments[index] == 0 or upvote_ratio_sum[index] == 0:
            popularity[index] = 0
        # Otherwise, calculate the popularity from saved data
        else:
            popularity[index] = math.log(sum_comments[index] * (upvote_ratio_sum[index] / companyFrequency[index])) * companyFrequency[index]

    # For each stock, get all stock data we have
    for index in range(0, 500):
        currentCompany = fullCompanyArray[index]
        currentSymbol = symbolArray[index]
        count = companyFrequency[index]
        pop = popularity[index]
        
        # Starting form the front, check if this stock is more popular than one in the current rankings
        for j in range(0, 10):
            # If we find a slot for this stock,
            if pop > topFivePops[j]:
                # Push all lower elements (including element at j that is smaller) down one
                # We start from the end - 1 so that the data overwrites itself and we avoid out of bounds issues
                for k in range(3, j-1, -1):
                    topFiveNames[k + 1] = topFiveNames[k]
                    topFiveSymbols[k + 1] = topFiveSymbols[k]
                    topFiveValues[k + 1] = topFiveValues[k]
                    topFivePops[k + 1] = topFivePops[k]
                # Now that our data has been shifted, we can insert at j
                topFiveNames[j] = currentCompany
                topFiveSymbols[j] = currentSymbol.rstrip().lstrip()
                topFiveValues[j] = count
                topFivePops[j] = pop
                break

    # Return our top 10 and relevant data to display in a consistent JSON format
    #d = 1/0

    response = JsonResponse(
        {
            "first": {
                "name": topFiveNames[0],
                "symbol": topFiveSymbols[0],
                "ocurrences": topFiveValues[0],
                "popularity": topFivePops[0],
            },
            "second": {
                "name": topFiveNames[1],
                "symbol": topFiveSymbols[1],
                "ocurrences": topFiveValues[1],
                "popularity": topFivePops[1],
            },
            "third": {
                "name": topFiveNames[2],
                "symbol": topFiveSymbols[2],
                "ocurrences": topFiveValues[2],
                "popularity": topFivePops[2],
            },
            "fourth": {
                "name": topFiveNames[3],
                "symbol": topFiveSymbols[3],
                "ocurrences": topFiveValues[3],
                "popularity": topFivePops[3],
            },
            "fifth": {
                "name": topFiveNames[4],
                "symbol": topFiveSymbols[4],
                "ocurrences": topFiveValues[4],
                "popularity": topFivePops[4],
            },
            "sixth": {
                "name": topFiveNames[5],
                "symbol": topFiveSymbols[5],
                "ocurrences": topFiveValues[5],
                "popularity": topFivePops[5],
            },
            "seventh": {
                "name": topFiveNames[6],
                "symbol": topFiveSymbols[6],
                "ocurrences": topFiveValues[6],
                "popularity": topFivePops[6],
            },
            "eighth": {
                "name": topFiveNames[7],
                "symbol": topFiveSymbols[7],
                "ocurrences": topFiveValues[7],
                "popularity": topFivePops[7],
            },
            "ninth": {
                "name": topFiveNames[8],
                "symbol": topFiveSymbols[8],
                "ocurrences": topFiveValues[8],
                "popularity": topFivePops[8],
            },
            "tenth": {
                "name": topFiveNames[9],
                "symbol": topFiveSymbols[9],
                "ocurrences": topFiveValues[9],
                "popularity": topFivePops[9],
            },
        }
    )
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"
    return response

def searchStock(request):
    print(request.GET)
    stock = " " + request.GET.get('q') + " "
    num_submissions = 0
    upvote_ratio_sum = 0

    comments = 0

    # Work on once we get Flutter-Django connection
    # Wildly untested and likely to be completely wrong

    # Get the JSON object from the body of the request and get the stock requested
    '''
    # TODO: I don't know what request.is_ajax is or does
    # I assume we're using GET, other option being POST
    if request.is_ajax() and request.method == 'GET':
        if request.method == 'GET':
            json_data = json.loads(request.body.decode("utf-8")) # Decode might or might not be necessary
            stock = json_data['stock']
    '''

    # Ignore stock case
    stock = stock.upper()
    
    # Find the other representation of the stock, either the name or the symbol (whatever isn't supplied)
    # Checks for this stock string to be in one of our loaded lists, takes the same index from the one it's not found in
    stockAlternative = ''
    for index in range(0, 500):
        if(fullCompanyArray[index].lower().find(stock) != -1):
            stockAlternative = symbolArray[index]
            break
        elif(symbolArray[index].find(stock) != -1):
            stockAlternative = shortCompanyArray[index]
            break

        
    # Ignore stockAlternative case
    stockAlternative = stockAlternative.lower()
    stock = stock.lower()

    # Connect to Reddit
    reddit = praw.Reddit(
        user_agent="Retalica Stock Popularity Analysis",
        client_id="oylqrww5RDa-RQ",
        client_secret="JOM9pkVc3g6aufzohc1mDDP1EOEBhw"
    )

    # For each of the 500 most host posts on r/wallstreetbets,
    for submission in reddit.subreddit("wallstreetbets").hot(limit=500):
        # Get the title in lower case
        matchCaseTitle = " " + submission.title.lower() + " "
        # Check if the stock name or symbol appears in the title.
        # Again, we check length because we don't want to compare symbols that are one character like 'A',
            # which could appear in a title as a legitimate English word.
            # The check is on both strings this time since we don't know which one is the symbol and which is the name
        #debugFail = 1/0
        if (len(stock) >= 3 and matchCaseTitle.find(stock) != -1) or (len(stockAlternative) > 3 and matchCaseTitle.find(stockAlternative) != -1):
            # Store data if we find a matching submission
            num_submissions += 1
            upvote_ratio_sum += submission.upvote_ratio
            comments += submission.num_comments

    # Calculate popularity metric from stored data
    if num_submissions == 0 or comments == 0 or upvote_ratio_sum == 0:
        popularity = 0
    else:
        comment_ave = upvote_ratio_sum / num_submissions
        popularity = math.log(comments * comment_ave) * num_submissions

    # Package for nice and tidy return to Flutter
    #d = 1/0
    response = JsonResponse(
        {
            "stock": stock.rstrip().lstrip().upper(),
            "submissionCount": num_submissions,
            "num_comments": comments,
            "popularity_score": popularity,
        }
    )
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"
    return response

def test(request):
    print(request.GET)
    return JsonResponse({})