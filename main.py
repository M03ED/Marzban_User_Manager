import requests
import logging
import os
import datetime

def get_access_token(username, password):
    url = f'https://{DOMAIN}:{PORT}/api/admin/token'
    data = {
        'username': username,
        'password': password
    }

    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        access_token = response.json()['access_token']
        return access_token
    except requests.exceptions.RequestException as e:
        logging.error(f'Error occurred while obtaining access token: {e}')
        return None

def get_users_list(access_token):
    url = f'https://{DOMAIN}:{PORT}/api/users'
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        users_list = response.json()
        return users_list
    except requests.exceptions.RequestException as e:
        logging.error(f'Error occurred while retrieving users list: {e}')
        return None
    
def delete_user(access_token, username):
    url = f'https://{DOMAIN}:{PORT}/api/user/{username}'
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        user_details = response.json()


        response = requests.delete(url, json=user_details, headers=headers)
        response.raise_for_status()
        return True

    except requests.exceptions.RequestException as e:
        logging.error(f'Error occurred while modifying user : {e}')
        return False


def modify_user_data(access_token, username, final_data_limit , timestamp):
    url = f'https://{DOMAIN}:{PORT}/api/user/{username}'
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        user_details = response.json()

        if final_data_limit is not None and timestamp is not None:

            user_details['data_limit'] = final_data_limit
            user_details['expire'] = timestamp

            response = requests.put(url, json=user_details, headers=headers)
            response.raise_for_status()

            return True
        else:
            logging.error(f'Invalid data_limit or expire date for user {username}')
            return False
    except requests.exceptions.RequestException as e:
        logging.error(f'Error occurred while modifying user : {e}')
        return False

# Configure logging settings
logging.basicConfig(filename='script_log.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

def multiplication_traffic (data_limit , used_traffic , multiplication_factor):
    remain_traffic = float(data_limit) - float(used_traffic)
    new_data_limit = float(remain_traffic) * float(multiplication_factor)
    final_data_limit = float(new_data_limit) + float(used_traffic)
    return final_data_limit

def mod_traffic (data_limit , traffic, operator):
    if operator == '+':
        final_data_limit = float(data_limit) + float(traffic) * float(1024**3)
        return final_data_limit
    elif operator == '-':
        final_data_limit = float(data_limit) - float(traffic) * float(1024**3)
        return final_data_limit
    
def mod_expire (timestamp, days, operator):

    datetime_obj = datetime.datetime.fromtimestamp(timestamp)
    time_difference = datetime.timedelta(days=float(days))

    if operator == '+':
        new_datetime_obj = datetime_obj + time_difference
        timestamp = new_datetime_obj.timestamp()
        return timestamp
    elif operator == '-':
        new_datetime_obj = datetime_obj - time_difference
        timestamp = new_datetime_obj.timestamp()
        return timestamp
    
def remove (timestamp):
    current_timestamp = datetime.datetime.now().timestamp()
    time_difference = current_timestamp - timestamp
    return time_difference

def modify(factor, switch_number):
    if access_token:
        users_list = get_users_list(access_token)
        if users_list:
            for user in users_list['users']:
                data_limit = user['data_limit']
                used_traffic = user['used_traffic']
                timestamp = user['expire']
                if int(switch_number) <= 3:
                    if user['status'] == 'active':
                        if data_limit is not None :
                            if int(switch_number) == 1:
                                final_data_limit = multiplication_traffic(data_limit, used_traffic, factor)
                                final_timestamp = timestamp
                            elif int(switch_number) == 2:
                                final_data_limit = mod_traffic(data_limit, factor, '+')
                                final_timestamp = timestamp
                            elif int(switch_number) == 3:
                                final_data_limit = mod_traffic(data_limit, factor, '-')
                                final_timestamp = timestamp
                            else:
                                continue
                            if modify_user_data(access_token, user['username'], final_data_limit, final_timestamp):
                                print(f"User {user['username']} updated successfully.")
                            else:
                                print(f"Failed to update data limit or expire date for user {user['username']}.")
                                continue
                elif int(switch_number) == 4 or int(switch_number) == 5:
                        if timestamp is not None:
                            if int(switch_number) == 4:
                                final_data_limit = data_limit
                                final_timestamp = mod_expire(timestamp, factor, '+')
                            elif int(switch_number) == 5:
                                final_data_limit = data_limit
                                final_timestamp = mod_expire(timestamp, factor, '-')
                            else:
                                continue
                            if modify_user_data(access_token, user['username'], final_data_limit, final_timestamp):
                                    print(f"User {user['username']} updated successfully.")
                            else:
                                print(f"Failed to update data limit or expire date for user {user['username']}.")
                                continue
                        else:
                            print(f"Skipping user {user['username']} (data limit or expire date is None).")
                elif int(switch_number) > 5:
                    if user['status'] == 'expired' or 'limited' and user['status'] !='active':
                        if timestamp is not None :
                            time_difference = remove(timestamp)
                            if time_difference > float(factor) * 24 * 60 * 60:  
                                if delete_user(access_token, user['username'], ):
                                    print(f"User {user['username']} deleted successfully.")
                                else:
                                    print(f"Failed to delete user {user['username']}.")
                            else:
                                print(f"user {user['username']} is not expierd.")
                        else:
                            # Skip modifying the data limit for users with data_limit = None
                            print(f"Skipping user {user['username']} (expire time is None).")
                    else:
                        print(f"user {user['username']} is disabled or Invalid data limit or expire date for user.")                
                else:
                    print(f"Invalid switch number.")
        else:
            print("Failed to retrieve the users list.")
    else:
        print("Failed to obtain the access token.")
    
username = input('Enter Your Username:')
password = input('Enter Your Password:')
DOMAIN = input('Enter Your Panel Domain (without https):')
PORT = input('Enter Your Panel Port (1-65535):') 

access_token = get_access_token(username, password)

if access_token:
    class Switch:
        def case_1(self):
           multiplication_factor = input ('Enter The Coefficient You Want:')
           modify (multiplication_factor , switch_number)
           pass
        def case_2(self):
           traffic = input ('Enter Traffic You Want Increase To All Users (Per GB):')
           modify (traffic , switch_number)
           pass
        def case_3(self):
           traffic = input ('Enter Traffic You Want Decrease From All Users (Per GB):')
           modify (traffic , switch_number)
           pass 
        def case_4(self):
           Days = input ('Enter Days Number You Want Increase To All Users:')
           modify (Days , switch_number)
           pass 
        def case_5(self):
           Days = input ('Enter Days Number You Want Decrease To All Users:')
           modify (Days , switch_number)
           pass 
        def case_6(self):
           Days = input ('Enter The Number Of Past Days:')
           modify (Days , switch_number)
        def default(self):
           print("Invalid option")
           pass
        
    def process_data(option):
        switch = Switch()
        getattr(switch, 'case_' + option, switch.default)()

    os.system('cls')
    print('1- Multiplication Remaning Traffic For All Users')
    print('2- Increase The Same Traffic To All Users')
    print('3- Decrease The Same Traffic From All Users')
    print('4- Increase The Same Time To All Users')
    print('5- Decrease The Same Time From All Users')
    print('6- Delete Expired Users')

    switch_number = input("Enter the number : ")

    process_data(switch_number)
else:
    print("Failed to obtain the access token.")