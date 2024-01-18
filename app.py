import streamlit as st
import pandas as pd
import helper
import preprocessor
import warnings
warnings.filterwarnings("ignore")
import matplotlib.pyplot as plt
import seaborn as sns



df=pd.read_csv("data/athlete_events.csv")
region_df=pd.read_csv("data/noc_regions.csv")

df=preprocessor.preprocess(df,region_df)

st.sidebar.title("Olympics Analysis")
user_menu=st.sidebar.radio("Select an Option",
                 ("Medal Tally","Overall Analysis","Country-wise Analysis","Athlete wise Analysis"))

if user_menu == "Medal Tally":
    st.sidebar.header('Medal Tally')
    years,country=helper.country_year_list(df)

    selected_year=st.sidebar.selectbox("Select Year",years)
    selected_country=st.sidebar.selectbox("Select Country",country)
    medal_tally=helper.fetch_medal_tally(df,selected_year,selected_country)
    if selected_year=="Overall" and selected_country=="Overall":
        st.title("Overall Tally")
    if selected_year!="Overall" and selected_country=="Overall":
        st.title("Medal Tally in "+str(selected_year)+" Olympics")
    if selected_year=="Overall" and selected_country!="Overall":
        st.title(selected_country+"'s overall performance")
    if selected_year!="Overall" and selected_country!="Overall":
        st.title(selected_country+"'s performance in "+str(selected_year)+" Olympics")
    
    st.table(medal_tally)

if user_menu=="Overall Analysis":
    editions=df['Year'].unique().shape[0] -1
    cities=df['City'].unique().shape[0]
    sports=df["Sport"].unique().shape[0]
    events=df['Event'].unique().shape[0]
    athletes=df['Name'].unique().shape[0]
    nations=df['region'].unique().shape[0]
    st.title("Top Statistics")
    col1,col2,col3=st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1,col2,col3=st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)

    st.header("Participating nations over the years")
    nations_over_time=helper.data_over_time(df,'region')
    fig1,ax1=plt.subplots(nrows=1,ncols=1)
    ax1=sns.lineplot(data=nations_over_time,x="Year",y='region',color='black').figure
    st.pyplot(ax1)

    st.header("Events over the years")
    events_over_time=helper.data_over_time(df,'Event')
    fig2,ax2=plt.subplots(ncols=1,nrows=1)
    ax2=sns.lineplot(data=events_over_time,x="Year",y='Event',color='black').figure
    st.pyplot(ax2)

    st.header("Athletes over the years")
    athletes_over_time=helper.data_over_time(df,'Name')
    fig2,ax2=plt.subplots(ncols=1,nrows=1)
    ax2=sns.lineplot(data=athletes_over_time,x="Year",y='Name',color='black').figure
    st.pyplot(ax2)

    st.header("Number of events over time relative to every sport ")
    fig,ax=plt.subplots(figsize=[25,25])
    x=df.drop_duplicates(["Year","Sport","Event"])
    ax=sns.heatmap(x.pivot_table(index='Sport',columns="Year",values="Event",aggfunc='count').fillna(0),annot=True).figure
    st.pyplot(ax)

    st.title("Most successful Athletes")
    sport_list=df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    selected_sport=st.selectbox("Select a sport",sport_list)
    x=helper.most_successful(df,selected_sport)
    st.table(x)

if user_menu=="Country-wise Analysis":
    