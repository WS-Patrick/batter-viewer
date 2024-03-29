import streamlit as st
import pandas as pd
from definition import select_league, stats, period_stats, seoson_inplay_events, period_inplay_events, season_pthrows, period_pthrows, stats_viewer_pkind, swing_viewer_pkind, stats_viewer_pitchname, swing_viewer_pitchname
from definition import season_pkind, period_pkind, season_pitchname, period_pitchname, stats_viewer, swing_viewer, event_viewer, stats_viewer_pthrows, swing_viewer_pthrows, swingmap_df, spraychart_df
from dataframe import dataframe
from map import select_count_option, select_sum_option, select_sum_plate_option, swingmap_count_option, season_spraychart, season_period_spraychart, factor_year_count_map, factor_year_sum_map,factor_year_sum_plate_map, swingmap_count_map, season_hangtime_spraychart, zone_spraychart_fig
import time
from PIL import Image
from user import login

# Set a unique token for the cookie
COOKIE_TOKEN = "my_unique_cookie_token"

st.set_page_config(page_title="Batting Analytics Page", layout="wide")
st.title("KT WIZ :red[BATTING ANALYTICS] PAGE[Multiple Choice]")

headerSection = st.container()
mainSection = st.container()
loginSection = st.container()
logOutSection = st.container()

# Define a function to get the user's ID from the session cookie
def get_user_id():
    return st.session_state.get(COOKIE_TOKEN)

# Define a function to set the user's ID in the session cookie
def set_user_id(user_id):
    st.session_state[COOKIE_TOKEN] = user_id

def find_id(player_dataset, select_player):
    find_player = player_dataset[player_dataset['NAME'] == select_player]
    id = find_player.iloc[0]['TM_ID']
    return id

def LoggedOut_Clicked():
    st.session_state['loggedIn'] = False
  
def show_logout_page():
    loginSection.empty();
    with logOutSection:
        st.sidebar.button("Log Out", key="logout", on_click=LoggedOut_Clicked)

def LoggedIn_Clicked(userName, password):
    if login(userName, password):
        set_user_id(userName)  # Set the user ID in the session cookie
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
    # Check if the user is logged in
    if not st.session_state.get('loggedIn'):
        show_login_page()
        return

    with mainSection:

        st.markdown("""<style>[data-testid=stSidebar] [data-testid=stImage]{text-align: center;display: block;margin-left: auto; margin-right: auto; width: 85%;}</style>""", unsafe_allow_html=True)
        with st.sidebar:
            st.image("ktwiz_emblem.png")

        st.markdown("""<style>[data-testid="stSidebar"][aria-expanded="true"] > div:first-child{width: 340px; }""", unsafe_allow_html=True,)

        id_dataset = pd.read_csv('./player_id_info_2024.csv')
        id_dataset = id_dataset[['team','NAME','POS','TM_ID','Height']]
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
        player_id = find_id(player_dataset, select_player)

        height = int(player_dataset.iloc[0]['Height'])
        top_line = height * 0.5635
        bottom_line = height * 0.2764
        
        option = st.sidebar.selectbox('리그 선택', ("-", "KBO(1군)", "KBO(2군)", "AAA(마이너)","KBA(아마)"))


        # Create a session_state variable to store selected player information
        if 'selected_players' not in st.session_state:
            st.session_state.selected_players = []

        if st.sidebar.button('Add'):
            st.session_state.selected_players.append({'Team': select_team, 'Player Name': select_player, 'League': option, 'ID' : player_id})

        selected_player_df = pd.DataFrame()
        # Display the selected player names
        if st.session_state.selected_players:
            st.subheader('Selected Players:')
            for player_info in st.session_state.selected_players:
                st.write(f"Team: {player_info['Team']}, Player Name: {player_info['Player Name']}, League: {player_info['League']}, ID: {player_info['ID']}")

                select_player_df = id_dataset[ (id_dataset['team'] == player_info['Team']) & (id_dataset['TM_ID'] == player_info['ID']) ]
                selected_player_df = pd.concat([selected_player_df, select_player_df])


        if st.sidebar.button('실행'):
            
            concatenated_df = pd.DataFrame()
            final_results = pd.DataFrame()

            for player_info in st.session_state.selected_players:

                league = select_league(player_info['League'])
                id = player_info['ID']
                player_name = player_info['Player Name']

                player_df = dataframe(league, id)

                concatenated_df = pd.concat([concatenated_df, player_df])
            
            batter_dataframes = {}
            
            for batter, group in concatenated_df.groupby('batter'):
                batter_dataframes[batter] = group.copy()

