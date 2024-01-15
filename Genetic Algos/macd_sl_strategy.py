from evolution_operators import *
from utility_functions import *

def evaluate_strategy(data, fast_period, slow_period, fast_p_exit, slow_p_exit, stop_loss_percentage):
    # Calculate indicators
#     print(fast_period,slow_period,fast_p_exit, slow_p_exit, stop_loss_percentage)
    data['MACD'], data['Signal'] = calculate_macd(data, fast_period, slow_period)
    data['MACD_E'], data['Signal_E'] = calculate_macd(data, fast_p_exit, slow_p_exit)

    data['ROC'] = calculate_roc(data, 3)
#     data['RSI_Derivative'] = calculate_rsi_derivative(data, rsi_period)
    
    # Apply trailing stop-loss exit condition
#     stop_loss = trailing_stop_loss(data, stop_loss_percentage)
    
    # Simulated trading logic
    position = 0  # 0 for no position, 1 for long position
    profit = 0
    total_trades = 0
    winning_trades = 0
    stricly_winning_trades =0
    allocated_funds = 100000
    no_of_shares =0
    stop_loss_price = 0
    
    for i in range(1, len(data)):
        try:

            if position == 0:
                if data['MACD'][i] > data['Signal'][i] :#and data['ROC'][i] > 1: #and data['RSI_Derivative'][i] > rsi_derivative_threshold:
                
                    position = 1  # Buy (enter long position)
                    entry_price = data['Close'][i]
                    stop_loss_price = entry_price - (entry_price * 0.01 * stop_loss_percentage)
#                     print(f"Entry: {entry_price} on {data.index[i]} Stop Loss: {stop_loss_price}")
                    total_trades += 1
                    no_of_shares = allocated_funds//entry_price
                    
            elif position == 1 and data['MACD'][i] < data['Signal'][i]:
                
                if data['Close'][i] > entry_price:  # Adjust stop loss only when the price goes up
                    stop_loss_price = max(stop_loss_price, data['Close'][i] - (data['Close'][i] * 0.01 * stop_loss_percentage))

                if data['Low'][i] < stop_loss_price:
                    position = 0  # Sell due to stop loss
                    exit_price = data['Open'][i] if stop_loss_price > data['Open'][i] else stop_loss_price
                    trade_profit = (exit_price - entry_price) * no_of_shares  # Calculate profit/loss
                    profit=trade_profit
                    allocated_funds += profit
                    no_of_shares =0
#                     print(f"Exit: {exit_price} on {data.index[i]} exited on stop loss Allocated Funds {allocated_funds}")
#                     print(f"Profit: {profit}")
                    if(exit_price>= entry_price):
                        winning_trades += 1
                    if(exit_price> entry_price):
                        stricly_winning_trades += 1
                elif data['MACD_E'][i] < data['Signal_E'][i]:
                    position = 0  # Sell due to exit condition
                    exit_price = data['Close'][i]
                    trade_profit = (exit_price - entry_price) * no_of_shares  # Calculate profit/loss
                    profit=trade_profit#                     
#                     print(f"Exit: {exit_price} on {data.index[i]} exited on stop loss Allocated Funds {allocated_funds}")
#                     print(f"Profit: {profit}")
                    allocated_funds += profit

                    no_of_shares =0
                    if(exit_price>= entry_price):
                        winning_trades += 1
                    if(exit_price> entry_price):
                        stricly_winning_trades += 1
            
        except Exception as ex:
            print("Something caused the error",ex)
            break
        win_rate = winning_trades/total_trades if total_trades != 0 else 0
    
    return [profit,total_trades,winning_trades,stricly_winning_trades,win_rate,allocated_funds]