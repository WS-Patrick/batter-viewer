import streamlit as st
import pandas as pd
import numpy as np
import pymysql

# from pymysqlpool import ConnectionPool

# pool = ConnectionPool(
#     host='14.49.30.59',
#     port=33067,
#     user='ktwiz',
#     password='ktwiz1234!#',
#     database='ktwiz',
#     # autocommit=True,  # 필요에 따라 설정
#     # charset='utf8mb4'  # 필요에 따라 설정
# )

# connection = pool.get_connection()

# conn = st.experimental_connection("mydb", type="sql", autocommit=True)

def dataframe(level, player_id):

    # db = pymysql.connect(host='14.49.30.59', port = 33067, user = 'ktwiz', passwd = 'ktwiz1234!#', db = 'ktwiz', charset='utf8', autocommit=True)

    db.ping ()
  
    cursor = db.cursor()
    sql = """SELECT

    -- game id
    gameid

    -- pitch_type
    , PITKIND AS pitch_type

    -- game date
    , `DATE`

    -- release_speed
    , ROUND( Relspeed*0.621371,1) as release_speed

    -- release_pos_x
    , ROUND(RelSide*3.28084,2) AS release_pos_x

    -- release_pos_z
    , ROUND(RelHeight*3.28084,2) AS release_pos_z

    -- pitname
    , pitname

    -- batname
    , batname

    -- batter
    , batterid  AS batter

    -- pitcher
    , pitcherid as pitcher

    -- events
    , case when playresult = 'Out' then 'field_out'
    	when playresult = 'FieldersChoice' then 'fielders_choice_out'
    	when playresult = 'Error' then 'field_error'
    	when playresult = 'Single' then 'single'
    	when playresult = 'Double' then 'double'
    	when playresult = 'Triple' then 'triple'
    	when playresult = 'HomeRun' then 'home_run'
    	when playresult = 'Sacrifice' and distance >= 30 then 'sac_fly'
    	when (playresult = 'Sacrifice' and distance < 30) or (playresult = 'Sacrifice' and TaggedHitType = "Bunt") then 'sac_bunt'
    	when playresult = 'HitByPitch' or pitchcall = 'HitByPitch'  then 'hit_by_pitch'
    	when playresult = 'Undefined' and korbb = 'Strikeout' then 'strikeout'
    	when playresult = 'Undefined' and korbb = 'Walk' then 'walk' else NULL END as events

    -- description
    , case when pitchCall in('FoulBall', 'FoulballFieldable', 'FoulballNotFieldable') then 'foul'
    	when pitchCall in ('BallCalled', 'BallinDirt', 'BallAutomatic') then 'ball'
    	when pitchCall in ('StrikeCalled', 'AutomaticStrike', 'StrikeAutomatic') then 'called_strike'
    	when pitchCall = 'StrikeSwinging' then 'swinging_strike'
    	when pitchCall = 'InPlay' and playresult in ('Double','Single','HomeRun','Error','Triple','FieldersChoice')  and  runsscored = 0 then 'hit_into_play_no_out'
    	when pitchCall = 'InPlay' and runsscored >= 1 then 'hit_into_play_score'
    	when pitchCall = 'InPlay' and playresult in ('Out','Sacrifice') and runsscored = 0 then 'hit_into_play'
    	when pitchCall = 'HitByPitch' or playresult = 'HitByPitch'  then 'hit_by_pitch'
    	when pitchCall = 'BallIntentional' then 'pitchout'
     	else null END AS description

    -- zone
    , CASE WHEN PlateLocSide >= -0.25 AND PlateLocSide < -0.08333 AND PlateLocHeight >= 0.85 AND PlateLocHeight < 1.05 THEN 3 
        WHEN PlateLocSide >= -0.08333 AND PlateLocSide < 0.08333 AND PlateLocHeight >= 0.85 AND PlateLocHeight < 1.05 THEN 2
        WHEN PlateLocSide >= 0.08333 AND PlateLocSide < 0.25 AND PlateLocHeight >= 0.85 AND PlateLocHeight < 1.05 THEN 1
        WHEN PlateLocSide >= -0.25 AND PlateLocSide < -0.08333 AND PlateLocHeight >= 0.65 AND PlateLocHeight < 0.85 THEN 6 
        WHEN PlateLocSide >= -0.08333 AND PlateLocSide < 0.08333 AND PlateLocHeight >= 0.65 AND PlateLocHeight < 0.85 THEN 5
        WHEN PlateLocSide >= 0.08333 AND PlateLocSide < 0.25 AND PlateLocHeight >= 0.65 AND PlateLocHeight < 0.85 THEN 4
        WHEN PlateLocSide >= -0.25 AND PlateLocSide < -0.08333 AND PlateLocHeight >= 0.45 AND PlateLocHeight < 0.65 THEN 9 
        WHEN PlateLocSide >= -0.08333 AND PlateLocSide < 0.08333 AND PlateLocHeight >= 0.45 AND PlateLocHeight < 0.65 THEN 8
        WHEN PlateLocSide >= 0.08333 AND PlateLocSide < 0.25 AND PlateLocHeight >= 0.45 AND PlateLocHeight < 0.65 THEN 7
        
        WHEN ZONEIN ='OUT' AND PlateLocSide >= 0 AND PlateLocHeight >= 0.75 THEN 11 
        WHEN ZONEIN ='OUT' AND PlateLocSide < 0 AND PlateLocHeight >= 0.75 THEN 12
        WHEN ZONEIN ='OUT' AND PlateLocSide >= 0 AND PlateLocHeight < 0.75 THEN 13 
        WHEN ZONEIN ='OUT' AND PlateLocSide < 0 AND PlateLocHeight < 0.75 THEN 14 ELSE 0 END AS 'zone'

    -- des
    , 'des'

    -- stand
    , CASE WHEN BATTERSIDE = 'RIGHT' THEN 'R' WHEN BATTERSIDE = 'LEFT' THEN 'L' ELSE NULL END AS stand

    -- p_throws
    , CASE WHEN PITCHERTHROWS = 'RIGHT' THEN 'R' WHEN PITCHERTHROWS = 'LEFT' THEN 'L' ELSE NULL END  AS p_throws

    -- pitcherteam
    , pitcherteam

    -- batterteam
    , batterteam

    -- hometeam, awayteam
    , HomeTeam, AwayTeam

    -- type
    , CASE WHEN pitchCall IN ('BallinDirt','BallCalled','HitByPitch','BallIntentional','BallAutomatic') THEN 'B'
    	WHEN PITCHCALL IN ('StrikeCalled','FoulBall','StrikeSwinging','StrikeAutomatic','FoulBallNotFieldable','FoulBallFieldable') THEN 'S' 
    	WHEN PITCHCALL IN ('InPlay') THEN 'X' ELSE NULL END AS 'type'

    -- bb_type
    -- , CASE WHEN pitchcall='inplay' AND exitspeed >= 1 and angle < 10 then 'Groundball'
    -- 	WHEN pitchcall='inplay' AND exitspeed >= 1 and angle >= 25 and angle < 50 then 'Flyball'
    -- 	WHEN pitchcall='inplay' AND exitspeed >= 1 and angle >= 10 and angle < 25 then 'LineDrive'
    -- 	WHEN pitchcall='inplay' AND exitspeed >= 1 and angle >= 50 then 'Popup' ELSE NULL END AS bb_type          -- bb_type 계산용
    , case when pitchcall  = 'inplay' and TaggedHitType = 'GroundBall' then 'ground_ball' 
        when pitchcall  = 'inplay' and TaggedHitType = 'LineDrive' then 'line_drive'
        when pitchcall  = 'inplay' and TaggedHitType = 'FlyBall' then 'fly_ball'
        when pitchcall  = 'inplay' and TaggedHitType = 'Popup' then 'popup'
        when pitchcall  = 'inplay' and TaggedHitType = 'Bunt' then 'bunt'
        else null end as bb_type

    -- count
    , balls , strikes 

    -- pfx_x, pfx_z
    , HorzBreak * 0.032808 AS pfx_x , InducedVertBreak *0.032808 as pfx_z

    -- plate_x, plate_z
    , PlateLocSide as plate_x	, PlateLocHeight as plate_z

    -- outs
    ,  Outs AS outs_when_up

    -- inning
    , inning

    -- topbot
    , Top_Bottom as inning_topbot
    
    -- hit_distance_sc
    , round(DISTANCE * 3.28084,0) AS hit_distance_sc

    -- launch speed
    , round(EXITSPEED * 0.621371 ,1) as launch_speed

    -- launch angle
    , round(ANGLE,0) AS launch_angle

    -- release_extension
    , round(SpinRate,0) as release_spin_rate	, round(Extension * 3.28084,2) as release_extension

    -- launch speed angle
    , case 
        when (EXITSPEED/ 1.609344 * 1.5 - angle) >= 117
        and (EXITSPEED/ 1.609344 + angle) >= 124
        and EXITSPEED/ 1.609344 >= 98
        and angle between 4 and 50
        and pitchcall = 'InPlay'
        then 6 -- 'Barrel'

        when (EXITSPEED/ 1.609344 * 1.5 - angle) >= 111
        and (EXITSPEED/ 1.609344 + angle) >= 119
        and EXITSPEED/ 1.609344 >= 95
        and angle between 0 and 52
        and pitchcall = 'InPlay'
        then 5 -- 'Solid-Contact'
    
        when EXITSPEED/ 1.609344 <= 59
        and pitchcall = 'InPlay'
        then 1 -- 'Poorly-Weak'
    
        when (EXITSPEED/ 1.609344 * 2 - angle) >= 87
        and angle <= 41
        and (EXITSPEED/ 1.609344 * 2 + angle) <= 175
        and (EXITSPEED/ 1.609344 + angle * 1.3) >= 89
        and EXITSPEED/ 1.609344 between 59 and 72
        and pitchcall = 'InPlay'
        then 4 -- 'Flare-or-Burner'
    
        when (EXITSPEED/ 1.609344 + angle * 1.3) <= 112
        and (EXITSPEED/ 1.609344 + angle * 1.55) >= 92
        and EXITSPEED/ 1.609344 between 72 and 86
        and pitchcall = 'InPlay'
        then 4 -- 'Flare-or-Burner'
    
        when angle <= 20
        and (EXITSPEED/ 1.609344 + angle * 2.4) >= 98
        and EXITSPEED/ 1.609344 between 86 and 95
        and pitchcall = 'InPlay'
        then 4 -- 'Flare-or-Burner'
    
        when (EXITSPEED/ 1.609344 - angle) >= 76
        and (EXITSPEED/ 1.609344 + angle * 2.4) >= 98
        and EXITSPEED/ 1.609344 >= 95
        and angle <= 30
        and pitchcall = 'InPlay'
        then 4 -- 'Flare-or-Burner'

        when (EXITSPEED/ 1.609344 + angle * 2) >= 116
        and pitchcall = 'InPlay'
        then 3 -- 'Poorly-Under'

        when (EXITSPEED/ 1.609344 + angle * 2) <= 116
        and pitchcall = 'InPlay'
        then 2 -- 'Poorly-Topped'

    else NULL -- 'Unclassified'
    end AS launch_speed_angle

    -- pitch_number
    , pitchofpa AS pitch_number

    -- pa of inning
    , paofinning

    -- pitch name
    , CASE WHEN PITKIND = 'FF' THEN '4-Seam Fastball'
    	WHEN PITKIND = 'CH' THEN 'Changeup'
    	WHEN PITKIND = 'SL' THEN 'Slider'
    	WHEN PITKIND = 'CU' THEN 'Curveball'
    	WHEN PITKIND = 'ST' THEN 'Sweeper'
    	WHEN PITKIND = 'FS' THEN 'Split-Finger'
    	WHEN PITKIND IN ('FT','SI') THEN '2-Seam Fastball'
    	WHEN PITKIND = 'FC' THEN 'Cutter' ELSE PITKIND END AS pitch_name
     
    -- , PlateLocSide, PlateLocHeight

    , home_score_cn
    , away_score_cn
    , LEVEL
    , vertrelangle
    , case when bearing >= 0 then 'R' WHEN BEARING < 0 THEN 'L' ELSE NULL END
    , round(ContactPositionX,2) , round(ContactPositionY,2) , round(ContactPositionZ,2)

    , case when pitchcall = 'inplay' and bearing >= 0 and bearing <= 45 then convert(round(distance *cos(radians(45-bearing)),0),int)
    when pitchcall = 'inplay' and bearing < 0 and bearing >= -45 then convert(round(distance *cos(radians(45 + abs(bearing))),0),int) else '' end as groundxside
    , case when pitchcall = 'inplay' and bearing >= 0 and bearing <= 45 then convert(round(distance *sin(radians(45-bearing)),0),int)
    when pitchcall = 'inplay' and bearing < 0 and bearing >= -45 then convert(round(distance *sin(radians(45 + abs(bearing))),0),int) else '' end as groundyside

    -- year
    , SEASON AS game_year

    -- hit spin rate
    , hitspinrate

    -- catcher
    , catcher as catcher

    -- hangtime
    , HangTime

     -- pitkind
    	FROM 
    		
    		(
    		SELECT a.*, substring(GameID ,1,4) as SEASON
    		, CASE WHEN pit_kind_cd = '31' THEN 'FF'
    		WHEN pit_kind_cd = '32' THEN 'CU'
    		WHEN pit_kind_cd = '33' THEN 'SL'
    		WHEN pit_kind_cd = '34' THEN 'CH'
    		WHEN pit_kind_cd = '35' THEN 'FS'
    		WHEN pit_kind_cd = '36' THEN 'SI'
    		WHEN pit_kind_cd = '37' THEN 'FT'
    		WHEN pit_kind_cd = '38' THEN 'FC'
      		WHEN pit_kind_cd = '131' THEN 'ST'
      		WHEN PIT_KIND_CD IS NULL and (AUTOPITCHTYPE = 'Fastball' OR AUTOPITCHTYPE = 'Four-Seam')  then 'FF'
    		WHEN PIT_KIND_CD IS NULL and AUTOPITCHTYPE = 'Sinker' then 'SI' 
    		WHEN PIT_KIND_CD IS NULL and AUTOPITCHTYPE = 'Curveball' then 'CU' 
    		WHEN PIT_KIND_CD IS NULL and AUTOPITCHTYPE = 'Slider' then 'SL'
    		WHEN PIT_KIND_CD IS NULL and AUTOPITCHTYPE = 'Changeup' then 'CH'
    		WHEN PIT_KIND_CD IS NULL and AUTOPITCHTYPE = 'Splitter' then 'FS'
    		WHEN PIT_KIND_CD IS NULL and AUTOPITCHTYPE = 'Cutter' then 'FC'
      		WHEN PIT_KIND_CD IS NULL and AUTOPITCHTYPE = 'Sweeper' then 'ST'
    		ELSE 'OT' END  AS PITKIND
            
            , PITCHER as pitname, BATTER as batname 
            , CASE WHEN PlateLocSide >= -0.25 AND  PlateLocSide < 0.25 AND PlateLocHeight >= 0.45 AND PlateLocHeight < 1.05 THEN 'IN' ELSE 'OUT' END AS 'ZONEIN'
            , CASE WHEN PlateLocSide >= -0.5 AND  PlateLocSide < 0.5 AND PlateLocHeight >= 0.2 AND PlateLocHeight < 1.3 THEN 'END' ELSE 'ENDOUT' END AS 'ENDOUT' 
            , POS1_P_ID, POS2_P_ID, POS3_P_ID, POS4_P_ID, POS5_P_ID, POS6_P_ID, POS7_P_ID, POS8_P_ID, POS9_P_ID
            , home_score_cn , away_score_cn
            FROM 
                (SELECT* FROM pda_trackman ) a
            -- JOIN
                Left outer join 
                (SELECT* FROM pda_analyzer ) b
                ON a.game_seq = b.game_seq AND a.pit_seq = b.pit_seq
            
        
            ) ZZ
        
        
    WHERE 

    -- game year
    -- gameid Like '2020%'
    gameid >= '2022'

    -- league(aaa, KoreaBaseballOrganization, npb, mlb, aa, KBO Minors)
    AND level IN ({0})

    -- player id
    -- AND pitcherid = '64004'
    AND batterid = {1}

    order by gameid, pitchno  """


    cursor.execute(sql.format(level, player_id))
    raw = cursor.fetchall()

    df=pd.DataFrame([[item.decode('latin-1') if isinstance(item, bytes) else item for item in row] for row in raw],
                      columns = ['game_id','pitch_type', 'game_date', 'release_speed', 'release_pos_x', 'release_pos_z',  'player_name', 'batname', 'batter', 'pitcher', 'events', 'description', 'zone', 'des', 'stand', 'p_throw', 'pitcherteam','batterteam', 'home_team' , 'away_team',
                                    'type', 'bb_type', 'balls', 'strikes', 'pfx_x', 'pfx_z', 'plate_x', 'plate_z', 'out_when_up', 'inning', 'inning_topbot', 'hit_distance_sc',
                                    'launch_speed','launch_angle','release_spin_rate','release_extension',
                                    'launch_speed_angle','pitch_number','PAofinning','pitch_name','home_score','away_score','level','verrelangle','launch_direction', 'contactX' , 'contactY' , 'contactZ', 'groundX','groundY','game_year','hit_spin_rate', 'catcher', 'hangtime'])

    # df.to_sql(name='dataframe', con=db, ttl=360)
  
    db.commit()  
    db.close()
  
    if len(df) > 0:

        df['plate_x'] = df['plate_x'] * -1.0
        df['pfx_x'] = df['pfx_x'] * -1.0

        df['hit_distance'] = df['hit_distance_sc']*0.3048

        df[['batter','pitcher','groundX','groundY','game_year','hangtime']] = df[['batter','pitcher','groundX', 'groundY','game_year','hangtime']].apply(pd.to_numeric)

        conv_fac = 0.3048
        df['rel_height'] = df['release_pos_z']*conv_fac
        df['rel_side'] = df['release_pos_x']*conv_fac
        df['hor_break'] = df['pfx_x']*conv_fac
        df['ver_break'] = df['pfx_z']*conv_fac

        p_type = df[['pitcher','rel_height']]
        rel_height = p_type.groupby(['pitcher'], as_index=False).mean()
        rel_height['type'] = rel_height['rel_height'].apply(lambda x: 'S' if x <= 1.5 else 'R')
        side_arm = rel_height[rel_height['type'] == 'S']

        y = side_arm['pitcher'].unique()

        df['side_arm'] = df['pitcher'].apply(lambda x: 'S' if x in y else 'Reg')
        df['p_throws'] = df['pitcher'].apply(lambda x: 'S' if x in y else list(set(df.loc[df['pitcher'] == x, 'p_throw'].unique()))[0])

        pa = ['double','double_play','field_error','field_out','fielders_choice_out','force_out','grounded_into_double_play','hit_by_pitch','home_run','sac_bunt','sac_fly','sac_fly_double_play','single','strikeout','strikeout_double_play','triple','walk']
        ab = ['double','double_play','field_error','field_out','fielders_choice_out','force_out','grounded_into_double_play','home_run','single','strikeout','strikeout_double_play','triple']
        hit = ['double','home_run','single','triple']
        swing = ['foul','foul_tip','hit_into_play','hit_into_play_no_out','hit_into_play_score','swinging_strike','swing_strike_blocked']
        con = ['foul','foul_tip','hit_into_play','hit_into_play_no_out','hit_into_play_score']
        whiff = ['swinging_strike','swing_strike_blocked']
        foul = ['foul','foul_tip']

        df['pa'] = df['events'].apply(lambda x: 1 if x in pa else 0)
        df['ab'] = df['events'].apply(lambda x: 1 if x in ab else 0)
        df['hit'] = df['events'].apply(lambda x: 1 if x in hit else 0)
        df['swing'] = df['description'].apply(lambda x: 1 if x in swing else 0)
        df['con'] = df['description'].apply(lambda x: 1 if x in con else 0)
        df['whiff'] = df['description'].apply(lambda x: 1 if x in whiff else 0)
        df['foul'] = df['description'].apply(lambda x: 1 if x in foul else 0)

        df['z_in'] = df['zone'].apply(lambda x: 1 if x < 10 else 0)
        df['z_out'] = df['zone'].apply(lambda x: 1 if x > 10 else 0)

        df['balls'] = df['balls'].apply(str)
        df['strikes'] = df['strikes'].apply(str)
        df['count'] = df['balls'].str.cat(df['strikes'], sep='-')

        speed_fac = 1.609344
        distance_fac = 0.3048

        df['rel_speed(km)'] = df['release_speed']*speed_fac
        df['exit_speed(km)'] = df['launch_speed']*speed_fac
        df['rel_height'] = df['release_pos_z']*distance_fac
        df['rel_side'] = df['release_pos_x']*distance_fac
        df['extension'] = df['release_extension']*distance_fac
        # df['hit_distance'] = df['hit_distance_sc']*distance_fac

        p_type = df[['pitcher','rel_height']]
        rel_height = p_type.groupby(['pitcher'], as_index=False).mean()

        rel_height['type'] = rel_height['rel_height'].apply(lambda x: 'S' if x <= 1.5 else 'R')
        side_arm = rel_height[rel_height['type'] == 'S']
        y = side_arm['pitcher'].unique()

        df['p_type'] = df['pitcher'].apply(lambda x: 'S' if x in y else 'R')

        def pkind(x):
        
          if x == '4-Seam Fastball':
            return 'Fastball'
          elif x == '2-Seam Fastball':
            return 'Fastball'
          elif x == 'Cutter':
            return 'Fastball'
          elif x == 'Slider':
            return 'Breaking'
          elif x == 'Curveball':
            return 'Breaking'
          elif x == 'Sweeper':
            return 'Breaking'
          elif x == 'Changeup':
            return 'Off_Speed'
          elif x == 'Split-Finger':
            return 'Off_Speed'
          else:
            return 'OT'


        df['p_kind'] = df['pitch_name'].apply(lambda x: pkind(x))

        def count(x):

            if x == '0-0':
                return 'First_Pitch'
            elif x == '3-2':
                return 'Else'
            elif x == '0-1':
                return 'Else'
            elif x == '0-2':
                return 'After_2S'
            elif x == '1-1':
                return 'Else'
            elif x == '1-2':
                return 'After_2S'
            elif x == '2-2':
                return 'After_2S'
            elif x == '1-0':
                return 'Hitting'
            elif x == '2-0':
                return 'Hitting'
            elif x == '2-1':
                return 'Hitting'
            elif x == '3-0':
                return 'Else'
            elif x == '3-1':
                return 'Else'

        def hangtime(x):
            if x <= 1:
                return 'short'
            elif x >= 4:
                return 'long'
            else:
                return 'challenge'

        df['hangtime_type'] = df['hangtime'].apply(lambda x: hangtime(x))

        df['count_value'] = df['count'].apply(lambda x: count(x))

        df['after_2s'] = df['count_value'].apply(lambda x: 1 if x == 'After_2S' else 0)
        df['hitting'] = df['count_value'].apply(lambda x: 1 if x == 'Hitting' else 0)
        df['else'] = df['count_value'].apply(lambda x: 1 if x == 'Else' else 0)

        df['ld'] = df['bb_type'].apply(lambda x: 1 if x == 'Line_Drive' else 0)
        df['fb'] = df['bb_type'].apply(lambda x: 1 if x == 'Fly_Ball' else 0)
        df['gb'] = df['bb_type'].apply(lambda x: 1 if x == 'Ground_Ball' else 0)
        df['pu'] = df['bb_type'].apply(lambda x: 1 if x == 'Popup' else 0)

        df['single'] = df['events'].apply(lambda x: 1 if x == 'single' else 0)
        df['double'] = df['events'].apply(lambda x: 1 if x == 'double' else 0)
        df['triple'] = df['events'].apply(lambda x: 1 if x == 'triple' else 0)
        df['home_run'] = df['events'].apply(lambda x: 1 if x == 'home_run' else 0)
        df['walk'] = df['events'].apply(lambda x: 1 if x == 'walk' else 0)
        df['hit_by_pitch'] = df['events'].apply(lambda x: 1 if x == 'hit_by_pitch' else 0)
        df['sac_fly'] = df['events'].apply(lambda x: 1 if x == 'sac_fly' else 0)
        df['sac_bunt'] = df['events'].apply(lambda x: 1 if x == 'sac_bunt' else 0)
        df['field_out'] = df['events'].apply(lambda x: 1 if x == 'field_out' else 0)

        df['inplay'] = df['type'].apply(lambda x: 1 if x == 'X' else 0)

        df['weak'] = df['launch_speed_angle'].apply(lambda x: 1 if x == 1 else 0)
        df['topped'] = df['launch_speed_angle'].apply(lambda x: 1 if x == 2 else 0)
        df['under'] = df['launch_speed_angle'].apply(lambda x: 1 if x == 3 else 0)
        df['flare'] = df['launch_speed_angle'].apply(lambda x: 1 if x == 4 else 0)
        df['solid_contact'] = df['launch_speed_angle'].apply(lambda x: 1 if x == 5 else 0)
        df['barrel'] = df['launch_speed_angle'].apply(lambda x: 1 if x == 6 else 0)
        df['plus_lsa4'] = df['launch_speed_angle'].apply(lambda x: 1 if x >=4 else 0)

        df['game_date'] = pd.to_datetime(df['game_date'], format='mixed', dayfirst=True)

        condition1 = [
                    (df['zone'] == 1) & (df['swing'] != 1),
                    (df['zone'] == 3) & (df['swing'] != 1),
                    (df['zone'] == 4) & (df['swing'] != 1),
                    (df['zone'] == 6) & (df['swing'] != 1),
                    (df['zone'] == 7) & (df['swing'] != 1),
                    (df['zone'] == 9) & (df['swing'] != 1),
        ]

        choicelist1 = ['Left_take','Right_take', 'Left_take', 'Right_take', 'Left_take', 'R_Right_takeake']

        df['l_r'] = np.select(condition1, choicelist1, default='Not Specified')

        condition2 = [
                    (df['zone'] == 1) & (df['swing'] != 1),
                    (df['zone'] == 2) & (df['swing'] != 1),
                    (df['zone'] == 3) & (df['swing'] != 1),
                    (df['zone'] == 7) & (df['swing'] != 1),
                    (df['zone'] == 8) & (df['swing'] != 1),
                    (df['zone'] == 9) & (df['swing'] != 1),
        ]

        choicelist2 = ['High_take','High_take', 'High_take', 'Low_take', 'Low_take', 'Low_take']

        df['h_l'] = np.select(condition2, choicelist2, default='Not Specified')

        df['z_left'] = df['zone'].apply(lambda x: 1 if x == 1 or x == 4 or x== 7 else 0)
        df['z_right'] = df['zone'].apply(lambda x: 1 if x == 3 or x == 6 or x== 9 else 0)
        df['z_high'] = df['zone'].apply(lambda x: 1 if x == 1 or x == 2 or x== 3 else 0)
        df['z_low'] = df['zone'].apply(lambda x: 1 if x == 7 or x == 8 or x== 9 else 0)

        condition3 = [
                    (df['plate_x'] < -0.12) & (df['plate_x'] > -0.34) & (df['plate_z'] > 0.91) & (df['plate_z'] < 1.16),
                    (df['plate_x'] > -0.12) & (df['plate_x'] < 0.12) & (df['plate_z'] > 0.91) & (df['plate_z'] < 1.16),
                    (df['plate_x'] > 0.12) & (df['plate_x'] < 0.34) & (df['plate_z'] > 0.91) & (df['plate_z'] < 1.16),
                    (df['plate_x'] > -0.34) & (df['plate_x'] < -0.14) & (df['plate_z'] > 0.59) & (df['plate_z'] < 0.91),
                    (df['plate_x'] > -0.12) & (df['plate_x'] < 0.12) & (df['plate_z'] > 0.59) & (df['plate_z'] < 0.91),
                    (df['plate_x'] > 0.12) & (df['plate_x'] < 0.34) & (df['plate_z'] > 0.59) & (df['plate_z'] < 0.91),
                    (df['plate_x'] > -0.34) & (df['plate_x'] < -0.12) & (df['plate_z'] > 0.35) & (df['plate_z'] < 0.59),
                    (df['plate_x'] > -0.12) & (df['plate_x'] < 0.12) & (df['plate_z'] > 0.35) & (df['plate_z'] < 0.59),
                    (df['plate_x'] > 0.12) & (df['plate_x'] < 0.34) & (df['plate_z'] > 0.35) & (df['plate_z'] < 0.59),
        ]

        choicelist3 = ['nz1','nz2', 'nz3', 'nz4', 'core', 'nz6','nz7','nz8','nz9']

        df['new_zone'] = np.select(condition3, choicelist3, default='Not Specified')

        ndf = df[['game_year', 'game_date', 'inning', 'home_team','home_score', 'away_team','away_score',
                'pitch_number','balls', 'strikes', 'zone', 'new_zone','stand', 'p_throw', 'p_throws', 'p_type', 'type', 'bb_type','events', 'description', 'hor_break','ver_break','plate_x','plate_z',
                'pitcherteam', 'player_name', 'pitcher','catcher','batterteam', 'batname', 'batter',
                'rel_speed(km)','release_spin_rate','rel_height', 'rel_side', 'extension','pitch_name', 'p_kind',
                'exit_speed(km)','launch_angle','launch_direction','hit_distance','hit_spin_rate','launch_speed_angle', 'contactX', 'contactY', 'contactZ', 'groundX', 'groundY', 'l_r','h_l',
                'pa', 'ab', 'hit', 'swing', 'con', 'whiff','foul','z_in','z_out','count', 'count_value', 'z_left','z_right','z_high','z_low',
                'ld','fb','gb','pu','single','double','triple','home_run','walk','hit_by_pitch','sac_fly','sac_bunt','field_out','inplay',
                'weak','topped','under','flare','solid_contact','barrel','plus_lsa4', 'level', 'hangtime','hangtime_type'
                ]]

        def ntype(x):

            if x == 'called_strike':
                return 'strike'
            elif x == 'ball':
                return 'ball'   
            elif x == 'hit_into_play':
                return 'inplay'  
            elif x == 'hit_into_play_no_out':
                return 'inplay'   
            elif x == 'hit_into_play_score':
                return 'inplay'   
            elif x == 'swinging_strike':
                return 'whiff'   
            elif x == 'swing_strike_blocked':
                return 'whiff'   
            elif x == 'foul':
                return 'foul'   
            elif x == 'hit_by_pitch':
                return 'hit_by_pitch'   

        ndf['ntype'] = ndf['description'].apply(lambda x: ntype(x))

        z_df = ndf[ndf['zone'] < 10]
        z_df['z_swing'] = z_df['swing'].apply(lambda x: 1 if x == 1 else 0)
        z_df['z_con'] = z_df['con'].apply(lambda x: 1 if x == 1 else 0)
        z_df['z_inplay'] = z_df['inplay'].apply(lambda x: 1 if x == 1 else 0)

        z_swing = z_df[['z_swing']]
        z_con = z_df[['z_con']]
        z_inplay = z_df[['z_inplay']]

        o_df = ndf[ndf['zone'] > 10]
        o_df['o_swing'] = o_df['swing'].apply(lambda x: 1 if x == 1 else 0)
        o_df['o_con'] = o_df['con'].apply(lambda x: 1 if x == 1 else 0)
        o_df['o_inplay'] = o_df['inplay'].apply(lambda x: 1 if x == 1 else 0)

        o_swing = o_df[['o_swing']]
        o_con = o_df[['o_con']]
        o_inplay = o_df[['o_inplay']]

        f_pitch = ndf[ndf['count'] == '0-0']
        f_pitch['f_swing'] = f_pitch['swing'].apply(lambda x: 1 if x == 1 else 0)
        f_swing = f_pitch[['f_swing']]

        inplay_df = ndf[ndf['type'] == 'X']
        inplay_df = inplay_df[['exit_speed(km)','launch_angle']]
        inplay_df.columns = ['exit_velocity','launch_angleX']

        whiff = ndf[ndf['whiff'] == 1]
        whiff['z_str_swing'] = whiff['zone'].apply(lambda x: 1 if x < 10 else 0)
        z_ztr_swing = whiff[['z_str_swing']]

        ndf = ndf.join(z_swing, how='outer')
        ndf = ndf.join(o_swing, how='outer')
        ndf = ndf.join(z_con, how='outer')
        ndf = ndf.join(o_con, how='outer')
        ndf = ndf.join(f_swing, how='outer')
        ndf = ndf.join(inplay_df, how='outer')
        ndf = ndf.join(z_ztr_swing, how='outer')
        ndf = ndf.join(z_inplay, how='outer')
        ndf = ndf.join(o_inplay, how='outer')

        ndf['f_pitch'] = ndf['count'].apply(lambda x: 1 if x == '0-0' else 0)

        ndf['Left_take'] = ndf['l_r'].apply(lambda x: 1 if x == 'Left_take' else 0)
        ndf['Right_take'] = ndf['l_r'].apply(lambda x: 1 if x == 'Right_take' else 0)
        ndf['High_take'] = ndf['h_l'].apply(lambda x: 1 if x == 'High_take' else 0)
        ndf['Low_take'] = ndf['h_l'].apply(lambda x: 1 if x == 'Low_take' else 0)

        ndf['looking'] = ndf['description'].apply(lambda x: 1 if x == "ball" or x == "called_strike" else 0)

        ot = ndf[ndf['p_kind'] == 'OT'].index
        ndf = ndf.drop(ot)

        ndf['month'] = ndf['game_date'].dt.month

        start18 = '2018-04-01'
        end18 = '2018-10-18'
        start19 = '2019-03-23'
        end19 = '2019-10-01'
        start20 = '2020-05-05'
        end20 = '2020-10-31'
        start21 = '2021-04-03'
        end21 = '2021-10-30'
        start22 = '2022-04-02'
        end22 = '2022-10-11'
        start23 = '2023-04-01'
        end23 = '2023-10-30'
        start24 = '2024-03-23'
        end24 = '2024-10-30'   

        season18 = ndf[(ndf['game_date'] >= start18) & (ndf['game_date'] <= end18)]
        season19 = ndf[(ndf['game_date'] >= start19) & (ndf['game_date'] <= end19)]
        season20 = ndf[(ndf['game_date'] >= start20) & (ndf['game_date'] <= end20)]
        season21 = ndf[(ndf['game_date'] >= start21) & (ndf['game_date'] <= end21)]
        season22 = ndf[(ndf['game_date'] >= start22) & (ndf['game_date'] <= end22)]
        season23 = ndf[(ndf['game_date'] >= start23) & (ndf['game_date'] <= end23)]
        season24 = ndf[(ndf['game_date'] >= start24) & (ndf['game_date'] <= end24)]

        ndf = pd.concat([season18, season19, season20, season21, season22, season23, season24], ignore_index=True)

        player_df = ndf

        player_df = player_df.reset_index(drop=True)
        player_df['game_date'] = pd.to_datetime(player_df['game_date'])

    else:
        raise ValueError("데이터가 존재하지 않습니다.")
    
    return player_df
    


