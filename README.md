# OpenOptionsTrading
Python program to choose the best Option trading stratgey based on risk/reward criteria.

# Algorithms for Options Trading
This project utilizes the Black-Scholes model and market data from Yahoo Finance (`yfinance`) to analyze different options trading strategies. Strategies include low-risk short wait, low-risk long wait, and high-risk short wait options strategies.

Here is a table with risk, reward, time, and a generated title based on the cell values:

| Risk  | Reward | Time  |
|-------|--------|-------|
| Low   | Good   | Short |
| Low   | Better | Long  |
| High  | Best   | Short |

Remember to handle edge cases and input validation appropriately when integrating this function into your trading system.


## Installation
Ensure you have Python 3.6+ installed. Clone this repository and install the required dependencies:

```bash
git clone <repository-url>
cd <repository-directory>
pip install -r requirements.txt
```

Dependencies include `yfinance`, `numpy`, `pandas`, and `scipy`.

## Usage

Import the necessary libraries and define the functions from the project:

```python
import yfinance as yf
import numpy as np
import pandas as pd
from scipy.stats import norm

# Define the functions here...
```

### Running the Strategies

To execute a strategy, first set your parameters:

```python
underlying_symbol = "MSFT"
expiry_date = "2024-04-26"
risk_free_rate = 0.02
```

Then, run the desired strategy function:

```python
# Low risk, short wait strategy
low_risk_short_options, low_risk_short_return = low_risk_short_wait(underlying_symbol, expiry_date, risk_free_rate)
print("Low Risk, Short Wait Options:", low_risk_short_options)
print("Expected Return:", low_risk_short_return)

# For low risk long wait and high risk short wait, uncomment and run similar lines
```

### Important Notes

- This project uses real-time market data from Yahoo Finance. Ensure you are connected to the internet.
- The `expiry_date` format should be `YYYY-MM-DD`.
- Adjust `risk_free_rate` according to the current risk-free interest rate environment.

## Contributing

Contributions are welcome. Please open an issue first to discuss what you would like to change or add.

## License

[MIT](LICENSE.txt)
```

This markdown guide provides a straightforward explanation for users on how to get started with your project, including installation, running the provided strategies, and contributing to the project.
