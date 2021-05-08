# required python packages
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

#test data
# df = pd.read_csv('https://raw.githubusercontent.com/Soot3/testing/master/ICMLA_2014_2015_2016_2017.csv',encoding='latin',skip_blank_lines=True)

# function inputs; the topics as a string, the dataset with reviewer topics and the reviewer name
# reviewer_dataset = df.loc[:,('keywords', 'session')]
# paper_topic = df['keywords'].sample()

# vectorizer function (takes in string values and outputs vector with word frequencies)
# vec = CountVectorizer()

# string matching function
def similar(topic,dataset):
  # function inputs; the topics as a string, the dataset with reviewer topics and the reviewer name
  df = dataset
  reviewer_dataset = df.loc[:, ('keywords', 'session')]
  paper_topic = df['keywords'].sample()

  # vectorizer function (takes in string values and outputs vector with word frequencies)
  vec = CountVectorizer()

  # topics from the reviewers are isolated and vectorized
  reviewer_topics = dataset['keywords']
  reviewer = vec.fit_transform(reviewer_topics)
  # vector is used to transform the user topics
  paper = vec.transform(topic)

  # cosine similarity is calculated for the whole dataset, looking at which topic is simiiar to the user input
  cos = cosine_similarity(reviewer,paper)

  # the highest similarity is isolated
  dataset['similarity'] = cos
  dataset.sort_values(by='similarity', ascending=False, inplace=True)
  top = dataset.head(1) 
  
  # returns the reviewer name
  return top['session'].to_string(index=False)

#test function
# similar(paper_topic, reviewer_dataset)