import re
import pandas as pd


def preprocess(data):
    # Pattern to extract message timestamps
    pattern = r'\d{2}/\d{2}/\d{2},\s\d{1,2}:\d{2}\s?[ap]m\s-\s'

    # Split messages and extract timestamps
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    # Create initial DataFrame
    df = pd.DataFrame({'message_date': dates, 'user_message': messages})

    # Replace strange spaces (optional but good)
    df['message_date'] = df['message_date'].str.replace('\u202f', ' ', regex=True)

    # Convert to datetime using the correct format
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %I:%M %p - ', errors='coerce')

    # Rename the column for clarity
    df.rename(columns={'message_date': 'date'}, inplace=True)

    # Extract users and messages
    users = []
    messages = []

    for message in df['user_message']:
        entry = re.split(r'([\w\W]+?):\s', message, maxsplit=1)
        if len(entry) > 2:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    # Add new columns
    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    # Add datetime parts for analysis
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df["day_name"] = df['date'].dt.day_name()
    df['only_date'] = df['date'].dt.date
    df['month_num'] = df['date'].dt.month
    df['day_name'] = df['date'].dt.day_name( )
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
             period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))
    df['period'] = period

    return df
