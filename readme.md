First Step

for chatbot most important part is to understand the  intent. Intent is the intention of the users, interacting wiht the chatbot.
 
 We use a supervised learning approach of training an sentence classifier i.e we classify the intent in the classes or entities. Entities are the objects/topics useful in further knowing the purpose of User's inputs.

Examples :- 

intent : greet => examples: hey hi hello etc.

intent : read with entity: book
examples: I would like to read a book. 

so we are classifying the intent with entity.

To identify the intent of the user we have to train the model, rasa provide two option :-

Component which are already pre trained model and use them in rasa with integrating them in the pipeline.

Components which train on your RASA NLU training data & improve as we make change in the training data.

We will be using both integrating custom models as well providing the training data to the rasa nlu.