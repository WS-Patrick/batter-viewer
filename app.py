import streamlit as st
import pandas as pd
from definition import select_league, stats, period_stats, seoson_inplay_events, period_inplay_events, season_pthrows, period_pthrows, stats_viewer_pkind, swing_viewer_pkind, stats_viewer_pitchname, swing_viewer_pitchname
from definition import season_pkind, period_pkind, season_pitchname, period_pitchname, stats_viewer, swing_viewer, event_viewer, stats_viewer_pthrows, swing_viewer_pthrows, swingmap_df, spraychart_df
from dataframe import dataframe
from map import select_count_option, select_sum_option, select_sum_plate_option, swingmap_count_option, season_spraychart
import time
from PIL import Image
from user import login

# st.markdown(""" <style>[data-testid=stSidebar] [data-testid=stImage]{text-align: center; display: block; margin-left: auto; margin-right: auto; width: 25%;}</style>""", unsafe_allow_html=True)
# with st.image("ktwiz_emblem.png")

st.set_page_config(page_title="Batting Analytics Page", layout="wide")

# main_title = '<p style="text-align: left; font-family:serif; color:black; font-size: 40px;"> [KT WIZ BATTING ANALYTICS PAGE] </p>'
# st.markdown(main_title, unsafe_allow_html=True)

st.title("KT WIZ :red[BATTING ANALYTICS] PAGE", help)

