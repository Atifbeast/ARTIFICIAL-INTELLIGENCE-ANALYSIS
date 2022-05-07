import streamlit as st
import pickle
import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('omw-1.4')
nltk.download('wordnet')
from nltk.tokenize import word_tokenize
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import string
from nltk.stem.wordnet import WordNetLemmatizer
import tweepy 
from PIL import Image
image = Image.open('artificial-intelligence.jpg')

stops = stopwords.words('english')
punct = list(string.punctuation)
ps = PorterStemmer()
lemmatizer = WordNetLemmatizer()

Model = pickle.load(open("EmailModel.pkl", 'rb'))
Vector = pickle.load(open("TfidfEmail.pkl", 'rb'))

Model2 = pickle.load(open("Tweets.pkl", 'rb'))
vector2 = pickle.load(open("TweetsTf.pkl", 'rb'))

col1, col2 = st.columns(2)
col3, col4, col5 = st.columns(3)
col6, col7, col8 = st.columns(3)

import tweepy

consumer_key = "TSTOsLg7xZYFoSaIGYuzodKIR"
consumer_secret = "aoEys8Q0xbk8qO2iyd2E7nnplPg3KfeDmx1Yqw1G0JokpjOgKy"
access_key = "1503228035130007559-XqocHKgXzvLxwpalUVfgv58HysMr4K"
access_secret = "ZWVE72yJlX3ATKLlczVbonXVwpjsNFdtRgCpSYVnO7KXx"


ml = st.selectbox("SELECT BELOW", ['CLICK ME', 'EMAIL SPAM DETECTOR', 'TWITTER SENTIMENT ANALYSIS'])

def tweets(username, num):
    global tmp
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

    
    auth.set_access_token(access_key, access_secret)

    api = tweepy.API(auth)
    # number = st.number_input('Select Number Of Tweets To Perform Sentiments', min_value=10, max_value=3200, step=10) 
    number_of_tweets = num   
    try:

        tweets = api.user_timeline(screen_name = username, count = number_of_tweets)
        tmp = []
        tweets_for_csv = [tweet.text for tweet in tweets]

        for j in tweets_for_csv:
            tmp.append(j)

    except Exception:
            st.error("ERROR : UserName Not Found Check If You Are Entering Correctly With '@' Included")

def stream():
    st.title('EMAIL/MSG SPAM CLASSIFICATION')
    intro = 'DEVELOPED IN PYTHON BY "ATIF"'
    st.header(intro) 

    email = st.text_input('Enter Your Email/Message')

    but = st.button('CHECK')
    if but:
        waste = []
        youlist = word_tokenize(email)
        for i in youlist:
            if i in stops or i in punct:
                youlist.remove(i)
                waste.append(i)
        for i,j in enumerate(youlist):
            youlist[i] = ps.stem(j)

        final_msg = [' '.join(youlist)]
        Email = Vector.transform(final_msg)
        Prediction = Model.predict(Email)
        if Prediction == 1: 
            output = "It's a HAM Mail"
            st.success(output)
            
        elif Prediction == 0:
            output2 = "It's a SPAM Mail"
            st.error(output2)

def stream2():
    st.warning('WARNING : Extracting Government Handled Tweets Might Result in Lot of Negative "Tweets" Coz Government Agencies Tweets on Issue Related To Global Disturbances "Like Israel Oppression/Illegal Settlements On Palestinian Lands" Or "Shanghai Crueality on Uyghur" Or "American Forces in Middle-East !!!"')
    st.warning("Search For User With '@' Symbol In The Beginning Else Results Might Not Get Fetched")
    st.warning("IT ONLY SHOWS THE RECENT TWEETS {<7 DAYS} MADE BY THE USER HENCE IF YOU DONT GET REQUIRED NUMBER OF TWEETS DO NOT REPORT IT AS A BUG !!!")
    st.header('TWEETS SENTIMENT ANALYSIS')
    with col2:
        st.markdown("<h6 style='text-align: right; color: red;'>DEVELOPED BY ATIF</h1>", unsafe_allow_html=True)
    twit = st.text_input('SEARCH FOR A TWITTER-USER', '@Twitter')
    numberv = st.number_input('Select Number Of Tweets To Perform Sentiments', min_value=10, max_value=3200, step=10)                      
    but = st.button("ANALYZE IT", key=1) 
    # global pos, neg, neuS
    if but and len(twit)!=0: 
        tweets(twit, numberv) # tmp is a list stored with tweets
        pos = []
        neg = []
        neu = []
        tokenizer = TweetTokenizer()
        try:
            for i in tmp:
                n = tokenizer.tokenize(i)
                for j in n: 
                    if j in punct:
                        n.remove(j)
                    else: 
                        pass
                for k in n: 
                    if k in stops:
                        n.remove(k)
                    else:
                        pass           
                for a,b in enumerate(n):
                    n[a] = lemmatizer.lemmatize(b, pos='a')
                    
                for p,q in enumerate(n):
                    n[p] = ps.stem(q)
                    
                for z in n:
                        z = z.lower()


                final = ' '.join(n)
                final = [final]

                final = vector2.transform(final).toarray()
                ans = Model2.predict(final)
                
                l = [0.47, 0.46, 0.45, 0.48, 0.49, 0.50, 0.51, 0.52, 0.53] 

                prob = Model2.predict_proba(final)
                prob = prob[0][1]
                f = "{0:.2f}" 
                prob = f.format(prob) 
                prob = float(prob)

                if prob in l:
                    # print('Neutral Tweet')
                    neu.append(i)
                elif ans == 1:
                    # print('Positive Tweet')
                    pos.append(i)
                elif ans == 0:
                    neg.append(i)
            st.write('idhar')
            st.write(f"NUMBER OF POSITIVE TWEETS : {len(pos)}")
            st.write(f"NUMBER OF NEGATIVE TWEETS : {len(neg)}")
            st.write(f"NUMBER OF NEUTRAL TWEETS : {len(neu)}")

            st.markdown(f'<p style="background-color:cyan;color:black;font-size:24px;border-radius:2%;">CHECK OUT THE TWEETS REPORT BELOW :)</p>', unsafe_allow_html=True)
            st.markdown(f'<p style="background-color:black;color:green;font-size:24px;border-radius:2%;">POSITIVE TWEETS : </p>', unsafe_allow_html=True)
            st.write(pos)
            st.markdown(f'<p style="background-color:black;color:red;font-size:24px;border-radius:2%;">NEGATIVE TWEETS : </p>', unsafe_allow_html=True)
            st.write(neg)
            st.markdown(f'<p style="background-color:black;color:orange;font-size:24px;border-radius:2%;">NEUTRAL TWEETS : </p>', unsafe_allow_html=True)
            st.write(neu)

        except Exception as e:
            pass

    elif len(twit) == 0:
        st.error("ERROR : UserName Required")     

if ml == 'EMAIL SPAM DETECTOR':
    stream()
elif ml == 'CLICK ME':
    st.title("WELCOME TO ARTIFICIAL INTELLIGENCE WORLD DEVELOPED BY ATIF")
    st.image(image, 'AI BY ATIF')
else:
    stream2()
