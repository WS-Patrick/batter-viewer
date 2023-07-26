import pandas as pd
import streamlit as st
import os
import logging

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

# def update_log(userName):
#     user = str(userName)
    
#     log_data = {
#         'UserName': [user],
#         'Timestamp': [pd.Timestamp.now()]}

#     log_df = pd.DataFrame(log_data)

#     # Check if the log file already exists
#     try:
#         existing_log = pd.read_csv('./login_log.csv')
#         updated_log = pd.concat([existing_log, log_df], ignore_index=True)
#     except FileNotFoundError:
#         updated_log = log_df

#     st.dataframe(updated_log)

#     # Save the log to a CSV file
#     updated_log.to_csv('./login_log.csv', index=False, encoding='utf-8')

#     os.system('git add login_log.csv')   
#     os.system('git commit -m "Update login_log.csv"')
#     os.system('git push https://github.com/PATRICK-KTWIZ/batter-viewer.git main') 

def update_log(userName):
    
    user = str(userName)
    
    log_data = {
        'UserName': [user],
        'Timestamp': [pd.Timestamp.now()]}

    log_df = pd.DataFrame(log_data)

    # Check if the log file already exists
    try:
        existing_log = pd.read_csv('./login_log.csv')
        updated_log = pd.concat([existing_log, log_df], ignore_index=True)
    except FileNotFoundError:
        updated_log = log_df

    st.dataframe(updated_log)

    # Save the log to a log file using Python logging module
    logging.basicConfig(filename='https://github.com/PATRICK-KTWIZ/batter-viewer.git', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info(f"User {user} logged in at {pd.Timestamp.now()}")

    # Save the updated_log DataFrame to a CSV file (optional, if needed)
    updated_log.to_csv('./login_log.csv', index=False, encoding='utf-8')

    os.system('git add login_history.log')   
    os.system('git commit -m "Update login_history.log"')
    os.system('git push https://github.com/PATRICK-KTWIZ/batter-viewer.git main') 
