def sentiment():
    s=''''
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
    print(s)