# README

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://python.org)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE.md)

This repository is meant mostly as a learning project on low discrepancy sampling and importance sampling, as well as its computational implementation. To apply it to real world scenarios, the classic example of European options pricing under Black-Scholes hypothesis is taken, as it is a fundational benchmark for these methods.

## Quick start

Download or clone the repo, navigate to the directory in the terminal, and run `pip install .` to install the package. This will allow for all the example notebooks to work correctly, which can be explored and modified. Then go to the [documentation](/Docs/Documentation.md) to read the writeup for the project, or to the [index](/Docs/INDEX.md). For development purposes, simply run

```bash
git clone https://github.com/Pablo-RTZ/QMC_option_pricing.git
cd QMC_option_pricing
pip install -e .
```

This way, modifications to the code will update automatically.

## Contents

This repository contains the following sections

- The Black Scholes model
- Monte Carlo Implementation
- Improvements to Monte Carlo
- Quasi Monte Carlo
- Importance sampling
- Path dependent options
- Final comparisons

## License

This project is licensed under the GNU General Public License v3.0 or later (GPL-3.0-or-later).

See the [LICENSE](LICENSE.md) file for details.

If you use this repository, please cite following the [citation](citation.cff).
