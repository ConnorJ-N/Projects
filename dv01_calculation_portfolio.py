import numpy as np
import pandas as pd

portfolio = {'notional':[50000000, 30000000, 40000000, 60000000], 
             'fixed_rate':[0.03, 0.027, 0.032, 0.026], 
             'maturity':[3, 5, 2, 4]}
df = pd.DataFrame(portfolio)

class dv01_calc():
    
    def __init__(self, notional, fixed_rate, maturity, payments=2, rate=0.015):
        
        self.notional = notional
        self.fixed_rate = fixed_rate
        self.maturity = maturity
        self.payments = payments
        self.rate = rate
    
    def calc_dv01(self):
        cash_flows = [self.notional*(self.fixed_rate/2) for i in range(int(self.maturity*self.payments))]
        cash_flows[-1]+=self.notional
        
        base_pv = self.calc_pv(cash_flows, self.rate, self.payments)
        pv_up = self.calc_pv(cash_flows, self.rate+0.0001, self.payments)
        dv01 = base_pv-pv_up
        return dv01
        
    def calc_pv(self, cash_flows, rate, payments):
        pvs = sum(cf/(1+rate/payments)**(t+1) for t, cf in enumerate(cash_flows))
        return pvs

dv01_list = []
for index, rows in df.iterrows(): 
    notional = rows['notional']
    fixed_rate = rows['fixed_rate']
    maturity = rows['maturity']
    dv01_list.append(dv01_calc(notional, fixed_rate, maturity).calc_dv01())
    
portfolio_dv01 = sum(dv01_list)
print(portfolio_dv01)
y5_dv01 = dv01_calc(1, 0.025, 5).calc_dv01()
Notional_5y = portfolio_dv01/y5_dv01
print(Notional_5y)


