# Package Name

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This Python package contains functions for investigating the correlation between economic and financial data.

## Installation

You can install the package via pip:

```bash
pip install EcoStock
```
## Usage

Here is an example of how to use the package:

```python
import EcoStock

# Fetch stock data
stock_data = EcoStock.get_stock_data('AAPL', '2022-01-01', '2022-12-31')

# Fetch economic data
econ_data = EcoStock.get_world_bank_data('NY.GDP.MKTP.CD', 'US', '2022', '2022')

# Plot correlation
EcoStock.plot_correlation(stock_data, econ_data, 'Apple Stock', 'GDP')

# Calculate correlation
correlation = EcoStock.calculate_correlation(stock_data, econ_data)
print("Correlation Coefficient:", correlation)
```

## Documentation

For more detailed documentation, including the list of available functions and their parameters, please refer to the documentation.

## License

This project is licensed under the MIT License - see the LICENSE file for details.