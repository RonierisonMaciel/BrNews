import streamlit as st
from PIL import Image
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
from newspaper import Article
import io
import nltk
nltk.download('punkt')

st.set_page_config(page_title='BrNews 🇧🇷: Uma notícia resumida 📰 Portal', page_icon='./Meta/newspaper.ico')


def fetch_news_search_topic(topic):
    site = 'https://news.google.com.br/rss/search?q={}'.format(topic)
    op = urlopen(site)  # Open that site
    rd = op.read()  # read data from site
    op.close()  # close the object
    sp_page = soup(rd, 'xml')  # scrapping data from site
    news_list = sp_page.find_all('item')  # finding news
    return news_list


def fetch_top_news():
    site = 'https://news.google.com.br/news/rss'
    op = urlopen(site)  # Open that site
    rd = op.read()  # read data from site
    op.close()  # close the object
    sp_page = soup(rd, 'xml')  # scrapping data from site
    news_list = sp_page.find_all('item')  # finding news
    return news_list


def fetch_category_news(topic):
    site = 'https://news.google.com.br/news/rss/headlines/section/topic/{}'.format(topic)
    op = urlopen(site)  # Open that site
    rd = op.read()  # read data from site
    op.close()  # close the object
    sp_page = soup(rd, 'xml')  # scrapping data from site
    news_list = sp_page.find_all('item')  # finding news
    return news_list


def fetch_news_poster(poster_link):
    try:
        u = urlopen(poster_link)
        raw_data = u.read()
        image = Image.open(io.BytesIO(raw_data))
        st.image(image, use_column_width=True)
    except:
        image = Image.open('./Meta/no_image.jpg')
        st.image(image, use_column_width=True)


def display_news(list_of_news, news_quantity):
    c = 0
    for news in list_of_news:
        c += 1
        # st.markdown(f"({c})[ {news.title.text}]({news.link.text})")
        st.write('**({}) {}**'.format(c, news.title.text))
        news_data = Article(news.link.text)
        try:
            news_data.download()
            news_data.parse()
            news_data.nlp()
        except Exception as e:
            st.error(e)
        fetch_news_poster(news_data.top_image)
        with st.expander(news.title.text):
            st.markdown(
                '''<h6 style='text-align: justify;'>{}"</h6>'''.format(news_data.summary),
                unsafe_allow_html=True)
            st.markdown("[Leia mais em {}...]({})".format(news.source.text, news.link.text))
        st.success("Data da publicação: " + news.pubDate.text)
        if c >= news_quantity:
            break


def run():
    st.title("BrNews 🇧🇷: Uma notícia resumida 📰")
    image = Image.open('./Meta/newspaper.png')

    col1, col2, col3 = st.columns([3, 5, 3])

    with col1:
        st.write("")

    with col2:
        st.image(image, use_column_width=False)

    with col3:
        st.write("")
    category = ['--Selecione--', 'Top notícias 🔥', 'Notícias favoritas 💙', 'Busque tópicos 🔍']
    cat_op = st.selectbox('Selecione a categoria', category)
    if cat_op == category[0]:
        st.warning('Selecione o tópico!!')
    elif cat_op == category[1]:
        st.subheader("✅ Aqui estão as notícias top 🔥 para você")
        no_of_news = st.slider('Número de notícias:', min_value=5, max_value=25, step=1)
        news_list = fetch_top_news()
        display_news(news_list, no_of_news)
    elif cat_op == category[2]:
        av_topics = ['Escolha o tópico', 'WORLD', 'NATION', 'BUSINESS', 'TECHNOLOGY', 'ENTERTAINMENT', 'SPORTS', 'SCIENCE',
                     'HEALTH']
        st.subheader("Escolha seu tópico favorito")
        chosen_topic = st.selectbox("Escolha o seu tópico favorito", av_topics)
        if chosen_topic == av_topics[0]:
            st.warning("Escolha o tópico")
        else:
            no_of_news = st.slider('Número de notícias:', min_value=5, max_value=25, step=1)
            news_list = fetch_category_news(chosen_topic)
            if news_list:
                st.subheader("✅ Aqui estão algumas notícias do {} para você".format(chosen_topic))
                display_news(news_list, no_of_news)
            else:
                st.error("Nenhuma notícia encontrada para {}".format(chosen_topic))

    elif cat_op == category[3]:
        user_topic = st.text_input("Digite seu tópico 🔍", encoding='utf-8')
        no_of_news = st.slider('Número de notícias:', min_value=5, max_value=15, step=1)

        if st.button("Procurar") and user_topic != '':
            user_topic_pr = user_topic.replace(' ', '')
            news_list = fetch_news_search_topic(topic=user_topic_pr)
            if news_list:
                st.subheader("✅ Aqui estão algumas {} notícias para você".format(user_topic.capitalize()))
                display_news(news_list, no_of_news)
            else:
                st.error("Nenhuma notícia encontrada para {}".format(user_topic))
        else:
            st.warning("Escreva o nome do tópico para pesquisar 🔍")


run()
