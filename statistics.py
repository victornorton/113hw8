import os
import pickle

class StatisticsManager:
    def __init__(self, path='statistics'):
        self.path = path
        self.data = {'users': {}, 'deleted': []}
        self._load()

    def _load(self):
        if not os.path.exists(self.path):
            self._save()
            return
        try:
            with open(self.path, 'rb') as f:
                self.data = pickle.load(f)
        except Exception:
            self.data = {'users': {}, 'deleted': []}

    def _save(self):
        dirpath = os.path.dirname(os.path.abspath(self.path))
        if dirpath and not os.path.exists(dirpath):
            os.makedirs(dirpath, exist_ok=True)
        with open(self.path, 'wb') as f:
            pickle.dump(self.data, f)

    def get_user_stats(self, username):
        return self.data['users'].get(username, {'correct': 0, 'attempted': 0, 'category_ratings': {}})

    def update_user_stats(self, username, correct, attempted, ratings):
        entry = self.data['users'].get(username, {'correct': 0, 'attempted': 0, 'category_ratings': {}})
        entry['correct'] = entry.get('correct', 0) + correct
        entry['attempted'] = entry.get('attempted', 0) + attempted
        cat_ratings = entry.get('category_ratings', {})
        for category, rating in ratings.items():
            if category not in cat_ratings:
                cat_ratings[category] = {'sum': 0, 'count': 0}
            if rating is not None:
                cat_ratings[category]['sum'] += rating
                cat_ratings[category]['count'] += 1
        entry['category_ratings'] = cat_ratings
        self.data['users'][username] = entry
        self._save()

    def delete_user(self, username):
        if username in self.data['users']:
            del self.data['users'][username]
            if username not in self.data['deleted']:
                self.data['deleted'].append(username)
            self._save()

    def get_leaderboard(self, top_n=5):
        users = []
        for username, entry in self.data['users'].items():
            users.append((username, entry.get('correct', 0)))
        users.sort(key=lambda x: x[1], reverse=True)
        return users[:top_n]

    def get_category_preference(self, username, category):
        entry = self.get_user_stats(username)
        cat_ratings = entry.get('category_ratings', {})
        cr = cat_ratings.get(category)
        if not cr or cr.get('count', 0) == 0:
            return 5.0
        return cr['sum'] / cr['count']
