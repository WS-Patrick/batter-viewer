import pandas as pd

# import mysql.connector
from configparser import ConfigParser
# cnx: mysql.connector.connect = None

def login (userName, password):
    user_df = pd.read_csv('./user_info_2023.csv')
    user_id = user_df['ID'].tolist()
    user_password = user_df['Password'].tolist()
    
    if userName in user_id:
        index = user_id.index(userName)
        if password == user_password[index]:
            return True
    else:
        return False


def update_log(userName):
    st.write(userName)
    # log_data = {
    #     'UserName': [userName],
    #     'Timestamp': [pd.Timestamp.now()]
    # }

    # log_df = pd.DataFrame(log_data)
    # st.dataframe(log_df)






    
    # user = userName
    # log_data = {
    #     'UserName': [user],
    #     'Timestamp': [pd.Timestamp.now()]
    # }

    # log_df = pd.DataFrame(log_data)

    # # Check if the log file already exists
    # try:
    #     existing_log = pd.read_csv('./login_log.csv')
    #     updated_log = pd.concat([existing_log, log_df], ignore_index=True)
    # except FileNotFoundError:
    #     updated_log = log_df

    # # Save the log to a CSV file
    # updated_log.to_csv('./login_log.csv', index=False)
