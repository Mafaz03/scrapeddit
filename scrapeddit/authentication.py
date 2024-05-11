import praw

class InvalidSubreddit(Exception): pass
class RestrictedSubreddit(Exception): pass
class AuthFailed(Exception): pass
class IncompleteAuth(Exception): pass
   
auths = []

def auth_reddit(client_id, client_secret, username, password, redirect_uri, user_agent, check_for_async = False):
  reddit = praw.Reddit(client_id = client_id,
            client_secret = client_secret,
            username = username,
            password = password,
            redirect_uri = redirect_uri,
            user_agent = user_agent,
            check_for_async=check_for_async)
  sub = reddit.subreddit('aww')
  try: sub_type = sub.subreddit_type
  except: raise InvalidSubreddit("Invalid Authentication, please recheck and try again")
  auths.append(reddit)
  print(f"Authentication was successful, auth stack: {len(auths)}")
  