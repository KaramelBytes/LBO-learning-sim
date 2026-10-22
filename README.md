# LBO Value Creation Bridge (Streamlit)

A finance-focused Streamlit dashboard for decomposing equity value creation in a Leveraged Buyout (LBO) into four additive components:

- **EBITDA Growth Impact**
- **Multiple Expansion Impact**
- **Interaction Effect**
- **Debt Paydown / Additional Borrowing Impact**

The app is designed for MBA classroom demos and practitioner-style walkthroughs.
It attributes equity value changes between entry and exit; it does not forecast operating
cash flow or test whether assumed debt repayment is fundable.

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
  with discussion questions
- Shareable scenario URLs that initialize inputs while allowing subsequent edits and presets
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
- Bridge arithmetic reconciles when |Reconciliation Check| < 0.01 USD million ($10,000)
- The tolerance is applied to the unrounded residual
- Reconciliation checks arithmetic consistency, not economic feasibility

### Return Metrics

- MOIC = Exit Equity / Entry Equity
- IRR = MOIC^(1 / Holding Period Years) - 1
- IRR shown here assumes a single terminal equity cash flow and no interim dividends.
- With positive entry equity and zero exit equity, MOIC is 0.00x and IRR is -100%.
- Negative exit equity and MOIC are algebraic residuals, not ordinary shareholder sale
  proceeds or investor cash-flow returns; IRR is N/M for these cases.

## Inputs and Assumption Notes

- Multiples must be non-negative
- EBITDA may be negative (distressed cases), but interpretation of multiples may be limited
- Holding period must be >= 1 year
- If Entry Equity <= 0, MOIC and IRR are displayed as N/M (Not Meaningful)

### Reading Contributions

Contribution percentages divide each signed component by the absolute net equity change.
Positive values add equity and negative values reduce it. Offsetting drivers can exceed
100%; percentages sum to +100% for a net gain or -100% for a net loss before rounding.
They are N/M when the net change is zero.

Interaction is positive when EBITDA and the multiple both rise or both fall. In the latter
case, it offsets the overlap between the separately calculated losses; it is not an
independent operating lever.

## Project Structure

- `app.py`: Streamlit application (single file)
- `tests/test_app.py`: Scenario and interaction regression checks
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
python -m unittest discover -s tests -v
```

## License

MIT. See [LICENSE](LICENSE).
