###

this assumes you have a CSV export of trades from kucoin bigdata with these EXACT headers

name: `kucoin.csv`

```ini
user_id, trade_id, symbol, order_type, deal_price, amount, direction, funds, fee_currency, fee,	created_at,	created_date
```


and want to convert it to this cointracker accepted format

name: `cointracker.csv`

```ini
Date, Received Quantity, Received Currency, Sent Quantity, Sent Currency, Fee Amount, Fee Currency
```	


```bash
rm cointracker.csv 
pip3 install -r requirements
python3 convert_kucoin_to_cointracker.py -f kucoin.csv -o cointracker.csv
```

this script comes with exactly no warranty, use at your own risk

make sure to verify your results before uploading to cointracker


