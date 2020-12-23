from PrjtCF_model_pkg.config import *

class schedule(object):
    def __init__(self, mtrt = 0):
        self.mtrt = mtrt
        self.index = np.arange(-1, self.mtrt + 1)
        self.amt = np.zeros_like(self.index)
        self.df = pd.DataFrame({'amt':self.amt}, index=self.index)
        
    def setval(self, index, val):
        self.df.loc[index] = np.array(val).reshape((-1, 1))

    def addval(self, index, val):
        self.df.loc[index] += np.array(val).reshape((-1, 1))

    def subval(self, index, val):
        self.df.loc[index] -= np.array(val).reshape((-1, 1))

    def setext(self, val):
        self.df.loc[-1] = val

    def setintl(self, val):
        self.df.loc[0] = val
    
    def setmtrt(self, val):
        self.df.loc[self.mtrt] = val
    
    @property
    def getext(self):
        return self.df.loc[-1]
    
    @property
    def getintl(self):
        return self.df.loc[0]
    
    @property
    def getmtrt(self):
        return self.df.loc[self.mtrt]
    
    @property
    def ttlamt(self):
        return self.df.amt.sum()