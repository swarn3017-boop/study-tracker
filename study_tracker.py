"""
Study Tracker

This is a beginner-friendly terminal application for recording study sessions.
It saves the data in a JSON file so the sessions are still available after the
program closes.
"""
# This opening docstring gives the file a simple title and description.
# A docstring is a string placed at the top of a file, function, or class.
# Python ignores it while running the logic, but humans can read it as helpful
# documentation. It is needed here so a beginner immediately understands the
# purpose of this program.

import json
# The json module is built into Python.
# We use it to convert Python data, such as lists and dictionaries, into JSON
# text that can be saved in a file. We also use it to read JSON text back into
# Python data when the program starts again.

from datetime import datetime
# The datetime module is built into Python.
# We import datetime so we can check whether a date typed by the user is in the
# correct format. This program uses dates like 2026-06-06, which is the
# year-month-day format.


DATA_FILE = "study_sessions.json"
# DATA_FILE stores the name of the JSON file that will hold the study sessions.
# The variable is written in capital letters because it is a constant, meaning
# we do not plan to change it while the program runs. Constants are not a
# special Python feature, but capital letters are a common naming habit.


def load_sessions():
    """
    Load all saved study sessions from the JSON file.
    If the file does not exist yet, return an empty list.
    """
    # This function is responsible for getting saved data from the JSON file.
    # A function groups related instructions under one name, so we can reuse
    # those instructions without copying code. The function returns a list
    # because the program stores many study sessions, and a list is a good
    # beginner-friendly way to keep multiple items in order.

    try:
        # try tells Python to attempt the indented code below.
        # It is needed because opening a file can fail if the file has not been
        # created yet. Instead of crashing, the program can handle that problem
        # calmly with except.

        with open(DATA_FILE, "r") as file:
            # open(DATA_FILE, "r") opens the JSON file in read mode.
            # The variable file represents the opened file while we are inside
            # this with block. The with statement is useful because it closes
            # the file automatically when we are done reading it.

            sessions = json.load(file)
            # json.load(file) reads JSON text from the file and converts it into
            # Python data. In this program, that data should be a list of
            # dictionaries. Each dictionary represents one study session.

            return sessions
            # return sends the loaded list back to the part of the program that
            # called load_sessions(). Returning data is how functions give
            # results to the rest of the program.

    except FileNotFoundError:
        # FileNotFoundError happens when the JSON file does not exist.
        # This is normal the first time the program runs, so we handle it by
        # starting with an empty list instead of showing an error.

        return []
        # [] is an empty list. It means there are currently no saved study
        # sessions. Later, new session dictionaries will be added to this list.

    except json.JSONDecodeError:
        # JSONDecodeError happens if the file exists but does not contain valid
        # JSON. This might happen if the file was edited by mistake.
        # For a beginner app, we keep the program simple and start fresh.

        print("The data file could not be read, so the app will start empty.")
        # print displays a message in the terminal. This message tells the user
        # what happened instead of silently hiding the issue.

        return []
        # Returning an empty list allows the program to keep running. The
        # variable that receives this result will still have the same type it
        # expects: a list of sessions.


def save_sessions(sessions):
    """
    Save all study sessions to the JSON file.
    """
    # This function writes the current sessions list into the JSON file.
    # The parameter sessions is a variable that receives the list passed into
    # the function. Parameters let functions work with data from outside the
    # function.

    with open(DATA_FILE, "w") as file:
        # open(DATA_FILE, "w") opens the file in write mode.
        # Write mode creates the file if it does not exist. If it already
        # exists, write mode replaces the old contents with the new contents.

        json.dump(sessions, file, indent=4)
        # json.dump converts the Python list into JSON text and writes it to
        # the file. The indent=4 part makes the JSON file easier for humans to
        # read by adding spaces and line breaks.


