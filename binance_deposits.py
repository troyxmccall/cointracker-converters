import pandas as pd
import argparse
import re
import sys
from datetime import datetime

def load_binance_deposits_file(file):
    try:
        return pd.read_csv(file, index_col=False)
    except Exception as e:
        print(f'[-] Error: {e}')

def convert_binance_deposits_to_cointracker(df):

    # binance is stupod and has commas in their numbered data - remove 'em'
    df = df.replace(',','', regex=True)



    df['Received Currency'] = df['Coin']
    df['Received Quantity'] = df['Amount']

    # zero these out for deposits
    df['Sent Quantity'] = ''
    df['Sent Currency'] = ''
    df['Fee Currency'] = ''
    df['Fee Amount'] = ''

    # fix date time stamps

    #df[['fixed_data']] = df[['Date(UTC)']]

    df['Coin Tracker Date'] = pd.to_datetime(df['Date(UTC)']).dt.strftime('%m/%d/%Y %H:%M:%S')

    # # Filter on only the columns Cointracker cares about
    df = df[['Coin Tracker Date', 'Received Quantity', 'Received Currency', 'Sent Quantity', 'Sent Currency', 'Fee Amount', 'Fee Currency']]

    # # Change the column names to what Cointracker expects
    df.columns = ['Date', 'Received Quantity', 'Received Currency', 'Sent Quantity', 'Sent Currency', 'Fee Amount', 'Fee Currency']

    return df

def export_csv(df, filename):
    df.to_csv(filename, index=False)

def main(args):

    # Ignoring deprecated feature warning
    pd.set_option('mode.chained_assignment', None)

    # Load the CSV file
    df = load_binance_deposits_file(args.file)

    # Convert the transactions
    cointracker_dataframe = convert_binance_deposits_to_cointracker(df)

    # Export the Cointracker CSV file
    export_csv(cointracker_dataframe, filename=args.output)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=f'binance BigData export CSV to Cointracker compatible CSV file')
    # Positional
    parser.add_argument('-f', '--file', type=str, metavar='', help="Location of the binance BigData CSV file")
    parser.add_argument('-o', '--output', type=str, default='./cointracker_binance_deposits.csv', metavar='',help="Location to output the Cointracker compatible CSV file")
    args = parser.parse_args()
    main(args)
