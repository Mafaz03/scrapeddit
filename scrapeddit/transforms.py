class ResizeWithPadding(object):
  def __init__(self, size):
    self.size = size
  def __call__(self, img):
    w, h = img.size
    aspect_ratio = w / h
    if aspect_ratio > 1:
      new_w = self.size
      new_h = int(self.size / aspect_ratio)
    else:
      new_h = self.size
      new_w = int(self.size * aspect_ratio)
    resized_img = img.resize((new_w, new_h))
    new_img = Image.new("RGB", (self.size, self.size), color=(0, 0, 0))
    left = (self.size - new_w) // 2
    top = (self.size - new_h) // 2
    new_img.paste(resized_img, (left, top))
    return new_img
