from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse

db = settings.DATABASE


def index(request):
    df = db.get_tweets()

    context = {'df': df}
    return render(request, 'unhcr/index.html', context)


def detail(request, country):
    df = db.get_tweets()

    # Check country
    if not country.capitalize() in df.geo_location.value_counts():
        if not country.upper() in df.geo_location.value_counts():
            return render(request, '404.html')
        else:
            country = country.upper()
    else:
        country = country.capitalize()

    df = df.loc[df['geo_location'] == country]
    total = len(df)
    pos = len(df.loc[df['label'] == 'pos'])
    neg = len(df.loc[df['label'] == 'neg'])
    neu = len(df.loc[df['label'] == 'neu'])

    context = {'country': country, 'total': len(df), 'pos': pos, 'neg': neg, 'neu': neu,
                'pos_per': pos/total*100, 'neg_per': neg/total*100, 'neu_per': neu/total*100}
    return render(request, 'unhcr/detail.html', context)
