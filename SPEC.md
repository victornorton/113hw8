This is a python command line quiz app with a local login system. When run, the program should display a greeting message, and prompt the user to either sign in or "create an account" by entering a new username and passwork. When signed in, the program should ask the user if they would like to take a quiz, view statistics, log out, or quit. If 'view statistics' is selected, the program should display the total number of questions correctly answered and percent of correct answers across all quizzed taken so far. It should also show a leaderboard with the top 5 users based on total correct answers. If 'take quiz' is selected the program should sample 10 random questions from the question bank and display them to the user, telling them if they are correct right after they provide an answer. Before moving on to the next question, the user should be given a chance to rate how much they liked the question out of 10 points, question categories that a user gives poor overall ratings should eventually be chosen less often by the program. After all 10 questions are answered a summary of the statistics for that quiz will be displayed with a prompt to continue. When continue is selected the user will be returned to original state with the quiz, statistics, logout, and quit options. If 'log out' is selected the user should return to the sign-in/sign-up page, and if quit is selected the program should end.

The question bank should be a json file with the following format:

{
  "questions": [
    {
      "question": "What country contains the epicenter of the lagerst earthquake ever reliably recorded?",
      "type": "multiple_choice",
      "options": ["china", "united states", "japan", "chile", "indonesia"],
      "answer": "chile",
      "category": "Earthquakes",
      "difficulty": "4"
    },
    {
      "question": "All tornadoes spin in the same direction.",
      "type": "true_false",
      "answer": "false",
      "category": "Tornadoes",
      "difficulty": "2"
    },
    {
      "question": "In 2005, what hurricane devastated New Orleans? (Capitalize Name)",
      "type": "short_answer",
      "answer": "Katrina",
      "category": "Hurricanes",
      "difficulty": "1"
    },
    {
      "question": "Type of fault is most likely to create a tsunami?",
      "type": "multiple_choice",
      "options": ["strike-slip", "megathrust", "intraplate", "transform"],
      "answer": "megathrust",
      "category": "Tsunamis",
      "difficulty": "3"
    },
    {
      "question": "Taking shelter under a highway overpass can proctect you from a tornado.",
      "type": "true_false",
      "answer": "false",
      "category": "Tornadoes",
      "difficulty": "2"
    }
  ]
}

The questions should all be themed around the 4 natural disaster categories seen here, earthquake, tsunami, hurricane, and tornado. 

The following files should exist in this project:
- main.py, which starts the app when run
- questions.json, which contains all the questions in human readable form. There should always be at least 32 questions, at least 8 per category, and at least two per difficulty per category. 
-  statistics, a file containing performance statistics for each user in a relatively secure, non human readable format. Usernames can be potentially be seen here but nothing else should be easily gained from reading the file
- login, a secure file that implements the local login system. Passwords should not be easily revealed. 

If the user enters a blank or invalid quiz response, the program should tell them to try again, and should humorously scold the user and  mark the question as incorrect if three invalid responses are given. If the questions.json file doesn't have enough questions then running the problem should result in an error message that tells the user that more questions are needed. If any of the earlier described files are missing the program should display a message stating which files it was unable to access before closing without crashing catastrophically. If a user tries to create an account with a preexisting username then the program should tell them that the name has already been used and to try again. 


As a bonus feature, if a user is doing well on a quiz they should start to face more difficult questions, and if they are doing poorly they should start to see easier questions. If the user is doing very well this effect should begin to override the user's responses to what questions they liked. If the user is doing very poorly, the user's preferences should be weighted even more. The difficulty of the questions should not be explicitly displayed by the program, but the system should subtlely congratulate the user while displaying the correct answer message, whenever one of the harder questions is answered correctly. The users should not be told that they are getting easier questions when they are struggling on a quiz.

As another bonus feature, though it should not be referenced by the program, if a user submits "I give up." at any point while signed in, the program should respond with "Are you sure? Everything will be destroyed.", and if the user responds with "Yes." ,their account and all their statistics should be deleted. They should no longer appear on the leaderboard. Trying to make an account with a username that had been used before but was since deleted should work, but should display a special message that says, "You cannot recover what has been lost." before taking the user to the main page. 


None of this should involve a backend, html, css, a gui, or any APIs. 

Before accepting that the project is complete the following behaviors must be confirmed:

 - Running the app with an empty or incomplete question bank returns helpful error message asking for more questions and closes app. 
 - Trying to create a new account with a preexisting username does results in a message saying that that name is already taken.
 - Entering "I give up." at any point while signed in has the described effect
 - Taking a quiz runs smoothly and it is apparent that the user's input affects the subsequent questions, and that the users performance also affects the difficulty. 
 - Viewing statistics shows user their the total number of correct answers, correct answer percentage, and the leaderboard
 - logging out and quitting work as expected
 - no sensitive information, ie passwords, statistics, etc, can be found by looking at the statistics and login files. 