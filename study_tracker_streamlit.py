"""
Study Tracker - Streamlit Web App

Run this file with:

streamlit run study_tracker_streamlit.py
"""
# This docstring explains what this file is.
# The original program was a terminal app, but this version is a web app.
# Streamlit lets us create a web interface using normal Python code.

import json
# json is still used exactly like the terminal version.
# It reads and writes the study session data so the data persists after the app
# is closed.

from datetime import date
# date is used for the Streamlit date picker.
# The date picker gives us a real date value, and we convert it to text before
# saving it in JSON.

import streamlit as st
# streamlit is the web app library.
# We use the nickname st because that is the common Streamlit convention.
# Streamlit widgets, such as st.text_input and st.number_input, replace the
# terminal input() statements.


DATA_FILE = "study_sessions.json"
# This is the same storage filename used by the terminal app.
# Keeping the same filename means both versions can read and write the same
# kind of JSON data.


def load_sessions():
    """
    Load all saved study sessions from the JSON file.
    If the file does not exist yet, return an empty list.
    """
    # This backend function is intentionally kept the same as the terminal app.
    # It uses Python file handling, a try/except block, and json.load.
    # Streamlit changes the user interface, but the storage logic can stay the
    # same because JSON reading is not tied to the terminal.

    try:
        # try means "attempt this code, but be ready if an error happens."
        # Opening a file may fail the first time because the JSON file may not
        # exist yet.

        with open(DATA_FILE, "r") as file:
            # open(DATA_FILE, "r") opens the file in read mode.
            # The file variable represents the open file object.
            # The with statement closes the file automatically.

            sessions = json.load(file)
            # json.load reads JSON text and converts it into Python data.
            # In this app, sessions should be a list of dictionaries.

            return sessions
            # return sends the loaded list back to the caller.

    except FileNotFoundError:
        # FileNotFoundError means there is no saved JSON file yet.
        # This is normal when the app is used for the first time.

        return []
        # An empty list means there are currently no study sessions.

    except json.JSONDecodeError:
        # JSONDecodeError means the file exists, but the JSON text is broken.
        # For a beginner project, we keep the app running and start with an
        # empty list.

        print("The data file could not be read, so the app will start empty.")
        # This print statement is part of the same backend logic from the
        # terminal app. In Streamlit, this message appears in the server
        # terminal, not on the web page.

        return []
        # Returning an empty list keeps the rest of the app working.


def save_sessions(sessions):
    """
    Save all study sessions to the JSON file.
    """
    # This backend function is also the same as the terminal app.
    # The sessions parameter receives the complete list of study sessions.

    with open(DATA_FILE, "w") as file:
        # open(DATA_FILE, "w") opens the JSON file in write mode.
        # Write mode creates the file if needed and replaces old contents with
        # the updated session list.

        json.dump(sessions, file, indent=4)
        # json.dump converts Python data into JSON text.
        # indent=4 makes the JSON file easier to read.


def calculate_subject_statistics(sessions):
    """
    Calculate attempted questions, correct answers, and accuracy for each subject.
    """
    # This function is backend logic because it works with data, not the page.
    # It receives the sessions list and returns a dictionary of subject totals.

    subject_totals = {}
    # This dictionary will store one entry per subject.
    # Example:
    # {
    #     "Math": {"questions_attempted": 20, "correct_answers": 15}
    # }

    for session in sessions:
        # A for loop repeats once for each session dictionary in the list.
        # During each repeat, the session variable stores one study session.

        subject = session["subject"]
        # This gets the subject name from the current session dictionary.

        if subject not in subject_totals:
            # If this subject has not appeared before, create its starting
            # totals.

            subject_totals[subject] = {
                "questions_attempted": 0,
                "correct_answers": 0,
            }
            # Both totals begin at 0 before we add the session's numbers.

        subject_totals[subject]["questions_attempted"] += session["questions_attempted"]
        # This adds attempted questions to the running total for this subject.

        subject_totals[subject]["correct_answers"] += session["correct_answers"]
        # This adds correct answers to the running total for this subject.

    return subject_totals
    # Returning the dictionary lets another function display these statistics.


def calculate_overall_statistics(sessions):
    """
    Calculate the overall totals used by the statistics page.
    """
    # This helper function keeps the statistics page clean and readable.
    # It uses the same counting logic as the terminal version, but returns the
    # values instead of printing them.

    total_sessions = len(sessions)
    # len counts how many session dictionaries are in the list.

    total_questions = 0
    # This variable will store the total number of attempted questions.

    total_correct = 0
    # This variable will store the total number of correct answers.

    for session in sessions:
        # This loop visits every saved session.

        total_questions += session["questions_attempted"]
        # Add this session's attempted questions to the total.

        total_correct += session["correct_answers"]
        # Add this session's correct answers to the total.

    if total_questions == 0:
        # This prevents division by zero.

        overall_accuracy = 0
        # If no questions were attempted, accuracy is shown as 0 percent.

    else:
        # This runs when there is at least one attempted question.

        overall_accuracy = (total_correct / total_questions) * 100
        # This is the same accuracy formula from the terminal app.

    return total_sessions, total_questions, total_correct, overall_accuracy
    # Returning multiple values lets Streamlit display them with st.metric.


