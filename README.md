# technical-analysis

```
pip install git+https://github.com/Ruin2121/technical-analysis.git
```

# Currently Implemented  
Many of the indicators below have minor limitations, Known limitations are under their respective indicator.  

## Basic Indicators  
Simple Moving Average (SMA)

## Composite Indicators  
### Moving Average Crossover  
```
Limitations:
May yield false positives for values before the longest window. i.e. with a 50 SMA and 200 SMA crossover, the first 199 values may yield a false positive.
```
#### Common Variants  
SMA 50 Cross SMA 200
