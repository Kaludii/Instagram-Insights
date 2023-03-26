import streamlit as st
import pandas as pd
import json
import plotly.express as px
from datetime import datetime
import plotly.graph_objs as go
import base64
from io import StringIO

import base64

def generate_download_link(df, filename):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    button_style = (
        "background-color: #4CAF50;"
        "border: none;"
        "color: white;"
        "padding: 10px 20px;"
        "text-align: center;"
        "text-decoration: none;"
        "display: inline-block;"
        "font-size: 16px;"
        "margin: 4px 2px;"
        "cursor: pointer;"
        "border-radius: 8px;"
    )
    return f'<a href="data:file/csv;base64,{b64}" download="{filename}" style="{button_style}">Download {filename}</a>'


def count_users(json_data, key):
    return len(json_data[key])

def get_users(data, key, file_name):
    users = []
    json_data = data[file_name]

    if key == 'string_list_data':
        for item in json_data:
            user_data = item[key][0]
            timestamp = datetime.utcfromtimestamp(user_data['timestamp']).strftime('%m/%d/%Y %H:%M')
            users.append({'Username': user_data['value'], 'Profile URL': user_data['href'], 'Timestamp': timestamp})
    else:
        for item in json_data[key]:
            user_data = item['string_list_data'][0]
            timestamp = datetime.utcfromtimestamp(user_data['timestamp']).strftime('%m/%d/%Y %H:%M')
            users.append({'Username': user_data['value'], 'Profile URL': user_data['href'], 'Timestamp': timestamp})

    return users


def get_missing_files(data):
    required_files = [
        'followers.json',
        'following.json',
        "follow_requests_you've_received.json",
        'pending_follow_requests.json',
        'recent_follow_requests.json',
        'recently_unfollowed_accounts.json',
    ]
    missing_files = [file for file in required_files if file not in data]

    if ('followers.json' not in data and 'followers_1.json' not in data) or ('followers.json' in missing_files and 'followers_1.json' in data):
        missing_files.remove('followers.json')
    elif 'followers.json' in missing_files and 'followers_1.json' not in data:
        missing_files.remove('followers.json')
        missing_files.append('followers_1.json')

    return missing_files



st.set_page_config(page_title='Instagram Insights')
st.title('Instagram Insights')

st.markdown('''
Welcome to Instagram Insights, a tool to help you analyze and understand your Instagram data like users not following you back or users you aren't following back.
Upload your Instagram data, and the app will visualize various insights such as followers, following, follow requests, and more.
Filter and download the data for further analysis. You can download your Instagram data by going to Settings > Data Download, and click on 'Request Download'.
Make sure you download the data as a JSON file. When the data is emailed to you, upload all the files in the 'followers_and_following' folder, and that's it!
''')


uploaded_files = st.file_uploader('Upload your Instagram folder', type=['json'], accept_multiple_files=True)

