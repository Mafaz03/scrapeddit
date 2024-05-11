from tqdm import tqdm
import praw
from datetime import datetime
import pandas as pd
from scrapeddit import authentication
from scrapeddit.authentication import *
auths = authentication.auths

def scrape_reddit(subreddit: str, limit = 10, sortby = 'year', show_safe = None):
  if len(auths) == 0: raise IncompleteAuth("Complete Authentication by calling `authentication.auth_reddit` before proceeding")
  reddit = auths[0]
  sub = reddit.subreddit(subreddit)
  try:
    sub_type = sub.subreddit_type
    if sub_type != 'public':
      raise RestrictedSubreddit(f"r/{subreddit} is restricted to public access")
  except: raise InvalidSubreddit(f"r/{subreddit} is invalid Subreddit, make sure the subreddit is valid")
  result = []
  sub_itter = sub.top(sortby,limit = limit)
  for submission in tqdm(sub_itter, total = limit):
    d = {}
    d['id'] = submission.id
    d['title'] = submission.title
    d['num_comments'] = submission.num_comments
    d['score'] = submission.score
    d['upvote_ratio'] = submission.upvote_ratio
    d['date'] = datetime.fromtimestamp(submission.created_utc)
    d['domain'] = submission.domain
    d['nsfw'] = submission.over_18
    try: d['image'] = submission.preview["images"][0]["source"]["url"]
    except: d['image'] = None
    try: d['author'] = submission.author.name
    except: d['author'] = 'Not Found'
    if show_safe == True and d['nsfw'] == True: d={}
    if show_safe == False and d['nsfw'] == False: d={}
    result.append(d)
  result = [item for item in result if item]
  return pd.DataFrame(result)