def get_positive_integer(message):
    """
    Ask the user for a whole number that is zero or greater.
    Keep asking until the user types valid input.
    """
    # This helper function prevents repeated input-checking code.
    # The message parameter stores the text we want to show the user, such as
    # "Questions attempted: ". The function returns an integer when the input is
    # valid.

    while True:
        # while True creates a loop that keeps running until we use return.
        # This is useful for input validation because we do not know how many
        # tries the user will need.

        user_input = input(message)
        # input displays the message and waits for the user to type something.
        # Python always stores input as a string first, so user_input is text
        # even if the user typed digits.

        if user_input.isdigit():
            # isdigit() checks whether every character in the string is a digit.
            # This helps us safely convert the input to an integer without
            # causing an error.

            number = int(user_input)
            # int(user_input) converts the string into an integer.
            # The variable number is easier to use for math than the original
            # text stored in user_input.

            return number
            # return sends the valid integer back to the caller and stops the
            # loop because the function ends when it returns.

        print("Please enter a whole number that is 0 or greater.")
        # This line runs only when the input was not made of digits.
        # It explains the problem and then the while loop starts again.


def get_date():
    """
    Ask the user for a date in YYYY-MM-DD format.
    If the user presses Enter, use today's date.
    """
    # This function collects and checks the date for a study session.
    # It uses a loop because the user might type the date in the wrong format.

    while True:
        # The loop keeps asking for a date until the user gives a valid one.
        # This is another example of input validation, which means checking
        # user input before using it in the program.

        date_text = input("Date (YYYY-MM-DD, press Enter for today): ")
        # date_text stores whatever the user typed.
        # It is a string because input always gives us text.

        if date_text == "":
            # An empty string means the user pressed Enter without typing a date.
            # This gives the app a convenient shortcut for today's date.

            today = datetime.now().strftime("%Y-%m-%d")
            # datetime.now() gets the current date and time.
            # strftime("%Y-%m-%d") formats it as text like 2026-06-06.
            # The variable today stores that formatted date string.

            return today
            # Returning today lets the rest of the program store the date in
            # the same format as dates typed by the user.

        try:
            # This try block checks whether the typed date follows the required
            # format. Date checking can fail, so try lets us catch the problem.

            datetime.strptime(date_text, "%Y-%m-%d")
            # strptime tries to read date_text using the year-month-day format.
            # If the format is wrong, Python raises a ValueError.

            return date_text
            # If strptime did not fail, the date format is valid, so we return
            # the original text typed by the user.

        except ValueError:
            # ValueError happens when the date text does not match YYYY-MM-DD
            # or when the date is impossible, such as 2026-99-99.

            print("Please enter a valid date in YYYY-MM-DD format.")
            # This message tells the user exactly what kind of input the
            # program expects. After this, the loop asks again.


def log_study_session(sessions):
    """
    Log one new study session to the sessions list and save the updated list.
    """
    # This function handles menu option 1.
    # The sessions parameter receives the current list of saved sessions.
    # The function adds one new dictionary to that list.

    print("\nLog a Study Session")
    # \n creates a blank line before the heading.
    # This makes the terminal output easier to read.

    subject = input("Subject: ").strip()
    # The subject variable stores the subject typed by the user.
    # strip() removes extra spaces from the beginning and end of the text.

    chapter = input("Chapter: ").strip()
    # The chapter variable stores the chapter typed by the user.
    # This is also text, so a string is the correct data type.

    questions_attempted = get_positive_integer("Questions attempted: ")
    # This calls our helper function to get a valid whole number.
    # The result is stored in questions_attempted, which will be used for
    # statistics later.

    while True:
        # This loop asks for correct answers until the number makes sense.
        # Correct answers should not be greater than questions attempted.

        correct_answers = get_positive_integer("Correct answers: ")
        # correct_answers stores another whole number from the user.
        # It uses the same helper function because the validation rules are
        # almost the same.

        if correct_answers <= questions_attempted:
            # This condition checks the relationship between two variables.
            # It prevents impossible data, such as 12 correct answers out of
            # 10 attempted questions.

            break
            # break stops the nearest loop. Here it stops asking for correct
            # answers because the value is valid.

        print("Correct answers cannot be greater than questions attempted.")
        # This message appears only when the user enters an impossible value.
        # The loop then repeats and asks again.

    date = get_date()
    # This calls the date helper function.
    # The date variable stores either the user's valid date or today's date.

    session = {
        "subject": subject,
        "chapter": chapter,
        "questions_attempted": questions_attempted,
        "correct_answers": correct_answers,
        "date": date,
    }
    # A dictionary stores related pieces of information using key-value pairs.
    # The keys, such as "subject" and "date", describe what each value means.
    # The values come from variables collected from the user.

    sessions.append(session)
    # append adds the new session dictionary to the end of the sessions list.
    # The list now contains one more study session than before.

    save_sessions(sessions)
    # After changing the list, we save it immediately.
    # This is needed so the new session remains available after the program is
    # closed.

    print("Study session added successfully.")
    # This message confirms that the action is complete.
    # Clear feedback helps users know the program worked.


