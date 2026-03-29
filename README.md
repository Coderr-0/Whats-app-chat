# Whats-app-chat

app.py code explination
This code builds a **Streamlit web app** for analyzing a WhatsApp chat file that the user uploads. It reads the chat, converts it into a DataFrame, lets the user choose either overall chat analysis or a specific person, and then shows statistics and charts like timelines, activity maps, word clouds, common words, busy users, and emoji analysis. 
Imports
`streamlit` is used to create the app interface, while `matplotlib` and `seaborn` are used for charts that are displayed in the app with `st.pyplot()`. The `preprocessor` and `helper` modules are custom Python files that likely contain the logic for cleaning the chat data and generating the analysis results. 
## File upload
The app creates a sidebar and asks the user to upload a file using `st.sidebar.file_uploader()`, which is a standard Streamlit widget for file uploads. After a file is uploaded, the code reads its content, decodes it from bytes into text, and sends that text to `preprocessor.preprocess(data)` to convert the raw chat into a structured DataFrame called `df`. 
## User selection
The code gets all unique users from the `user` column, removes `group_notification`, sorts the names, and adds `"Overall"` at the top. Then `st.sidebar.selectbox()` shows a dropdown so the user can choose whether the analysis should be for the whole chat or for one selected user. 
## Statistics section
When the user clicks **Show Analysis**, the app calls `helper.fetch_stats(selected_user, df)` and displays four key values: total messages, total words, media shared, and links shared. It places these values in four side-by-side columns using `st.columns(4)`, which is a common Streamlit layout feature for dashboard-style display. 
## Charts and insights
The app then shows multiple visualizations: monthly timeline, daily timeline, busy day, busy month, and a weekly activity heatmap. The line charts and bar charts are created with Matplotlib, while the heatmap uses Seaborn’s `heatmap()` and is shown in Streamlit through `st.pyplot(fig)`. 

It also shows the most busy users when `"Overall"` is selected, a word cloud of commonly used words, a bar chart of the most common words, and an emoji analysis using both a table and a pie chart. In simple terms, this part helps the user understand who talks the most, when messages are sent most often, which words appear frequently, and which emojis are used the most. 
Simple flow
You can think of the app in this order:
- Upload WhatsApp chat file.
- Convert chat text into a DataFrame.
- Choose a user or overall analysis.
- Click the button to generate results.
- View stats, charts, word analysis, and emoji analysis. 

 
 
helper.py

 
Imports
from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
URLExtract is used to find links inside chat messages.
WordCloud is used to generate a word cloud from all messages.
pandas is used for working with DataFrames and grouping data.
Counter counts repeated items like words or emojis.
emoji helps detect emoji characters in messages.
extractor = URLExtract()
This creates an object that will be used later to extract URLs from each message.
fetch_stats()
def fetch_stats(selected_user, df):
This function calculates the main statistics of the chat for either one selected user or the full chat.
   if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
If the user selects a specific person, the DataFrame is filtered to include only that person’s messages. If "Overall" is selected, the full DataFrame is used.
   num_messages = df.shape[0]
This counts the total number of messages by checking how many rows are in the DataFrame.
   words = []
    for message in df['message']:
        words.extend(message.split())
This loops through every message, splits each message into words, and stores them all in a list. Later, the total word count is found using the list length.
   num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]
This counts how many messages are media placeholders like images or videos instead of text.
   links = []
    for message in df['message']:
        links.extend(extractor.find_urls(message))
This checks every message for URLs and stores all detected links in a list.
   return num_messages, len(words), num_media_messages, len(links)
This returns four values: total messages, total words, media messages, and links shared.
monthly_timeline()
def monthly_timeline(selected_user, df):
This function creates a month-wise message timeline.
   if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
Again, it filters the DataFrame if a particular user is selected.
   timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
This groups the data by year and month, counts the number of messages in each group, and converts the result back into a normal table.
   time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
This creates a new readable label like January-2024 or May-2023 for plotting.
   timeline['time'] = time
    return timeline
The new time column is added and the final timeline DataFrame is returned.
daily_timeline()
def daily_timeline(selected_user, df):
This function creates a day-wise timeline of messages.
   if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
