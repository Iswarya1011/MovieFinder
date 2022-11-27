import streamlit as st 
from streamlit_option_menu import option_menu 
import pandas as pd
import numpy as np
import plotly.express as px

def closeFilms(film_name, df, r=0.5, cols=["0","1","2","3","4","5","6","7","8","9"]):

    
    dataf = df.copy()
    
    i = dataf.loc[dataf['name'] == film_name]

    
    dataf["dist"] = 0
    for c in cols:
        
        dataf["tempDist"] = dataf[c].apply(lambda x : (x-i[c])**2)
        dataf["dist"] += dataf["tempDist"]

    dataf["dist"] = dataf["dist"].apply(lambda x : np.sqrt(x))
    
    dataf.drop(columns=["tempDist"], inplace=True)
    
    dataf = dataf[dataf["dist"]<r]
    dataf = dataf.sort_values("dist")

    return dataf

with st.sidebar:
    selected = option_menu(
        menu_title = "Main Menu",
        options = ["Home","Movie Finder","About"]
    )

if selected == "Home":
    st.title('Home')
if selected == "Movie Finder":
    st.title('This is my first app!')
    st.write('This is a table')

    df = pd.read_csv("all_films.csv",sep=";")

    genres = []
    for i in range(df.shape[0]):
        sti = df['genre'].loc[i]
        sti = sti.replace(" ", "")
        sti = sti.replace('[',"")
        sti = sti.replace(']',"")
        sti = sti.replace("'", "")
        sti = sti.split(",")
        genres.append(sti)

    s = set()
    for i in range(len(genres)):
        for j in range(len(genres[i])):
            s.add(genres[i][j])
    s = list(s)


    with st.sidebar:
        st.header("Search your Films !")
        filter = st.multiselect('Genres', s)
        
        if len(filter) != 0:
            is_in = []
            for i in range(len(df)):
                if all(elem in df['genre'][i] for elem in filter):
                    is_in.append(1)
                else:
                    is_in.append(0)
            df['is_in'] = is_in

        with st.form(key = 'searchform'):
            nav1,nav2 = st.columns([2,1])

            with nav1:
                search_term = st.text_input('Film Name')
            with nav2:
                st.text("")
                st.text("")
                search_submit = st.form_submit_button()
        
        st.title("Our recommendations")
        st.write("Input a Film Name we will choose the right film for you !")
        
        with st.form(key = 'searchform2'):
            nav1,nav2 = st.columns([2,1])

            with nav1:
                search_term2 = st.text_input('Film Name')
            with nav2:
                st.text("")
                st.text("")
                search_submit2 = st.form_submit_button()
    

    st.write(df)

    data = pd.read_csv('data_famd_web.csv', sep =';')
    data.drop_duplicates(["name"], inplace=True)
    st.write("Distances")
    st.write(data)

    st.write('FAMD')

    fig = px.scatter_3d(data, x='4', y='1', z='2', color='3')

    fig.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor="LightSteelBlue"
        )

    st.plotly_chart(fig)
    try:
        if len(filter) != 0:
            st.title('Research by genre')
            st.write(df[df['is_in']== 1])
    except:
        st.error('This is an error', icon="🚨")

    if search_submit:
        st.success("You searched for {}".format(search_term))
        df_result = df.loc[df['name'].str.contains(search_term, case=False)]
        df_result = df_result.reset_index()
        st.title(f"Results for {search_term}")
        st.write(df_result)
        

    if search_submit2:
        df_result = df.loc[df['name'].str.contains(search_term2, case=False)]
        df_result = df_result.reset_index()
        st.success("You searched for {}".format(df_result['name'][0]))
        cf = closeFilms(df_result['name'][0],data, r=1)
        st.write(cf.head(10))
        fig = px.scatter_3d(cf.head(10), x='4', y='1', z='2', color='3')

        fig.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor="LightSteelBlue"
        )

        st.plotly_chart(fig)
    
    

    
if selected == "About":
    st.title("About us")



