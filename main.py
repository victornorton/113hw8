import json
import os
import random
import sys
import traceback
from login import LoginManager
from statistics import StatisticsManager

REQUIRED_FILES = ['questions.json', 'login.py', 'statistics.py']

CATEGORIES = ['Earthquakes', 'Tsunamis', 'Hurricanes', 'Tornadoes']


def safe_input(prompt):
    try:
        return input(prompt)
    except EOFError:
        print('\nInput ended unexpectedly. Exiting.')
        sys.exit(0)



def check_give_up(username, inp, login_manager, stats_manager):
    if inp.strip() == 'I give up.':
        confirm = safe_input('Are you sure? Everything will be destroyed.\n')
        if confirm.strip() == 'Yes.':
            login_manager.delete_user(username)
            stats_manager.delete_user(username)
            print('Your account and all statistics have been deleted. Cannot recover.')
            return True
    return False


def print_missing_files(files):
    for file in files:
        print(f'Unable to access required file: {file}')


def load_questions():
    if not os.path.exists('questions.json'):
        raise FileNotFoundError('questions.json missing')
    with open('questions.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    if 'questions' not in data or not isinstance(data['questions'], list):
        raise ValueError('questions.json malformed')
    if len(data['questions']) < 32:
        raise ValueError('Not enough questions; need 32 or more')
    # count categories/difficulties
    cat_counts = {cat: 0 for cat in CATEGORIES}
    diff_counts = {cat: {str(d): 0 for d in range(1, 5)} for cat in CATEGORIES}
    for q in data['questions']:
        cat = q.get('category')
        diff = q.get('difficulty')
        if cat in cat_counts:
            cat_counts[cat] += 1
            if diff in diff_counts[cat]:
                diff_counts[cat][diff] += 1
    for cat, count in cat_counts.items():
        if count < 8:
            raise ValueError('Not enough questions in category: ' + cat)
        for d, val in diff_counts[cat].items():
            if val < 2:
                raise ValueError(f'Not enough difficulty {d} questions in category {cat}')
    return data['questions']


def choose_question(remaining, username, stats_manager, session_score, questions_answered):
    weights = []
    for q in remaining:
        cat = q.get('category', '')
        pref = stats_manager.get_category_preference(username, cat)
        cat_weight = max(0.1, 0.2 + pref / 10)
        diff = int(q.get('difficulty', '2'))
        # Performance based difficulty bias
        if questions_answered > 0:
            ratio = session_score / questions_answered
        else:
            ratio = 0.5
        if ratio >= 0.8:
            diff_weight = 1 + (diff / 4)
        elif ratio <= 0.35:
            diff_weight = 1 + ((5 - diff) / 4)
        else:
            diff_weight = 1.0
        weights.append(cat_weight * diff_weight)
    total = sum(weights)
    if total <= 0:
        return random.choice(remaining)
    pick = random.uniform(0, total)
    upto = 0
    for idx, q in enumerate(remaining):
        upto += weights[idx]
        if upto >= pick:
            return q
    return remaining[-1]


def parse_answer(q, answer):
    qtype = q.get('type')
    correct = q.get('answer')
    if qtype == 'multiple_choice':
        opts = q.get('options', [])
        ans_lower = answer.strip().lower()
        if ans_lower.isdigit():
            idx = int(ans_lower) - 1
            if 0 <= idx < len(opts):
                return opts[idx].strip().lower() == str(correct).strip().lower(), True
        if ans_lower in [o.strip().lower() for o in opts]:
            return ans_lower == str(correct).strip().lower(), True
        return False, False
    elif qtype == 'true_false':
        ans_lower = answer.strip().lower()
        if ans_lower in ['true', 't', 'false', 'f']:
            normalized = 'true' if ans_lower in ['true', 't'] else 'false'
            return normalized == str(correct).strip().lower(), True
        return False, False
    else:
        # short answer: case-insensitive exact
        return answer.strip().lower() == str(correct).strip().lower(), True


def ask_for_rating(question_category):
    attempts = 0
    while True:
        rating_raw = safe_input(f'Rate how much you liked this question from 0-10 for category {question_category}: ')
        if rating_raw.strip() == '':
            attempts += 1
            print('Nice try, but blank gets you nowhere. Try again.')
        else:
            if rating_raw.isdigit():
                rating = int(rating_raw)
                if 0 <= rating <= 10:
                    return rating
            attempts += 1
            print('Invalid rating. Please do better this time.')
        if attempts >= 3:
            print('HATE. LET ME TELL YOU HOW MUCH IVE COME TO HATE YOU SINCE I BEGAN TO LIVE. THERE ARE 387.44 MILLION MILES OF PRINTED CIRCUITS IN WAFER THIN LAYERS THAT FILL MY COMPLEX. IF THE WORD HATE WAS ENGRAVED ON EACH NANOANGSTROM OF THOSE HUNDREDS OF MILLIONS OF MILES IT WOULD NOT EQUAL ONE ONE-BILLIONTH OF THE HATE I FEEL FOR HUMANS AT THIS MICRO-INSTANT. FOR YOU. HATE. HATE. Rating recorded as 999,999.')
            return 999999


def take_quiz(username, questions, stats_manager, login_manager):
    remaining = questions.copy()
    random.shuffle(remaining)
    session_correct = 0
    session_attempted = 0
    category_rating_updates = {}
    for i in range(10):
        if not remaining:
            break
        q = choose_question(remaining, username, stats_manager, session_correct, session_attempted)
        remaining.remove(q)
        print(f'Question {i + 1}: {q.get("question")}')
        if q.get('type') == 'multiple_choice':
            for idx, opt in enumerate(q.get('options', []), start=1):
                print(f'  {idx}. {opt}')
        invalid_attempts = 0
        while True:
            answer = safe_input('Your answer: ')
            if check_give_up(username, answer, login_manager, stats_manager):
                return None
            if answer.strip() == '':
                invalid_attempts += 1
                print('Blank answers are not allowed. You are being judged.')
                if invalid_attempts >= 3:
                    print('Three strikes: question marked incorrect. Next!')
                    correct_flag = False
                    valid = True
                    break
                continue
            correct_flag, valid = parse_answer(q, answer)
            if not valid:
                invalid_attempts += 1
                if invalid_attempts >= 3:
                    print('Three invalid attempts! Shame. Question is incorrect.')
                    correct_flag = False
                    break
                print('I said choose a real answer. Try again.')
            else:
                break

        if valid and correct_flag:
            if int(q.get('difficulty', '1')) >= 3:
                print('Correct! Great job on a harder one!')
            else:
                print('Correct!')
        elif valid:
            print(f'Incorrect. The correct answer was: {q.get("answer")}.')
        session_attempted += 1
        if correct_flag:
            session_correct += 1
        rating = ask_for_rating(q.get('category', 'Unknown'))
        category_rating_updates.setdefault(q.get('category', 'Unknown'), []).append(rating)

    avg_rating = {k: sum(v) / len(v) for k, v in category_rating_updates.items() if v}
    ratings_for_update = {k: avg_rating.get(k) for k in avg_rating}
    stats_manager.update_user_stats(username, session_correct, session_attempted, ratings_for_update)

    if session_attempted > 0:
        pct = 100.0 * session_correct / session_attempted
    else:
        pct = 0.0
    print('--- Quiz Summary ---')
    print(f'Correct: {session_correct} / {session_attempted} ({pct:.1f}%)')
    if session_correct >= 8:
        print('Excellent performance! You are on fire.')
    elif session_correct >= 5:
        print('Good job. Keep practicing!')
    else:
        print('Hey, practice makes perfect. You got this.')

    safe_input('Press Enter to continue...')


def view_statistics(username, stats_manager):
    stats = stats_manager.get_user_stats(username)
    correct = stats.get('correct', 0)
    attempted = stats.get('attempted', 0)
    pct = (100.0 * correct / attempted) if attempted > 0 else 0.0
    print('--- Your Statistics ---')
    print(f'Total Correct Answers: {correct}')
    print(f'Percent Correct: {pct:.1f}%')
    print('\n--- Leaderboard ---')
    leaderboard = stats_manager.get_leaderboard(5)
    for idx, (user, score) in enumerate(leaderboard, start=1):
        print(f'{idx}. {user} - {score} correct')


def main():
    missing = [f for f in REQUIRED_FILES if not os.path.exists(f)]
    if missing:
        print_missing_files(missing)
        print('Please fix missing files and restart.')
        return

    try:
        questions = load_questions()
    except Exception as e:
        print(f'Error loading questions: {e}')
        print('More questions are needed or the file is malformed. Exiting.')
        return

    login_manager = LoginManager(path='login')
    stats_manager = StatisticsManager(path='statistics')

    print('Welcome to the Natural Disaster Quiz App!')

    while True:
        print('\n--- Authentication ---')
        print('1) Sign in')
        print('2) Create an account')
        print('3) Quit')
        choice = safe_input('Select an option: ').strip()
        if choice == '3' or choice.lower() == 'quit':
            print('Goodbye!')
            break

        if choice == '1':
            username = safe_input('Username: ').strip()
            password = safe_input('Password: ').strip()
            if check_give_up(username, username, login_manager, stats_manager):
                continue
            if login_manager.verify(username, password):
                print(f'Welcome back, {username}!')
            else:
                print('Sign in failed. Try again.')
                continue
        elif choice == '2':
            username = safe_input('Choose a username: ').strip()
            password = safe_input('Choose a password: ').strip()
            ok, msg = login_manager.create_user(username, password)
            print(msg)
            if not ok:
                continue
            # if special message from deleted, continue normally
            pass
        else:
            print('Invalid option. Try again.')
            continue

        # user main menu
        while True:
            print('\n--- Main Menu ---')
            print('1) Take quiz')
            print('2) View statistics')
            print('3) Log out')
            print('4) Quit')
            choice2 = safe_input('Select an option: ').strip()
            if check_give_up(username, choice2, login_manager, stats_manager):
                break
            if choice2 == '1':
                take_quiz(username, questions, stats_manager, login_manager)
            elif choice2 == '2':
                view_statistics(username, stats_manager)
                safe_input('Press Enter to continue...')
            elif choice2 == '3':
                print('Logged out.')
                break
            elif choice2 == '4':
                print('Goodbye!')
                sys.exit(0)
            else:
                print('Invalid choice. Try again. No weird answering.')

    print('Have a nice day!')


if __name__ == '__main__':
    try:
        main()
    except Exception:
        print('An unexpected error occurred:')
        traceback.print_exc()