It filters the chat by selected user if needed.
   daily_timeline = df.groupby('only_date').count()['message'].reset_index()
It groups messages by date and counts how many messages were sent on each day.
   return daily_timeline
It returns the daily timeline table.
week_activity_map()
def week_activity_map(selected_user, df):
This function finds how many messages were sent on each weekday.
   if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
It filters by user if required.
   return df['day_name'].value_counts()
It counts how many times each day name like Monday or Tuesday appears.
month_activity_map()
def month_activity_map(selected_user, df):
This function counts messages month-wise.
   if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
It filters for a selected user if needed.
   return df['month'].value_counts()
It counts the number of messages in each month.
activity_heatmap()
def activity_heatmap(selected_user, df):
This function creates data for a heatmap showing chat activity across days and time periods.
   if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
It filters the DataFrame when one person is selected.
   user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
This creates a pivot table where rows are days, columns are time periods, and cell values show the count of messages. fillna(0) replaces empty cells with 0.
   return user_heatmap
It returns the heatmap data.
most_busy_users()
def most_busy_users(df):
This function finds which users send the most messages in the group.
   x = df['user'].value_counts().head()
This gets the top 5 most active users by message count.
   df_percent = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index()
This calculates what percentage of total messages each user contributed.
   return x, df_percent
It returns both the top user counts and the percentage table.
create_wordcloud()
def create_wordcloud(selected_user, df):
This function creates a word cloud from the chat messages.
   if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
It filters data if one user is selected.
   wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
This creates a WordCloud object and sets its size, font size, and background color.
   df_wc = wc.generate(df['message'].str.cat(sep=" "))
This joins all messages into one large text string and generates the word cloud from it.
   return df_wc
It returns the word cloud object so it can be displayed in the app.
most_common_words()
def most_common_words(selected_user, df):
This function finds the most frequently used words in the chat.
   if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
It filters messages for the selected user if needed.
   words = []
This creates an empty list to store all words.
   for message in df['message']:
        words.extend(message.lower().split())
This converts each message to lowercase, splits it into words, and adds those words to the list.
   most_common_df = pd.DataFrame(Counter(words).most_common(20))
Counter counts word frequency, and most_common(20) returns the top 20 words. Then it converts the result into a DataFrame.
   return most_common_df
It returns the table of most common words.
emoji_helper()
def emoji_helper(selected_user, df):
This function finds and counts emojis used in the chat.
   if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
It filters the DataFrame for a specific user if selected.
   emojis = []
This creates an empty list to store emojis.
   for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
This checks each character in each message and keeps only those characters that are valid emojis.
   emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
This counts emoji frequency and converts the results into a DataFrame.
   return emoji_df
It returns the emoji count table.
Duplicate function
At the end, activity_heatmap() is written again with the same logic. That means the second version simply overwrites the first one, so it is unnecessary duplication and can be removed.
Overall purpose
In simple words, this file contains all the analysis functions for the WhatsApp Chat Analyzer. The main app calls these functions to compute statistics, timelines, most active users, word clouds, common words, emoji counts, and heatmap data from the chat DataFrame.


preprocess.py


This code is the preprocessing part of your WhatsApp Chat Analyzer. Its job is to take the raw exported chat text, separate each message, identify the sender and message content, convert dates into proper datetime format, and create extra columns like year, month, day, hour, and time period for analysis.
Main purpose
The function preprocess(data) takes the full WhatsApp chat text as input and converts it into a clean Pandas DataFrame. This is important because analysis functions work better on structured tabular data than on raw text.
Regex pattern
pattern = r'\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4},?\s\d{1,2}:\d{2}\s?(?:am|pm|AM|PM)?\s?-\s'
This regular expression is used to detect WhatsApp timestamps such as 12/5/23, 9:45 pm - or 12-5-2023 9:45 -. It matches date, time, optional AM/PM, and the dash that usually appears before the message text.
Splitting messages and dates
messages = re.split(pattern, data)[1:]
dates = re.findall(pattern, data)
re.split() breaks the chat text into individual message parts using the timestamp pattern.
re.findall() extracts all matching date-time strings.
So after this:
messages contains the message text parts.
dates contains the corresponding timestamps.
if len(messages) == 0:
    raise ValueError("No valid WhatsApp messages found")
