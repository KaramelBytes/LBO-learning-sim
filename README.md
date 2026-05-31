# LBO Value Creation Bridge (Streamlit)

A finance-focused Streamlit dashboard for decomposing equity value creation in a Leveraged Buyout (LBO) into four additive components:

- **EBITDA Growth Impact**
- **Multiple Expansion Impact**
- **Interaction Effect**
- **Debt Paydown / Additional Borrowing Impact**

The app is designed for MBA classroom demos and practitioner-style walkthroughs.

> ⚠️ **Disclaimer:** This tool is for educational purposes only. It is not investment advice, and none of the outputs should be relied upon for actual transaction or valuation decisions.

## Try It Live

The app is deployed on Streamlit Community Cloud:

**[Open the LBO Value Creation Bridge](https://lbo-learning-sim-karamelbytes.streamlit.app)**

## What It Teaches

LBO models often produce a single MOIC or IRR figure, but that number hides *how* value was created. This tool breaks the total equity change into its drivers so you can see exactly which levers pulled returns up or down.

The four components map to the real-world decisions and market forces in any buyout:
- Did operational performance improve?
- Did the exit multiple expand or contract?
- How much of the return came from the cross-effect of growth and re-rating?
- How much did leverage (or deleveraging) contribute?

## Features

- Interactive sidebar assumptions for entry/exit operating and capital structure variables
- Warm cream/gold finance-theme dashboard layout optimized for classroom projection
- Key metrics strip: Entry Equity, Exit Equity, MOIC, IRR
- Plotly waterfall bridge from Entry Equity to Exit Equity
- Four-tab layout: Bridge, Detailed Data, Executive Summary, and How It Works
- Five scenario presets (Growth Story, Multiple Expansion, Debt Paydown, Distressed, All Engines)
- Educational tooltips on every input field
- Dynamic executive summary narrative (value creation vs. value erosion vs. invalid structure)
- Live algebraic walkthrough that uses your current inputs as worked examples
- Reconciliation check with explicit tolerance threshold
- Validation guardrails for assumptions and model integrity
- Responsive layout for tablets and mobile devices

## Financial Logic

### Core Equity Values

- Entry EV = Entry EBITDA x Entry EV/EBITDA Multiple
- Exit EV = Exit EBITDA x Exit EV/EBITDA Multiple
- Entry Equity = Entry EV - Initial Debt
- Exit Net Debt = Initial Debt - Debt Paydown
- Exit Equity = Exit EV - Exit Net Debt

### Bridge Components

- EBITDA Growth Impact = (Exit EBITDA - Entry EBITDA) x Entry Multiple
- Multiple Expansion Impact = Entry EBITDA x (Exit Multiple - Entry Multiple)
- Interaction Effect = (Exit EBITDA - Entry EBITDA) x (Exit Multiple - Entry Multiple)
- Debt Component = Debt Paydown (positive) or Additional Borrowing (negative)

### Reconciliation

- Reconciliation Check = Exit Equity - (Entry Equity + sum(all bridge components))
- Balanced status is true when |Reconciliation Check| < $0.01

### Return Metrics

- MOIC = Exit Equity / Entry Equity
- IRR = MOIC^(1 / Holding Period Years) - 1
- IRR shown here assumes a single terminal equity cash flow and no interim dividends.

## Inputs and Assumption Notes

- Multiples must be non-negative
- EBITDA may be negative (distressed cases), but interpretation of multiples may be limited
- Holding period must be >= 1 year
- If Entry Equity <= 0, MOIC and IRR are displayed as N/M (Not Meaningful)

## Project Structure

- `app.py`: Streamlit application (single file, ~960 lines)
- `requirements.txt`: Python dependencies
- `requirements.lock.txt`: Fully pinned dependency lockfile for reproducibility
- `requirements-dev.txt`: Developer tooling dependencies (linting)
- `pyproject.toml`: Ruff lint configuration

## Development

To run the app locally for development or testing:

1. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

### Quality Checks

```bash
pip install -r requirements-dev.txt
ruff check .
python -m py_compile app.py
```

## License

MIT. See [LICENSE](LICENSE).