def view_all_sessions(sessions):
    """
    Display every saved study session.
    """
    # This function handles menu option 2.
    # It reads from the sessions list and prints the details in a friendly
    # format. It does not change the list.

    print("\nAll Study Sessions")
    # This heading separates the session list from previous terminal output.

    if len(sessions) == 0:
        # len(sessions) counts how many items are in the list.
        # If the count is 0, there are no sessions to display.

        print("No study sessions have been added yet.")
        # This message is clearer than showing a blank screen.

        return
        # return exits the function early because there is nothing else to
        # display.

    for index, session in enumerate(sessions, start=1):
        # A for loop repeats code for every item in a collection.
        # enumerate gives us both a counter and the session dictionary.
        # start=1 makes the counter begin at 1, which is friendlier for users.

        print(f"\nSession {index}")
        # An f-string lets us place a variable directly inside a string.
        # Here, index is displayed as the session number.

        print(f"Subject: {session['subject']}")
        # session['subject'] gets the value stored under the "subject" key in
        # the current session dictionary.

        print(f"Chapter: {session['chapter']}")
        # This line prints the chapter value from the current session.
        # Dictionary keys make it clear which piece of data we are using.

        print(f"Questions attempted: {session['questions_attempted']}")
        # This displays how many questions were attempted in this session.
        # The value is an integer, but f-strings can display it as text.

        print(f"Correct answers: {session['correct_answers']}")
        # This displays how many answers were correct in this session.

        print(f"Date: {session['date']}")
        # This displays the saved date for the session.


def calculate_subject_statistics(sessions):
    """
    Calculate attempted questions, correct answers, and accuracy for each subject.
    """
    # This function builds subject-wise statistics.
    # It returns a dictionary where each subject has its own totals.

    subject_totals = {}
    # subject_totals starts as an empty dictionary.
    # Each key will be a subject name. Each value will be another dictionary
    # containing totals for that subject.

    for session in sessions:
        # This loop visits each saved study session one at a time.
        # The session variable holds one dictionary during each loop cycle.

        subject = session["subject"]
        # This gets the subject name from the current session.
        # We store it in a variable so the next lines are easier to read.

        if subject not in subject_totals:
            # This checks whether we have already created totals for this
            # subject. If the subject is not present yet, we need to set it up.

            subject_totals[subject] = {
                "questions_attempted": 0,
                "correct_answers": 0,
            }
            # This creates a nested dictionary for one subject.
            # The totals start at 0 because no values have been added yet for
            # this subject.

        subject_totals[subject]["questions_attempted"] += session["questions_attempted"]
        # += adds the session's attempted questions to the running subject total.
        # This is the same as writing:
        # subject_totals[subject]["questions_attempted"] =
        # subject_totals[subject]["questions_attempted"] + session["questions_attempted"]

        subject_totals[subject]["correct_answers"] += session["correct_answers"]
        # This adds the session's correct answers to the running subject total.
        # The nested dictionary lets each subject keep its own separate numbers.

    return subject_totals
    # The completed dictionary is returned to the statistics display function.
    # Returning it keeps the calculation separate from printing the results.


