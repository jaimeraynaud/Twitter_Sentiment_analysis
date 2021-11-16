import requests
import numpy as np
import seaborn as sns
import nltk
import pandas as pd
from seaborn.external.husl import max_chroma_pastel

#Wordcloud imports
from wordcloud import WordCloud, ImageColorGenerator
from PIL import Image
import matplotlib.pyplot as plt
from collections import Counter


def display_wordcloud(self):
    from main import get_hashtags_from_file

    Mask = np.array(Image.open(requests.get('http://clipart-library.com/image_gallery2/Twitter-PNG-Image.png', stream=True).raw))
    image_colors = ImageColorGenerator(Mask)

    # Create and generate a word cloud image 
    my_cloud = WordCloud(background_color='black', mask=Mask).generate(' '.join(self.df['text']))

    # Display the generated wordcloud image
    plt.imshow(my_cloud.recolor(color_func=image_colors), interpolation='bilinear') 
    plt.axis("off")

    # Don't forget to show the final image
    plt.show()

def graph(df, len=20, name='words'):
    word_frequency = pd.Series(' '.join(df['text']).lower().split()).value_counts().to_dict()
    word_frequency = dict(Counter(word_frequency).most_common(len))

    # print(word_frequency)
    frecuency = list(word_frequency.values())
    labels = [*word_frequency]
    title = f"Word Frequency for {name}"

    #Plot the figures
    plt.figure(figsize=(10,5))
    plt.bar(np.arange(len), frecuency, width=0.8, 
            color = sns.color_palette("bwr"), alpha=0.5, 
            edgecolor = "black", capsize=8, linewidth=1)
    plt.xticks(np.arange(len), labels, rotation=90, size=14)
    plt.xlabel(f"{len} more frequent words", size=14)
    plt.ylabel("Frequency", size=14)
    plt.title(f'Word Frequency for {name}', size=18) 
    plt.title(title, size=18)
    plt.grid(False)
    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["right"].set_visible(False)
    plt.show() 