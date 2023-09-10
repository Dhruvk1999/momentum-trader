import pandas as pd
import talib

def bbRsiFiler(data):
    """
    Apply trading logic to data of different stocks.

    Parameters:
        data (pd.DataFrame): DataFrame containing data for multiple stocks. The 'Date' column must be the index.

    Returns:
        pd.DataFrame: DataFrame containing the trades for each stock. The 'Symbol' and 'Date' columns are retained.
    """
    results = []

    for symbol, group_data in data.groupby('Symbol'):
        is_position = False
        entry_date = None
        entry_price = 0
        trailing_stop = None

        # Compute technical indicators (Bollinger Bands and RSI) for the group data
        group_data['SMA'] = talib.SMA(group_data['Close'], timeperiod=10)
        group_data['upper'], group_data['middle'], group_data['lower'] = talib.BBANDS(group_data['Close'], timeperiod=20, nbdevup=2, nbdevdn=2)
        group_data['RSI'] = talib.RSI(group_data['Close'], timeperiod=5)

        for _, row in group_data.iterrows():
            # Apply your entry and exit conditions here based on the row data
            # For example:
            if row['Close'] < row['lower'] and row['RSI'] < 30:
                entry_date = row.name
                entry_price = row['Close']
                trailing_stop = entry_price * (1 - 0.02)
                is_position = True
                results.append({
                    'Symbol': symbol,
                    'Date': row.name,
                    'Entry_date': entry_date,
                    'Entry_price': entry_price,
                    'Exit_date': row.name,
                    'Exit_price': row['Close'],
                    'Profit': row['Close'] - entry_price,
                })

        

    return pd.DataFrame(results)


# Example usage:
# Assuming 'data' is a DataFrame containing data for multiple stocks with 'Symbol' as one of the columns