# -------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------
            
            st.title('[시즌별 :red[주요현황]]')
            st.subheader(':gray[기록 & 타구]')

            season_stats_concat_df = pd.DataFrame()

            for batter, batter_df in batter_dataframes.items():
                batter_raw_df = globals()[f"df_{batter}"] = batter_df

                season_stats_df = stats(batter_raw_df)
                stats_viewer_df = stats_viewer(season_stats_df)

                batter_str = str(batter)
                batter_finder = selected_player_df[selected_player_df['TM_ID'] == batter_str]
                batter_name = batter_finder.iloc[0]['NAME']

                stats_f_row_df = stats_viewer_df.iloc[:1]
                game_year = stats_f_row_df.index.values[0]

                stats_f_row_df['선수명'] = batter_name
                stats_f_row_df.set_index('선수명', inplace=True)

                stats_f_row_df.insert(0,'연도',game_year)
                
                season_stats_concat_df = pd.concat([season_stats_concat_df, stats_f_row_df])

            pd.set_option('display.max_colwidth', 100)

            st.dataframe(season_stats_concat_df, width=1400)
            
            for batter, batter_df in batter_dataframes.items():
                batter_raw_df = globals()[f"df_{batter}"] = batter_df

                season_stats_df = stats(batter_raw_df)
                stats_viewer_df = stats_viewer(season_stats_df)

                stats_viewer_df = stats_viewer_df.reset_index()
                stats_viewer_df = stats_viewer_df.astype({'game_year':'str'})
                stats_viewer_df = stats_viewer_df.rename(columns={'game_year':'연도'})
                stats_viewer_df = stats_viewer_df.set_index('연도')

                batter_str = str(batter)
                batter_finder = selected_player_df[selected_player_df['TM_ID'] == batter_str]
                batter_name = batter_finder.iloc[0]['NAME']                

                with st.expander(f"상세기록:  {batter_name}"):
                    st.dataframe(stats_viewer_df, width=1300)

#-------------------------------------------------------------------------------------------------------

            st.subheader(':gray[스윙경향성]')

            season_swing_concat_df = pd.DataFrame()

            for batter, batter_df in batter_dataframes.items():
                batter_raw_df = globals()[f"df_{batter}"] = batter_df

                season_stats_df = stats(batter_raw_df)
                swing_viewer_df = swing_viewer(season_stats_df)

                batter_str = str(batter)
                batter_finder = selected_player_df[selected_player_df['TM_ID'] == batter_str]
                batter_name = batter_finder.iloc[0]['NAME']

                swing_f_row_df = swing_viewer_df.iloc[:1]
                game_year = swing_f_row_df.index.values[0]

                swing_f_row_df['선수명'] = batter_name
                swing_f_row_df.set_index('선수명', inplace=True)

                swing_f_row_df.insert(0,'연도',game_year)
                
                season_swing_concat_df = pd.concat([season_swing_concat_df, swing_f_row_df])

            pd.set_option('display.max_colwidth', 100)

            st.dataframe(season_swing_concat_df, width=1400)
            
            for batter, batter_df in batter_dataframes.items():
                batter_raw_df = globals()[f"df_{batter}"] = batter_df

                season_stats_df = stats(batter_raw_df)
                swing_viewer_df = swing_viewer(season_stats_df)

                swing_viewer_df = swing_viewer_df.reset_index()
                swing_viewer_df = swing_viewer_df.astype({'game_year':'str'})
                swing_viewer_df = swing_viewer_df.rename(columns={'game_year':'연도'})
                swing_viewer_df = swing_viewer_df.set_index('연도')

                batter_str = str(batter)
                batter_finder = selected_player_df[selected_player_df['TM_ID'] == batter_str]
                batter_name = batter_finder.iloc[0]['NAME']                

                with st.expander(f"상세기록:  {batter_name}"):
                    st.dataframe(swing_viewer_df, width=1300)

            
            with st.expander("LSA(Launch Speed Angle) 이란?"):
                st.write("LSA(Launch Speed Angle)은 Baseball Savant의 타구표에서 활용되는 지표로 6단계로 타구의 질을 구분하고 있음 (*괄호의 %는 안타확률)")
                st.write("LSA 1: Weak(10.4%) / LSA 2: Topped(22.3%) / LSA 3: Under(7.7%) / LSA 4: Flare & Burner(70.8%) / LSA 5: Solid Contact(46.3%) / LSA 6: Barrel(70.5%)")
                st.markdown("""<style>[data-testid=stExpander] [data-testid=stImage]{text-align: left;display: block;margin-left: 10; margin-right: auto; width: 50%;}</style>""", unsafe_allow_html=True)
                st.image("approach.jpg")

            with st.expander("타격 어프로치 구분"):
                st.write("타격 어프로치는 타자들의 타격성향을 나타내기 위해 작성된 내용으로 리그의 평균적인 존에 대한 스윙시도, 존 외부에 대한 스윙시도를 기준으로 4가지의 성향을 구분하고 있음")
                st.markdown("""<style>[data-testid=stExpander] [data-testid=stImage]{text-align: left;display: block;margin-left: 10; margin-right: auto; width: 80%;}</style>""", unsafe_allow_html=True)
                st.image("plate_discipline.png")


            st.divider()


