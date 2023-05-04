# Project Overview 
#### A chabot based on rasa which is able to carry out conversation and recommend the required movies.
# How to run :- 
### First train the external model using ipynp files.
### Once that has been completed put model in external_models file.

## Run following command :- 

rasa train  (to train the model)
rasa run actions  (to active the rasa action servcer for custom actions)
rasa shell (to activate the chatbot).

## Dataset Overview 
Following external datasets has been used :- 

IMDB Dataset of 50K Movie Reviews | Kaggle
Wikipedia Movie Plots | Kaggle
IMDB 5000 Movie Dataset | Kaggle

Manually prepared dataset :- 

Create manually sets of questions that can be asked to the chat-bot and matched them with intent and entity present in them. Folder /data/ contains the manually created data.

## RASA Pipeline :- 

pipeline:

## initialize the spacy configurations 
 
 - name: SpacyNLP
   model: external_models/spacy.word2vec.model
 ### used to create tokens on the basis of the whitespace e.g. => how are you ? =conversion> tokensList=>["how","are","you","?"]
 - name: SpacyTokenizer
 ### used to vector representation of user message or features for entity extraction, intent classification, and response classification using the spaCy featurizer.
 - name: SpacyFeaturizer
 - name: LanguageModelFeaturizer
   model_name: bert
   model_weights: "rasa/LaBSE"
 ### Creates features for entity extraction and intent classification. During training the RegexFeaturizer creates a list of regular expressions defined in the training data format
 - name: RegexFeaturizer
#### used to map synonym of entity. 
 - name: EntitySynonymMapper
 ### Dual Intent Entity Transformer (DIET) used for intent classification and entity extraction
 - name: DIETClassifier
   epochs: 200
   random_seed: 2
Kaggle Notebook :- https://www.kaggle.com/code/akshat1608/movie-prediction-plot
https://www.kaggle.com/code/akshat1608/movie-prediction-with-name
