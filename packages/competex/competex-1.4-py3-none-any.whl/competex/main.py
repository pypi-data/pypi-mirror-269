def code(name):
    twitter='''
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt

    df = pd.read_csv('Exp3_twitter-sentiment-analysis.csv')
    df.drop(columns=df.columns[df.columns != 'tweet'], inplace=True)
    df

    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    from nltk.stem import WordNetLemmatizer
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')
    stop_words = set(stopwords.words('english'))


    def preprocess(t):
        w = word_tokenize(t.lower())
        data = list()
        for word in w:
            if word.lower() not in stop_words:
                data.append(word)
        return ' '.join(data)
    df['tweet'] = df['tweet'].apply(preprocess)
    df['tweet'].reset_index(drop=True, inplace=True)

    import re
    def remove_special_characters(text):
        pattern = r'[^a-zA-Z0-9\s]'
        clean_text = re.sub(pattern, '', text)
        return clean_text
    df['tweet'] = df['tweet'].apply(remove_special_characters)

    import string
    def remove_punctuation(text):
        return text.translate(str.maketrans('', '', string.punctuation))
    df['tweet'] = df['tweet'].apply(remove_punctuation)
    df['tweet'].reset_index(drop=True, inplace=True)

    df.isnull().sum()

    from textblob import TextBlob
    def get_subjectivity(text):
        return TextBlob(text).sentiment.subjectivity
    def get_polarity(text):
        return TextBlob(text).sentiment.polarity
    df['subjectivity'] = df['tweet'].apply(get_subjectivity)
    df['polarity'] = df['tweet'].apply(get_polarity)

    df

    threshold = 0.05
    df['sentiment'] = df['polarity'].apply(lambda x: ('Positive' if x
            >= threshold else ('Negative' if x < -threshold else 'Neutral'
            )))
    df['sentiment'].value_counts()
    
    df['sentiment'].value_counts().plot.barh()

    df_positive = df[df['sentiment'] == 'Positive']
    df_negative = df[df['sentiment'] == 'Negative']
    df_neutral = df[df['sentiment'] == 'Neutral']

    from wordcloud import WordCloud
    wordcloud = WordCloud(width=800, height=400, background_color='white'
                        ).generate(' '.join(df_positive['tweet']))
    plt.figure(figsize=(10, 5))
    plt.title('WordCloud for positive sentiments')
    plt.imshow(wordcloud, interpolation='lanczos')
    plt.axis('off')
    plt.show()

    wordcloud = WordCloud(width=800, height=400, background_color='white'
                        ).generate(' '.join(df_negative['tweet']))
    plt.figure(figsize=(10, 5))
    plt.title('WordCloud for negatvie sentiments')
    plt.imshow(wordcloud, interpolation='lanczos')
    plt.axis('off')
    plt.show()
    '''

    eda='''
    from matplotlib import pyplot as plt
    import seaborn as sns, pandas as pd, numpy as np

    df=pd.read_csv("manhattan.csv")
    df = df.select_dtypes(include=['number'])
    df

    df.mean()

    df.mode()

    df.median()

    print(f"Max Rent is: {df.max()['rent']}")
    print(f"Min Rent is: {df.max()['rent']}")
    print(f"Difference in Rent is: {df.max()['rent']-df.min()['rent']}")

    df.var()

    df.std()

    df.skew()

    df.kurt()

    sns.boxplot(x="building_age_yrs", data=df)
    plt.title("Boxplot")
    plt.show()

    sns.barplot(x=df["min_to_subway"],y=df["building_age_yrs"],palette="viridis")
    plt.xlabel('Mins to Subway')
    plt.ylabel('Building Age')
    plt.title('Bar Graph')
    plt.show()

    sns.histplot(df['rent'], bins=10, kde=False, color='blue')
    plt.xlabel('Rent')
    plt.ylabel('Frequency')
    plt.title('Histogram')
    plt.show()

    sns.scatterplot(x="rent",y="floor",data=df)
    plt.title('Scatterplot')
    plt.show()

    sns.lineplot(x="rent",y="bedrooms",data=df)
    plt.title("Lineplot")
    plt.show()
    '''

    competitor='''
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt

    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    from nltk.stem import WordNetLemmatizer
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')
    stop_words = set(stopwords.words('english'))

    import string

    def preprocess(t):
        w = word_tokenize(t.lower())
        data = list()
        for word in w:
            if word.lower() not in stop_words:
                data.append(word)
        text = ' '.join(data)
        return text.translate(str.maketrans('', '', string.punctuation))

    def remove_punctuation(text):
        return text.translate(str.maketrans('', '', string.punctuation))


    import re
    def remove_special_characters(text):
        pattern = r'[^a-zA-Z0-9\s]'
        clean_text = re.sub(pattern, '', text)
        return clean_text


    from textblob import TextBlob


    def get_subjectivity(text):
        return TextBlob(text).sentiment.subjectivity


    def get_polarity(text):
        return TextBlob(text).sentiment.polarity


    df = pd.read_csv('k_competitor.csv')
    df

    apple = pd.DataFrame({'Review': df['apple']})
    apple.head()

    garbage = apple['Review'].apply(lambda x: isinstance(x, float))
    apple = apple[~garbage]

    apple['Review'] = apple['Review'].apply(preprocess)
    apple['Review'] = apple['Review'].apply(remove_special_characters)
    apple['Review'] = apple['Review'].apply(remove_punctuation)
    apple['Review'].reset_index(drop=True, inplace=True)
    apple['subjectivity'] = apple['Review'].apply(get_subjectivity)
    apple['polarity'] = apple['Review'].apply(get_polarity)
    apple.head()

    threshold = 0.05
    apple['sentiment'] = apple['polarity'].apply(lambda x: ('Positive' if x
            >= threshold else ('Negative' if x < -threshold else 'Neutral'
            )))

    sentiment_counts = apple['sentiment'].value_counts()
    plt.barh(sentiment_counts.index, sentiment_counts.values)
    plt.xlabel('Count')
    plt.ylabel('Sentiment')
    plt.title('Sentiment Distribution in Apple Data')
    plt.show()

    apple_sentiments = apple.groupby('sentiment')['sentiment'].count()
    print("Apple",apple_sentiments)

    samsung = pd.DataFrame({'Review': df['samsung']})
    samsung.head()

    garbage = samsung['Review'].apply(lambda x: isinstance(x, float))
    samsung = samsung[~garbage]

    samsung['Review'] = samsung['Review'].apply(preprocess)
    samsung['Review'] = samsung['Review'].apply(remove_special_characters)
    samsung['Review'] = samsung['Review'].apply(remove_punctuation)
    samsung['Review'].reset_index(drop=True, inplace=True)
    samsung['subjectivity'] = samsung['Review'].apply(get_subjectivity)
    samsung['polarity'] = samsung['Review'].apply(get_polarity)
    samsung.head()

    threshold = 0.05
    samsung['sentiment'] = samsung['polarity'].apply(lambda x: ('Positive'
            if x >= threshold else ('Negative' if x
            < -threshold else 'Neutral')))

    sentiment_counts = samsung['sentiment'].value_counts()
    plt.barh(sentiment_counts.index, sentiment_counts.values)
    plt.xlabel('Count')
    plt.ylabel('Sentiment')
    plt.title('Sentiment Distribution of Samsung Data')
    plt.show()

    samsung_sentiments = samsung.groupby('sentiment')['sentiment'].count()
    print("Samsung",samsung_sentiments)

    colors = ['red', 'blue']
    (fig, ax) = plt.subplots()
    apple_sentiments.plot(
        kind='bar',
        ax=ax,
        position=0,
        width=0.4,
        label='apple',
        color=colors[0],
        )
    samsung_sentiments.plot(
        kind='bar',
        ax=ax,
        position=1,
        width=0.4,
        label='samsung',
        color=colors[1],
        )
    ax.set_xlabel('Sentiment Label')
    ax.set_ylabel('Number of Tweets')
    ax.legend()
    plt.show()
    '''
    
    amazon='''
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt

    df = pd.read_csv('70_10_mobile-reviews.csv')
    df.drop(columns=df.columns[df.columns != 'reviewTitle'], inplace=True)

    df

    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    from nltk.stem import WordNetLemmatizer
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')
    stop_words = set(stopwords.words('english'))


    def preprocess(t):
        w = word_tokenize(t.lower())
        data = list()
        for word in w:
            if word.lower() not in stop_words:
                data.append(word)
        return ' '.join(data)


    df['reviewTitle'] = df['reviewTitle'].apply(preprocess)
    df['reviewTitle'].reset_index(drop=True, inplace=True)

    import re


    def remove_special_characters(text):
        pattern = r'[^a-zA-Z0-9\s]'
        clean_text = re.sub(pattern, '', text)
        return clean_text


    df['reviewTitle'] = df['reviewTitle'].apply(remove_special_characters)

    import string


    def remove_punctuation(text):
        return text.translate(str.maketrans('', '', string.punctuation))


    df['reviewTitle'] = df['reviewTitle'].apply(remove_punctuation)
    df['reviewTitle'].reset_index(drop=True, inplace=True)

    df.isnull().sum()

    from textblob import TextBlob


    def get_subjectivity(text):
        return TextBlob(text).sentiment.subjectivity


    def get_polarity(text):
        return TextBlob(text).sentiment.polarity


    df['subjectivity'] = df['reviewTitle'].apply(get_subjectivity)
    df['polarity'] = df['reviewTitle'].apply(get_polarity)

    df

    threshold = 0.05
    df['sentiment'] = df['polarity'].apply(lambda x: ('Positive' if x
            >= threshold else ('Negative' if x < -threshold else 'Neutral'
            )))

    df['sentiment'].value_counts()

    df['sentiment'].value_counts().plot.barh()

    df_positive = df[df['sentiment'] == 'Positive']
    df_negative = df[df['sentiment'] == 'Negative']
    df_neutral = df[df['sentiment'] == 'Neutral']

    from wordcloud import WordCloud
    wordcloud = WordCloud(width=800, height=400, background_color='white'
                        ).generate(' '.join(df_positive['reviewTitle']))
    plt.figure(figsize=(10, 5))
    plt.title('WordCloud for positive sentiments')
    plt.imshow(wordcloud, interpolation='lanczos')
    plt.axis('off')
    plt.show()

    wordcloud = WordCloud(width=800, height=400, background_color='white'
                        ).generate(' '.join(df_negative['reviewTitle']))
    plt.figure(figsize=(10, 5))
    plt.title('WordCloud for negatvie sentiments')
    plt.imshow(wordcloud, interpolation='lanczos')
    plt.axis('off')
    plt.show()
    '''
    
    network='''
    import networkx as nx
    import csv
    import matplotlib.pyplot as plt


    def load_facebook_network(file_path):
        with open(file_path, "r") as file:
            edges = [line.strip().split() for line in file.readlines()]
        return edges


    def compute_centrality_measures(graph):
        degree_centrality = nx.degree_centrality(graph)
        betweenness_centrality = nx.betweenness_centrality(graph)
        edge_betweenness_centrality = nx.edge_betweenness_centrality(graph)
        eigenvector_centrality = nx.eigenvector_centrality(graph, max_iter=1000)
        return (
            degree_centrality,
            betweenness_centrality,
            edge_betweenness_centrality,
            eigenvector_centrality,
        )


    def find_bridges(graph):
        bridges = list(nx.bridges(graph))
        return bridges


    def main():
        facebook_network = load_facebook_network("facebook_networkdata.txt")
        G = nx.Graph()
        G.add_edges_from(facebook_network)
        nx.draw(G)
        plt.show()
        
        (
            degree_centrality,
            betweenness_centrality,
            edge_betweenness_centrality,
            eigenvector_centrality,
        ) = compute_centrality_measures(G)
        print("Degree Centrality:")
        for node, centrality in degree_centrality.items():
            print(f"Node {node}: {centrality}")

        print()
        print("Betweenness Centrality:")
        for node, centrality in betweenness_centrality.items():
            print(f"Node {node}: {centrality}")

        print()
        print("Edge Betweenness Centrality:")
        for edge, centrality in edge_betweenness_centrality.items():
            print(f"Edge {edge}: {centrality}")

        print()
        print("Eigenvector Centrality:")
        for node, centrality in eigenvector_centrality.items():
            print(f"Node {node}: {centrality}")

        print()
        print("Bridges:")
        bridges = find_bridges(G)
        print(bridges)

    if __name__ == "__main__":
        main()
    '''
    
    fb_network='''
    1 4
    1 5
    2 3
    2 4
    2 5
    3 1
    3 5
    4 1
    4 2
    4 5
    5 1
    5 2
    5 3
    5 6
    6 7
    6 10
    7 8
    7 9
    8 6
    8 9
    8 10
    9 7
    9 8
    10 6
    10 7
    10 11
    11 13
    11 15
    12 13
    12 14
    12 15
    13 12
    13 15
    14 12
    14 13
    14 15
    15 13
    15 14
    ''' 
    if name=='twitter':
        print(twitter)
    elif name=='eda':
        print(eda)
    elif name=='competitor':
        print(competitor)
    elif name=='amazon':
        print(amazon)
    elif name=='network':
        print(network)
    elif name=='fb-data':
        print(fb_network)
    else:
        print(f'ValueError: name should be any one from [\'twitter\', \'brand\', \'amazon\', \'network\', \'fb-data\', \'eda\', \'competitor\']')