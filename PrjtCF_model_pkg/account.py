import pandas as pd
import numpy as np
from IPython.display import display, HTML


class account(object):
    def __init__(self, mtrt=0):
        self.mtrt = mtrt
        self.index = np.arange(-1, self.mtrt + 1)
        self.columns = ['bal_intl', 'amt_add', 'amt_sub', 'bal_clsn']
        self.df = pd.DataFrame(np.zeros([len(self.index), len(self.columns)]),
                               columns=self.columns, index=self.index)
        self._cal_amt()

    def addamt(self, index, val):
        tmpamt = val
        self.df.loc[index, 'amt_add'] += tmpamt
        self._cal_amt()
        return tmpamt

    def subamt(self, index, val):
        tmpamt = min(self.bal_clsn(index), val)
        self.df.loc[index, 'amt_sub'] += tmpamt
        self._cal_amt()
        return tmpamt

    def bal_intl(self, index=None):
        if index is None:
            return self.df.loc[:, 'bal_intl']
        else:
            return self.df.loc[index, 'bal_intl']

    def bal_clsn(self, index=None):
        if index is None:
            return self.df.loc[:, 'bal_clsn']
        else:
            return self.df.loc[index, 'bal_clsn']

    def _cal_amt(self):

        self.df.loc[-1, 'bal_clsn'] = self.df.loc[-1, 'bal_intl'] + self.df.loc[-1, 'amt_add'] \
                                      - self.df.loc[-1, 'amt_sub']
        for idx in np.arange(0, self.mtrt + 1):
            self.df.loc[idx, 'bal_intl'] = self.df.loc[idx - 1, 'bal_clsn']
            self.df.loc[idx, 'bal_clsn'] = self.df.loc[idx, 'bal_intl'] + self.df.loc[idx, 'amt_add'] \
                                           - self.df.loc[idx, 'amt_sub']