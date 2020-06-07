# Moonlight

## Fetching historical data

This command will fetch the price and write to a new CSV file:

```python3 mine.py -sym <SYMBOL> -i <INTERVAL> -start <STARTDATE> -end <ENDDATE>```

### SYMBOL [REQUIRED]
The symbol in pair
eg. BTCUSDT

### INTERVAL [REQUIRED] 
Expect any one of the values
1,3,5,15,30m (minute)
1,2,4,6,8,12h (hours)
1,3d (days)
1w (week)
1mth (month)

### STARTDATE/ENDDATE [OPTIONAL]

start date must be earlier than end date
default value: end: today, start: -1month
accepted format: `"DD MMM, YYYY"` 

Eg. ```-start "13 MAY, 2020"```
