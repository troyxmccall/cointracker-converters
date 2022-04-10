import pandas as pd
import argparse
import re
import sys

def load_binance_file(file):
    try:
        return pd.read_csv(file, index_col=False)
    except Exception as e:
        print(f'[-] Error: {e}')

def convert_binance_to_cointracker(df):

    # binance is stupod and has commas in their numbered data - remove 'em'
    df = df.replace(',','', regex=True)


    # Split by buys and sells
    sells = df.loc[df['Side']=='SELL'].copy()
    buys = df.loc[df['Side']=='BUY'].copy()


    # get coin name from Amount Column
    buys['Sent Currency'] = buys['Amount'].str.extract('([a-zA-Z ]+)', expand=False)
    # get coin number from Amount Column
    buys['Sent Quantity'] = buys['Amount'].str.extract('(^\d*\.?\d+)', expand=False)


    # get coin name from Executed column
    buys['Received Currency'] = buys['Executed'].str.extract('([a-zA-Z ]+)', expand=False)
    buys['Received Quantity'] = buys['Executed'].str.extract('(^\d*\.?\d+)', expand=False)
    # buys and sells have different directions

    # get coin name from Executed Column
    sells['Sent Currency'] = sells['Executed'].str.extract('([a-zA-Z ]+)', expand=False)
    # get coin number from Executed Column
    sells['Sent Quantity'] = sells['Executed'].str.extract('(^\d*\.?\d+)', expand=False)


    # get coin name from Amount column
    sells['Received Currency'] = sells['Amount'].str.extract('([a-zA-Z ]+)', expand=False)
    sells['Received Quantity'] = sells['Amount'].str.extract('(^\d*\.?\d+)', expand=False)


    # # Combine the two dataframes back together
    combined_df = pd.concat([buys,sells]).reset_index(drop=True)

    # handle fees

    combined_df['Fee Currency'] = combined_df['Fee'].str.extract('([a-zA-Z ]+)', expand=False)
    combined_df['Fee Amount'] = combined_df['Fee'].str.extract('(^\d*\.?\d+)', expand=False)


    # # Filter on only the columns Cointracker cares about
    combined_df = combined_df[['Date(UTC)', 'Received Quantity', 'Received Currency', 'Sent Quantity', 'Sent Currency', 'Fee Amount', 'Fee Currency']]

    # # Change the column names to what Cointracker expects
    combined_df.columns = ['Date', 'Received Quantity', 'Received Currency', 'Sent Quantity', 'Sent Currency', 'Fee Amount', 'Fee Currency']

    return combined_df

def export_csv(df, filename):
    df.to_csv(filename, index=False)

def main(args):

    # Ignoring deprecated feature warning
    pd.set_option('mode.chained_assignment', None)

    # Load the CSV file
    df = load_binance_file(args.file)

    # Convert the transactions
    cointracker_dataframe = convert_binance_to_cointracker(df)

    # Export the Cointracker CSV file
    export_csv(cointracker_dataframe, filename=args.output)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=f'binance BigData export CSV to Cointracker compatible CSV file')
    # Positional
    parser.add_argument('-f', '--file', type=str, metavar='', help="Location of the binance BigData CSV file")
    parser.add_argument('-o', '--output', type=str, default='./cointracker_binance.csv', metavar='',help="Location to output the Cointracker compatible CSV file")
    args = parser.parse_args()
    main(args)
