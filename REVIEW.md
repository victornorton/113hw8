1. [PASS] File existence checks. `main.py` verifies required files list includes `questions.json`, `login.py`, and `statistics.py` (main.py lines ~183-190). If missing, prints each missing file and exits cleanly.

2. [PASS] Question bank validation. `load_questions()` in `main.py` (line 38) enforces `len(data['questions']) >= 32`, category count >= 8, difficulty count >= 2 per category, and reports errors if malformed or insufficient.

3. [PASS] Login system with hashes. `login.py` (lines 1-79) uses salted PBKDF2-HMAC-SHA256 and stores only salt/hash, not raw passwords.

4. [PASS] Existing username creation prevented. `LoginManager.create_user` (line 38) returns failure and message when username exists. This meets spec.

5. [PASS] Deleted-username special message and reuse handling. `LoginManager.create_user` checks `data['deleted']` and returns "You cannot recover what has been lost." (line ~48), then allows account recreation. Good.

6. [PASS] I give up feature. `check_give_up` in `main.py` (line 22) deletes account and statistics if input is exactly "I give up." and confirm is exactly "Yes.". Called from quiz answer path and main menu. Good.

7. [PASS] Quiz flow and question selection logic. `take_quiz()` in `main.py` (line 140) runs 10 questions, uses `choose_question()` (line 66) with random weighted selection by category preference and performance-adjusted difficulty, giving the required dynamic behavior.

8. [PASS] Immediate correctness feedback. `take_quiz` reports correct/wrong and gives harder-question praise when difficulty >= 3 (line ~172). It also records question rating and updates stats.

9. [PASS] Rating and invalid handling inside quiz. `ask_for_rating()` (line ~124) scolds on invalid/blank input and on 3 invalid attempts assigns rating 5. `take_quiz` invalid answer handling 3 strikes with question marked incorrect (line ~156). Meets spec.

10. [PASS] Stats view and leaderboard. `view_statistics()` in `main.py` (line 213) prints total correct, percentage, and top 5 from `StatisticsManager.get_leaderboard`.

11. [PASS] Logout and quit behavior. Main menu in `main.py` (line ~231) handles 3=logout, 4=quit, and both work.

12. [WARN] Inconsistent `check_give_up` invocation at sign-in path. At sign-in, `check_give_up(username, username, ...)` uses username as both current user and input, which is ineffective for intentional "I give up." from the user. (main.py lines 220-224). Good design intention, but bug.

13. [WARN] Broad exception swallowing in data loads. `LoginManager._load` and `StatisticsManager._load` catch all exceptions and silently reset data, potentially masking corruption or deserialization bugs (login.py lines ~14, statistics.py lines ~14). This could hide issues.

14. [WARN] Unsafe serialization format. `login.py` and `statistics.py` use `pickle` with world-writable files, which is insecure for untrusted environment. This is relevant to security concerns (file names logins/stats have arbitrary code execution risk if tampered). (login.py lines ~10, statistics.py lines ~10)

15. [WARN] `questions.json` not rechecked in main loop. If file is deleted during runtime, app doesn't detect until restart. Minor.

16. [WARN] `parse_answer` for short answer marks all nonexact as incorrect without tolerance for trailing spaces; acceptable but maybe harsh. Not strong though.

17. [WARN] `choose_question` handles missing `difficulty` by default 2 but with bad non-int text raises ValueError in `int()` call. Should validate gracefully. (main.py line ~75)

18. [FAIL] The spec says "questions that a user gives poor overall ratings should eventually be chosen less often". Implementation uses per-user category average ratings (line 70) but only in category weight formula `0.2 + pref/10`, which ranges from 0.2 to 1.2 and never reduces below 0.2. This means low ratings have limited effect; strictly speaking the selected category is still chosen at minimum 0.1 relative weight, so behavior is weak but present. Marking as WARN/partial; I'd treat this as partial pass.

19. [PASS] Handling incomplete/insufficient questions gracefully. `load_questions` raises and main catches with message about more questions needed and exits (main.py lines 183). Good behavior.

20. [WARN] `REQUIRED_FILES` expresses login.py/statistics.py exist but not checking login/statistics data file (path "login", "statistics"). Workaround is okay but not fully aligned with wording (spec says file `statistics` and `login` should exist, yes they do if not created on first run.)
