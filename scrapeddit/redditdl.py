
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
import praw
import pandas as pd
from tqdm import tqdm
import requests
from PIL import Image
from torchvision import transforms
from io import BytesIO
import numpy as np
import seaborn as sns
from collections import Counter

import torch
from torch.utils.data import Dataset, DataLoader
import requests
from PIL import Image
from io import BytesIO
import numpy as np
from tqdm import tqdm
import torchvision.transforms as transforms
from torchinfo import summary
from scrapeddit import authentication
from scrapeddit.authentication import *
auths = authentication.auths
import random
from PIL import UnidentifiedImageError

class ScrapeditDataset(Dataset):
  def __init__(self, subreddit: list, limit=10, sortby='year', show_safe=None, max_size=500, transform=None, upsample = False):
    if len(auths) == 0: raise IncompleteAuth("Complete Authentication by calling `authentication.auth_reddit` before proceeding")
    reddit = auths[0]
    if transform: self.transform = transform
    else: self.transform = transforms.ToTensor()
    self.subreddit = subreddit
    self.max_size = max_size
    self.results = {}
    self.limit = limit
    print(f"Collecting Data from {len(self.subreddit)} subreddits")
    for r in self.subreddit:
      sub = reddit.subreddit(r)
      try:
        sub_type = sub.subreddit_type
        if sub_type != 'public':
          raise RestrictedSubreddit(f"r/{r} is restricted to public access")
      except: raise InvalidSubreddit(f"r/{r} is invalid Subreddit, make sure the subreddit is valid")
      sub_itter = sub.top(sortby, limit=self.limit)
      self.result = []
      for submission in tqdm(sub_itter, total = self.limit):
        self.d = {}
        try: 
          if show_safe == True and submission.over_18 == True: break
          elif show_safe == False and submission.over_18 == False: break
          self.d['image'] = submission.preview["images"][0]["source"]["url"]
        except: self.d['image'] = None
        self.d['domain'] = submission.domain
        self.result.append(self.d)
      self.results[r] = self.result

    self.collated_ds = []
    print(f"Collecting Images from {len(self.subreddit)} subreddits")
    for r in self.subreddit:
      for image in tqdm(self.results[r], total = len(self.results)) :
        try:
          response = requests.get(image['image'])
          pil_image = Image.open(BytesIO(response.content))
          self.collated_ds.append([pil_image, r])
        except: pass

    z = [i[1] for i in self.collated_ds]
    self.ds_count = dict(Counter(z))

    if upsample: 
      print(f"Before upsample, size of dataset: {len(self.collated_ds)}")
      self.collated_ds = upsample(self.collated_ds)
      print(f"After upsample, size of dataset: {len(self.collated_ds)}")

  def __call__(self):
    print(f"Out of {len(self.subreddit) * self.limit}, {len(self.collated_ds)} were able to scrape")
    plt.bar(self.ds_count.keys(), self.ds_count.values())
    plt.title('Distribution of Data Sources')
    plt.xlabel('Data Sources')
    plt.ylabel('Count')
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

  def __len__(self):
    return len(self.collted_ds)

  def __getitem__(self, idx):
    pil_image, y = self.collated_ds[idx]
    try:
      pil_image.thumbnail((self.max_size, self.max_size), Image.LANCZOS)
      if pil_image.mode != 'RGB': pil_image = pil_image.convert('RGB')
      img_tensor = self.transform(pil_image)
      if img_tensor.shape[0] == 3: img_tensor = img_tensor.permute(1, 2, 0)
      np_image = np.array(img_tensor)
      return {'image': np_image, 'y': y}
    except UnidentifiedImageError:
      return None

def upsample(collated_ds):
  labels = [i[1] for i in collated_ds]
  labels_idx = {}
  for i, label in enumerate(labels):
    if label not in labels_idx:
      labels_idx[label] = []
    labels_idx[label].append(i)

  count_dict = {i: len(labels_idx[i]) for i in labels_idx}
  max_key = max(count_dict, key=count_dict.get)
  to_sample = [key for key in list(count_dict.keys()) if key != max_key]
  for i in to_sample:
    temp = []
    for k, j in enumerate(collated_ds):
      if collated_ds[k][1] == i:
        temp.append(collated_ds[k])
    extra_sample = random.choices(temp, k=count_dict[max_key]-count_dict[i])
    collated_ds += extra_sample
  return collated_ds