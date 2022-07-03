import pandas as pd
import sys

class get_data:

    def __init__(self, data1, data2):

        self.movie_data = pd.read_csv(data1)
        self.credit_data = pd.read_csv(data2)

    def get(self):

        try:        
            merged_data = self.movie_data.merge(self.credit_data, on = 'title')
            return merged_data
        except Exception as e:
            print(e)
            sys.exit(1)
            