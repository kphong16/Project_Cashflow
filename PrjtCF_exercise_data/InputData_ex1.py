from PrjtCF_model_pkg.config import *
import PrjtCF_model_pkg.sales as S
import PrjtCF_model_pkg.cost as C
import PrjtCF_model_pkg.loan as L
import PrjtCF_model_pkg.account as acc

import importlib
importlib.reload(S)
importlib.reload(C)
importlib.reload(L)
importlib.reload(acc)

#### Input Basic Data ####
mtrt = 26 # 개월
prd_prjt = 24 # 개월

#### Input Sales Data ####
pmnt_scd = [1, 8, 16, 24]
pmnt_rate = [0.1, 0.2, 0.2, 0.5]
repybal_rate = 0.8
sales_dct = {}

#ProductA
sales_prdtA = S.sales(title = 'ProductA', aream2 = 7_000, unitprcm2 = 10.000, unitmtpl = pmnt_rate, inptidx = pmnt_scd, mtrt = mtrt,
                     sep1 = 'ProductA', sep2 = '-', note = "")
sales_dct['sales_prdtA'] = sales_prdtA

#ProductA
sales_prdtB = S.sales(title = 'ProductB', aream2 = 3_000, unitprcm2 = 20.000, unitmtpl = pmnt_rate, inptidx = pmnt_scd, mtrt = mtrt,
                     sep1 = 'ProductB', sep2 = '-', note = "")
sales_dct['sales_prdtB'] = sales_prdtB

#Merge
sales = S.salesmerge(sales_dct)


#### Input Cost Data ####
mthly = pd.Series(np.ones(prd_prjt), index=np.arange(1, prd_prjt+1))
prcs_rate = pd.Series(np.ones(prd_prjt) * 1 / prd_prjt, index=np.arange(1, prd_prjt+1))

cstfxd_dct = {} # Fixed cost
cstfsl_dct = {} # Cost for sale

#토지매입비
cost_lndprc = C.cost(title = '토지매입비', unitamt = 30_000.000, mtrt = mtrt,
                     sep1 = '토지비', sep2 = '-', note = '-')
cstfxd_dct['cost_lndprc'] = cost_lndprc

#공사비
cost_cstnlnd_fxd = C.cost(title='공사비(고정불)', unitamt=50_000.000 * 0.7, unitmtpl=prcs_rate.values, inptidx=prcs_rate.index, mtrt=mtrt,
                     sep1 = '공사비', sep2 = '직접공사비', note = '-')
cost_cstnlnd_fsl = C.cost(title = '공사비(분양불)', unitamt = 50_000.000 * 0.3, mtrt = mtrt,
                     sep1 = '공사비', sep2 = '직접공사비', note = '-')
cstfxd_dct['cost_cstnlnd'] = cost_cstnlnd_fxd # 고정불 공사비
cstfsl_dct['cost_cstnlnd'] = cost_cstnlnd_fsl # 분양불 공사비

#설계비
cost_cstnegnr = C.cost(title = '설계비', unitamt = 2_000.000, mtrt = mtrt,
                     sep1 = '공사비', sep2 = '간접공사비', note = '-')
cstfxd_dct['cost_cstnegnr'] = cost_cstnegnr
                
#감리비
cost_cstnspvn = C.cost(title = '감리비', unitamt = 1_000.000, unitmtpl=prcs_rate.values, inptidx=prcs_rate.index, mtrt = mtrt,
                     sep1 = '공사비', sep2 = '간접공사비', note = '-')
cstfxd_dct['cost_cstnspvn'] = cost_cstnspvn

#MH운영비
cost_mhoprt = C.cost(title = 'MH운영비', unitamt = 11.000, unitmtpl = mthly.values, inptidx = mthly.index, mtrt = mtrt,
                     sep1 = '판매비', sep2 = '모델하우스', note = '-')
cstfxd_dct['cost_mhoprt'] = cost_mhoprt

#분양대행수수료
cost_mktprct = C.cost(title = '분양대행수수료', unitamt = sum(sales.amt()), unitmtpl = 0.05, mtrt = mtrt,
                     sep1 = '판매비', sep2 = '분양대행', note = '-')
cstfsl_dct['cost_mktprct'] = cost_mktprct

cstfxd = C.costmerge(cstfxd_dct)
cstfsl = C.costmerge(cstfsl_dct)


#### Input Loan Data ####
cstfnc_dct = {} # Cost for sale

TrA_amt = 60_000.000
TrA = L.loan(title='TrA', amt=TrA_amt, mtrt=mtrt, fee=0.02, IR=0.05)
TrA.amt_repy_scd(mtrt, TrA_amt)

TrB_amt = 30_000.000
TrB = L.loan(title='TrB', amt=TrB_amt, mtrt=mtrt, fee=0.05, IR=0.07)
TrB.amt_repy_scd(mtrt, TrB_amt)

# 신탁수수료
cost_fntrst = C.cost(title='신탁수수료', unitamt=sum(sales.amt()), unitmtpl=0.02, mtrt=mtrt,
                     sep1='금융비', sep2='신탁수수료', note='-')
cstfnc_dct['cost_fntrst'] = cost_fntrst

# 주관수수료
cost_fnarng = C.cost(title='주관수수료', unitamt = TrA_amt + TrB_amt, unitmtpl=0.02, mtrt=mtrt,
                     sep1='금융비', sep2='주선수수료', note='금융주선수수료')
cstfnc_dct['cost_fnarng'] = cost_fnarng

cstfnc = C.costmerge(cstfnc_dct)