def base_df(player_df):

    game = pd.pivot_table(player_df, index='game_year', values='game_date', aggfunc='nunique', margins=False)
    pitched = pd.pivot_table(player_df, index='game_year', values='player_name', aggfunc='count', margins=False)
    rel_speed = pd.pivot_table(player_df, index='game_year', values='rel_speed(km)', aggfunc='mean', margins=False)
    inplay = pd.pivot_table(player_df, index='game_year', values='inplay', aggfunc='sum', margins=False)
    exit_velocity = pd.pivot_table(player_df, index='game_year', values='exit_velocity', aggfunc='mean', margins=False)
    launch_angleX = pd.pivot_table(player_df, index='game_year', values='launch_angleX', aggfunc='mean', margins=False)
    hit_spin_rate = pd.pivot_table(player_df, index='game_year', values='hit_spin_rate', aggfunc='mean', margins=False)

    hit = pd.pivot_table(player_df, index='game_year', values='hit', aggfunc='sum', margins=False)
    ab = pd.pivot_table(player_df, index='game_year', values='ab', aggfunc='sum', margins=False)
    pa = pd.pivot_table(player_df, index='game_year', values='pa', aggfunc='sum', margins=False)
    single = pd.pivot_table(player_df, index='game_year', values='single', aggfunc='sum', margins=False)
    double = pd.pivot_table(player_df, index='game_year', values='double', aggfunc='sum', margins=False)
    triple = pd.pivot_table(player_df, index='game_year', values='triple', aggfunc='sum', margins=False)
    home_run = pd.pivot_table(player_df, index='game_year', values='home_run', aggfunc='sum', margins=False)
    walk = pd.pivot_table(player_df, index='game_year', values='walk', aggfunc='sum', margins=False)
    hit_by_pitch = pd.pivot_table(player_df, index='game_year', values='hit_by_pitch', aggfunc='sum', margins=False)
    sac_fly = pd.pivot_table(player_df, index='game_year', values='sac_fly', aggfunc='sum', margins=False)

    z_in = pd.pivot_table(player_df, index='game_year', values='z_in', aggfunc='sum', margins=False)
    z_swing = pd.pivot_table(player_df, index='game_year', values='z_swing', aggfunc='sum', margins=False)
    z_con = pd.pivot_table(player_df, index='game_year', values='z_con', aggfunc='sum', margins=False)
    z_out = pd.pivot_table(player_df, index='game_year', values='z_out', aggfunc='sum', margins=False)
    z_inplay = pd.pivot_table(player_df, index='game_year', values='z_inplay', aggfunc='sum', margins=False)
    o_swing = pd.pivot_table(player_df, index='game_year', values='o_swing', aggfunc='sum', margins=False)
    o_con = pd.pivot_table(player_df, index='game_year', values='o_con', aggfunc='sum', margins=False)
    o_inplay = pd.pivot_table(player_df, index='game_year', values='o_inplay', aggfunc='sum', margins=False)

    f_swing = pd.pivot_table(player_df, index='game_year', values='f_swing', aggfunc='sum', margins=False)
    f_pitch = pd.pivot_table(player_df, index='game_year', values='f_pitch', aggfunc='sum', margins=False)
    swing = pd.pivot_table(player_df, index='game_year', values='swing', aggfunc='sum', margins=False)
    whiff = pd.pivot_table(player_df, index='game_year', values='whiff', aggfunc='sum', margins=False)

    weak = pd.pivot_table(player_df, index='game_year', values='weak', aggfunc='sum', margins=False)
    topped = pd.pivot_table(player_df, index='game_year', values='topped', aggfunc='sum', margins=False)
    under = pd.pivot_table(player_df, index='game_year', values='under', aggfunc='sum', margins=False)
    flare = pd.pivot_table(player_df, index='game_year', values='flare', aggfunc='sum', margins=False)
    solid_contact = pd.pivot_table(player_df, index='game_year', values='solid_contact', aggfunc='sum', margins=False)
    barrel = pd.pivot_table(player_df, index='game_year', values='barrel', aggfunc='sum', margins=False)

    merged_base_df = pd.concat([game, pitched, rel_speed, inplay, exit_velocity, launch_angleX, hit_spin_rate, hit, ab, pa, single, double, triple, home_run, walk, hit_by_pitch, sac_fly,
                        z_in, z_swing, z_con, z_out, z_inplay, o_swing, o_con, o_inplay, f_swing, f_pitch, swing, whiff,
                        weak, topped, under, flare, solid_contact, barrel], axis=1)
    
    return merged_base_df


