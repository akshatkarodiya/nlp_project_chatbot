# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
from typing import Any, Text, Dict, List
import pandas as pd
from gensim.models.doc2vec import Doc2Vec
from gensim.parsing.preprocessing import preprocess_string
from rasa_sdk import Action, Tracker
import numpy as np
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.interfaces import Tracker
from rasa_sdk.types import DomainDict

movie_plot_model = Doc2Vec.load('external_models/movie_plot_recommend_model/Movie_recommend.model')
movie_data_with_plot = pd.read_csv('datasets/wiki_movie_plots_deduped.csv',sep=',',usecols=['Release Year', 'Title', 'Plot'])
movie_data_with_plot = movie_data_with_plot[movie_data_with_plot['Release Year'] >= 2001]

movie_cosine_similarity = np.loadtxt("external_models/cosine_sim.csv",
                 delimiter=",",dtype=float)
movie_dataset = pd.read_csv('datasets/movies_dataset.csv')

indices = pd.Series(movie_dataset['Title'])
def predict(title, cosine_sim = movie_cosine_similarity):
    recommended_movies = []
    try:
        idx = indices[indices == title].index[0]
        score_series = pd.Series(cosine_sim[idx]).sort_values(ascending = False)  # similarity scores in descending order
        top_5_indices = list(score_series.iloc[1:6].index)   # to get the indices of top 6 most similar movies     
        for i in top_5_indices:   # to append the titles of top 10 similar movies to the recommended_movies list
            recommended_movies.append(list(movie_dataset['Title'])[i])
    except:
        recommended_movies.append("No suggession found")
        
    return recommended_movies

class ActionHello(Action):
    
    def name(self) -> Text:
        return "action_hello"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text,Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Hello Please provide plot")
        return []
    

class ActionSearchMoviePlot(Action):
    def name(self) -> Text:
        return "action_search_movie_plot"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> List[Dict[Text, Any]]:
        userMessage = tracker.latest_message['text']
		# use model to find the movie
        print("heree")
        new_doc = preprocess_string(userMessage)
        test_doc_vector = movie_plot_model.infer_vector(new_doc)
        sims = movie_plot_model.dv.most_similar(positive = [test_doc_vector])		
		# Get first 5 matches
        movies = [movie_data_with_plot['Title'].iloc[s[0]] for s in sims[:5]]
        botResponse = f"I found the following movies: {movies}.".replace('[','').replace(']','')
        dispatcher.utter_message(text=botResponse)
        return []
    
class ActionSearchSimilarMovie(Action):
    def name(self) -> Text:
        return "action_search_similar_movie"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> List[Dict[Text, Any]]:
        userMessage = tracker.latest_message['text']
		# use model to find the movie
        print(userMessage)
        movies = predict(userMessage)
        print("skskss")
        botResponse = f"I found the following movies: {movies}.".replace('[','').replace(']','')
        dispatcher.utter_message(text=botResponse)
        # new_doc = preprocess_string(userMessage)

        return []
    
class ActionSearchActorMovie(Action):
    def name(self) -> Text:
        return "action_search_actor_movie"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> List[Dict[Text, Any]]:
        userMessage = tracker.get_slot()
		# use model to find the movieS
        print(userMessage)
        botResponse = f"Movies with actor {userMessage}."
        dispatcher.utter_message(text=botResponse)
        # new_doc = preprocess_string(userMessage)

        return []
    
# class ActionTemp(Action):

#     def name(self) -> Text:
#         return "action_temp"
    
#     def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> Coroutine[Any, Any, List[Dict[Text, Any]]]:
#         return await super().run(dispatcher, tracker, domain)


    