def show_log_session_page(sessions):
    """
    Show the page where the user logs a new study session.
    """
    # In the terminal app, this section used input().
    # In Streamlit, each input() is replaced with a widget that appears in the
    # browser.

    st.subheader("Log a Study Session")
    # st.subheader creates a clear section heading under the main app title.

    with st.form("study_session_form"):
        # st.form groups several widgets together.
        # The app waits until the user clicks the submit button before saving
        # the data. This feels similar to filling out a normal web form.

        subject = st.text_input("Subject")
        # st.text_input replaces input("Subject: ").
        # It shows a text box in the browser and stores the typed text in the
        # subject variable.

        chapter = st.text_input("Chapter")
        # This is another text box.
        # The chapter variable stores the text typed by the user.

        question_column, correct_column = st.columns(2)
        # st.columns creates two side-by-side layout areas.
        # This replaces one long vertical list with a more balanced form layout.
        # Each column variable works like a small container for widgets.

        with question_column:
            # The with statement tells Streamlit to place this widget in the
            # left column.

            questions_attempted = st.number_input(
                "Questions attempted",
                min_value=0,
                step=1,
            )
            # st.number_input replaces asking for a number with input().
            # min_value=0 prevents negative numbers.
            # step=1 makes the control move in whole numbers.

        with correct_column:
            # This with block places the next widget in the right column.

            correct_answers = st.number_input(
                "Correct answers",
                min_value=0,
                step=1,
            )
            # This number input also prevents negative numbers.
            # We do not use max_value=questions_attempted here because this
            # widget is inside a Streamlit form. Form values update only after
            # the submit button is clicked, so a live max_value can become
            # confusing. Instead, we check the values after form submission.

        session_date = st.date_input("Date", value=date.today())
        # st.date_input replaces manually typing a date with input().
        # It shows a calendar/date widget and gives us a date object.

        submitted = st.form_submit_button("Log session")
        # A Streamlit form needs a submit button.
        # The submitted variable becomes True only after the user clicks it.

    if submitted:
        # This block runs only when the user clicks "Log session".
        # Without this check, the app would save data every time Streamlit
        # reruns the script.

        if subject.strip() == "" or chapter.strip() == "":
            # This simple validation checks that the user typed both text fields.

            st.error("Please enter both a subject and a chapter.")
            # st.error displays a red error message in the web app.

        elif correct_answers > questions_attempted:
            # This validation replaces max_value=questions_attempted.
            # It prevents impossible data, such as 12 correct answers out of
            # 10 attempted questions, after the form is submitted.

            st.error("Correct answers cannot be greater than questions attempted.")
            # This message clearly explains what the user needs to fix.

        else:
            # This block runs when the form data is valid.

            session = {
                "subject": subject.strip(),
                "chapter": chapter.strip(),
                "questions_attempted": int(questions_attempted),
                "correct_answers": int(correct_answers),
                "date": session_date.strftime("%Y-%m-%d"),
            }
            # This dictionary has the same keys as the terminal app.
            # int() is used because Streamlit number widgets return number
            # values, and we want clean integers in the JSON file.
            # strftime converts the date object into text for JSON storage.

            sessions.append(session)
            # append adds the new session dictionary to the list.

            save_sessions(sessions)
            # Saving immediately keeps the data persistent.

            st.success("Study session logged successfully.")
            # st.success displays a green success message in the web app.


def show_all_sessions_page(sessions):
    """
    Show all saved study sessions.
    """
    # In the terminal app, this page used print().
    # In Streamlit, we use page display functions such as st.write and st.table.

    st.subheader("All Study Sessions")
    # st.subheader creates a section heading below the main page title.

    if len(sessions) == 0:
        # If the list is empty, there is nothing to display.

        st.info("No study sessions have been logged yet.")
        # st.info displays a friendly information message.

    else:
        # This runs when at least one study session exists.

        st.table(sessions)
        # st.table displays the list of dictionaries as a table.
        # Each dictionary key becomes a column, such as subject or date.


