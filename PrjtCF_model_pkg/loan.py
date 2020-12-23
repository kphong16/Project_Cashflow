"""

"""

from PrjtCF_model_pkg.config import *
from PrjtCF_model_pkg.schedule import *


class loan(object):
    def __init__(self,
                 title=None,
                 amt=0,
                 mtrt=0,
                 fee=0.0,
                 IR=0.0,
                 IRccl=1):
        self.title = title
        self.amt = amt
        self.mtrt = mtrt
        self.fee = fee
        self.IR = IR
        self.IRccl = IRccl # IR payment cycle
        self.IRcalprd = self.IRccl / 12 # IR calculation period

        self.setloan()

    def setloan(self):
        self.index = np.arange(-1, self.mtrt + 1)
        self.df = pd.DataFrame({'amt_ntnl': np.ones_like(self.index) * self.amt,  # Notional Amount
                                'amt_rdcd': np.zeros_like(self.index), # Reduced Withdrawable Amount
                                'amt_rdcd_cum': np.zeros_like(self.index), # Cumulated Reduced Withdrawable Amount
                                'amt_paid': np.zeros_like(self.index),  # Withdrawn Amount
                                'amt_paid_cum': np.zeros_like(self.index),  # Cumulated Withdrawn Amount
                                'amt_wtdrwbl': np.zeros_like(self.index),  # Residual Withdrawable Amount
                                'amt_repy_scd': np.zeros_like(self.index), # Amount Repayment Schedule
                                'amt_repd': np.zeros_like(self.index),  # Repaid Amount
                                'amt_repd_cum': np.zeros_like(self.index),  # Cumulated Repaid Amount
                                'amt_rsdl': np.zeros_like(self.index),  # Residual Amount
                                'amt_paid_forIR': np.zeros_like(self.index),  # Residual Amount for IR
                                'IR_rate': np.ones_like(self.index) * self.IR,  # IR Rate on Agreement
                                'IR_amt': np.zeros_like(self.index),  # IR Amount on Agreement
                                'IR_amt_cum': np.zeros_like(self.index),  # Cumulated IR Amount on Agreement
                                'IR_repd': np.zeros_like(self.index),  # Repaid IR Amount
                                'IR_repd_cum': np.zeros_like(self.index),  # Cumulated IR Amount Repaid
                                'IR_rsdl': np.zeros_like(self.index),  # Residual unpaid IR Amount
                                'fee_amt': np.ones_like(self.index) * self.amt * self.fee,  # Fee Payable
                                'fee_repd': np.zeros_like(self.index),  # Repaid Fee
                                'fee_unpd': np.zeros_like(self.index)  # Unpaid Fee
                                },
                               index=self.index)
        self._cal_amt()

    # Input Data
    def amt_rdc(self, index, amt):
        self.df.loc[index, 'amt_rdcd'] = amt
        self._cal_amt()

    def amt_pay(self, index, amt):
        self.df.loc[index, 'amt_paid'] = amt
        self._cal_amt()

    def amt_repay(self, index, amt):
        self.df.loc[index, 'amt_repd'] = amt
        self._cal_amt()

    def amt_repy_scd(self, index, amt):
        self.df.loc[index, 'amt_repy_scd'] = amt
        self._cal_amt()

    def IR_repay(self, index, amt):
        self.df.loc[index, 'IR_repd'] = amt
        self._cal_amt()

    def fee_repay(self, index, amt):
        self.df.loc[index, 'fee_repd'] = amt
        self._cal_amt()

    # Output Data
    def amt_wtdrwbl(self, index=None):
        if index is None:
            return self.df.loc[:, 'amt_wtdrwbl']
        else:
            return self.df.loc[index, 'amt_wtdrwbl']

    def amt_rsdl(self, index=None):
        if index is None:
            return self.df.loc[:, 'amt_rsdl']
        else:
            return self.df.loc[index, 'amt_rsdl']

    def IR_amt(self, index=None):
        if index is None:
            return self.df.loc[:, 'IR_amt']
        else:
            return self.df.loc[index, 'IR_amt']

    def IR_rsdl(self, index=None):
        if index is None:
            return self.df.loc[:, 'IR_rsdl']
        else:
            return self.df.loc[index, 'IR_rsdl']

    def fee_amt(self, index):
        return self.df.loc[index, 'fee_unpd']

    def IR_repd(self, index=None):
        if index is None:
            return self.df.loc[:, 'IR_repd']
        else:
            return self.df.loc[index, 'IR_repd']

    def fee_repd(self, index=None):
        if index is None:
            return self.df.loc[:, 'fee_repd']
        else:
            return self.df.loc[index, 'fee_repd']

    def is_repaid(self):
        if self.amt_wtdrwbl(self.mtrt) <= 0 and self.amt_rsdl(self.mtrt) <= 0:
            return True
        else:
            return False

    # Caculate Data
    def _cal_amt(self):
        self.df.loc[:, 'amt_rdcd_cum'] = self.df.loc[:, 'amt_rdcd'].cumsum()
        self.df.loc[:, 'amt_paid_cum'] = self.df.loc[:, 'amt_paid'].cumsum()
        self.df.loc[:, 'amt_wtdrwbl'] = self.df.loc[:, 'amt_ntnl'] - self.df.loc[:, 'amt_rdcd_cum'] - self.df.loc[:, 'amt_paid_cum']
        self.df.loc[:, 'amt_repd_cum'] = self.df.loc[:, 'amt_repd'].cumsum()
        self.df.loc[:, 'amt_rsdl'] = self.df.loc[:, 'amt_paid_cum'] - self.df.loc[:, 'amt_repd_cum']
        self.df.loc[:, 'amt_paid_forIR'] = self._deferarray(self.df.loc[:, 'amt_rsdl'])
        self.df.loc[:, 'IR_amt'] = self.df.loc[:, 'amt_paid_forIR'] * self.df.loc[:, 'IR_rate'] * self.IRcalprd
        self.df.loc[:, 'IR_amt_cum'] = self.df.loc[:, 'IR_amt'].cumsum()
        self.df.loc[:, 'IR_repd_cum'] = self.df.loc[:, 'IR_repd'].cumsum()
        self.df.loc[:, 'IR_rsdl'] = self.df.loc[:, 'IR_amt_cum'] - self.df.loc[:, 'IR_repd_cum']
        self.df.loc[:, 'fee_unpd'] = self.df.loc[:, 'fee_amt'] - self.df.loc[:, 'fee_repd'].cumsum()

    def _deferarray(self, arr):
        return np.hstack([[0], np.hsplit(arr, [len(arr) - 1])[0]])

    # Summary
    def summary(self):
        tmp_df = pd.DataFrame({'amt_paid': B(self.df.amt_paid),
                               'amt_wtdrwbl': B(self.df.amt_wtdrwbl),
                               'amt_repd': B(self.df.amt_repd),
                               'amt_rsdl': B(self.df.amt_rsdl),
                               'IR_rate': P(self.df.IR_rate),
                               'IR_amt': B(self.df.IR_amt),
                               'IR_repd': B(self.df.IR_repd),
                               'fee_repd': B(self.df.fee_repd)
                               }, index=self.index)

        return tmp_df
