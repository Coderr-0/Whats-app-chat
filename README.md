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

A very simple one-line summary is: this code makes a WhatsApp chat dashboard where a user uploads a chat file and gets visual insights from it. 

