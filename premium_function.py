import csv
import yfinance as yf
from datetime import datetime, timedelta

def read_tickers_from_csv(file_path):
    tickers = []
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            tickers.append(row[0])
    return tickers

def find_closest_expiration_date(ticker):
    expiration_dates = ticker.options
    today = datetime.now().date()
    closest_date = None
    min_days_diff = float('inf')
    
    for date in expiration_dates:
        expiration_date = datetime.strptime(date, '%Y-%m-%d').date()
        days_diff = (expiration_date - today).days
        if 0 < days_diff < min_days_diff:
            min_days_diff = days_diff
            closest_date = date
    
    return closest_date

def allocate_capital(tickers, capital):
    allocations = []
    
    for ticker_symbol in tickers:
        ticker = yf.Ticker(ticker_symbol)
        expiration_date = find_closest_expiration_date(ticker)
        
        if expiration_date:
            options_chain = ticker.option_chain(expiration_date)
            puts = options_chain.puts
            
            for _, row in puts.iterrows():
                contracts = int(capital // (row['lastPrice'] * 100))
                if contracts > 0:
                    premium = contracts * row['bid'] * 100
                    allocations.append({
                        'ticker': ticker_symbol,
                        'expiration_date': expiration_date,
                        'strike': row['strike'],
                        'premium': premium,
                        'contracts': contracts
                    })
    
    allocations.sort(key=lambda x: x['premium'], reverse=True)
    
    utilized_capital = 0
    final_allocations = []
    
    for allocation in allocations:
        remaining_capital = capital - utilized_capital
        if remaining_capital >= allocation['premium']:
            utilized_capital += allocation['premium']
            final_allocations.append(allocation)
        else:
            contracts = int(remaining_capital // (allocation['premium'] / allocation['contracts']))
            if contracts > 0:
                premium = contracts * allocation['premium'] / allocation['contracts']
                utilized_capital += premium
                allocation['contracts'] = contracts
                allocation['premium'] = premium
                final_allocations.append(allocation)
                break
    
    return final_allocations

def main():
    csv_file_path = 'stock_tickers.csv'
    capital = 10000  # $10,000
    
    tickers = read_tickers_from_csv(csv_file_path)
    allocations = allocate_capital(tickers, capital)
    
    print("Allocation Results:")
    for allocation in allocations:
        print(f"Ticker: {allocation['ticker']}")
        print(f"Expiration Date: {allocation['expiration_date']}")
        print(f"Strike Price: ${allocation['strike']:.2f}")
        print(f"Contracts: {allocation['contracts']}")
        print(f"Premium: ${allocation['premium']:.2f}")
        print("---")
    
    total_premium = sum(allocation['premium'] for allocation in allocations)
    print(f"Total Premium: ${total_premium:.2f}")
    print(f"Utilized Capital: ${sum(allocation['premium'] for allocation in allocations):.2f}")

if __name__ == '__main__':
    main()