def view_statistics(sessions):
    """
    Display overall statistics and subject-wise accuracy.
    """
    # This function handles menu option 3.
    # It calculates totals from the sessions list and prints useful study
    # information for the user.

    print("\nStudy Statistics")
    # This heading tells the user they are viewing statistics.

    total_sessions = len(sessions)
    # len(sessions) gives the total number of study session dictionaries in the
    # list. The result is stored in total_sessions.

    if total_sessions == 0:
        # If there are no sessions, statistics such as accuracy cannot be
        # calculated in a meaningful way.

        print("No study sessions have been added yet.")
        # This message explains why no statistics are shown.

        return
        # return exits the function early to avoid dividing by zero later.

    total_questions = 0
    # total_questions will store the sum of all attempted questions.
    # We begin at 0 because no sessions have been counted yet.

    total_correct = 0
    # total_correct will store the sum of all correct answers.
    # This is another running total that starts at 0.

    for session in sessions:
        # This loop goes through every saved session.
        # Each loop cycle adds that session's numbers to the overall totals.

        total_questions += session["questions_attempted"]
        # This adds the current session's attempted questions to total_questions.
        # The variable grows as the loop visits more sessions.

        total_correct += session["correct_answers"]
        # This adds the current session's correct answers to total_correct.
        # Both totals will be used to calculate the overall accuracy.

    if total_questions == 0:
        # This condition protects the program from division by zero.
        # Accuracy requires dividing by total questions, so if the total is 0,
        # we choose 0 percent accuracy.

        overall_accuracy = 0
        # overall_accuracy stores the final percentage for all sessions.
        # We use 0 here because no questions were attempted.

    else:
        # The else block runs when total_questions is not 0.
        # That means it is safe to divide by total_questions.

        overall_accuracy = (total_correct / total_questions) * 100
        # This formula calculates the percentage of correct answers.
        # Division creates a decimal, and multiplying by 100 turns it into a
        # percentage.

    print(f"Total study sessions: {total_sessions}")
    # This line prints how many sessions have been saved.

    print(f"Total questions attempted: {total_questions}")
    # This line prints the total number of attempted questions.

    print(f"Total correct answers: {total_correct}")
    # This line prints the total number of correct answers.

    print(f"Overall accuracy: {overall_accuracy:.2f}%")
    # :.2f formats the number to 2 decimal places.
    # This makes percentages look clean, such as 87.50%.

    subject_totals = calculate_subject_statistics(sessions)
    # This calls the helper function that groups totals by subject.
    # The returned dictionary is stored in subject_totals.

    print("\nSubject-wise Accuracy")
    # This heading separates subject statistics from the overall statistics.

    for subject, totals in subject_totals.items():
        # .items() lets us loop through both keys and values in a dictionary.
        # subject stores the subject name. totals stores that subject's nested
        # dictionary of attempted and correct answers.

        attempted = totals["questions_attempted"]
        # attempted stores the total attempted questions for this subject.
        # A shorter variable name makes the accuracy formula easier to read.

        correct = totals["correct_answers"]
        # correct stores the total correct answers for this subject.

        if attempted == 0:
            # This check avoids division by zero for a subject with no attempted
            # questions.

            accuracy = 0
            # If no questions were attempted, the subject accuracy is shown as
            # 0 percent.

        else:
            # This block runs when the subject has at least one attempted
            # question, so division is safe.

            accuracy = (correct / attempted) * 100
            # This calculates subject accuracy using the same percentage formula
            # as the overall accuracy.

        print(f"{subject}: {accuracy:.2f}% ({correct}/{attempted})")
        # This displays the subject name, accuracy percentage, correct answers,
        # and attempted questions in one readable line.


def show_menu():
    """
    Display the main menu choices.
    """
    # This function prints the menu.
    # Keeping it in its own function makes the main program loop easier to read.

    print("\nStudy Tracker")
    # This prints the program title each time the menu appears.

    print("1. Log a study session")
    # This is the first menu option. The user can type 1 to log data.

    print("2. View all study sessions")
    # This is the second menu option. The user can type 2 to view saved data.

    print("3. View statistics")
    # This is the third menu option. The user can type 3 to see totals and
    # accuracy percentages.

    print("4. Exit")
    # This is the fourth menu option. The user can type 4 to stop the program.


