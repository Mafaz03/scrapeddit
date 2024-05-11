class ScrapeditDataset(Dataset):
  def __init__(self, subreddit: list, limit=10, sortby='year', show_safe=None, max_size=500, transform=None):
    if transform: self.transform = transform
    else: self.transform = transforms.ToTensor()
    self.subreddit = subreddit
    self.max_size = max_size
    self.results = {}
    for r in self.subreddit:
      sub = reddit.subreddit(r)
      sub_itter = sub.top(sortby, limit=limit)
      self.result = []
      for submission in tqdm(sub_itter):
        self.d = {}
        try:
            self.d['image'] = submission.preview["images"][0]["source"]["url"]
        except:
            self.d['image'] = None
        self.d['domain'] = submission.domain
        self.result.append(self.d)
      self.results[r] = self.result

    self.colated_ds = []
    for r in self.subreddit:
      for image in self.results[r]:
        try:
          response = requests.get(image['image'])
          self.colated_ds.append([image['image'], r])
        except: pass

  def __len__(self):
    return len(self.colated_ds)

  def __getitem__(self, idx):

    link, y = self.colated_ds[idx]
    response = requests.get(link)
    image = Image.open(BytesIO(response.content))
    image.thumbnail((self.max_size, self.max_size), Image.LANCZOS)
    if image.mode != 'RGB': image = image.convert('RGB')
    img_tensor = self.transform(image)
    if img_tensor.shape[0] == 3: img_tensor = img_tensor.permute(1, 2, 0)
    np_image = np.array(img_tensor)
    return {'image': np_image, 'y': y}
