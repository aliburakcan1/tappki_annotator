import streamlit as st
import random
from tweet import Tweet
from functions import get_people, get_tags, get_programs, get_sports, get_animals

# wider layout
st.set_page_config(layout="wide")

if "tweet_ids" not in st.session_state:
    with open("data/tweet_ids.txt") as f:
        tweet_ids = f.read().splitlines()
    st.session_state.tweet_ids = tweet_ids

if "tweet_id" not in st.session_state:
    st.session_state.tweet_id = random.choice(st.session_state.tweet_ids)

print({k:v for k,v in st.session_state.items() if k != "tweet_ids"})

col1, col2 = st.columns(2)

with col1:
    new_tweet = st.session_state.next if "next" in st.session_state else False
    if new_tweet:
        current_tweet_id = random.choice(st.session_state.tweet_ids)
        Tweet("https://twitter.com/i/status/{}".format(current_tweet_id)).component()
        st.session_state.tweet_id = current_tweet_id
    else:
        Tweet("https://twitter.com/i/status/{}".format(st.session_state.tweet_id)).component()
        

with col2:
    if new_tweet:
        st.session_state.title = ""
        st.session_state.content = ""
        st.session_state.people = []
        st.session_state.tags = []
        st.session_state.program = "Yok"
        st.session_state.sport = "Yok"
        st.session_state.music = ""
        st.session_state.animal = "Yok"

    #print({k:v for k,v in st.session_state.items() if k != "tweet_ids"})
    col1, col2 = st.columns(2)
    with col1:
        title = st.text_input("Başlık", key="title", placeholder="Tepki Başlığı")
        content = st.text_area("İçerik", key="content", placeholder="Tepkinin içinde geçen tüm cümleyi/cümleleri yazın.")
        people = st.multiselect("Kişiler", get_people(), key="people", help="Tepkinin içinde varsa fenomenleri/ünlüleri seçin.")
        tags = st.multiselect("Etiketler", get_tags(), key="tags", help="Tepki için en uygun olan etiketleri seçin.")
    with col2:
        program = st.selectbox("Film - Dizi - Program - YT kanalı", get_programs(), key="program", help="Tepkinin hangi program içerisinde gerçekleştiğini girin.")
        sport = st.selectbox("Spor", get_sports(), key="sport", help="Tepkinin hangi spor dalı ile ilgili olduğunu seçin.")
        animal = st.selectbox("Hayvan", get_animals(), key="animal", help="Tepkinin hangi hayvan ile ilgili olduğunu seçin.")
        music = st.text_input("Müzik", key="music", placeholder="Müzik", help="Tepkinin içinde geçen müzik varsa yazın.")
    
        if st.button("Tepkiyi Kaydet", key="save", type="primary", use_container_width=True):
            print({"title": title, "content": content, "people": people, "tags": tags, "program": program, "music": music, "animal": animal})
            st.success("Kaydedildi Sırada ki tweet'e geçebilirsiniz.")
        
        st.button("Sonraki Tweet", key="next", type="secondary", use_container_width=True)
    
    with st.expander("Tepkide var seçeneklerde yoksa buraya tıklayın"):
        add_type = st.selectbox("Tip", ["Kişi", "Etiket", "Film - Dizi - Program - YT kanalı", "Spor", "Hayvan"], key="add_type", help="Ekleme yapmak istediğiniz seçeneği seçin.", label_visibility="collapsed")
        add_input = st.text_input("Değer", key="add_input", placeholder=f"Eklemek istediğiniz {add_type} girin.", help=f"{add_type} adını girin.", label_visibility="collapsed")
        
        if st.button("Ekle", key="add", type="primary", use_container_width=True):
            st.success(f"{add_input} ismindeki {add_type} eklendi")

