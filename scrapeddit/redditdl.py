from PIL import UnidentifiedImageError

class InvalidSubreddit(Exception):
    pass
class RestrictedSubreddit(Exception):
    pass

class ScrapeditDataset(Dataset):
  def __init__(self, subreddit: list, limit=10, sortby='year', show_safe=None, max_size=500, transform=None):
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

    self.colated_ds = []
    print(f"Collecting Images from {len(self.subreddit)} subreddits")
    for r in self.subreddit:
      for image in tqdm(self.results[r], total = len(self.results)) :
        try:
          response = requests.get(image['image'])
          pil_image = Image.open(BytesIO(response.content))
          self.colated_ds.append([pil_image, r])
        except: pass

    z = [i[1] for i in self.colated_ds]
    self.ds_count = dict(Counter(z))

  def __call__(self):
    print(f"Out of {len(self.subreddit) * self.limit}, f{len(self.colated_ds)} were able to scrape")
    plt.bar(self.ds_count.keys(), self.ds_count.values())
    plt.title('Distribution of Data Sources')
    plt.xlabel('Data Sources')
    plt.ylabel('Count')
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

  def __len__(self):
    return len(self.colated_ds)

  def __getitem__(self, idx):
    pil_image, y = self.colated_ds[idx]
    try:
      pil_image.thumbnail((self.max_size, self.max_size), Image.LANCZOS)
      if pil_image.mode != 'RGB': pil_image = pil_image.convert('RGB')
      img_tensor = self.transform(pil_image)
      if img_tensor.shape[0] == 3: img_tensor = img_tensor.permute(1, 2, 0)
      np_image = np.array(img_tensor)
      return {'image': np_image, 'y': y}
    except UnidentifiedImageError:
      return None
