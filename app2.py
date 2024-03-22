import streamlit as st
import pandas as pd
from definition import select_league, stats, period_stats, seoson_inplay_events, period_inplay_events, season_pthrows, period_pthrows, stats_viewer_pkind, swing_viewer_pkind, stats_viewer_pitchname, swing_viewer_pitchname
from definition import season_pkind, period_pkind, season_pitchname, period_pitchname, stats_viewer, swing_viewer, event_viewer, stats_viewer_pthrows, swing_viewer_pthrows, swingmap_df, spraychart_df
from dataframe import dataframe
from map import select_count_option, select_sum_option, select_sum_plate_option, swingmap_count_option, season_spraychart, season_period_spraychart
import time
from PIL import Image
from user import login

st.set_page_config(page_title="Batting Analytics Page", layout="wide")
st.title("KT WIZ :red[BATTING ANALYTICS] PAGE")

headerSection = st.container()
mainSection = st.container()
loginSection = st.container()
logOutSection = st.container()

def LoggedOut_Clicked():
    st.session_state['loggedIn'] = False
  
def show_logout_page():
    loginSection.empty();
    with logOutSection:
        st.sidebar.button("Log Out", key="logout", on_click=LoggedOut_Clicked)

def LoggedIn_Clicked(userName, password):
    if login(userName, password):
        st.session_state['loggedIn'] = True
    else:
        st.session_state['loggedIn'] = False;
        st.error("유효하지 않은 ID 또는 패스워드 입니다.")

def show_login_page():
    with loginSection:
        if st.session_state['loggedIn'] == False:
            userName = st.text_input(label="", value="", placeholder="ID를 입력하시오")
            password = st.text_input(label="", value="", placeholder="패스워드를 입력하시오", type="password")
            st.button("Log In", on_click=LoggedIn_Clicked, args=(userName, password))

