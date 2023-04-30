[![CodeFactor](https://www.codefactor.io/repository/github/ruin2121/technical-analysis/badge)](https://www.codefactor.io/repository/github/ruin2121/technical-analysis)
[![Documentation Status](https://readthedocs.org/projects/technical-analysis/badge/?version=latest)](https://technical-analysis.readthedocs.io/en/latest/?badge=latest)
# technical-analysis

```
pip install git+https://github.com/Ruin2121/technical-analysis.git
```

# Basic Indicators  
Simple Moving Average (SMA)

# Composite Indicators  
## Moving Average Crossover  
```
Limitations:
May yield false positives for values before the longest window. i.e. with a 50 SMA and 200 SMA crossover, the first 199 values may yield a false positive.
```
### Common Variants  
SMA 50 Cross SMA 200