def pivot_base_df(player_df, pivot_index):

    game = player_df.groupby(['game_year']).apply(lambda x: x.pivot_table(index=pivot_index, values='game_date', aggfunc='nunique', margins=True))
    pitched = player_df.groupby(['game_year']).apply(lambda x: x.pivot_table(index=pivot_index, values='player_name', aggfunc='count', margins=True))
    rel_speed = player_df.groupby(['game_year']).apply(lambda x: x.pivot_table(index=pivot_index, values='rel_speed(km)', aggfunc='mean', margins=True))
    inplay = player_df.groupby(['game_year']).apply(lambda x: x.pivot_table(index=pivot_index, values='inplay', aggfunc='sum', margins=True))
    exit_velocity = player_df.groupby(['game_year']).apply(lambda x: x.pivot_table(index=pivot_index, values='exit_velocity', aggfunc='mean', margins=True))
    launch_angleX = player_df.groupby(['game_year']).apply(lambda x: x.pivot_table(index=pivot_index, values='launch_angleX', aggfunc='mean', margins=True))
    hit_spin_rate = player_df.groupby(['game_year']).apply(lambda x: x.pivot_table(index=pivot_index, values='hit_spin_rate', aggfunc='mean', margins=True))

    hit = player_df.groupby(['game_year']).apply(lambda x: x.pivot_table(index=pivot_index, values='hit', aggfunc='sum', margins=True))
    ab = player_df.groupby(['game_year']).apply(lambda x: x.pivot_table(index=pivot_index, values='ab', aggfunc='sum', margins=True))
    pa = player_df.groupby(['game_year']).apply(lambda x: x.pivot_table(index=pivot_index, values='pa', aggfunc='sum', margins=True))
    single = player_df.groupby(['game_year']).apply(lambda x: x.pivot_table(index=pivot_index, values='single', aggfunc='sum', margins=True))
    double = player_df.groupby(['game_year']).apply(lambda x: x.pivot_table(index=pivot_index, values='double', aggfunc='sum', margins=True))
    triple = player_df.groupby(['game_year']).apply(lambda x: x.pivot_table(index=pivot_index, values='triple', aggfunc='sum', margins=True))
    home_run = player_df.groupby(['game_year']).apply(lambda x: x.pivot_table(index=pivot_index, values='home_run', aggfunc='sum', margins=True))
    walk = player_df.groupby(['game_year']).apply(lambda x: x.pivot_table(index=pivot_index, values='walk', aggfunc='sum', margins=True))
    hit_by_pitch = player_df.groupby(['game_year']).apply(lambda x: x.pivot_table(index=pivot_index, values='hit_by_pitch', aggfunc='sum', margins=True))
    sac_fly = player_df.groupby(['game_year']).apply(lambda x: x.pivot_table(index=pivot_index, values='sac_fly', aggfunc='sum', margins=True))

    z_in = player_df.groupby(['game_year']).apply(lambda x: x.pivot_table(index=pivot_index, values='z_in', aggfunc='sum', margins=True))
    z_swing = player_df.groupby(['game_year']).apply(lambda x: x.pivot_table(index=pivot_index, values='z_swing', aggfunc='sum', margins=True))
    z_con = player_df.groupby(['game_year']).apply(lambda x: x.pivot_table(index=pivot_index, values='z_con', aggfunc='sum', margins=True))
    z_out = player_df.groupby(['game_year']).apply(lambda x: x.pivot_table(index=pivot_index, values='z_out', aggfunc='sum', margins=True))
    z_inplay = player_df.groupby(['game_year']).apply(lambda x: x.pivot_table(index=pivot_index, values='z_inplay', aggfunc='sum', margins=True))
    o_swing = player_df.groupby(['game_year']).apply(lambda x: x.pivot_table(index=pivot_index, values='o_swing', aggfunc='sum', margins=True))
    o_con = player_df.groupby(['game_year']).apply(lambda x: x.pivot_table(index=pivot_index, values='o_con', aggfunc='sum', margins=True))
    o_inplay = player_df.groupby(['game_year']).apply(lambda x: x.pivot_table(index=pivot_index, values='o_inplay', aggfunc='sum', margins=True))

    f_swing = player_df.groupby(['game_year']).apply(lambda x: x.pivot_table(index=pivot_index, values='f_swing', aggfunc='sum', margins=True))
    f_pitch = player_df.groupby(['game_year']).apply(lambda x: x.pivot_table(index=pivot_index, values='f_pitch', aggfunc='sum', margins=True))
    swing = player_df.groupby(['game_year']).apply(lambda x: x.pivot_table(index=pivot_index, values='swing', aggfunc='sum', margins=True))
    whiff = player_df.groupby(['game_year']).apply(lambda x: x.pivot_table(index=pivot_index, values='whiff', aggfunc='sum', margins=True))

    weak = player_df.groupby(['game_year']).apply(lambda x: x.pivot_table(index=pivot_index, values='weak', aggfunc='sum', margins=True))
    topped = player_df.groupby(['game_year']).apply(lambda x: x.pivot_table(index=pivot_index, values='topped', aggfunc='sum', margins=True))
    under = player_df.groupby(['game_year']).apply(lambda x: x.pivot_table(index=pivot_index, values='under', aggfunc='sum', margins=True))
    flare = player_df.groupby(['game_year']).apply(lambda x: x.pivot_table(index=pivot_index, values='flare', aggfunc='sum', margins=True))
    solid_contact = player_df.groupby(['game_year']).apply(lambda x: x.pivot_table(index=pivot_index, values='solid_contact', aggfunc='sum', margins=True))
    barrel = player_df.groupby(['game_year']).apply(lambda x: x.pivot_table(index=pivot_index, values='barrel', aggfunc='sum', margins=True))

    pivot_df = pd.concat([game, pitched, rel_speed, inplay, exit_velocity, launch_angleX, hit_spin_rate, hit, ab, pa, single, double, triple, home_run, walk, hit_by_pitch, sac_fly,
                        z_in, z_swing, z_con, z_out, z_inplay, o_swing, o_con, o_inplay, f_swing, f_pitch, swing, whiff,
                        weak, topped, under, flare, solid_contact, barrel], axis=1)
    
    return pivot_df




