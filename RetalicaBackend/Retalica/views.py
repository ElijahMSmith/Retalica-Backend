from django.http import HttpResponse
import praw

# If we want to include additional subreddits
# subreddits = ["wallstreetbets"]

def index(request):
    # Request should be incoming JSON with request for specific stock or top 5
    # Will need some way of differentiating

    # Search for a top stock
    # Top 5 on Reddit currently

    reddit = praw.Reddit(
        user_agent="Retalica Stock Popularity Analysis",
        client_id="oylqrww5RDa-RQ",
        client_secret="JOM9pkVc3g6aufzohc1mDDP1EOEBhw"
    )

    return findTop(reddit)
    #return findSpecific(reddit, stock) - String format

def findTop(reddit):
    mentionCount = {}

    # Just need the top five, not any specific information about the stock
    # Can get a list of important stocks from somewhere to evaluate

    # TODO:
    # How do we know what to look for? Ask the group

    # .hot(), .controversial(), .new(), .rising(), .top(time_filter: str = 'all') - can be all, day, hour, month, week, year
    for submission in reddit.subreddit("wallstreetbets").top('hour'):

    '''
    https://praw.readthedocs.io/en/latest/code_overview/models/submission.html
    created_utc: Time the submission was created, represented in Unix Time.
    num_comments: The number of comments on the submission.
    score: The number of upvotes for the submission.
    title: The title of the submission.
    upvote_ratio: The percentage of upvotes from all votes on the submission.
    '''

    return HttpResponse("Trying comment API.")


def findSpecific(reddit, stock): #stock is a String
    # .hot(), .controversial(), .new(), .rising(), .top(time_filter: str = 'all') - can be all, day, hour, month, week, year
    # Keep track of: Number of title mentions in the past hour
    # Number of upvotes? Total number of upvotes?
        # Probably needs to be whatever our proposed measurement is
    
    for submission in reddit.subreddit("wallstreetbets").top('hour'):
        if submission.title.lower().rfind(stock) == True:
            

    '''
    https://praw.readthedocs.io/en/latest/code_overview/models/submission.html
    created_utc: Time the submission was created, represented in Unix Time.
    num_comments: The number of comments on the submission.
    score: The number of upvotes for the submission.
    title: The title of the submission.
    upvote_ratio: The percentage of upvotes from all votes on the submission.
    '''

# For now, just worry about post quantity. We can evaluate other factors later.

'''
Check for what stocks are posted about the most
Upvotes and quantity of posts weigh into most popular stocks

Develop how we're weighing these stocks and return these values to Flutter, 
which will deal with stocks API and caching values

After we get ticker information, we can go back to reddit API - 
Two main functions:
    - JSON file that gives top five
    - Searching for a specific stock and its information
'''