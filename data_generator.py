import os
import pandas as pd
import yfinance as yf


def get_ibovespa_tickers():
    ibovespa = pd.read_csv("./data/ibovespa.csv")
    ibovespa_tickers = []

    for row in ibovespa.iterrows():
        ibovespa_tickers.append(row[1]["empresas"] + ".SA")

    return ibovespa_tickers


def create_tickers_folder(ibovespa_tickers):
    path = os.getcwd()

    for ticker in ibovespa_tickers:
        try:
            os.mkdir(path + "/data/FA/" + ticker.split(".")[0])
        except OSError:
            print("Creation of the directory %s failed" % path)
        else:
            print("Successfully created the directory %s " % path)


def get_FA_data(ibovespa_tickers):
    path = os.getcwd()

    for ticker in ibovespa_tickers:
        yf_ticker = yf.Ticker(ticker)
        pd.DataFrame([yf_ticker.info]).to_csv(
            path + "/data/FA/" + ticker.split(".")[0] + "/" + "info.csv")
        yf_ticker.quarterly_financials.to_csv(
            path + "/data/FA/" + ticker.split(".")[0] + "/" + "quarterly_financials.csv")
        yf_ticker.actions.to_csv(
            path + "/data/FA/" + ticker.split(".")[0] + "/" + "actions.csv")
        yf_ticker.quarterly_balancesheet.to_csv(
            path + "/data/FA/" + ticker.split(".")[0] + "/" + "quarterly_balancesheet.csv")
        yf_ticker.quarterly_cashflow.to_csv(
            path + "/data/FA/" + ticker.split(".")[0] + "/" + "quarterly_cashflow.csv")

        print('- {}: has been downloaded.'.format(ticker))


def main():
    ibovespa_tickers = get_ibovespa_tickers()
    print("Create folders? (y/n)")
    ans = input()
    if(ans == "y"):
        create_tickers_folder(ibovespa_tickers)

    print("Obtain companies data? (y/n)")
    ans = input()
    if(ans == "y"):
        get_FA_data(ibovespa_tickers)


if __name__ == "__main__":
    main()
