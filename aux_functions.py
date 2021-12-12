import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("darkgrid")

def plot_lookahead_prices(ticker, close, **kwargs):
    """
    Plot three lookahead prices and close price for comparison

    Parameters
    ----------
    ticker: String
        String for ticker identification
    close : Dataframe
        Close Datframe
    kwargs : Dataframe
        Unlimited number of dataframes with X days ahead in time

    """
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=close.index, y=close[ticker], name='close',
                             line=dict(color='green', width=1)))

    for key, value in kwargs.items():
        fig.add_trace(go.Scatter(x=value.index, y=value[ticker], name=key))

    fig.update_layout(title='Lookahead Prices for {} ticker'.format(ticker),
                      xaxis_title='Date',
                      yaxis_title='Stock Price')

    fig.show()


def plot_price_return(ticker, **kwargs):
    """
    Plot three price returns for specific ticker

    Parameters
    ----------
    ticker: String
        String for ticker identification
    kwargs : Dataframe
        Unlimited number of dataframes with price return with X days ahead in time
    """

    fig = go.Figure()

    for key, value in kwargs.items():
        fig.add_trace(go.Scatter(x=value.index,
                                 y=value[ticker],
                                 name=key))

    fig.update_layout(title='Lookahead Returns for {} ticker'.format(ticker),
                      xaxis_title='Date',
                      yaxis_title='Stock Price')

    fig.show()


def plot_log_return(df_close_hist, start_date, end_date):
    """
    Plot the distribution of log_returns of the given dataframe

    Parameters
    ----------
    df_close_hist : Dataframe
        Dataframe with the log_returns for a given time range

    Returns
    -------
    lookahead_prices : DataFrame
        The lookahead prices for each ticker and date
    """

    sns.displot(df_close_hist.log_return, kde=True, stat="density")


    mean_return = df_close_hist.log_return.mean()
    plt.title(
        'Distribution of Log Returns in IBOVESPA from {} - {}'.format(start_date, end_date))
    plt.axvline(mean_return, ls=':',
                label='Index Mean: {}'.format(round(mean_return, 2)))
    plt.legend()
