# %%
# Create State Income Tax Bracket w/ Marginal Rates
def CreateBracket(rate_arr, salary_arr) -> dict:

    new_dict = {}
    i = 0
    for rate in rate_arr:
        new_dict[rate] = [salary_arr[i], salary_arr[i+1]]
        i+=1
    return new_dict

# Recursively solve for total tax owed in $
def EffectiveTaxTotal(annual, Bracket_dict) -> float:

    if( annual == 0):
        return 0

    for (key, val) in Bracket_dict.items():
        [lower, upper] = val
        inRange = (lower < annual <= upper)
        if inRange:
            Total = (annual-lower) * (key/100)
            next = lower

    return Total + EffectiveTaxTotal(next, Bracket_dict)

# Find a salary at a given tax rate
def FindSalaryAtTaxRate(eff_tax: np.ndarray,
                        salaries: np.ndarray,
                        search_rate: float) -> float:
    diffs = np.abs(eff_tax - search_rate)
    return salaries[np.where(diffs == diffs.min())[0]][0]


incomes = [0, 11925, 48475, 103350, 197300, 250525, 626350, 1000000]
rates = [10, 12, 22, 24, 32, 35, 37]

bracket = CreateBracket(rates, incomes)

eff_tax = []
salaries = range(1, 500_000)
for salary in salaries:
    eff_tax.append(EffectiveTaxTotal(salary, bracket) /  salary * 100)

import numpy as np
import plotly.graph_objects as go

eff_tax = np.array(eff_tax)
salaries = np.array(salaries)

fig = go.Figure(data=go.Scatter(x=list(salaries), y=eff_tax))

sal_15pct = FindSalaryAtTaxRate(eff_tax, salaries, 15)
sal_20pct = FindSalaryAtTaxRate(eff_tax, salaries, 20)
fig.add_vline(x=sal_15pct, line_width=3, line_dash="dash", line_color="red")
fig.add_vline(x=sal_20pct, line_width=3, line_dash="dash", line_color="red")
fig.update_layout(
    annotations=[
        dict(x=sal_15pct, y=0, yref="paper", text=f"${sal_15pct:,.0f}", showarrow=True, arrowhead=2),
        dict(x=sal_20pct, y=0, yref="paper", text=f"${sal_20pct:,.0f}", showarrow=True, arrowhead=2),
    ])
fig.add_hline(y=15, line_width=3, line_dash="dash", line_color="red")
fig.add_hline(y=20, line_width=3, line_dash="dash", line_color="red")

fig.update_layout(xaxis_title='salary', yaxis_title='Effective tax rate (%)', xaxis_tickformat="$,.0f", width=1200, height=800)
fig.write_html('tax.html')



# %%

def recur(payment, interest, i = 0):
    if i == len(payment)-1:
        return payment[i]*(1 + interest/100)**i
    return payment[i]*(1 + interest/100)**i + recur(payment, interest, i+1)

payments = [7000] * 40
recur(payments, 10)

# %%
payments = [7000] * 40
recur(payments, 10) / np.sum(payments)
# %%