# -------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------

            st.title('[시즌별 :red[인플레이 현황]]')

            season_inplay_concat_df = pd.DataFrame()

            for batter, batter_df in batter_dataframes.items():
                batter_raw_df = globals()[f"df_{batter}"] = batter_df

                season_events_df = seoson_inplay_events(batter_raw_df)
                season_events_df = season_events_df.rename(columns={'game_year':'연도', 'events':'구분','pitch_name':'인플레이수','exit_velocity':'타구속도','launch_angleX':'발사각도','hit_spin_rate':'타구스핀량','hit_distance':'비거리'})

                batter_str = str(batter)
                batter_finder = selected_player_df[selected_player_df['TM_ID'] == batter_str]
                batter_name = batter_finder.iloc[0]['NAME']

                events_f_row_df = season_events_df.iloc[:1]
                game_year = events_f_row_df.iloc[0]['연도']
                events_f_row_df = season_events_df[season_events_df['연도'] == game_year]
                
                events_f_row_df['선수명'] = batter_name
                events_f_row_df.set_index('선수명', inplace=True)
                
                season_inplay_concat_df = pd.concat([season_inplay_concat_df, events_f_row_df])

            pd.set_option('display.max_colwidth', 100)

            st.dataframe(season_inplay_concat_df, width=1400)
            
            for batter, batter_df in batter_dataframes.items():
                batter_raw_df = globals()[f"df_{batter}"] = batter_df

                season_events_df = seoson_inplay_events(batter_raw_df)


                batter_str = str(batter)
                batter_finder = selected_player_df[selected_player_df['TM_ID'] == batter_str]
                batter_name = batter_finder.iloc[0]['NAME']                

                with st.expander(f"상세기록:  {batter_name}"):
                    st.dataframe(season_events_df, width=1300)
            
            st.divider()

# -------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------

            st.title('[시즌 :red[투수유형별] 현황]')
            st.subheader(':gray[기록 & 타구]')

            throws_stats_concat_df = pd.DataFrame()

            for batter, batter_df in batter_dataframes.items():
                batter_raw_df = globals()[f"df_{batter}"] = batter_df

                throws_stats_df = season_pthrows(batter_raw_df)
                throws_stats_df = throws_stats_df.set_index('game_year')
                stats_viewer_df = stats_viewer_pthrows(throws_stats_df)

                batter_str = str(batter)
                batter_finder = selected_player_df[selected_player_df['TM_ID'] == batter_str]
                batter_name = batter_finder.iloc[0]['NAME']

                stats_viewer_df = stats_viewer_df.reset_index()
                stats_viewer_df = stats_viewer_df.astype({'game_year':'str'})
                stats_viewer_df = stats_viewer_df.rename(columns={'game_year':'연도'})

                stats_f_row_df = stats_viewer_df.iloc[:1]
                game_year = stats_f_row_df.iloc[0]['연도']
                stats_f_row_df = stats_viewer_df[stats_viewer_df['연도'] == game_year]

                stats_f_row_df['선수명'] = batter_name
                stats_f_row_df.set_index('선수명', inplace=True)

                # stats_f_row_df.insert(0,'연도',game_year)
                
                throws_stats_concat_df = pd.concat([throws_stats_concat_df, stats_f_row_df])

            pd.set_option('display.max_colwidth', 100)

            st.dataframe(throws_stats_concat_df, width=1400)
            
            for batter, batter_df in batter_dataframes.items():
                batter_raw_df = globals()[f"df_{batter}"] = batter_df

                throws_stats_df = season_pthrows(batter_raw_df)
                throws_stats_df = throws_stats_df.rename(columns={'game_year':'연도'})
                throws_stats_df = throws_stats_df.set_index('연도')
                stats_viewer_df = stats_viewer_pthrows(throws_stats_df)

                batter_str = str(batter)
                batter_finder = selected_player_df[selected_player_df['TM_ID'] == batter_str]
                batter_name = batter_finder.iloc[0]['NAME']                

                with st.expander(f"상세기록:  {batter_name}"):
                    st.dataframe(stats_viewer_df, width=1300)

