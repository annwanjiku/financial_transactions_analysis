import csv
import pandas as pd
import numpy as np
import math
import seaborn as sns
import matplotlib.pyplot as plt
from collections import defaultdict
from datetime import datetime
from pprint import pprint

df = pd.read_csv("transactionHistory.csv")
print(df)

print("\n ANALYSIS OF SPEND FOR THE PAST 12 MONTHS\n")

moneyIn = df["MoneyIn"].sum()
print(f'The total Money In is {moneyIn:,.2f} ')
print("\n")

moneyOut = df["MoneyOut"].sum()
print(f"The total Money Out is {moneyOut:,.2f}")
print("\n")

InitialBalance = df.loc[0, "LedgerBalance"]
print(f'Initial Balance was {InitialBalance:,.2f}')
print("\n")

Balance = moneyIn + moneyOut + InitialBalance
print(f'Your Current Balance is {Balance:,.2f} because your Initial Balance was  {InitialBalance:,.2f} and not 0')
print("\n")

df["TransactionDate"] = pd.to_datetime(df["TransactionDate"], format='%d.%m.%Y')

money_in_dict = defaultdict(float)
money_out_dict = defaultdict(float)
ledger_balance_dict = defaultdict(float)

for index, row in df.iterrows():
    month_year = row['TransactionDate'].strftime('%B%Y')
    money_in_dict[month_year] += row['MoneyIn']
    money_out_dict[month_year] += row['MoneyOut']
    ledger_balance_dict[month_year] = row['LedgerBalance']

print("Money In per Month:")
for month_year, money_in in money_in_dict.items():
    print(f"{month_year}: {money_in:,.2f}")

print("\nMoney Out per Month:")
for month_year, money_out in money_out_dict.items():
    print(f"{month_year}: {money_out:,.2f}")

print("\nAccumulated Ledger Balance over 12 months:")
for month_year, balance in ledger_balance_dict.items():
    print(f"{month_year}: {balance:,.2f}")

max_ledger_balance_key = max(ledger_balance_dict, key=ledger_balance_dict.get)
max_ledger_balance = ledger_balance_dict[max_ledger_balance_key]
print(f"\nThe maximum ledger balance is {max_ledger_balance:,.2f} in the month of {max_ledger_balance_key}")

min_ledger_balance_key = min(ledger_balance_dict, key=ledger_balance_dict.get)
min_ledger_balance = ledger_balance_dict[min_ledger_balance_key]
print(f"\nThe minimum ledger balance is {min_ledger_balance:,.2f} in the month of {min_ledger_balance_key}")

max_money_in_key = max(money_in_dict, key=money_in_dict.get)
max_money_in = money_in_dict[max_money_in_key]
print(f"\nThe maximum money in is {max_money_in:,.2f} in the month of {max_money_in_key}")

non_zero_money_in = {key: value for key, value in money_in_dict.items() if value != 0}
min_money_in_key = min(non_zero_money_in, key=non_zero_money_in.get)
min_money_in = non_zero_money_in[min_money_in_key]
print(f"\nThe minimum money in is {min_money_in:,.2f} in the month of {min_money_in_key}")

max_money_out_key = min(money_out_dict, key=money_out_dict.get)
max_money_out = money_out_dict[max_money_out_key]
print(f"\nThe maximum money out is {max_money_out:,.2f} in the month of {max_money_out_key}")

non_zero_money_out = {key: value for key, value in money_out_dict.items() if value != 0}
min_money_out_key = max(non_zero_money_out, key=non_zero_money_out.get)
min_money_out = non_zero_money_out[min_money_out_key]
print(f"\nThe minimum money out is {min_money_out:,.2f} in the month of {min_money_out_key}")

# figure 1
positive_money_out_dict = {key: abs(value) for key, value in money_out_dict.items()}
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(money_in_dict.keys(), money_in_dict.values(), marker='*',  color='#157326' ,markerfacecolor='black',  label='Money In')
ax.plot(positive_money_out_dict.keys(), positive_money_out_dict.values(), marker='.',markerfacecolor='black', color='#f20f0f', label='Money Out')
ax.bar(ledger_balance_dict.keys(), ledger_balance_dict.values(), color='#b28df7', label='Ledger Balance',width=0.5, edgecolor='#706c70')
ax.set_xlabel('Months')
ax.set_ylabel('Amount')
ax.set_title('COMPARISON OF LEDGER BALANCE, MONEY IN, AND MONEY OUT OVER 12 MONTHS!')
ax.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()



#figure2
x = np.arange(len(money_in_dict))
width = 0.35
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(x - width/2, money_in_dict.values(), width, color='#3b3539',label='Money In')
ax.bar(x + width/2, positive_money_out_dict.values(), width, color='#638ff7', label='Money Out')
ax.set_xticks(x)
ax.set_xticklabels(money_in_dict.keys(), rotation=90)
ax.set_xlabel('Month')
ax.set_ylabel('Amount')
ax.set_title('COMPARISON OF MONEY IN AND MONEY OUT OVER 12 MONTHS')
ax.legend()
plt.tight_layout()
plt.show()