# main_text = '<p style="text-align: center; font-family:sans-serif; color:gray; font-size: 16px;">본 웹페이지는 kt wiz 전략데이터팀이<br> 개발 및 발행하였으며 허용되는 사용자 외 <br>배포 및 사용을 엄금함</p>'
# st.markdown(main_text, unsafe_allow_html=True)
# st.image("ktwiz_emblem.png")

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

        st.markdown("""<style>[data-testid=stSidebar] [data-testid=stImage]{text-align: center;display: block;margin-left: auto; margin-right: auto; width: 85%;}</style>""", unsafe_allow_html=True        )
        with st.sidebar:
            st.image("ktwiz_emblem.png")

        st.markdown("""<style>[data-testid="stSidebar"][aria-expanded="true"] > div:first-child{width: 340px; }""", unsafe_allow_html=True,)

        id_dataset = pd.read_csv('./player_id_info_2023.csv')
        id_dataset = id_dataset[['team','NAME','POS','TM_ID']]
        id_dataset = id_dataset[id_dataset['POS'] != 'P']

        #------------------------------------------------------------------------------

        sidebar_title = '<p style="text-align: center; font-family:Times New Roman; color:black; font-size: 70px;font-weight:bold"></p>'
        st.sidebar.markdown(sidebar_title, unsafe_allow_html=True)

        sidebar_text = '<p style="text-align: center; font-family:sans-serif; color:red; font-size: 24px;font-weight:bold">[타자분석 페이지]</p>'
        st.sidebar.markdown(sidebar_text, unsafe_allow_html=True)

        sidebar_text = '<p style="text-align: center; font-family:sans-serif; color:gray; font-size: 16px;">본 웹페이지는 kt wiz 전략데이터팀이<br> 개발 및 발행하였으며 허용되는 사용자 외 <br>배포 및 사용을 엄금함</p>'
        st.sidebar.markdown(sidebar_text, unsafe_allow_html=True)

        #-------------------------------------------------------------------------

        teams = id_dataset['team'].tolist() 
        teams_list = id_dataset['team'].unique().tolist()
        select_team = st.sidebar.selectbox('팀명 선택', teams_list)

        player_dataset = id_dataset[id_dataset['team'] == select_team]
        player_list = player_dataset['NAME'].unique().tolist()
        select_player = st.sidebar.selectbox('선수 선택', player_list)

        player_dataset = player_dataset[player_dataset['NAME'] == select_player]
        id = player_dataset.iloc[0]['TM_ID']

        # #---------------------------------------------------------------------------------

        option = st.sidebar.selectbox(
            '리그 선택',
            ("-", "KBO(1군)", "KBO(2군)", "AAA"))

        sidebar_text = '<p style="font-family:sans-serif; color:gray; font-size: 14px;">(팀 / 선수 / 리그 선택시 자동실행)</p>'
        st.sidebar.markdown(sidebar_text, unsafe_allow_html=True)

        # @st.cache_data
        # def square(x):
        #     return x**2

        # @st.cache_data
        # def cube(x):
        #     return x**3

        # if st.sidebar.button("RESET PAGE"):
        #     # Clear values from *all* memoized functions:
        #     # i.e. clear values from both square and cube
        #     st.cache_data.clear()
        #     show_login_page()

        # if st.sidebar.button("RESET PAGE"):
        #     st.experimental_rerun
        
        if option != "-":
            league = select_league(option)

        #------------------------------------------------------------------------------
            
            # if st.sidebar.button('실행'):
        
            id = int(id)
            player_df = dataframe(league, id)

            progress_text = "Operation in progress. Please wait."
            my_bar = st.progress(0, text=progress_text)
            
            for percent_complete in range(100):
                time.sleep(0.1)
                my_bar.progress(percent_complete + 1, text=progress_text)
            
        #----------------------------------------------------------------------------------

            season_stats_df = stats(player_df)
            period_stats_df = period_stats(player_df)

            stats_df = pd.concat([period_stats_df, season_stats_df])

            stats_viewer_df = stats_viewer(stats_df)
            swing_viewer_df = swing_viewer(stats_df)

            st.title('[시즌별 :red[주요현황]]')
            st.subheader(':gray[기록 & 타구]')
            st.dataframe(stats_viewer_df, width=1300)

            st.subheader(':gray[스윙경향성]')
            st.dataframe(swing_viewer_df, width=1300)

            st.divider()

        #----------------------------------------------------------------------------------

            season_events_df = seoson_inplay_events(player_df)
            period_events_df = period_inplay_events(player_df)
            events_df = pd.concat([period_events_df, season_events_df])
            events_df = events_df.set_index('game_year')

            event_viewer_df = event_viewer(events_df)

            st.title('[시즌별 :red[인플레이 현황]]')
            st.dataframe(event_viewer_df, width=700, column_config=None)

            st.divider()

        #----------------------------------------------------------------------------------

            season_pthrows_df = season_pthrows(player_df)
            period_pthrows_df = period_pthrows(player_df)
            pthrows_df = pd.concat([period_pthrows_df, season_pthrows_df])

            pthrows_df = pthrows_df.set_index('game_year')
            pthrows_stats_df = stats_viewer_pthrows(pthrows_df)
            pthrows_swing_df = swing_viewer_pthrows(pthrows_df)

            st.title('[시즌 :red[투수유형별] 현황]')
            st.subheader(':gray[기록 & 타구]')
            st.dataframe(pthrows_stats_df, width=1300)

            st.subheader(':gray[스윙경향성]')
            st.dataframe(pthrows_swing_df, width=1300)

            st.divider()

        # -----------------------------------------------------------------------------------

            season_pkind_df = season_pkind(player_df)
            period_pkind_df = period_pkind(player_df)
            pkind_df = pd.concat([period_pkind_df, season_pkind_df])
            pkind_df = pkind_df.set_index('game_year')

            pkind_stats_df = stats_viewer_pkind(pkind_df)
            pkind_swing_df = swing_viewer_pkind(pkind_df)

            st.title('[시즌 :red[구종유형별] 현황]')
            st.subheader(':gray[기록 & 타구]')
            st.dataframe(pkind_stats_df, width=1300)

            st.subheader(':gray[스윙경향성]')
            st.dataframe(pkind_swing_df, width=1300)

            st.divider()

        #-----------------------------------------------------------------------------------

            season_pitchname_df = season_pitchname(player_df)
            period_pitchname_df = period_pitchname(player_df)
            pitchname_df = pd.concat([period_pitchname_df, season_pitchname_df])
            pitchname_df = pitchname_df.set_index('game_year')

            pitchname_stats_df = stats_viewer_pitchname(pitchname_df)
            pitchname_swing_df = swing_viewer_pitchname(pitchname_df)

            st.title('[시즌 :red[세부구종별] 현황]')
            st.subheader(':gray[기록 & 타구]')
            st.dataframe(pitchname_stats_df, width=1300)

            st.subheader(':gray[스윙경향성]')
            st.dataframe(pitchname_swing_df, width=1300)

            st.divider()

        #-----------------------------------------------------------------------------------

            st.title('시즌별 :red[투구지점]')
            pitched_factor = 'player_name'
            selection1 = st.selectbox('구종유형 선택(투구)',('Season', 'Fastball', 'Breaking','Off-Speed'))

            select_count_option(player_df, pitched_factor, selection1)

            st.divider()

        #-----------------------------------------------------------------------------------

            st.title('시즌별 :red[스윙지점]')
            swing_factor = 'swing'
            selection2 = st.selectbox('구종유형 선택(스윙)',('Season', 'Fastball', 'Breaking','Off-Speed'))

            select_sum_option(player_df, swing_factor, selection2)

            st.divider()


        #-----------------------------------------------------------------------------------

            st.title('시즌별 :red[LSA 4+]')
            # lsa_dataframe = player_df[player_df['launch_speed_angle'] >= 4]
            lsa_factor = 'launch_speed_angle'
            selection3 = st.selectbox('구종유형 선택(LSA 4+)',('Season', 'Fastball', 'Breaking','Off-Speed'))

            select_sum_option(player_df, lsa_factor, selection3)
            select_sum_plate_option(player_df, lsa_factor, selection3)

            st.divider()

        #------------------------------------------------------------------------------------

            st.title('시즌별 :red[Swing Map]')
            swingmap_factor = 'player_name'
            swingmap_dataframe = swingmap_df(player_df)
            selection4 = st.selectbox('구종유형 선택(SWING MAP)',('Season', 'Fastball', 'Breaking','Off-Speed'))

            swingmap_count_option(swingmap_dataframe, swingmap_factor, selection4)

            st.divider()

        #-------------------------------------------------------------------------------------

            st.title('시즌별 :red[Spray Chart]')
            spraychart_dataframe = spraychart_df(player_df)

            spraychart_fig = season_spraychart(spraychart_dataframe)
            st.divider()





with headerSection:
    if 'loggedIn' not in st.session_state:
        st.session_state['loggedIn'] = False
        show_login_page()
    else:
        if st.session_state['loggedIn']:
            show_main_page()
            show_logout_page()
        else:
            show_login_page()
