"""
"""
from FS_dangjin_pkg.config import *
from FS_dangjin_pkg.schedule import *

class cost(object):
    """
    [cost 취합]
    title : 제목
    sep1 : 구분1
    sep2 : 구분2
    fixedamt : 고정비용
    unitprc : 비율적용 비용 기준비용
    unitmtpl : 비율적용 비용 기준비율
    note : 비고란
    
    [keyward amount 계산 방법]
    tmp_cl = cost()
    tmp_fnc = lambda d: d['amt'] * d['tax']
    tmp_cl.kwcost(tmp_fnc, amt=1000, tax=2)
    tmp_cl.kwamt
    
    tmp_cl = cost()
    tmp_fnc = lambda l: l[0] * l[1]
    tmp_cl.kwcost(tmp_fnc, 1000, 2)
    tmp_cl.kwamt
    """

    def __init__(self,
                 title=None,
                 unitamt=0,
                 unitmtpl=1,
                 inptidx=[0],
                 mtrt=0,
                 sep1=None,
                 sep2=None,
                 note=""):
        self.title = title
        self.unitamt = np.array(unitamt)
        self.unitmtpl = np.array(unitmtpl)
        self.inptidx = np.array(inptidx)
        self.mtrt = mtrt
        self.sep1 = sep1
        self.sep2 = sep2
        self.note = note
        self.setscd()


    # Input Data
    def setscd(self):
        self.columns = ['amt_scdd', 'amt_scdd_cum', 'amt_paid', 'amt_paid_cum', 'amt_rsdl']
        self.index = np.arange(-1, self.mtrt + 1)
        self.df = pd.DataFrame(np.zeros([len(self.index), len(self.columns)]), columns=self.columns, index=self.index)
        self.df.loc[self.inptidx, 'amt_scdd'] = self.unitamt * self.unitmtpl
        self._cal_amt()

    def addval(self, index, val):
        self.df.loc[index, 'amt_scdd'] += np.array(val)
        self._cal_amt()

    def kwcost(self, func, index, *args, **kwargs):
        self.func = func
        if args and kwargs:
            raise AssertionError("Only positional or keyword args are allowed")
        self.params = args or kwargs
        self.__iskwcost = True

        kwamt = self.func(self.params)
        self.addval(index, kwamt)

    def amt_pay(self, index, amt=None):
        if amt is None:
            self.df.loc[index, 'amt_paid'] += self.cost_amt(index)
        else:
            self.df.loc[index, 'amt_paid'] += amt
        self._cal_amt()

    # Calculate Data
    def _cal_amt(self):
        self.df.loc[:, 'amt_scdd_cum'] = self.df.loc[:, 'amt_scdd'].cumsum()
        self.df.loc[:, 'amt_paid_cum'] = self.df.loc[:, 'amt_paid'].cumsum()
        self.df.loc[:, 'amt_rsdl'] = self.df.loc[:, 'amt_scdd_cum'] - self.df.loc[:, 'amt_paid_cum']

    # Output Data
    @property
    def amt(self):
        return self.df.amt_scdd.sum()

    @property
    def amt_paid(self):
        return self.df.amt_paid.sum()

    def cost_amt(self, index=None):
        if index is None:
            return self.df.loc[:, 'amt_rsdl']
        else:
            return self.df.loc[index, 'amt_rsdl']


class costmerge(object):
    def __init__(self, costdct):
        self.costdct = costdct

    ### 자료 취합 및 출력 함수 ###
    def _sep_blean(self, sep1=None, sep2=None):
        if sep1 is not None:
            sep1_blean = np.array([x in sep1 for x in self.sep1().values])
        else:
            sep1_blean = np.array([True for x in self.sep1().values])

        if sep2 is not None:
            sep2_blean = np.array([x in sep2 for x in self.sep2().values])
        else:
            sep2_blean = np.array([True for x in self.sep2().values])

        return sep1_blean & sep2_blean

    def _sep_idx(self, sep1=None, sep2=None):
        tmpseries = pd.Series(self.costdct)
        return tmpseries[self._sep_blean(sep1=sep1, sep2=sep2)].index

    def sep1(self, sep2=None):
        tmp_dct = pd.Series({x: self.costdct[x].sep1 for x in self.costdct})
        if sep2:
            tmp_dct = tmp_dct[self._sep_idx(sep2=sep2)]
        return tmp_dct

    def sep2(self, sep1=None):
        tmp_dct = pd.Series({x: self.costdct[x].sep2 for x in self.costdct})
        if sep1:
            tmp_dct = tmp_dct[self._sep_idx(sep1=sep1)]
        return tmp_dct

    def title(self, sep1=None, sep2=None):
        tmp_dct = pd.Series({x: self.costdct[x].title for x in self.costdct})
        return tmp_dct[self._sep_idx(sep1=sep1, sep2=sep2)]

    def amt(self, sep1=None, sep2=None):
        tmp_dct = pd.Series({x: self.costdct[x].amt for x in self.costdct})
        return tmp_dct[self._sep_idx(sep1=sep1, sep2=sep2)]

    def note(self, sep1=None, sep2=None):
        tmp_dct = pd.Series({x: self.costdct[x].note for x in self.costdct})
        return tmp_dct[self._sep_idx(sep1=sep1, sep2=sep2)]

    def df(self, var='amt_scdd', sep1=None, sep2=None):
        tmp_dct = pd.DataFrame({x: self.costdct[x].df.loc[:, var] for x in self.costdct})
        return tmp_dct.loc[:, self._sep_idx(sep1=sep1, sep2=sep2)]