def show_statistics_page(sessions):
    """
    Show study statistics using metrics and a bar chart.
    """
    # The terminal version printed statistics as plain text.
    # This Streamlit version uses st.metric for key numbers and st.bar_chart for
    # subject-wise accuracy.

    st.subheader("Study Statistics")
    # st.subheader creates a section heading below the main page title.

    if len(sessions) == 0:
        # If there are no sessions, we cannot show meaningful statistics.

        st.info("No study sessions have been logged yet.")
        # This message tells the user why no stats are visible.

        return
        # return exits this function early.

    total_sessions, total_questions, total_correct, overall_accuracy = calculate_overall_statistics(sessions)
    # This line calls the statistics helper and stores each returned value in a
    # separate variable.

    col1, col2, col3, col4 = st.columns(4)
    # st.columns creates four side-by-side layout areas.
    # Each column variable can display one metric.

    col1.metric("Sessions", total_sessions)
    # st.metric displays an important number in a clean visual style.

    col2.metric("Questions", total_questions)
    # This metric shows total attempted questions.

    col3.metric("Correct", total_correct)
    # This metric shows total correct answers.

    col4.metric("Accuracy", f"{overall_accuracy:.2f}%")
    # This metric shows the overall accuracy percentage formatted to 2 decimals.

    subject_totals = calculate_subject_statistics(sessions)
    # This gets attempted and correct totals for each subject.

    chart_data = []
    # chart_data will become a list of dictionaries.
    # Streamlit can use this list to create a simple bar chart.

    for subject, totals in subject_totals.items():
        # Loop through each subject and its totals.

        attempted = totals["questions_attempted"]
        # Store the attempted questions for this subject.

        correct = totals["correct_answers"]
        # Store the correct answers for this subject.

        if attempted == 0:
            # Prevent division by zero.

            accuracy = 0
            # Accuracy is 0 when no questions were attempted.

        else:
            # Calculate accuracy normally when attempted questions exist.

            accuracy = (correct / attempted) * 100
            # This gives the subject accuracy percentage.

        chart_data.append(
            {
                "Subject": subject,
                "Accuracy": accuracy,
            }
        )
        # append adds one row of chart data.
        # Each row stores a subject name and its accuracy percentage.

    st.subheader("Subject-wise Accuracy")
    # This subheading labels the chart.

    st.bar_chart(chart_data, x="Subject", y="Accuracy")
    # st.bar_chart draws a bar chart from the chart_data list.
    # x="Subject" means subject names appear along the bottom.
    # y="Accuracy" means bar height is based on the accuracy percentage.


def main():
    """
    Run the Streamlit Study Tracker app.
    """
    # Streamlit apps do not usually use a while loop.
    # Instead, Streamlit reruns the script whenever the user interacts with a
    # widget. The selected sidebar page decides what gets shown.

    st.set_page_config(page_title="Study Tracker")
    # This sets basic browser tab information for the app.

    st.title("Study Tracker")
    # st.title displays the main app title.
    # It is the highest-level heading on the page.

    st.markdown(
        """
        <style>
        div[data-testid="stHorizontalBlock"] {
            flex-wrap: nowrap;
        }

        div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {
            min-width: 0;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    # st.markdown can display text, but with unsafe_allow_html=True it can also
    # add a small amount of HTML or CSS.
    # This CSS keeps Streamlit column layouts side-by-side in narrower browser
    # windows. The app still uses st.columns for layout; the CSS only tells the
    # browser not to wrap those columns onto separate lines too early.

    sessions = load_sessions()
    # Load saved JSON data each time the app script runs.
    # This keeps the page synced with the file.

    page = st.sidebar.radio(
        "Navigation",
        [
            "📚 Log Session",
            "🗂️ View Sessions",
            "📊 View Statistics",
        ],
    )
    # st.sidebar.radio replaces the terminal menu.
    # The user chooses one page from the sidebar instead of typing 1, 2, or 3.
    # The selected option is stored in the page variable.

    if page == "📚 Log Session":
        # This branch displays the logging form.

        show_log_session_page(sessions)
        # Call the function that contains the Streamlit form widgets.

    elif page == "🗂️ View Sessions":
        # This branch displays the saved sessions table.

        show_all_sessions_page(sessions)
        # Call the function that displays all sessions.

    elif page == "📊 View Statistics":
        # This branch displays statistics and charts.

        show_statistics_page(sessions)
        # Call the function that displays Streamlit metrics and a bar chart.


main()
# Streamlit runs this file from top to bottom.
# Calling main() starts the app layout.
# Unlike the terminal app, we do not need if __name__ == "__main__" here,
# because this file is meant to be run with streamlit run.


# Code Walkthrough
# ----------------
# 1. The app imports json for storage, date for the date widget, and streamlit
#    for the web interface.
#
# 2. load_sessions and save_sessions keep the same JSON backend idea as the
#    terminal app. Data is stored in study_sessions.json.
#
# 3. calculate_subject_statistics and calculate_overall_statistics work with
#    Python lists and dictionaries to prepare totals and percentages.
#
# 4. show_log_session_page replaces input() with Streamlit widgets:
#    st.text_input for text, st.number_input for numbers, st.date_input for
#    dates, and st.form_submit_button for saving the form.
#
# 5. show_all_sessions_page replaces print() output with st.table, which shows
#    saved dictionaries as a web table.
#
# 6. show_statistics_page replaces printed statistics with st.metric cards and
#    st.bar_chart for subject-wise accuracy.
#
# 7. main loads the JSON data, creates sidebar navigation, and shows the page
#    selected by the user.
#
# 8. To run the web app, open a terminal in the folder containing this file and
#    use:
#
#    streamlit run study_tracker_streamlit.py
#
# 9. The important difference is that a terminal program waits inside input(),
#    while a Streamlit app displays widgets in the browser and reruns the script
#    when the user interacts with them.
