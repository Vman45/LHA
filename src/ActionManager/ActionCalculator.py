from sklearn.feature_extraction.text import TfidfVectorizer
from typing import List
from sklearn.metrics.pairwise import cosine_similarity
from src.ActionManager.Action import Action


class ActionCalculator:
    actions: List[Action]
    model: TfidfVectorizer
    threshold: float

    def __init__(self, actions: List[Action], threshold: float = 0.5):
        self.actions = actions
        self.model = TfidfVectorizer()
        self.threshold = threshold

    def train_model(self, data):
        return self.model.fit_transform(data)

    def get_all_tags(self):
        tags_list = []
        for action in self.actions:
            tags_list.append(action.tags)
        return [' '.join(tag) for tag in tags_list]

    def select_action_to_execute(self, transcript: str):
        train = self.train_model(self.get_all_tags())
        test = self.model.transform([transcript.lower()])

        all_tags = [a.tags for a in self.actions]
        data = [val for sublist in all_tags for val in sublist]

        similarities = cosine_similarity(train, test)
        closest_action = similarities.argsort(axis=None)[-1]
        if similarities[closest_action] >= self.threshold:
            s = data[closest_action]
            act = [a for a in self.actions if s in a.tags]
            return act[0]
        else:
            return None