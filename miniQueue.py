import numpy as np
class miniQueue():
    
    def __init__(self,maxlen=20):
        self.data=[]
        self.maxlen=maxlen
        
    def put(self,x):
        if len(self.data)==self.maxlen:
            self.data.pop(0)
            self.data.append(x)
        else:
            self.data.append(x)
            
    def get(self):
        if len(self.data)>0:
            return self.data.pop()
    def allData(self):
        return self.data
    def size(self):
        return len(self.data)
    def full(self):
        return len(self.data)==self.maxlen
    def erase(self):
        self.data=[]
    def mean(self):
        return np.mean(self.data)
        
    

