### Kucoin

this assumes you have a CSV export of trades from kucoin bigdata with these EXACT headers

name: `kucoin.csv`

```ini
user_id, trade_id, symbol, order_type, deal_price, amount, direction, funds, fee_currency, fee,	created_at,	created_date
```


and want to convert it to this cointracker accepted format

name: `cointracker_kucoin.csv`

```ini
Date, Received Quantity, Received Currency, Sent Quantity, Sent Currency, Fee Amount, Fee Currency
```	


```bash
rm cointracker_kucoin.csv
pip3 install -r requirements
python3 kucoin.py -f kucoin.csv -o cointracker_kucoin.csv
```




### Binance

this assumes you have a CSV export of trades from binance [https://www.binance.com/en/my/orders/exchange/usertrade] with these EXACT headers


name: `binance.csv`

```csv
"Date(UTC)","Pair","Side","Price","Executed","Amount","Fee"
```


#### usage

```bash
rm cointracker_binance.csv
pip3 install -r requirements
python3 binance.py -f binance.csv -o cointracker_binance.csv
```


and want to convert it to this cointracker accepted format

name: `cointracker_binance.csv`

```ini
Date, Received Quantity, Received Currency, Sent Quantity, Sent Currency, Fee Amount, Fee Currency
```



### disclaimer

this script comes with absolutely no warranty, use at your own risk

make sure to verify your results before uploading to cointracker
