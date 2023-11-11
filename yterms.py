# 매출 액 (Total Revenue)
TotalRevenue = 'Total Revenue'

# 매출 원가 (Cost Of Revenue)
CostOfRevenue = 'Cost Of Revenue'

# 매출 총이익 (Gross Profit)
GrossProfit = 'Gross Profit'

# 판매비 와 관리비 (Selling And Marketing Expense,
# General And Administrative Expense)
SellingGeneralAndAdministration = 'Selling General And Administration'
SellingAndMarketingExpense = 'Selling And Marketing Expense'
GeneralAndAdministrativeExpense = 'General And Administrative Expense'

# 영업 이익 (Operating Income)
# 영업 이익 ('Operating Revenue' - 'Operating Expense')
OperatingRevenue = 'Operating Revenue'
OperatingExpense = 'Operating Expense'
OperatingIncome = 'Operating Income'

# 지분법 손익 (Net Income Including NonControlling Interests)
NetIncomeIncludingNonControllingInterests = 'Net Income Including Noncontrolling Interests'

# 금융 손익 (Net Interest Income, Net NonOperating Interest Income Expense)
NetInterestIncome = 'Net Interest Income'
InterestExpense = 'Interest Expense'
InterestIncomeNonOperating = 'Interest Income Non Operating'
NetNonOperatingInterestIncomeExpense = 'Net Non Operating Interest Income Expense'
SecuritiesAmortization = 'Securities Amortization'
TotalOtherFinanceCost = 'Total Other Finance Cost'

# 기타 손익 (Other Income Expense, Other NonOperating Income Expenses, Gain On Sale Of Security)
OtherIncomeExpense = 'Other Income Expense'
GainOnSaleOfSecurity = 'Gain On Sale Of Security'
OtherunderPreferredStockDividend = 'Otherunder Preferred Stock Dividend'
OtherNonOperatingIncomeExpenses = 'Other Non Operating Income Expenses'
SpecialIncomeCharges = 'Special Income Charges'
OtherSpecialCharges = 'Other Special Charges'
TotalUnusualItems = 'Total Unusual Items'
TotalUnusualItemsExcludingGoodwill = 'Total Unusual Items Excluding Goodwill'

# 법인세 비용 차감전 순 이익 (Pretax Income)
PretaxIncome = 'Pretax Income'

# 법인세 비용 (Tax Provision)
TaxProvision = 'Tax Provision'

# 당기 순 이익 (Net Income)
NetIncome = 'Net Income'

# 시가 총액
MarketCap = 'marketCap'

# 주주환원
# Preferred Stock Dividend Paid: 우선주 주주에게 지급한 배당금입니다.
# Repurchase Of Capital Stock: 회사의 자기 주식을 다시 구입하는 것으로, 주주환원 프로그램의 일부로 주주에게 주식을 되돌려주는 계정입니다.
# Common Stock Dividend Paid: 보통주 주주에게 지급한 배당금입니다.
# Preferred Stock Issuance: 우선주 주식 발행입니다. 회사가 새로운 우선주 주식을 발행하여 자금을 조달하는 경우를 나타냅니다.
# Net Preferred Stock Issuance: 우선주 주식 발행에서 발행비용을 고려한 순액을 나타냅니다.
# Common Stock Payments: 보통주 주주에게 지급한 금액입니다.
RepurchaseOfCapitalStock = 'Repurchase Of Capital Stock'
CommonStockDividendPaid = 'Common Stock Dividend Paid'
CommonStockPayments = 'Common Stock Payments'
CashDividendsPaid = 'Cash Dividends Paid'
FinancingCashFlow = 'Financing Cash Flow'
# 판매관리비에 관한 key:
#
# Selling General And Administration
# Selling And Marketing Expense
#
# 금융 손익에 관한 key:
#
# Interest Expense
# Interest Income Non Operating
# Net Non Operating Interest Income Expense
# Securities Amortization
# Total Other Finance Cost
#
# 기타 손익에 관한 key:
#
# Other Non Operating Income Expenses
# Other Income Expense
# Other Special Charges
# Total Unusual Items
# Total Unusual Items Excluding Goodwill
# Special Income Charges

## https://github.com/light-src/toberich/issues/10
판관비리스트 = [
    SellingAndMarketingExpense,
    GeneralAndAdministrativeExpense,
    SellingGeneralAndAdministration
]

금융손익리스트 = [
    NetInterestIncome,
    InterestExpense,
    InterestIncomeNonOperating,
    NetNonOperatingInterestIncomeExpense,
    SecuritiesAmortization,
    TotalOtherFinanceCost
]

기타손익리스트 = [
    OtherNonOperatingIncomeExpenses,
    OtherIncomeExpense,
    OtherSpecialCharges,
    OtherunderPreferredStockDividend,
    SpecialIncomeCharges,
    GainOnSaleOfSecurity,
    TotalUnusualItemsExcludingGoodwill,
    TotalUnusualItems
]

## https://github.com/light-src/toberich/issues/9
주주환원리스트 = [
    RepurchaseOfCapitalStock,
    CommonStockDividendPaid,
    CashDividendsPaid,
    CommonStockPayments
]
