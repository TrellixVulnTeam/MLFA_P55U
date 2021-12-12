import os
import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_ibovespa_tickers(path="./data/ibovespa.csv"):
    ibovespa = pd.read_csv(path)
    ibovespa_tickers = []

    for row in ibovespa.iterrows():
        ibovespa_tickers.append(row[1]["empresas"] + ".SA")

    print("len: ", len(ibovespa_tickers))
    print(list(ibovespa_tickers))

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


def get_raw_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
    r = requests.get(url, headers=headers)
    r.encoding = 'utf-8'

    return r.content


def build_url(ticker):
    url_base = 'http://fundamentus.com.br/detalhes.php?papel={}'.format(ticker)
    return url_base


def parse_html(html):
    soup = BeautifulSoup(html, "html.parser")
    tables = soup.findAll("table")

    df = pd.read_html(str(tables).replace('?', ''), decimal=',', thousands='.')
    return df


def return_html_df(ticker):
    url = build_url(ticker)
    html = get_raw_data(url)
    dfs = parse_html(html)
    df_final = pd.DataFrame()

    for df in dfs:
        df_final = df_final.append(df)

    return df_final


def get_FA_data(tickers):
    path = os.getcwd()
    qtd_errors = 0

    for ticker in tickers:
        try:
            df_html = return_html_df(ticker.split(".")[0])

            # --- Fundamentus Dataframe
            df_html.to_csv(
                path + "/data/FA/" + ticker.split(".")[0] + "/" + "df_fundamentus.csv", index=False, header=False)

            # --- Dados Gerais
            df_dados_gerais = df_html.T.iloc[:2, 1:7]
            df_dados_gerais.columns = df_dados_gerais.iloc[0]
            df_dados_gerais = df_dados_gerais.iloc[1:2, :]
            df_dados_gerais.to_csv(
                path + "/data/FA/" + ticker.split(".")[0] + "/" + "dados_gerais.csv")

            # --- Cotação
            df_cotacao = df_html.T.iloc[2:4, :7]
            df_cotacao.columns = df_cotacao.iloc[0]
            df_cotacao = df_cotacao.iloc[1:2, :]
            df_cotacao.to_csv(
                path + "/data/FA/" + ticker.split(".")[0] + "/" + "cotacao.csv")

            # --- Indicadores Fundamentalistas
            df_indicadores_fundamentalistas_1 = df_html.T.iloc[2:6, 8:8+11]
            df_indicadores_fundamentalistas_1.columns = df_indicadores_fundamentalistas_1.iloc[
                0]
            df_indicadores_fundamentalistas_1 = df_indicadores_fundamentalistas_1.iloc[1:2, :]
            df_indicadores_fundamentalistas_1.reset_index(inplace=True)
            df_indicadores_fundamentalistas_1.drop(
                columns=['index'], inplace=True)

            df_indicadores_fundamentalistas_2 = df_html.T.iloc[2:6, 8:8+11]
            df_indicadores_fundamentalistas_2.columns = df_indicadores_fundamentalistas_2.iloc[
                2]
            df_indicadores_fundamentalistas_2 = df_indicadores_fundamentalistas_2.iloc[3:4, :]
            df_indicadores_fundamentalistas_2.reset_index(inplace=True)
            df_indicadores_fundamentalistas_2.drop(
                columns=['index'], inplace=True)
            df_indicadores_fundamentalistas_2

            df_indicadores_fundamentalistas = df_indicadores_fundamentalistas_1.join(
                df_indicadores_fundamentalistas_2)
            df_indicadores_fundamentalistas.to_csv(
                path + "/data/FA/" + ticker.split(".")[0] + "/" + "indicadores_fundamentalistas.csv")

            # # --- Dados Balanço Patrimonial
            # df_balanco_patrimonial_1 = df_html.T.iloc[:-2, 20:20+3]
            # df_balanco_patrimonial_1.columns = df_balanco_patrimonial_1.iloc[0]
            # df_balanco_patrimonial_1 = df_balanco_patrimonial_1.iloc[1:2, :]
            # df_balanco_patrimonial_1.reset_index(inplace=True)
            # df_balanco_patrimonial_1.drop(columns=['index'], inplace=True)
            # df_balanco_patrimonial_1

            # df_balanco_patrimonial_2 = df_html.T.iloc[:-2, 20:20+3]
            # df_balanco_patrimonial_2.columns = df_balanco_patrimonial_2.iloc[2]
            # df_balanco_patrimonial_2 = df_balanco_patrimonial_2.iloc[3:4, :]
            # df_balanco_patrimonial_2.reset_index(inplace=True)
            # df_balanco_patrimonial_2.drop(columns=['index'], inplace=True)
            # df_balanco_patrimonial_2

            # df_balanco_patrimonial = df_balanco_patrimonial_1.join(
            #     df_balanco_patrimonial_2)
            # df_balanco_patrimonial.to_csv(
            #     path + "/data/FA/" + ticker.split(".")[0] + "/" + "balanco_patrimonial.csv")

            # # --- Dados demonstrativos de resultados
            # # -- 12 meses
            # df_demonstrativos_result_12_meses = df_html.T.iloc[:, 25:25+4]
            # df_demonstrativos_result_12_meses.columns = df_demonstrativos_result_12_meses.iloc[
            #     0]
            # df_demonstrativos_result_12_meses = df_demonstrativos_result_12_meses.iloc[1:2, :]
            # df_demonstrativos_result_12_meses.reset_index(inplace=True)
            # df_demonstrativos_result_12_meses.drop(
            #     columns=['index'], inplace=True)
            # df_demonstrativos_result_12_meses.to_csv(
            #     path + "/data/FA/" + ticker.split(".")[0] + "/" + "demonstrativos_result_12_meses.csv")

            # # -- 3 meses
            # df_demonstrativos_result_3_meses = df_html.T.iloc[:, 25:25+4]
            # df_demonstrativos_result_3_meses.columns = df_demonstrativos_result_3_meses.iloc[
            #     2]
            # df_demonstrativos_result_3_meses = df_demonstrativos_result_3_meses.iloc[3:4, :]
            # df_demonstrativos_result_3_meses.reset_index(inplace=True)
            # df_demonstrativos_result_3_meses.drop(
            #     columns=['index'], inplace=True)
            # df_demonstrativos_result_3_meses.to_csv(
            #     path + "/data/FA/" + ticker.split(".")[0] + "/" + "demonstrativos_result_3_meses.csv")
        except:
            qtd_errors += 1
            print("Error occured in ticker: {}".format(ticker))

    return qtd_errors


def main():
    ibovespa_tickers = get_ibovespa_tickers(path="./data/ibovespa.csv")
    print("Create folders? (y/n)")
    ans = input()
    if(ans == "y"):
        create_tickers_folder(ibovespa_tickers)

    print("Obtain companies data? (y/n)")
    ans = input()
    if(ans == "y"):
        qtd_errors = get_FA_data(ibovespa_tickers)
        print("A total of {} tickers had errors.".format(qtd_errors))


if __name__ == "__main__":
    main()
