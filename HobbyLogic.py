import numpy as np
import pandas as pd

from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement

from gensim.models import Word2Vec

class HobbyLogic(LogicAdapter):
    products = ''
    hobbyModel = ''
    recommenderModel = ''

    keywords = []

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

        self.products = pd.read_csv('./product_hobby.csv', usecols=['Product Name Source', 'Keywords'])
        self.products.dropna(inplace=True)

        self.hobbyModel = Word2Vec.load('hobby.w2v')
        self.recommenderModel = Word2Vec.load('recommender.w2v')
    
    def can_process(self, statement):
        similar = False
        similarFound = False

        sentence = statement.text.lower().split(' ')

        for word in sentence:
            if word in self.hobbyModel.wv.vocab:
                sim_test = self.hobbyModel.wv.most_similar(positive=[word], topn=1)

                if len(sim_test) > 0 and sim_test[0][1] > 0.1:
                    similarFound = True
                    similar = True
                    
                    self.keywords.append(word.lower())
                else:
                    similar = False
            else:
                similar = False

        return (similar | similarFound)
    
    def lookup(self, frame):
        simi_score = 0
        counter = 0

        for word1 in self.keywords:
            if word1 in self.recommenderModel.wv.vocab:
                for word2 in str(frame['Keywords']).split(' '):
                    if word2 in self.recommenderModel.wv.vocab:
                        simi_score += self.recommenderModel.wv.similarity(word1, word2)
                        counter += 1
          
        frame['Score'] = simi_score

        return frame

    
    def process(self, input_statement, additional_response_selection_parameters):
        products_with_score = self.products.apply(self.lookup, axis=1)
        products_with_score_sorted = products_with_score.sort_values(by=['Score'], ascending=False)
        products_with_score_sorted.dropna(inplace=True)

        top_five = products_with_score_sorted.head()

        recommendations = ''

        for i in range(1, 6):
            recommendations += '\n' + str(i) + '. (' + str(top_five['Score'].iloc[i-1]) + ')' + str(top_five['Product Name Source'].iloc[i-1])

        response_statement = Statement(text = 'Based on your hobby, I am recommending the following products:{}\n'.format(recommendations))

        response_statement.confidence = 1.0

        return response_statement