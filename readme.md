###

this assumes you have a CSV export of trades from kucoin bigdata with these headers

```
kucoin.csv
```

```csv
user_id, trade_id, symbol, order_type, deal_price, amount, direction, funds, fee_currency, fee,	created_at,	created_date
```


and want to convert it to this cointracker accepted format

```csv
Date, Received Quantity,	Received Currency,	Sent Quantity,	Sent Currency,	Fee Amount,	Fee Currency														```					


```bash
pip3 install -r requirements
python3 -f kucoin.csv - 2021-kucoin.csv
```


