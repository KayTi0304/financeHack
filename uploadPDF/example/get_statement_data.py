from sec_api import QueryApi
from sec_api import XbrlApi
import json

queryApi = QueryApi(api_key="7d84412d1c2236517aba57d5aab13020072b7eb116b10f3e0855189cd840e682")
xbrlApi = XbrlApi("7d84412d1c2236517aba57d5aab13020072b7eb116b10f3e0855189cd840e682")

def getStatementData(userInput):
    user_input = userInput

    try:
        f = open("./Annual_Reports/" + str(user_input).casefold() + "_report.json", "r")
        annual_report = json.load(f)
        f.close()

    except:
        query = {
            "query": {
                "query_string": {
                    "query": "formType:\"10-K\" AND companyName:" + str(user_input)
                }
            },
            "from": "0",
            "size": "20",
            "sort": [{ "filedAt": { "order": "desc" } }]
        }

        filings = queryApi.get_filings(query)
        print(json.dumps(filings, indent=4))

        if filings['filings'] == []:
            print("Invalid company name!")
            quit()

        annual_report_url = filings['filings'][0]["linkToFilingDetails"]

        # 10-K HTM File URL example
        xbrl_json = xbrlApi.xbrl_to_json(
            htm_url=annual_report_url
        )

        annual_report = xbrl_json
        f = open("./Annual_Reports/" + str(user_input).casefold() + "_report.json", "w")
        json.dump(annual_report, f, indent=4, separators=(',', ': '))
        f.close()

    simple_data = {}

    income_statement = annual_report["StatementsOfIncome"]


    #retrieving total revenue from income statement
    if "RevenueFromContractWithCustomerExcludingAssessedTax" in income_statement:
        for revenue in income_statement["RevenueFromContractWithCustomerExcludingAssessedTax"]:
            if "segment" not in revenue:
                simple_data["Revenue"] = round(float(revenue["value"]), 2)
                break

    if "Revenues" in income_statement:
        simple_data["Revenue"] = round(float(income_statement["Revenues"][0]["value"]),2)

    if "Revenue" not in simple_data:
        simple_data["Revenue"] = None


    #summing other sources of income
    if "OtherIncome" in income_statement:
        simple_data["Other Income"] = round(float(income_statement["OtherIncome"][0]["value"]),2)
    else:
        simple_data["Other Income"] = 0

    if "NonoperatingIncomeExpense" in income_statement:
        simple_data["Other Income"] += round(float(income_statement["NonoperatingIncomeExpense"][0]["value"]),2)

    if "OtherNonoperatingIncomeExpense" in income_statement:
        simple_data["Other Income"] += float(income_statement["OtherNonoperatingIncomeExpense"][0]["value"])

    if "InvestmentIncomeInterest" in income_statement:
        simple_data["Other Income"] += float(income_statement["InvestmentIncomeInterest"][0]["value"])



    #retrieving gross profit from income statement
    if "GrossProfit" in income_statement:
        simple_data["Gross Profit"] =  float(income_statement["GrossProfit"][0]["value"])
    else:
        for key in income_statement:
            if "CostOf" in key:
                simple_data["Gross Profit"] = simple_data["Revenue"] - float(income_statement[key][0]["value"])

    #calculating gross profit margin
    try:
        simple_data["Gross Profit Margin (%)"] = round(simple_data["Gross Profit"] / simple_data["Revenue"] * 100, 2)
    except:
        simple_data["Gross Profit Margin (%)"] = None



    #retrieving net income from income statement
    if "NetIncomeLoss" in income_statement:
        simple_data["Net Income"] = float(income_statement["NetIncomeLoss"][0]["value"])
    else:
        simple_data["Net Income"] = None


    #calculating net profit margin
    try:
        simple_data["Net Profit Margin (%)"] = round(simple_data["Net Income"] / (simple_data["Revenue"] + simple_data["Other Income"]) * 100, 2)
    except:
        simple_data["Net Profit Margin (%) "] = None

    #retrieving diluted earnings per share
    if "EarningsPerShareDiluted" in income_statement:
        simple_data["Diluted Earnings Per Share ($/Share)"] = "{:.2f}".format(float(income_statement["EarningsPerShareDiluted"][0]["value"]))
    else:
        simple_data["Diluted Earnings Per Share ($/Share)"] = None

    #retrieving common stock outstanding
    if "EntityCommonStockSharesOutstanding" in annual_report["CoverPage"]:

        simple_data["Common Stock Shares Outstanding"] = 0

        if type(annual_report["CoverPage"]["EntityCommonStockSharesOutstanding"]) == list:
            for dict in annual_report["CoverPage"]["EntityCommonStockSharesOutstanding"]:
                simple_data["Common Stock Shares Outstanding"] += int(dict["value"])
        else:
            simple_data["Common Stock Shares Outstanding"] = int(annual_report["CoverPage"]["EntityCommonStockSharesOutstanding"]["value"])

    else:
        simple_data["Common Stock Shares Outstanding"] = None


    #retrieving data from balance sheet
    balance_sheet = annual_report["BalanceSheets"]

    if "AssetsCurrent" in balance_sheet:
        simple_data["Current Assets"] = float(balance_sheet["AssetsCurrent"][0]["value"])
    else:
        simple_data["Current Assets"] = None

    if "Assets" in balance_sheet:
        simple_data["Total Assets"] = float(balance_sheet["Assets"][0]["value"])
    else:
        simple_data["Total Assets"] = None

    if "LiabilitiesCurrent" in balance_sheet:
        simple_data["Current Liabilities"] = float(balance_sheet["LiabilitiesCurrent"][0]["value"])
    else:
        simple_data["Current Liabilities"] = None

    if "Liabilities" in balance_sheet:
        simple_data["Total Liablities"] = float(balance_sheet["Liabilities"][0]["value"])
    else:
        simple_data["Total Liablities"] = None

    if "StockholdersEquity" in balance_sheet:
        simple_data["Total Stockholders Equity"] =  float(balance_sheet["StockholdersEquity"][0]["value"])
    else:
        simple_data["Total Stockholders Equity"] = None

    if "LiabilitiesAndStockholdersEquity" in balance_sheet:
        simple_data["Total Liabilities and Stockholders Equity"] =  float(balance_sheet["LiabilitiesAndStockholdersEquity"][0]["value"])
    else:
        simple_data["Total Liabilities and Stockholders Equity"] = None



    #calculating current ratio
    try:    
        simple_data["Current Ratio"] = round(simple_data["Current Assets"] / simple_data["Current Liabilities"], 2)
    except:
        simple_data["Current Ratio"] = None

    #calculating return on equity
    try:
        simple_data["Return on Equity"] = round(simple_data["Net Income"] / simple_data["Total Stockholders Equity"], 2)
    except:
        simple_data["Return on Equity"] = None

    try:
        simple_data["Return on Assets"] = round(simple_data["Net Income"] / simple_data["Total Assets"], 2)
    except:
        simple_data["Return on Assets"] = None

    print(simple_data)
    return simple_data