# -------------------------------------------------------------------------------------------------------

            st.subheader(':gray[스윙경향성]')

            throws_swing_concat_df = pd.DataFrame()

            for batter, batter_df in batter_dataframes.items():
                batter_raw_df = globals()[f"df_{batter}"] = batter_df

                throws_stats_df = season_pthrows(batter_raw_df)
                throws_stats_df = throws_stats_df.set_index('game_year')
                swing_viewer_df = swing_viewer_pthrows(throws_stats_df)

                batter_str = str(batter)
                batter_finder = selected_player_df[selected_player_df['TM_ID'] == batter_str]
                batter_name = batter_finder.iloc[0]['NAME']

                swing_viewer_df = swing_viewer_df.reset_index()
                swing_viewer_df = swing_viewer_df.astype({'game_year':'str'})
                swing_viewer_df = swing_viewer_df.rename(columns={'game_year':'연도'})

                swing_f_row_df = swing_viewer_df.iloc[:1]
                game_year = swing_f_row_df.iloc[0]['연도']
                swing_f_row_df = swing_viewer_df[swing_viewer_df['연도'] == game_year]

                swing_f_row_df['선수명'] = batter_name
                swing_f_row_df.set_index('선수명', inplace=True)

                # swing_f_row_df.insert(0,'연도',game_year)
                
                throws_swing_concat_df = pd.concat([throws_swing_concat_df, swing_f_row_df])

            pd.set_option('display.max_colwidth', 100)

            st.dataframe(throws_swing_concat_df, width=1400)
            
            for batter, batter_df in batter_dataframes.items():
                batter_raw_df = globals()[f"df_{batter}"] = batter_df

                throws_stats_df = season_pthrows(batter_raw_df)
                throws_stats_df = throws_stats_df.rename(columns={'game_year':'연도'})
                throws_stats_df = throws_stats_df.set_index('연도')
                swing_viewer_df = swing_viewer_pthrows(throws_stats_df)

                batter_str = str(batter)
                batter_finder = selected_player_df[selected_player_df['TM_ID'] == batter_str]
                batter_name = batter_finder.iloc[0]['NAME']                

                with st.expander(f"상세기록:  {batter_name}"):
                    st.dataframe(swing_viewer_df, width=1300)

            st.divider()

# -------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------

            st.title('[시즌 :red[구종유형별] 현황]')
            st.subheader(':gray[기록 & 타구]')

            pkind_stats_concat_df = pd.DataFrame()

            for batter, batter_df in batter_dataframes.items():
                batter_raw_df = globals()[f"df_{batter}"] = batter_df

                pkind_stats_df = season_pkind(batter_raw_df)
                pkind_stats_df = pkind_stats_df.set_index('game_year')
                stats_viewer_df = stats_viewer_pkind(pkind_stats_df)

                batter_str = str(batter)
                batter_finder = selected_player_df[selected_player_df['TM_ID'] == batter_str]
                batter_name = batter_finder.iloc[0]['NAME']

                stats_viewer_df = stats_viewer_df.reset_index()
                stats_viewer_df = stats_viewer_df.astype({'game_year':'str'})
                stats_viewer_df = stats_viewer_df.rename(columns={'game_year':'연도'})

                stats_f_row_df = stats_viewer_df.iloc[:1]
                game_year = stats_f_row_df.iloc[0]['연도']
                stats_f_row_df = stats_viewer_df[stats_viewer_df['연도'] == game_year]

                stats_f_row_df['선수명'] = batter_name
                stats_f_row_df.set_index('선수명', inplace=True)

                # stats_f_row_df.insert(0,'연도',game_year)
                
                pkind_stats_concat_df = pd.concat([pkind_stats_concat_df, stats_f_row_df])

            pd.set_option('display.max_colwidth', 100)

            st.dataframe(pkind_stats_concat_df, width=1400)
            
            for batter, batter_df in batter_dataframes.items():
                batter_raw_df = globals()[f"df_{batter}"] = batter_df

                pkind_stats_df = season_pkind(batter_raw_df)
                pkind_stats_df = pkind_stats_df.rename(columns={'game_year':'연도'})
                pkind_stats_df = pkind_stats_df.set_index('연도')                
                pkind_stats_df = stats_viewer_pkind(pkind_stats_df)

                batter_str = str(batter)
                batter_finder = selected_player_df[selected_player_df['TM_ID'] == batter_str]
                batter_name = batter_finder.iloc[0]['NAME']                

                with st.expander(f"상세기록:  {batter_name}"):
                    st.dataframe(stats_viewer_df, width=1300)

