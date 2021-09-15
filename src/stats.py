import math
import numpy as np
import scipy.stats as st

# Calculates the upper and lower bound for the underlying spot price based on volatility
# probability param: if probability=0.7, probability of stock price in prob_cone is 70%
def prob_cone(stock_price:float, volatility:float, days_ahead:int, probability=0.7, return_stddev=False):

    # z_score param indicates the number of std deviations from the mean (i.e. 1.5 std dev covers about 87%)
    # Source: https://stackoverflow.com/questions/20864847/probability-to-z-score-and-vice-versa
    z_score = st.norm.ppf(1-((1-probability)/2))

    # Source: https://www.biocrudetech.com/index.php?option=com_blankcomponent&view=default&Itemid=670
    std_dev = z_score * stock_price * volatility * math.sqrt(days_ahead/252)

    if return_stddev:
        return std_dev
    else:
        upper_bound = round(stock_price + std_dev, 2)
        lower_lound = round(stock_price - std_dev, 2)
        return (lower_lound,upper_bound)

def get_prob(stock_price:float, strike_price:float, volatility:float, days_ahead:int) -> float:

    if None or 0 not in (stock_price, strike_price, volatility, days_ahead):        

        z_score = abs(stock_price - strike_price)/(stock_price * volatility * math.sqrt(days_ahead/252))

        return 2 * st.norm.cdf(z_score) - 1
    else:
        return 0

# Calculates annualized historical volatility using log returns 
def get_hist_volatility(price_ls:list) -> float:

    if None not in (price_ls):

        # Source: https://goodcalculators.com/historical-volatility-calculator/ 
        # Source: https://quantivity.wordpress.com/2011/02/21/why-log-returns/ 

        log_stock_returns = [math.log(price_ls[i+1]/price_ls[i]) for i in range(len(price_ls)-1)]

        if len(log_stock_returns) != 0:
            ave_log_return = sum(log_stock_returns)/len(log_stock_returns)
        else:
            ave_log_return = 0
        
        returns_diff = [(returns - ave_log_return)**2 for returns in log_stock_returns] 

        return math.sqrt(252) * math.sqrt(sum(returns_diff)/(len(returns_diff)-1))
    
    else:
        return 0