def main():
    """
    Run the Study Tracker program.
    """
    # main is the central function of the application.
    # It loads saved data, shows the menu, reads the user's choice, and calls
    # the correct function for that choice.

    sessions = load_sessions()
    # This loads existing sessions from the JSON file.
    # The sessions variable is a list that will be shared with the menu actions.

    while True:
        # This loop keeps the program running until the user chooses Exit.
        # A menu program usually needs a loop because the user may want to do
        # several actions before leaving.

        show_menu()
        # This displays the menu options before asking for a choice.

        choice = input("Choose an option: ")
        # choice stores the menu option typed by the user.
        # It is stored as a string because input always returns text.

        if choice == "1":
            # This condition checks whether the user chose option 1.
            # We compare to "1" as text because choice is a string.

            log_study_session(sessions)
            # This calls the function that logs and saves a new study session.
            # The sessions list is passed in so the function can update it.

        elif choice == "2":
            # elif means "else if". It checks another condition only if the
            # previous if condition was false.

            view_all_sessions(sessions)
            # This calls the function that displays every saved session.

        elif choice == "3":
            # This branch runs when the user chooses the statistics option.

            view_statistics(sessions)
            # This calls the function that calculates and prints statistics.

        elif choice == "4":
            # This branch runs when the user wants to exit the program.

            print("Goodbye. Keep studying!")
            # This friendly message confirms that the program is closing.

            break
            # break exits the while loop. Since the loop is the last part of
            # main, the program ends after this.

        else:
            # else runs when none of the previous choices matched.
            # This catches invalid menu options.

            print("Invalid choice. Please enter 1, 2, 3, or 4.")
            # This message tells the user what valid choices are.
            # After this, the loop repeats and shows the menu again.


if __name__ == "__main__":
    # This special condition checks whether this file is being run directly.
    # __name__ is a built-in Python variable. When the file is run directly,
    # Python sets __name__ to "__main__".

    main()
    # This starts the program by calling the main function.
    # Keeping the startup here is a common Python pattern because it makes the
    # file easier to reuse or import later.


# Code Walkthrough
# ----------------
# 1. Python first reads the import statements. The program imports json for file
#    storage and datetime for date validation.
#
# 2. The DATA_FILE constant stores the name of the JSON file where study
#    sessions will be saved.
#
# 3. The load_sessions function tries to read existing sessions from the JSON
#    file. If the file does not exist, it returns an empty list so the program
#    can start normally.
#
# 4. The save_sessions function writes the full sessions list into the JSON
#    file. This is what makes the data persist after the program closes.
#
# 5. The get_positive_integer function asks for a whole number and keeps asking
#    until the user types valid input. This prevents text or negative numbers
#    from being used in calculations.
#
# 6. The get_date function asks for a date. The user can type a date in
#    YYYY-MM-DD format or press Enter to use today's date.
#
# 7. The log_study_session function collects the subject, chapter, questions
#    attempted, correct answers, and date. It stores those values in a
#    dictionary, adds that dictionary to the sessions list, and saves the list.
#
# 8. The view_all_sessions function loops through the sessions list and prints
#    each saved session in a readable format.
#
# 9. The calculate_subject_statistics function groups attempted questions and
#    correct answers by subject. This makes subject-wise accuracy possible.
#
# 10. The view_statistics function calculates total sessions, total questions,
#     total correct answers, overall accuracy, and subject-wise accuracy.
#
# 11. The show_menu function prints the four menu options.
#
# 12. The main function controls the whole program. It loads the saved sessions,
#     repeatedly shows the menu, reads the user's choice, and calls the correct
#     function.
#
# 13. The if __name__ == "__main__" block starts the program by calling main
#     only when this file is run directly from the terminal.
#
# Overall, the program flow is:
# Start the app -> load saved JSON data -> show the menu -> wait for the user's
# choice -> run the chosen action -> save data when needed -> return to the menu
# until the user chooses Exit.
