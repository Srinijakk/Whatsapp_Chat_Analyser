
import streamlit as st
import preprocesser
import helper# Make sure this file exists in the same directory
import matplotlib.pyplot as plt
import seaborn as sns



st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocesser.preprocess(data)
     # Optional: To show the dataframe in the Streamlit app

    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")
    selected_user = st.sidebar.selectbox("Show analysis with respective to", user_list)
    if st.sidebar.button("Show Analysis"):
       num_messages,words ,num_media_messages ,num_links = helper.fetch_stats(selected_user,df)
       st.title("Top Stats")
       col1, col2, col3, col4 =st.columns(4)
       with col1:
            st.header("Total Msg's")
            st.title(num_messages)
       with col2:
            st.header("Total Words")
            st.title(words)
       with col3:
            st.header("Media Shared ")
            st.title(num_media_messages)
       with col4:
            st.header("Links Shared ")
            st.title(num_links)

       st.title("Monthly Timeline")
       timeline = helper.monthly_timeline(selected_user, df)
       fig, ax = plt.subplots()
       ax.plot(timeline['time'], timeline['message_count'])
       plt.xticks(rotation='vertical')
       st.pyplot(fig)

       # Daily Timeline
       st.title("Daily Timeline")
       daily_timeline = helper.daily_timeline(selected_user, df)

       fig, ax = plt.subplots()
       ax.plot(daily_timeline['only_date'], daily_timeline['message_count'])
       plt.xticks(rotation='vertical')
       st.pyplot(fig)

       #Activity map
       st.title('Activity Map')
       col1, col2 = st.  columns(2)
       with col1:
           st.header("Most busy day")
           busy_day = helper.week_activity_map(selected_user, df)
           fig, ax = plt.subplots()
           plt.xticks(rotation='vertical')
           ax.bar(busy_day.index, busy_day.values)
           st.pyplot(fig)

       with col2:
           st.header("Most busy Month")
           busy_month = helper.month_activity_map(selected_user, df)
           fig, ax = plt.subplots()
           plt.xticks(rotation='vertical')
           ax.bar(busy_month.index, busy_month.values,color = "orange")
           st.pyplot(fig)

       st.title("Weekly Activity Map")
       user_heatmap = helper.activity_heatmap(selected_user, df)
       fig, ax = plt.subplots()
       ax = sns.heatmap(user_heatmap)
       st.pyplot(fig)


    # finding the busiest users in the group
    if selected_user == 'Overall':  # Ensure this runs only for 'Overall' selection
        st.title('Most Busy Users')
        x, new_df = helper.most_busy_users(df)

        # Create columns for chart & table
        col1, col2 = st.columns(2)

        # Plot Bar Chart
        with col1:
            fig, ax = plt.subplots()
            ax.bar(x.index, x.values, color='skyblue')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # Show Data Table
        with col2:
            st.dataframe(new_df)

    # WordCloud
    st.title("WORDCLOUD")
    df_wc= helper.create_wordcloud(selected_user, df)
    fig, ax = plt.subplots()
    ax.imshow(df_wc)
    st.pyplot(fig)

    st.title("Emoji Analysis")
    emoji_df = helper.emoji_helper(selected_user, df)

    col1, col2 = st.columns(2)

    with col1:
        st.dataframe(emoji_df)

    with col2:
        fig, ax = plt.subplots()
        ax.pie(emoji_df['count'], labels=emoji_df['emoji'], autopct="%0.2f%%", startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        st.pyplot(fig)



