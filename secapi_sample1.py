from sec_api import QueryApi
from sec_api import XbrlApi
import json

xbrlApi = XbrlApi("7d84412d1c2236517aba57d5aab13020072b7eb116b10f3e0855189cd840e682")

# 10-K HTM File URL example
xbrl_json = xbrlApi.xbrl_to_json(
    htm_url="https://www.sec.gov/Archives/edgar/data/320193/000032019320000096/aapl-20200926.htm"
)

# access income statement, balance sheet and cash flow statement
print(xbrl_json["StatementsOfIncome"])
print(xbrl_json["BalanceSheets"])
print(xbrl_json["StatementsOfCashFlows"])

tesla_sample_report = xbrl_json
f = open("tesla_sample_report.json", "w")
json.dump(tesla_sample_report, f)
f.close()

# 10-K XBRL File URL example
xbrl_json = xbrlApi.xbrl_to_json(
    xbrl_url="https://www.sec.gov/Archives/edgar/data/1318605/000156459021004599/tsla-10k_20201231_htm.xml"
)

# 10-K accession number example
xbrl_json = xbrlApi.xbrl_to_json(accession_no="0001564590-21-004599")