This checks whether any valid messages were found. If not, it raises an error so the app knows the file format is not matching the expected WhatsApp export style.
Creating the DataFrame
df = pd.DataFrame({'user_message': messages, 'message_date': dates})
This creates a DataFrame with two columns:
user_message for the raw message text
message_date for the timestamp text
df['message_date'] = pd.to_datetime(df['message_date'], errors='coerce')
df.rename(columns={'message_date': 'date'}, inplace=True)
pd.to_datetime() converts the date strings into proper datetime values.
errors='coerce' means invalid date values become missing values instead of crashing the program.
Then the column is renamed from message_date to date.
Separating user and message
users = []
messages_list = []
These two empty lists will store:
sender names
actual message text
for message in df['user_message']:
    entry = re.split(r'([\w\W]+?):\s', message)
This tries to split each chat line into:
username
message text
The pattern looks for something like Rahul: Hello where the name appears before :.
   if entry[1:]:
        users.append(entry[1])
        messages_list.append(entry[2])
If the split successfully finds a sender name:
save the sender in users
save the message text in messages_list

   else:
        users.append('group_notification')
        messages_list.append(entry[0])
If no sender is found, it is treated as a group notification, like:
“X joined using this group's invite link”
“Messages and calls are end-to-end encrypted”
Adding cleaned columns
df['user'] = users
df['message'] = messages_list
df.drop(columns=['user_message'], inplace=True)
This adds the cleaned sender and message columns and removes the old combined column.
So now the DataFrame becomes more useful:
date
user
message
Date feature extraction
df['only_date'] = df['date'].dt.date
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month_name()
df['month_num'] = df['date'].dt.month
df['day'] = df['date'].dt.day
df['day_name'] = df['date'].dt.day_name()
df['hour'] = df['date'].dt.hour
df['minute'] = df['date'].dt.minute
These lines create extra columns from the datetime column so later analysis becomes easier. For example, you can now group messages by year, month, day, weekday, hour, or minute.
Creating time period
period = []
for hour in df[['day_name', 'hour']]['hour']:
    if hour == 23:
        period.append(str(hour) + "-" + str('00'))
    elif hour == 0:
        period.append(str('00') + "-" + str(hour + 1))
    else:
        period.append(str(hour) + "-" + str(hour + 1))
This creates a time slot for every message based on its hour. Examples:
0 becomes "00-1"
9 becomes "9-10"
23 becomes "23-00"
This is useful for heatmaps and hourly activity charts.
df['period'] = period
This stores those time slots in a new column called period.
Repeated code
After that, your code repeats these lines again:
df['hour'] = df['date'].dt.hour
df['minute'] = df['date'].dt.minute
df['day_name'] = df['date'].dt.day_name()

period = []
for hour in df['hour']:
    ...
df['period'] = period
This repeated block does the same work again, so it is unnecessary duplication. The second block overwrites the same columns with the same values, so you can remove it without changing the final result.
Return value
return df
This returns the final cleaned DataFrame. That DataFrame is then used by your helper functions and Streamlit dashboard.
Simple flow
Here is the full process in very simple words:
Read raw WhatsApp chat text.
Find date and time patterns using regex.
Split the text into separate messages.
Extract sender name and actual message.
Convert date text into datetime format.
Create useful columns like month, day, hour, and period.
Return a clean DataFrame for analysis.
Function summary
Function
Purpose
Input
Output
preprocess(data)
Converts raw WhatsApp chat text into structured tabular data. 
Full WhatsApp chat text as a string. 
A cleaned DataFrame with columns like date, user, message, year, month, day_name, and period. 

Very short viva answer
You can say: “This function preprocesses raw WhatsApp chat text using regex, extracts timestamps, usernames, and messages, converts them into a DataFrame, and creates additional date-time columns for further analysis.”
One improvement
A cleaner version would remove the duplicate hour, minute, day_name, and period block, because those columns are already created earlier. Also, when saving messages, using " ".join(entry[2:]) can be safer than only entry[2] if a split produces multiple text parts.
