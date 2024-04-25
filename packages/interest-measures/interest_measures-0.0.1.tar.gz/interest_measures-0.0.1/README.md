# Interest Measure Package for Association Rules and Class Association Rules

This package provides a set of interest measures for association rules and class association

## Installation

```bash
pip install interest-measures
```

## Usage

```python
from interest_measures import InterestMeasures

im = InterestMeasures(A=[0.1, 0.2, 0.3, 0.4],
                      B=[0.5, 0.6, 0.7, 0.8],
                      AB=[0.1, 0.2, 0.3, 0.4], N=100)

print(im.confidence) # 0.25
print(im.lift) # 1.0
print(im.conviction) # 1.0
```


## Available Interest Measures
- Accuracy
- Added value
- Chi square
- Collective strength
- Complement class support
- Conditional entropy
- Confidence
- Confidence causal
- Confirm causal
- Confirm descriptive
- Confirmed confidence causal
- Correlation coefficient
- Cosine
- Coverage
- Dir
- F measure
- Gini index
- Goodman kruskal
- Implication index
- J measure
- Kappa
- Klosgen
- K-measure
- Kulczynski 2
- Least contradiction
- Leverage
- Lift
- Loevinger
- Logical necessity
- Mutual information
- Normalized mutual information
- Odd multiplier
- Odds ratio
- One way support
- Piatetsky Shapiro
- Prevalence
- Putative causal dependency
- Recall
- Relative risk
- Specificity
- Support
- Theil Uncertainty Coefficiente
- Tic
- Two way support