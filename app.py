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
        # update_log(userName)
        st.session_state['loggedIn'] = True
        
    else:
        st.session_state['loggedIn'] = False;
        st.error("유효하지 않은 ID 또는 패스워드 입니다.")

def show_login_page():
    with loginSection:
        if st.session_state['loggedIn'] == False:
            userName = st.text_input(label="", value="", placeholder="ID를 입력하시오")
            password = st.text_input(label="", value="", placeholder="패스워드를 입력하시오", type="password")
            st.button("로그인", on_click=LoggedIn_Clicked, args=(userName, password))

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
        select_player = st.sidebar.selectbox('선수 선택', player_list)

        player_dataset = player_dataset[player_dataset['NAME'] == select_player]
        id = player_dataset.iloc[0]['TM_ID']

        # #---------------------------------------------------------------------------------

        option = st.sidebar.selectbox(
            '리그 선택',
            ("-", "KBO(1군)", "KBO(2군)", "AAA(마이너)","KBA(아마)"))

        # sidebar_text = '<p style="font-family:sans-serif; color:gray; font-size: 14px;">(팀 / 선수 / 리그 선택시 자동실행)</p>'
        # st.sidebar.markdown(sidebar_text, unsafe_allow_html=True)

        
        # if option != "-":
        if st.sidebar.button('실행'):
            
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

            st.caption(':gray[<본 기록관련 정보는 트랙맨이 설치되어 있지 않거나 측정이 되지 않을 경우 반영이 되지 않습니다. 실제 기록과 차이가 발생될 수 있음을 양지하여 주시기 바랍니다.>]')
            
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

            select_count_option(player_df, pitched_factor)

            st.divider()

        #-----------------------------------------------------------------------------------

            st.title('시즌별 :red[스윙지점]')
            swing_factor = 'swing'

            select_sum_option(player_df, swing_factor)

            st.divider()


        #-----------------------------------------------------------------------------------

            st.title('시즌별 :red[LSA 4+]')

            st.caption(':gray[<Baseball Savant에서 사용하는 타구의 6단계를 사용하여 타구의 질을 구분하고 그 중 안타 확률이 높은 LSA 4+ 타구를 맵에 구현<br>LSA 1: Weak / LSA 2: Topped / LSA 3: Under / LSA 4: Flare & Burner / LSA 5: Solid Contact / LSA 6: Barrel>]')
            
            # lsa_dataframe = player_df[player_df['launch_speed_angle'] >= 4]
            lsa_factor = 'launch_speed_angle'

            select_sum_option(player_df, lsa_factor)
            select_sum_plate_option(player_df, lsa_factor)

            st.caption(':gray[<Baseball Savant에서 사용하는 타구의 6단계를 사용하여 타구의 질을 구분하고 그 중 안타 확률이 높은 LSA 4+ 타구를 맵에 구현<br>LSA 1: Weak / LSA 2: Topped / LSA 3: Under / LSA 4: Flare & Burner / LSA 5: Solid Contact / LSA 6: Barrel>]')

            st.divider()

        #------------------------------------------------------------------------------------

            st.title('시즌별 :red[Swing Map]')
            swingmap_factor = 'player_name'
            swingmap_dataframe = swingmap_df(player_df)

            swingmap_count_option(swingmap_dataframe, swingmap_factor)

            st.divider()

        #-------------------------------------------------------------------------------------

            st.title('시즌별 :red[Spray Chart]')
            spraychart_dataframe = spraychart_df(player_df)

            season_spraychart(spraychart_dataframe)

            with st.expander("Recent 2 Weeks"):
                spraychart_period_fig = season_period_spraychart(spraychart_dataframe)
                st.plotly_chart(spraychart_period_fig, layout="wide")

            st.divider()
        else:
            st.write("옵션을 선택 후 실행 버튼을 눌러주세요.")

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
