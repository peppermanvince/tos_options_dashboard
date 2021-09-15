def create_pricelist(hist_price):
    output_ls = []
    for candle in hist_price['candles']:
        output_ls.append(candle['close'])    
    return output_ls

def optionchain_parser(response, df_cols=[], df_data=[]):
    for option_chain_type in ['call','put']:
        for exp_date in response[f'{option_chain_type}ExpDateMap'].values():
            for strike in exp_date.values():
                row_data = []
                for key, value in strike[0].items():
                    if key not in df_cols:
                        df_cols.append(key)
                    row_data.append(value)
                df_data.append(row_data)
    return df_cols, df_data                