def code(name):
    sentiment=''''
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
    stop_words=set(stopwords.words('english'))
    
    df=pd.read_csv('sentiment_tweets3.csv')
    df=df.drop(columns=['Index'])
    df.head()

    def preprocess(t):
        w=word_tokenize(t.lower())
        data=list()
        for word in w:
            if word.lower() not in stop_words:
                data.append(word)
        return ' '.join(data)
    df['message to examine']=df['message to examine'].apply(preprocess)
    df['message to examine'].reset_index(drop=True, inplace=True)

    df.head()

    import string
    def remove_punctuation(text):
        return text.translate(str.maketrans('', '', string.punctuation))

    df['message to examine']=df['message to examine'].apply(remove_punctuation)
    df['message to examine'].reset_index(drop=True, inplace=True)

    df.head()

    from textblob import TextBlob
    def get_subjectivity(text):
        return TextBlob(text).sentiment.subjectivity
    def get_polarity(text):
        return TextBlob (text).sentiment.polarity
    df['subjectivity']=df['message to examine'].apply(get_subjectivity)
    df['polarity']=df['message to examine'].apply(get_polarity)

    threshold=0.05
    df['sentiment'] = df['polarity'].apply(
        lambda x: "Positive" if x >= threshold
        else ("Negative" if x < -threshold else "Neutral"))

    df['sentiment'].value_counts()

    df['sentiment'].value_counts().plot.barh()

    df_positive=df[df['sentiment']=='Positive']
    df_negative=df[df['sentiment']=='Negative']
    df_neutral=df[df['sentiment']=='Neutral']

    from wordcloud import WordCloud
    def generate_wordcloud (text):
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate (text)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='lanczos')
        plt.axis('off')
        plt.show()
    
    generate_wordcloud(' '.join(df_positive['message to examine']))

    generate_wordcloud(' '.join(df_negative['message to examine']))

    generate_wordcloud(' '.join(df_neutral['message to examine']))
    '''

    eda='''
    from matplotlib import pyplot as plt
    import seaborn as sns, pandas as pd, numpy as np

    df=pd.read_csv("CardioGoodFitness.csv")
    df = df.select_dtypes(include=['number'])
    df

    df.mean()

    df.mode()

    df.median()

    print(f"Max Age is: {df.max()['Age']}")
    print(f"Min Age is: {df.max()['Age']}")
    print(f"Difference in Age is: {df.max()['Age']-df.min()['Age']}")

    df.var()

    df.std()

    df.skew()

    df.kurt()

    sns.boxplot(x="Age", data=df)
    plt.title("Boxplot")
    plt.show()

    sns.barplot(x=df["Fitness"],y=df["Education"],palette="viridis")
    plt.xlabel('Fitness')
    plt.ylabel('Education')
    plt.title('Bar Graph')
    plt.show()

    sns.histplot(df['Fitness'], bins=10, kde=False, color='blue')
    plt.xlabel('Fitness')
    plt.ylabel('Frequency')
    plt.title('Histogram')
    plt.show()

    sns.scatterplot(x="Age",y="Miles",data=df)
    plt.title('Scatterplot')
    plt.show()

    sns.lineplot(x="Age",y="Income",data=df)
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
    stop_words=set(stopwords.words('english'))

    import string
    def preprocess(t):
        w=word_tokenize(t.lower())
        data=list()
        for word in w:
            if word.lower() not in stop_words:
                data.append(word)
        text=' '.join(data)
        return text.translate(str.maketrans('', '', string.punctuation))

    from textblob import TextBlob
    def get_subjectivity(text):
        return TextBlob(text).sentiment.subjectivity
    def get_polarity(text):
        return TextBlob (text).sentiment.polarity

    swiggy=pd.read_csv("swiggy_n.csv")
    swiggy.info()
    swiggy=swiggy.drop(columns=['App','review_date','thumbsUpCount',
                                'developer_response','developer_response_date', 'appVersion'])
    swiggy.head()
    swiggy['Review']=swiggy['review_description'].apply(preprocess)
    swiggy['Review'].reset_index(drop=True, inplace=True)
    swiggy['subjectivity']=swiggy['Review'].apply(get_subjectivity)
    swiggy['polarity']=swiggy['Review'].apply(get_polarity)
    swiggy.head()

    threshold=0.05
    swiggy['sentiment'] = swiggy['polarity'].apply(
        lambda x: "Positive" if x >= threshold
        else ("Negative" if x < -threshold else "Neutral"))

    sentiment_counts = swiggy['sentiment'].value_counts()
    plt.barh(sentiment_counts.index, sentiment_counts.values)
    plt.xlabel('Count')
    plt.ylabel('Sentiment')
    plt.title('Sentiment Distribution in Swiggy Data')
    plt.show()

    swiggy_sentiments=swiggy.groupby('sentiment')['sentiment'].count()
    print(swiggy_sentiments)

    zomato=pd.read_csv("zomato_n.csv")
    zomato.info()
    zomato=zomato.drop(columns=['App','review_date','thumbsUpCount',
                                'developer_response','developer_response_date','appVersion'])
    zomato.head()
    garbage=zomato['review_description'].apply(lambda x: isinstance(x, float))
    zomato=zomato[~garbage]
    zomato['reviewText']=zomato['review_description'].apply(preprocess)
    zomato['reviewText'].reset_index(drop=True, inplace=True)
    zomato['subjectivity']=zomato['reviewText'].apply(get_subjectivity)
    zomato['polarity']=zomato['reviewText'].apply(get_polarity)
    zomato.head()

    threshold=0.05
    zomato['sentiment'] = zomato['polarity'].apply(
        lambda x: "Positive" if x >= threshold
        else ("Negative" if x < -threshold else "Neutral"))

    sentiment_counts = zomato['sentiment'].value_counts()
    plt.barh(sentiment_counts.index, sentiment_counts.values)
    plt.xlabel('Count')
    plt.ylabel('Sentiment')
    plt.title('Sentiment Distribution of Zomato Data')
    plt.show()

    zomato_sentiments=zomato.groupby('sentiment')['sentiment'].count()
    print(zomato_sentiments)

    colors = ['red', 'blue']
    fig, ax = plt.subplots()
    swiggy_sentiments.plot(kind='bar', ax=ax, position=0, width=0.4, label='swiggy', color=colors[0])
    zomato_sentiments.plot(kind='bar', ax=ax, position=1, width=0.4, label='zomato', color=colors[1])
    ax.set_xlabel('Sentiment Label')
    ax.set_ylabel('Number of Tweets')
    ax.legend()
    plt.show()
    '''
    if name=='sentiment':
        print(sentiment)
    elif name=='eda':
        print(eda)
    elif name=='competitor':
        print(competitor)
    else:
        print(f'ValueError: name should be any one from [\'sentiment\', \'eda\', \'competitor\']')