def show_main_page():
    with mainSection:

        st.markdown("""<style>[data-testid=stSidebar] [data-testid=stImage]{text-align: center;display: block;margin-left: auto; margin-right: auto; width: 85%;}</style>""", unsafe_allow_html=True)
        with st.sidebar:
            st.image("ktwiz_emblem.png")

        st.markdown("""<style>[data-testid="stSidebar"][aria-expanded="true"] > div:first-child{width: 340px; }""", unsafe_allow_html=True,)

        id_dataset = pd.read_csv('./player_id_info_2024.csv')
        id_dataset = id_dataset[['team','NAME','POS','TM_ID']]
        id_dataset = id_dataset[id_dataset['POS'] != 'P']

        #------------------------------------------------------------------------------

        # sidebar_title = '<p style="text-align: center; font-family:Times New Roman; color:black; font-size: 70px;font-weight:bold"></p>'
        # st.sidebar.markdown(sidebar_title, unsafe_allow_html=True)

        sidebar_text = '<p style="text-align: center; font-family:sans-serif; color:red; font-size: 22px;font-weight:bold">[타자분석 페이지]</p>'
        st.sidebar.markdown(sidebar_text, unsafe_allow_html=True)

        sidebar_text = '<p style="text-align: center; font-family:sans-serif; color:gray; font-size: 14px;">본 웹페이지는 kt wiz 전략데이터팀이<br> 개발 및 발행하였으며 허용되는 사용자 외 <br>배포 및 사용을 엄금함</p>'
        st.sidebar.markdown(sidebar_text, unsafe_allow_html=True)

        #-------------------------------------------------------------------------

        teams = id_dataset['team'].tolist() 
        teams_list = id_dataset['team'].unique().tolist()
        select_team = st.sidebar.selectbox('팀명 선택', teams_list)
        player_dataset = id_dataset[id_dataset['team'] == select_team]

        player_list = player_dataset['NAME'].unique().tolist()
        select_player = st.sidebar.multiselect('선수 선택', player_list)
        
        option = st.sidebar.selectbox('리그 선택', ("-", "KBO(1군)", "KBO(2군)", "AAA"))

        if st.sidebar.button('실행'):
            
            for i in range(len(select_player)):
                
                find_player = player_dataset[player_dataset['NAME'] == select_player[i]]
                id = find_player.iloc[0]['TM_ID']
                league = select_league(option)
        
                id = int(id)
                player_df = dataframe(league, id)
        
                season_stats_df = stats(player_df)
                period_stats_df = period_stats(player_df)
        
                stats_df = pd.concat([period_stats_df, season_stats_df])
        
                stats_viewer_df = stats_viewer(stats_df)
                swing_viewer_df = swing_viewer(stats_df)
        
                progress_text = "Operation in progress. Please wait."
                my_bar = st.progress(0, text=progress_text)
                
                for percent_complete in range(100):
                    time.sleep(0.1)
                    my_bar.progress(percent_complete + 1, text=progress_text)
        
                st.title(select_player[i])
        
                st.subheader('[시즌별 :red[주요현황]]')
                st.dataframe(stats_viewer_df, width=1300)
                st.dataframe(swing_viewer_df, width=1300)
        
                st.subheader('[시즌별 :red[투구지점]]')
                pitched_factor = 'player_name'
                select_count_option(player_df, pitched_factor)
        
                st.subheader('[시즌별 :red[스윙지점]]')
                swing_factor = 'swing'
                select_sum_option(player_df, swing_factor)
        
                st.subheader('[시즌별 :red[LSA 4+]]')
                lsa_factor = 'launch_speed_angle'
                select_sum_option(player_df, lsa_factor)
                select_sum_plate_option(player_df, lsa_factor)
        
                st.subheader('[시즌별 :red[Swing Map]]')
                swingmap_factor = 'player_name'
                swingmap_dataframe = swingmap_df(player_df)
                swingmap_count_option(swingmap_dataframe, swingmap_factor)
        
                st.subheader('[시즌별 :red[Spray Chart]]')
                spraychart_dataframe = spraychart_df(player_df)
                season_spraychart(spraychart_dataframe)

                st.divider()


            # tabs = st.tabs(select_player)
            
            # for i in range(len(tabs)):

            #     with tabs[i]:
                    
                    # find_player = player_dataset[player_dataset['NAME'] == select_player[i]]
                    # id = find_player.iloc[0]['TM_ID']
                    # league = select_league(option)

                    # id = int(id)
                    # player_df = dataframe(league, id)

                    # season_stats_df = stats(player_df)
                    # period_stats_df = period_stats(player_df)

                    # stats_df = pd.concat([period_stats_df, season_stats_df])

                    # stats_viewer_df = stats_viewer(stats_df)
                    # swing_viewer_df = swing_viewer(stats_df)

                    # progress_text = "Operation in progress. Please wait."
                    # my_bar = st.progress(0, text=progress_text)
                    
                    # for percent_complete in range(100):
                    #     time.sleep(0.1)
                    #     my_bar.progress(percent_complete + 1, text=progress_text)

                    # st.title(select_player[i])

                    # st.subheader('[시즌별 :red[주요현황]]')
                    # st.dataframe(stats_viewer_df, width=1300)
                    # st.dataframe(swing_viewer_df, width=1300)

                    # st.subheader('[시즌별 :red[투구지점]]')
                    # pitched_factor = 'player_name'
                    # select_count_option(player_df, pitched_factor)

                    # st.subheader('[시즌별 :red[스윙지점]]')
                    # swing_factor = 'swing'
                    # select_sum_option(player_df, swing_factor)

                    # st.subheader('[시즌별 :red[LSA 4+]]')
                    # lsa_factor = 'launch_speed_angle'
                    # select_sum_option(player_df, lsa_factor)
                    # select_sum_plate_option(player_df, lsa_factor)

                    # st.subheader('[시즌별 :red[Swing Map]]')
                    # swingmap_factor = 'player_name'
                    # swingmap_dataframe = swingmap_df(player_df)
                    # swingmap_count_option(swingmap_dataframe, swingmap_factor)

                    # st.subheader('[시즌별 :red[Spray Chart]]')
                    # spraychart_dataframe = spraychart_df(player_df)
                    # season_spraychart(spraychart_dataframe)

                    # st.divider()




with headerSection:
    if 'loggedIn' not in st.session_state:
        st.session_state['loggedIn'] = False
        show_login_page()
    else:
        if st.session_state['loggedIn']:
            show_main_page()
            # show_logout_page()
        else:
            show_login_page()
