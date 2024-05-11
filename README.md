# Scrapeddit

## Overview

Scrapeddit is a Python class designed for scraping images from Reddit subreddits and creating PyTorch datasets. It facilitates the collection of image data from various subreddits, allowing for easy integration into machine learning pipelines or data analysis projects.

## Key Features

- **Reddit Scraping:** Automatically retrieves image URLs from specified subreddits using the PRAW library.
- **Flexible Configuration:** Users can customize parameters such as subreddit names, post limits, sorting methods, and content safety filters.
- **Data Transformation:** Supports image transformation and resizing to fit specific requirements.
- **Error Handling:** Handles invalid subreddits, restricted subreddits, and failed image fetching gracefully, ensuring smooth data collection.
- **Data Visualization:** Provides visualization tools to understand the distribution of data sources across different subreddits.

## Usage
1. **Initialization:** Instantiate the ScrapeditDataset class with a list of subreddit names and optional parameters for customization.
Install by:
```
pip install scrapeddit
pip3 install scrapeddit
```

2. **Authentication:** Complete authentication by regestering and making a app in prawn, using that complete the authentication by:
```
from scrapeddit import authentication
authentication.auth_reddit(client_id = "",
                    client_secret = "",
                    username = "",
                    password = "",
                    redirect_uri = "",
                    user_agent = "",
                    check_for_async=False
)
```
3. **Getting Data:** This is for collecting information for only on subreddit, parameters like `limit`, `show_safe` can be set
```
from scrapeddit import scrapeonce
scrape_df = scrapeonce.scrape_reddit('spotted', limit = 50)
```
4. **Data Loading:** Access the dataset like any other PyTorch dataset, allowing for seamless integration into machine learning workflows.
Highly recommemded: Use the provided `ResizeWithPadding` tranform
```
from scrapeddit import redditdl
from scrapeddit.redditdl import ScrapeditDataset
from scrapeddit.transforms import ResizeWithPadding
import torchvision.transforms as transforms

size = 300
transform_resize=transforms.Compose([
                              ResizeWithPadding(size=size),
                              transforms.Resize((size,size)),
                              transforms.ToTensor()
                              ])

subreddits = ['Pizza', 'burgers']
dataset = ScrapeditDataset(subreddit=subreddits, limit = 200, transform = transform_resize, max_size = 100, show_safe = True)
```
Calling `dataset()` displays bar graph useful to visualize data imbalance caused due to data unavailability
utilize `torch.utils.data.random_split()` to split into *train* and *test*
5. **Data Analysis:** Use the provided visualization functions to gain insights into the distribution of data sources and explore the collected dataset.

6. **Model Training:** Utilize the ScrapeditDataset as a DataLoader for training machine learning models. Integrate it with PyTorch's DataLoader for efficient batch processing and model training.
7. **Getting models:** Added functionality includes getting known models, by default it freezes non classifier layers
```
from scrapeddit import models
model1 = models.get_efficient(device = True) # efficient net model
model2 = models.get_vision_model('vgg16', device = True) # Get any model that is available in torchvision.models
```
8. **Visualization:** Two types of visualization are 
    6.1 **show_images:** Uses list of links of images to fetch image from the sources and display them accordingly
    ```
    from scrapeddit import showit
    showit.show_images([list of links] figsize = (10,10), max_images = 24)
    ```
    
    6.2 **sample_batch:** Shows a batch of image data from a dataloader
    ```
    from scrapeddit.showit import show_batch
    sample_batch = next(iter(train_dataloader)) # Getting a batch of data
    show_batch(sample_batch = sample_batch, max = 100, figsize = (15,15))
    ```
    
## Requirements

- Python 3.x
- PRAW
- pandas
- requests
- matplotlib
- Pillow
- torch
- torchvision
- tqdm