if uploaded_files:
    try:
        st.sidebar.title('Filters')
        users_not_following_me_back = st.sidebar.checkbox('Users Not Following Me Back')
        users_im_not_following_back = st.sidebar.checkbox("Users I'm Not Following Back")

        # data loading and parsing
        data = {}
        for file in uploaded_files:
            file_name = file.name
            file_content = file.getvalue().decode()
            data[file_name] = json.loads(file_content)

        # Check if 'followers.json' or 'followers_1.json' is present and load the followers accordingly
        if 'followers.json' in data:
            followers = get_users(data, 'relationships_followers', 'followers.json')
        elif 'followers_1.json' in data:
            followers = get_users(data, 'string_list_data', 'followers_1.json')
        else:
            st.error("Please upload the followers.json or followers_1.json file.")

        following = get_users(data, 'relationships_following', 'following.json')

        # Create bar chart with counts
        chart_labels = [
            'Followers',
            'Following',
            "Follow Requests Received",
            "Pending Follow Requests",
            "Recent Follow Requests",
            "Recently Unfollowed Accounts",
        ]

        if 'followers.json' in data:
            followers_count = count_users(data['followers.json'], 'relationships_followers')
        elif 'followers_1.json' in data:
            followers_count = len(data['followers_1.json'])

        chart_values = [
            followers_count,
            count_users(data['following.json'], 'relationships_following'),
            count_users(data["follow_requests_you've_received.json"], 'relationships_follow_requests_received'),
            count_users(data['pending_follow_requests.json'], 'relationships_follow_requests_sent'),
            count_users(data['recent_follow_requests.json'], 'relationships_permanent_follow_requests'),
            count_users(data['recently_unfollowed_accounts.json'], 'relationships_unfollowed_users'),
        ]


        bar_chart = go.Figure(
            data=[
                go.Bar(x=chart_labels, y=chart_values, text=chart_values, textposition='auto')
            ]
        )

        bar_chart.update_layout(
            title="Instagram Insights Summary",
            xaxis_title="Categories",
            yaxis_title="Count",
            plot_bgcolor="rgba(0, 0, 0, 0)",
        )

        st.plotly_chart(bar_chart)
        
        if users_not_following_me_back:
            not_following_me_back = [user for user in following if user['Username'] not in [follower['Username'] for follower in followers]]
            df_not_following_me_back = pd.DataFrame(not_following_me_back)
            st.subheader(f"Users Not Following Me Back ({len(df_not_following_me_back) - 1})")
            st.write(df_not_following_me_back)
            st.markdown(generate_download_link(df_not_following_me_back, "users_not_following_me_back.csv"), unsafe_allow_html=True)

        if users_im_not_following_back:
            im_not_following_back = [user for user in followers if user['Username'] not in [following_user['Username'] for following_user in following]]
            df_im_not_following_back = pd.DataFrame(im_not_following_back)
            st.subheader(f"Users I'm Not Following Back ({len(df_im_not_following_back) - 1})")
            st.write(df_im_not_following_back)
            st.markdown(generate_download_link(df_im_not_following_back, "users_im_not_following_back.csv"), unsafe_allow_html=True)


        # Add 'Files Filter' section to the sidebar
        st.sidebar.title('Files Filter')
        show_followers = st.sidebar.checkbox('Show Followers')
        show_following = st.sidebar.checkbox('Show Following')
        show_received_requests = st.sidebar.checkbox("Show Follow Requests Received")
        show_pending_requests = st.sidebar.checkbox("Show Pending Follow Requests")
        show_recent_requests = st.sidebar.checkbox("Show Recent Follow Requests")
        show_unfollowed_accounts = st.sidebar.checkbox("Show Recently Unfollowed Accounts")

        # Display the corresponding dataframes based on the checkboxes
        if show_followers:
            st.subheader('Followers')
            st.write(pd.DataFrame(followers))
            st.markdown(generate_download_link(pd.DataFrame(followers), "followers.csv"), unsafe_allow_html=True)

        if show_following:
            st.subheader('Following')
            st.write(pd.DataFrame(following))
            st.markdown(generate_download_link(pd.DataFrame(following), "following.csv"), unsafe_allow_html=True)

        if show_received_requests:
            received_requests = get_users(data, 'relationships_follow_requests_received', "follow_requests_you've_received.json")
            st.subheader("Follow Requests Received")
            st.write(pd.DataFrame(received_requests))
            st.markdown(generate_download_link(pd.DataFrame(received_requests), "follow_requests_received.csv"), unsafe_allow_html=True)

        if show_pending_requests:
            pending_requests = get_users(data, 'relationships_follow_requests_sent', 'pending_follow_requests.json')
            st.subheader("Pending Follow Requests")
            st.write(pd.DataFrame(pending_requests))
            st.markdown(generate_download_link(pd.DataFrame(pending_requests), "pending_follow_requests.csv"), unsafe_allow_html=True)

        if show_recent_requests:
            recent_requests = get_users(data, 'relationships_permanent_follow_requests', 'recent_follow_requests.json')
            st.subheader("Recent Follow Requests")
            st.write(pd.DataFrame(recent_requests))
            st.markdown(generate_download_link(pd.DataFrame(recent_requests), "recent_follow_requests.csv"), unsafe_allow_html=True)

        if show_unfollowed_accounts:
            unfollowed_accounts = get_users(data, 'relationships_unfollowed_users', 'recently_unfollowed_accounts.json')
            st.subheader("Recently Unfollowed Accounts")
            st.write(pd.DataFrame(unfollowed_accounts))
            st.markdown(generate_download_link(pd.DataFrame(unfollowed_accounts), "recently_unfollowed_accounts.csv"), unsafe_allow_html=True)

    except KeyError as e:
        missing_files = get_missing_files(data)
        if missing_files:
            missing_files_str = ", ".join(missing_files)
            st.error(f"Please make sure to upload the following missing file(s): {missing_files_str}")
        else:
            st.error(f"An error occurred while processing your files: {e}")


else:
    st.warning("Please upload your Instagram data files.")