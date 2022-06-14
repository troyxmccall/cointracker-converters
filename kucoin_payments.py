import pandas as pd
import argparse

def load_kucoin_file(file):
    try:
        return pd.read_csv(file, index_col=False)
    except Exception as e:
        print(f'[-] Error: {e}')

def convert_kucoin_to_cointracker(df):

    
    # Split by buys and sells
    withdraws = df.loc[df['type']=='WITHDRAW'].copy()
    deposits = df.loc[df['type']=='DEPOSIT'].copy()
    
    # Split the buy into two columns with correct position e.g. BTC received currency and USDT sent currency
    withdraws[['Sent Currency']] = withdraws[['coin_type']]
    # buys and sells have different directions
    withdraws[['Sent Quantity']] = withdraws[['vol']]

    withdraws[['fee_currency']] = withdraws[['coin_type']]

    
    # Split the sell into two columns with correct position e.g. USDT received currency and BTC sent currency
    deposits[['Received Currency']] = deposits[['coin_type']]
    # buys and sells have different directions - hence the split reversal above - we have to match
    deposits[['Received Quantity']] = deposits[['vol']]

    deposits[['fee_currency']] = deposits[['coin_type']]


    
    # # Combine the two dataframes back together
    combined_df = pd.concat([deposits,withdraws]).reset_index(drop=True)
    
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
    parser.add_argument('-f', '--file', type=str, metavar='', help="Location of the Kucoin BigData CSV file")
    parser.add_argument('-o', '--output', type=str, default='./cointracker_kucoin.csv', metavar='',help="Location to output the Cointracker compatible CSV file")
    args = parser.parse_args()
    main(args)
