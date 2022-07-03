import ast
import numpy as np
import sys

class preprocess:

    def __init__(self, df):

        self.df = df

    def dropna(self):

        try:
            self.df.dropna(inplace=True)
        except Exception as e:
            print(e)
            sys.exit(1)

    def convert(self,text):

        try:
            L = []
            for i in ast.literal_eval(text):
                L.append(i['name']) 
            return L 
        except Exception as e:
            print(e)
            sys.exit(1)

    def fetch_director(self,text):
        
        try:
            L = []
            for i in ast.literal_eval(text):
                if i['job'] == 'Director':
                    L.append(i['name'])
            return L 
        except Exception as e:
            print(e)
            sys.exit(1)

    def collapse(self,L):

        try:
            L1 = []
            for i in L:
                L1.append(i.replace(" ",""))
            return L1

        except Exception as e:
            print(e)
            sys.exit(1)