import pandas as pd
import argparse

def load_kucoin_file(file):
    try:
        return pd.read_csv(file, index_col=False)
    except Exception as e:
        print(f'[-] Error: {e}')

def convert_kucoin_to_cointracker(df):

    
    # Split by buys and sells
    sells = df.loc[df['direction']=='SELL'].copy()
    buys = df.loc[df['direction']=='BUY'].copy()
    
    # Split the buy into two columns with correct position e.g. BTC received currency and USDT sent currency
    buys[['Received Currency', 'Sent Currency']] = buys['symbol'].str.split('-', expand=True)
    # buys
    buys[['Received Quantity']] = buys[['amount']]
    buys[['Sent Quantity']] = buys[['funds']]

    
    # Split the sell into two columns with correct position e.g. USDT received currency and BTC sent currency
    sells[['Sent Currency', 'Received Currency']] = sells['symbol'].str.split('-', expand=True)
    sells[['Received Quantity']] = sells[['funds']]
    sells[['Sent Quantity']] = sells[['amount']]

    
    # # Combine the two dataframes back together
    combined_df = pd.concat([buys,sells]).reset_index(drop=True)
    
    # # Filter on only the columns Cointracker cares about
    combined_df = combined_df[['created_date', 'Received Quantity', 'Received Currency', 'Sent Quantity', 'Sent Currency', 'fee', 'fee_currency']]

    # # Change the column names to what Cointracker expects
    combined_df.columns = ['Date', 'Received Quantity', 'Received Currency', 'Sent Quantity', 'Sent Currency', 'Fee Amount', 'Fee Currency']

    return combined_df

def export_csv(df, filename):
    df.to_csv(filename, index=False)

def main(args):

    # Ignoring deprecated feature warning
    pd.set_option('mode.chained_assignment', None)

    # Load the CSV file
    df = load_kucoin_file(args.file)
    
    # Convert the transactions
    cointracker_dataframe = convert_kucoin_to_cointracker(df)
    
    # Export the Cointracker CSV file
    export_csv(cointracker_dataframe, filename=args.output)
        
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=f'Kucoin BigData export CSV to Cointracker compatible CSV file')
    # Positional
    parser.add_argument('-f', '--file', type=str, metavar='', help="Location of the Kucoin Margin CSV file")
    parser.add_argument('-o', '--output', type=str, default='./cointracker.csv', metavar='',help="Location to output the Cointracker compatible CSV file")
    args = parser.parse_args()
    main(args)