def stats_df(merged_base_df):

    merged_base_df['inplay_pit'] = (merged_base_df['inplay'] / merged_base_df['player_name']).round(3)

    merged_base_df['avg'] = 0 
    merged_base_df['obp'] = 0
    merged_base_df['slg'] = 0
    merged_base_df['ops'] = 0
  
    # if merged_base_df['ab'] != 0:
    merged_base_df['avg'] = merged_base_df['hit'] / merged_base_df['ab']
    merged_base_df['obp'] = (merged_base_df['hit'] + merged_base_df['hit_by_pitch'] + merged_base_df['walk']) / (merged_base_df['ab'] + merged_base_df['hit_by_pitch'] + merged_base_df['walk'] + merged_base_df['sac_fly'])
    merged_base_df['slg'] = ((merged_base_df['single'] * 1) + (merged_base_df['double'] * 2) + (merged_base_df['triple'] * 3) + (merged_base_df['home_run'] * 4)) / merged_base_df['ab']
    merged_base_df['ops'] = merged_base_df['obp'] + merged_base_df['slg']

    merged_base_df['z%'] = merged_base_df['z_in'] / merged_base_df['player_name']
    merged_base_df['z_swing%'] = merged_base_df['z_swing'] / merged_base_df['z_in']
    merged_base_df['z_con%'] = merged_base_df['z_con'] / merged_base_df['z_swing']
    merged_base_df['z_inplay%'] = merged_base_df['z_inplay'] / merged_base_df['z_swing']

    merged_base_df['o%'] = merged_base_df['z_out'] / merged_base_df['player_name']
    merged_base_df['o_swing%'] = merged_base_df['o_swing'] / merged_base_df['z_out']
    merged_base_df['o_con%'] = merged_base_df['o_con'] / merged_base_df['o_swing']
    merged_base_df['o_inplay%'] = merged_base_df['o_inplay'] / merged_base_df['o_swing']

    merged_base_df['f_swing%'] = merged_base_df['f_swing'] / merged_base_df['f_pitch']
    merged_base_df['swing%'] = merged_base_df['swing'] / merged_base_df['player_name']
    merged_base_df['whiff%'] = merged_base_df['whiff'] / merged_base_df['swing']
    merged_base_df['inplay_sw'] = merged_base_df['inplay'] / merged_base_df['swing']

    kbo_z_swing = 0.654
    kbo_o_swing = 0.261

    condition = [
                    (merged_base_df['z_swing%'] >= kbo_z_swing) & (merged_base_df['o_swing%'] >= kbo_o_swing),
                    (merged_base_df['z_swing%'] >= kbo_z_swing) & (merged_base_df['o_swing%'] <= kbo_o_swing),
                    (merged_base_df['z_swing%'] <= kbo_z_swing) & (merged_base_df['o_swing%'] >= kbo_o_swing),
                    (merged_base_df['z_swing%'] <= kbo_z_swing) & (merged_base_df['o_swing%'] <= kbo_o_swing)
                    ]

    choicelist = ['Aggressive','Selective','Non_Selective','Passive']

    merged_base_df['approach'] = np.select(condition, choicelist, default='Not Specified')

    merged_base_df['sum'] = merged_base_df['weak'] + merged_base_df['topped'] + merged_base_df['under'] + merged_base_df['flare'] + merged_base_df['solid_contact'] + merged_base_df['barrel']

    merged_base_df['weak'] = (merged_base_df['weak'] / merged_base_df['sum']).round(3)
    merged_base_df['topped'] = (merged_base_df['topped'] / merged_base_df['sum']).round(3)
    merged_base_df['under'] = (merged_base_df['under'] / merged_base_df['sum']).round(3)
    merged_base_df['flare'] = (merged_base_df['flare'] / merged_base_df['sum']).round(3)
    merged_base_df['solid_contact'] = (merged_base_df['solid_contact'] / merged_base_df['sum']).round(3)
    merged_base_df['barrel'] = (merged_base_df['barrel'] / merged_base_df['sum']).round(3)

    merged_base_df['plus_lsa4'] = ((merged_base_df['flare'] + merged_base_df['solid_contact'] + merged_base_df['barrel']) / (merged_base_df['weak'] + merged_base_df['topped'] + merged_base_df['under'] + merged_base_df['flare'] + merged_base_df['solid_contact'] + merged_base_df['barrel'])).round(3)

    stats_output_df = merged_base_df[['game_date','player_name','pa','ab','hit','walk','rel_speed(km)','inplay_pit','exit_velocity','launch_angleX','hit_spin_rate','avg','obp','slg','ops',
                        'z%','z_swing%','z_con%', 'z_inplay%', 'o%','o_swing%', 'o_con%', 'o_inplay%', 'f_swing%', 'swing%', 'whiff%','inplay_sw',
                        'weak','topped','under','flare','solid_contact','barrel','approach', 'plus_lsa4']]
    stats_output_df = stats_output_df.round({'pa':0,'ab':0,'hit':0,'ab':0,'walk':0,'rel_speed(km)':1, 'exit_velocity':1, 'launch_angleX':1, 'hit_spin_rate':0,'avg':3, 'obp':3, 'slg':3, 'ops':3 , 
                                'z%': 3,'z_swing%':3,'z_con%':3,'z_inplay%':3, 'o%':3,'o_swing%':3, 'o_con%':3, 'o_inplay%':3, 'f_swing%':3, 'swing%':3, 'whiff%':3,'inplay_sw':3, 'inplay%':3, 'approach':3})

    return stats_output_df
