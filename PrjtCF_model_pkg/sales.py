"""

"""

from PrjtCF_model_pkg.config import *
from PrjtCF_model_pkg.schedule import *

class sales(object):
    '''
    매출액 설정 클래스
    - title : 입출력, 매출액 구분 명칭
    - aream2 : 입출력, 분양면적(m2)
    - areapy : 계산출력, 분양면적(평)
    - unitprcm2 : 입출력, 평균분양가(원/m2)
    - sep1 : 입출력, 매출액 구분 명칭 1
    - sep2 : 입출력, 매출액 구분 명칭 2
    - amt : 계산출력, 분양금액(원)
    '''
    def __init__(self, 
                 title = None,
                 aream2 = 0, 
                 unitprcm2 = 0,
                 unitmtpl = 1,
                 inptidx = [0],
                 mtrt = 0,
                 sep1 = None,
                 sep2 = None,
                 note = ""):
        self.title = title
        self.aream2 = aream2
        self.unitprcm2 = unitprcm2
        self.unitmtpl = np.array(unitmtpl)
        self.inptidx = np.array(inptidx)
        self.mtrt = mtrt
        self.sep1 = sep1
        self.sep2 = sep2
        self.note = note
        self.setscd()


    # Input Data
    def setscd(self):
        self.columns = ['amt_scdd', 'amt_scdd_cum', 'amt_paid', 'amt_paid_cum', 'amt_rsdl', 'rate_paid', 'rate_paid_cum']
        self.index = np.arange(-1, self.mtrt + 1)
        self.df = pd.DataFrame(np.zeros([len(self.index), len(self.columns)]), columns=self.columns, index=self.index)
        self.df.loc[self.inptidx, 'amt_scdd'] = self.amt * self.unitmtpl
        self._cal_amt()

    def addval(self, index, val):
        self.df.loc[index, 'amt_scdd'] += np.array(val)
        self._cal_amt()

    def amt_pay(self, index, amt=None):
        if amt is None:
            self.df.loc[index, 'amt_paid'] += self.sales_amt(index)
        else:
            self.df.loc[index, 'amt_paid'] += amt
        self._cal_amt()

    # Calculate Data
    def _cal_amt(self):
        self.df.loc[:, 'amt_scdd_cum'] = self.df.loc[:, 'amt_scdd'].cumsum()
        self.df.loc[:, 'amt_paid_cum'] = self.df.loc[:, 'amt_paid'].cumsum()
        self.df.loc[:, 'amt_rsdl'] = self.df.loc[:, 'amt_scdd_cum'] - self.df.loc[:, 'amt_paid_cum']
        self.df.loc[:, 'rate_paid'] = self.df.loc[:, 'amt_paid'] / self.amt
        self.df.loc[:, 'rate_paid_cum'] = self.df.loc[:, 'rate_paid'].cumsum()

    # Output Data
    @property
    def areapy(self):
        return self.aream2 / py

    @property
    def unitprcpy(self):
        return self.unitprcm2 * py

    @property
    def amt(self):
        tmp = self.aream2 * self.unitprcm2
        return tmp

    @property
    def amt_paid(self):
        return self.df.amt_paid.sum()

    def sales_amt(self, index=None):
        if index is None:
            return self.df.loc[:, 'amt_rsdl']
        else:
            return self.df.loc[index, 'amt_rsdl']


class salesmerge(object):
    """
    매출액 취합 클래스
    - title_ls : 출력, title 리스트 출력
    - aream2_ls : 출력, aream2 리스트 출력
    - aream2 : 출력, aream2 합계 출력
    - unitprcm2_ls : 출력, unitprcm2 리스트 출력
    - sep1_ls : 출력, sep1 리스트 출력
    - sep2_ls : 출력, sep2 리스트 출력
    - amt_ls : 출력, amt 리스트 출력
    - amt : 출력, amt 합계 출력
    - summary : 출력, 전체 데이터 취합 출력
    """
    def __init__(self, salesdct):
        self.salesdct = salesdct

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
        tmpseries = pd.Series(self.salesdct)
        return tmpseries[self._sep_blean(sep1=sep1, sep2=sep2)].index

    def title(self, sep1=None, sep2=None):
        tmp_dct = pd.Series({x:self.salesdct[x].title for x in self.salesdct})
        return tmp_dct[self._sep_idx(sep1=sep1, sep2=sep2)]

    def aream2(self, sep1=None, sep2=None):
        tmp_dct = pd.Series({x:self.salesdct[x].aream2 for x in self.salesdct})
        return tmp_dct[self._sep_idx(sep1=sep1, sep2=sep2)]

    def areapy(self, sep1=None, sep2=None):
        tmp_dct = pd.Series({x:self.salesdct[x].areapy for x in self.salesdct})
        return tmp_dct[self._sep_idx(sep1=sep1, sep2=sep2)]

    def unitprcm2(self, sep1=None, sep2=None):
        tmp_dct = pd.Series({x:self.salesdct[x].unitprcm2 for x in self.salesdct})
        return tmp_dct[self._sep_idx(sep1=sep1, sep2=sep2)]

    def unitprcpy(self, sep1=None, sep2=None):
        tmp_dct = pd.Series({x:self.salesdct[x].unitprcpy for x in self.salesdct})
        return tmp_dct[self._sep_idx(sep1=sep1, sep2=sep2)]

    def sep1(self, sep2=None):
        tmp_dct = pd.Series({x:self.salesdct[x].sep1 for x in self.salesdct})
        if sep2:
            tmp_dct = tmp_dct[self._sep_idx(sep2=sep2)]
        return tmp_dct

    def sep2(self, sep1=None):
        tmp_dct = pd.Series({x:self.salesdct[x].sep2 for x in self.salesdct})
        if sep1:
            tmp_dct = tmp_dct[self._sep_idx(sep1=sep1)]
        return tmp_dct

    def note(self, sep1=None, sep2=None):
        tmp_dct = pd.Series({x:self.salesdct[x].note for x in self.salesdct})
        return tmp_dct[self._sep_idx(sep1=sep1, sep2=sep2)]

    def amt(self, sep1=None, sep2=None):
        tmp_dct = pd.Series({x:self.salesdct[x].amt for x in self.salesdct})
        return tmp_dct[self._sep_idx(sep1=sep1, sep2=sep2)]

    def df(self, var='amt_scdd', sep1=None, sep2=None):
        tmp_dct = pd.DataFrame({x: self.salesdct[x].df.loc[:, var] for x in self.salesdct})
        return tmp_dct.loc[:, self._sep_idx(sep1=sep1, sep2=sep2)]

    def salesrate(self, sep1=None, sep2=None):
        tmp_dfsum = self.df(var='amt_paid', sep1=sep1, sep2=sep2).sum(axis=1)
        tmp_amtsum = self.amt(sep1=sep1, sep2=sep2).sum()
        return tmp_dfsum / tmp_amtsum