# -------------------------------------------------------------------------------------------------------

            st.subheader(':gray[스윙경향성]')

            pkind_swing_concat_df = pd.DataFrame()

            for batter, batter_df in batter_dataframes.items():
                batter_raw_df = globals()[f"df_{batter}"] = batter_df

                pkind_stats_df = season_pkind(batter_raw_df)
                pkind_stats_df = pkind_stats_df.set_index('game_year')
                swing_viewer_df = swing_viewer_pkind(pkind_stats_df)

                batter_str = str(batter)
                batter_finder = selected_player_df[selected_player_df['TM_ID'] == batter_str]
                batter_name = batter_finder.iloc[0]['NAME']

                swing_viewer_df = swing_viewer_df.reset_index()
                swing_viewer_df = swing_viewer_df.astype({'game_year':'str'})
                swing_viewer_df = swing_viewer_df.rename(columns={'game_year':'연도'})

                swing_f_row_df = swing_viewer_df.iloc[:1]
                game_year = swing_f_row_df.iloc[0]['연도']
                swing_f_row_df = swing_viewer_df[swing_viewer_df['연도'] == game_year]

                swing_f_row_df['선수명'] = batter_name
                swing_f_row_df.set_index('선수명', inplace=True)

                # swing_f_row_df.insert(0,'연도',game_year)
                
                pkind_swing_concat_df = pd.concat([pkind_swing_concat_df, swing_f_row_df])

            pd.set_option('display.max_colwidth', 100)

            st.dataframe(pkind_swing_concat_df, width=1400)
            
            for batter, batter_df in batter_dataframes.items():
                batter_raw_df = globals()[f"df_{batter}"] = batter_df

                pkind_stats_df = season_pkind(batter_raw_df)
                pkind_stats_df = pkind_stats_df.rename(columns={'game_year':'연도'})
                pkind_stats_df = pkind_stats_df.set_index('연도')
                pkind_stats_df = swing_viewer_pkind(pkind_stats_df)

                batter_str = str(batter)
                batter_finder = selected_player_df[selected_player_df['TM_ID'] == batter_str]
                batter_name = batter_finder.iloc[0]['NAME']                

                with st.expander(f"상세기록:  {batter_name}"):
                    st.dataframe(swing_viewer_df, width=1300)

            st.divider()

