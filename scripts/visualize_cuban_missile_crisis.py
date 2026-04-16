import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

def main():
    # Load data - skip the first 3 lines of metadata/headers
    # Line 1: Price,Adj Close,Close,High,Low,Open,Volume
    # Line 2: Ticker,...
    # Line 3: Date...
    df = pd.read_csv('data/^SPX.csv', skiprows=3, header=None)
    
    # The data has 7 columns: Date, Price, Adj Close, Close, High, Low, Open/Volume
    df.columns = ['Date', 'Price', 'Adj Close', 'Close', 'High', 'Low', 'Open']
    
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')
    
    # Filter for Cuban Missile Crisis period: 1962-09-01 to 1962-12-31
    start_date = '1962-09-01'
    end_date = '1962-12-31'
    mask = (df['Date'] >= start_date) & (df['Date'] <= end_date)
    crisis_df = df.loc[mask].copy()
    
    if crisis_df.empty:
        print("No data found for the specified period.")
        return

    plt.figure(figsize=(12, 6))
    plt.plot(crisis_df['Date'], crisis_df['Close'], label='S&P 500 Close', color='blue', linewidth=2)
    
    # Key Events
    events = [
        ('1962-10-16', 'Crisis Begins\n(Kennedy Informed)', 'red'),
        ('1962-10-22', 'Blockade Announced', 'green'),
        ('1962-10-28', 'Agreement Reached', 'orange'),
    ]
    
    for date_str, label, color in events:
        event_date = pd.to_datetime(date_str)
        # Find the closest date in the dataframe
        idx = (crisis_df['Date'] - event_date).abs().idxmin()
        event_val = crisis_df.loc[idx, 'Close']
        plt.axvline(x=event_date, color=color, linestyle='--', alpha=0.7)
        plt.text(event_date, event_val, label, color=color, fontsize=9, 
                 verticalalignment='bottom', horizontalalignment='center', fontweight='bold')

    plt.title('S&P 500 Trend During the Cuban Missile Crisis (1962)', fontsize=14)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Price', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Format dates
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.savefig('screenshot/cuban_missile_crisis_spx.png')
    print("Plot saved to screenshot/cuban_missile_crisis_spx.png")

if __name__ == "__main__":
    main()