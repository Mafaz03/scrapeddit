def show_images(links_, title = None, figsize=(15,15), sub_title=None, noframe=True, max_col = 6, max_size=500, max_images = None, fontsize = 10, **kwargs):
  transform = transforms.ToTensor()
  if isinstance(links_, str): links = [links_]
  if max_images: num_images = min(len(links_), max_images)
  else: num_images = len(links_)
  num_rows = (num_images - 1) // max_col + 1
  fig, axes = plt.subplots(num_rows, max_col, figsize=figsize)
  if num_images > 1: axes = axes.flatten()
  if sub_title:
    if isinstance(sub_title, list) and len(sub_title) == num_images: pass
    elif isinstance(sub_title, str): sub_title = [sub_title] * num_images
    else: sub_title = [''] * num_images
  failed = 0
  links = []
  for link in links_:
    if link is not None: 
      links.append(link)
    else: failed+=1
  if max_images and len(links)<= max_images:
    for link in links_:
      if link not in links_: links.append(link)
      if len(links) == max_images: break
  links = links[:num_images]
  print(f"Displaying {len(links)} images in total")
  for i, link in enumerate(links):
    try: 
      response = requests.get(link)
      image = Image.open(BytesIO(response.content))
      image.thumbnail((max_size, max_size), Image.LANCZOS)
      if image.mode != 'RGB': image = image.convert('RGB')
      img_tensor = transform(image)
      if img_tensor.shape[0] == 3: img_tensor = img_tensor.permute(1, 2, 0)
      np_image = np.array(img_tensor)
      if sub_title:
        word = sub_title[i] if len(sub_title[i]) <= 45 else ""
        axes[i].set_title(word, fontsize = fontsize)
      axes[i].imshow(np_image, **kwargs)
    except: pass
    if noframe: axes[i].axis('off')
  for j in range(i + 1, num_rows * max_col):
      axes[j].axis('off')
  if title: plt.suptitle(title)
  print(f"{failed} post did not have images, or failed to fetch")
  plt.tight_layout()
  plt.show()


def show_batch(sample_batch, max = 25, X = 'image', y = 'y', cmap=None, **kwargs):
  if max:
    images = sample_batch[X][:max]
    labels = sample_batch[y][:max]
  else:
    images = sample_batch[X]
    labels = sample_batch[y]

  img_len = images.shape[0]
  row = int(math.sqrt(img_len))
  img_len = row ** 2

  fig, axes = plt.subplots(row, row, figsize=(25,25))
  axes = axes.flatten()

  for i in range(img_len):
    axes[i].imshow(images[i], **kwargs)
    axes[i].set_title(labels[i])
    axes[i].axis('off')