# -------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------

            st.title('[시즌 :red[스윙지점]]')

            for batter, batter_df in batter_dataframes.items():
                batter_raw_df = globals()[f"df_{batter}"] = batter_df

                game_year = batter_raw_df['game_year'].max()
                batter_recent_df = batter_raw_df[batter_raw_df['game_year'] == game_year]

                batter_str = str(batter)
                batter_finder = selected_player_df[selected_player_df['TM_ID'] == batter_str]
                batter_name = batter_finder.iloc[0]['NAME']

                st.subheader(f"{batter_name}, {game_year}")

                col1, col2, col3, col4 = st.columns(4)

                pitched_factor = 'player_name'
                swing_factor = 'swing'
                lsa_factor = 'launch_speed_angle'

                with col1:
                    original_title = '<p style="text-align: center; color:gray; font-size: 25px;">투구지점</p>'
                    st.markdown(original_title, unsafe_allow_html=True)
                    season_pitched_fig = factor_year_count_map(batter_recent_df, pitched_factor)
                    season_pitched_fig.update_layout(height=450, width=450)
                    season_pitched_fig.update_coloraxes(showscale=False)
                    st.plotly_chart(season_pitched_fig, layout="wide")

                with col2:
                    original_title = '<p style="text-align: center; color:gray; font-size: 25px;">스윙지점</p>'
                    st.markdown(original_title, unsafe_allow_html=True)
                    season_swing_fig = factor_year_sum_map(batter_recent_df, swing_factor)
                    season_swing_fig.update_layout(height=450, width=450)
                    season_swing_fig.update_coloraxes(showscale=False)
                    st.plotly_chart(season_swing_fig, layout="wide")

                with col3:
                    original_title = '<p style="text-align: center; color:gray; font-size: 25px;">LSA 4+ Zone</p>'
                    st.markdown(original_title, unsafe_allow_html=True)
                    season_lsa_fig = factor_year_sum_map(batter_recent_df, lsa_factor)
                    season_lsa_fig.update_layout(height=450, width=450)
                    season_lsa_fig.update_coloraxes(showscale=False)
                    st.plotly_chart(season_lsa_fig, layout="wide")

                with col4:
                    original_title = '<p style="text-align: center; color:gray; font-size: 25px;">LSA 4+ Plate</p>'
                    st.markdown(original_title, unsafe_allow_html=True)
                    season_lsa_fig = factor_year_sum_plate_map(batter_recent_df, lsa_factor)
                    season_lsa_fig.update_layout(height=450, width=430)
                    season_lsa_fig.update_coloraxes(showscale=False)
                    st.plotly_chart(season_lsa_fig, layout="wide")

            st.divider()

# -------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------

            st.title('[시즌 :red[Swing Map]]')

            for batter, batter_df in batter_dataframes.items():
                batter_raw_df = globals()[f"df_{batter}"] = batter_df

                game_year = batter_raw_df['game_year'].max()
                batter_recent_df = batter_raw_df[batter_raw_df['game_year'] == game_year]

                batter_str = str(batter)
                batter_finder = selected_player_df[selected_player_df['TM_ID'] == batter_str]
                batter_name = batter_finder.iloc[0]['NAME']

                called_strike_df = batter_recent_df[batter_recent_df['description'] == "called_strike"]
                called_strike_df['swingmap'] = 'Called_Strike'
                whiff_df = batter_recent_df[batter_recent_df['whiff'] == 1]
                whiff_df['swingmap'] = 'Whiff'
                ball_df = batter_recent_df[batter_recent_df['type'] == "B"]
                ball_df['swingmap'] = 'Ball'
                foul_df = batter_recent_df[batter_recent_df['foul'] == 1]
                foul_df['swingmap'] = 'Foul'
                hit_df = batter_recent_df[batter_recent_df['hit'] == 1]
                hit_df['swingmap'] = 'HIT'
                out_df = batter_recent_df[batter_recent_df['field_out'] == 1]
                out_df['swingmap'] = 'Out'

                swingmap_dataframe = pd.concat([called_strike_df, whiff_df, ball_df, foul_df, hit_df, out_df])
                swingmap_factor = 'player_name'

                st.subheader(f"{batter_name}, {game_year}")

                season_pitched_fig = swingmap_count_map(swingmap_dataframe, swingmap_factor)
                st.plotly_chart(season_pitched_fig, layout="wide")

            st.divider()

# -------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------

            st.title('[시즌 :red[Spray Chart]]')

            for batter, batter_df in batter_dataframes.items():
                batter_raw_df = globals()[f"df_{batter}"] = batter_df

                batter_str = str(batter)
                batter_finder = selected_player_df[selected_player_df['TM_ID'] == batter_str]
                batter_name = batter_finder.iloc[0]['NAME']

                st.subheader(f"{batter_name}")
                
                spraychart_dataframe = spraychart_df(batter_raw_df)
                season_spraychart(spraychart_dataframe)

                with st.expander(f" by 스트라이크 존:  {batter_name}(최근연도)"):
                    st.write("S존 기준차트")
                    zone_spraychart_fig(spraychart_dataframe)

                with st.expander( f" by 타구비행시간:  {batter_name}(최근연도)"):
                    st.write("타구 비행시간")
                    spraychart_hangtime_fig = season_hangtime_spraychart(spraychart_dataframe)
                    st.plotly_chart(spraychart_hangtime_fig)


            st.divider()


# -------------------------------------------------------------------------------------------------------


with headerSection:
    # Get the user's ID from the session cookie
    user_id = get_user_id()

    if user_id is None:
        st.session_state['loggedIn'] = False
        show_login_page()
    else:
        st.session_state['loggedIn'] = True
        show_main_page()
