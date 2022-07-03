import sys
import pandas as pd 
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests
import pickle
from data.get_data import get_data
from preprocessing.preprocess import preprocess


class recommend:

    def __init__(self, data1, data2):

        self.data1 = data1
        self.data2 = data2
        self.get_obj = get_data(self.data1, self.data2)
        self.df = self.get_obj.get()
        self.pre = preprocess(self.df)
    
    def get_base_data(self):

        try:

            movie_df = self.df[['movie_id','title','overview','genres','keywords','cast','crew']].copy(deep=True)
            movie_df.dropna(inplace=True)

            for col in ['genres','keywords','cast']:
                movie_df[col] = movie_df[col].apply(self.pre.convert)
            
            movie_df['cast'] = movie_df['cast'].apply(lambda x:x[0:3])
            movie_df['crew'] = movie_df['crew'].apply(self.pre.fetch_director)

            for col in ['genres','keywords','cast','crew']:
                movie_df[col] = movie_df[col].apply(self.pre.collapse)
            
            movie_df['overview'] = movie_df['overview'].apply(lambda x:x.split())
            movie_df['tags'] = movie_df['overview'] + movie_df['genres'] + movie_df['keywords'] + movie_df['cast'] + movie_df['crew']
            new_df = movie_df.drop(columns=['overview','genres','keywords','cast','crew'])
            new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x))
            pickle.dump(new_df,open('movie_list.pkl','wb'))
            return new_df

        except Exception as e:
            print(e)
            sys.exit(1)

    def get_similarity_score(self):

        try:
            df = self.get_base_data()
            cv = CountVectorizer(max_features=5000,stop_words='english')
            vector = cv.fit_transform(df['tags']).toarray()
            similarity = cosine_similarity(vector)
            pickle.dump(similarity,open('similarity.pkl','wb'))
    
        except Exception as e:
            print(e)
            sys.exit(1)



    
if __name__ == '__main__':

    rec = recommend('tmdb_5000_movies.csv','tmdb_5000_credits.csv')
    rec.get_similarity_score()