import math

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="LBO Value Creation Bridge",
    page_icon="💰",
    layout="wide",
)

# ---------------------------------------------------------------------------
# Defaults & Presets
# ---------------------------------------------------------------------------

DEFAULT_ASSUMPTIONS = {
    "entry_ebitda": 100.0,
    "entry_multiple": 10.0,
    "initial_debt": 500.0,
    "exit_ebitda": 130.0,
    "exit_multiple": 11.0,
    "debt_paydown": 150.0,
    "holding_period_years": 5.0,
}

PRESETS = {
    "Growth Story": {
        "entry_ebitda": 100.0,
        "entry_multiple": 10.0,
        "initial_debt": 500.0,
        "exit_ebitda": 150.0,
        "exit_multiple": 10.0,
        "debt_paydown": 200.0,
        "holding_period_years": 5.0,
        "caption": "Operational improvement \u2014 EBITDA grows, multiple stays constant.",
    },
    "Multiple Expansion": {
        "entry_ebitda": 100.0,
        "entry_multiple": 8.0,
        "initial_debt": 400.0,
        "exit_ebitda": 100.0,
        "exit_multiple": 12.0,
        "debt_paydown": 100.0,
        "holding_period_years": 5.0,
        "caption": "Multiple re-rating \u2014 market pays more for the same earnings.",
    },
    "Debt Paydown": {
        "entry_ebitda": 100.0,
        "entry_multiple": 10.0,
        "initial_debt": 700.0,
        "exit_ebitda": 105.0,
        "exit_multiple": 10.0,
        "debt_paydown": 300.0,
        "holding_period_years": 5.0,
        "caption": "Aggressive deleveraging \u2014 debt paydown drives equity growth.",
    },
    "Distressed": {
        "entry_ebitda": 100.0,
        "entry_multiple": 10.0,
        "initial_debt": 600.0,
        "exit_ebitda": 70.0,
        "exit_multiple": 8.0,
        "debt_paydown": 50.0,
        "holding_period_years": 5.0,
        "caption": "Value destruction \u2014 falling EBITDA and multiple contraction.",
    },
    "All Engines": {
        "entry_ebitda": 100.0,
        "entry_multiple": 10.0,
        "initial_debt": 500.0,
        "exit_ebitda": 140.0,
        "exit_multiple": 12.0,
        "debt_paydown": 200.0,
        "holding_period_years": 5.0,
        "caption": "All four drivers contribute positively \u2014 the ideal LBO scenario.",
    },
}

# ---------------------------------------------------------------------------
# Custom CSS
# ---------------------------------------------------------------------------

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --bg-page: #faf8f5;
    --bg-surface: #ffffff;
    --bg-sidebar: #f7f4ef;
    --text-primary: #1a1a2e;
    --text-secondary: #5b5b6b;
    --text-muted: #8f8f9f;
    --border-light: #e8e3da;
    --border-strong: #d4ccc0;
    --accent: #c9a84c;
    --accent-light: #e8dba0;
    --accent-strong: #b8922e;
    --focus-ring: #c9a84c;
    --positive: #2e7d32;
    --negative: #c62828;
    --radius: 12px;
    --shadow: 0 1px 3px rgba(26,26,46,0.06), 0 1px 2px rgba(26,26,46,0.04);
}

html, body, .stApp {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    background-color: var(--bg-page);
    color: var(--text-primary);
}

[data-testid="stAppViewContainer"] {
    background-color: var(--bg-page);
}

[data-testid="stSidebar"] {
    background-color: var(--bg-sidebar);
    border-right: 1px solid var(--border-light);
}

[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] {
    color: var(--text-primary) !important;
    font-weight: 600;
}

h1, h2, h3, h4, h5, h6 {
    color: var(--text-primary);
    font-weight: 700;
    letter-spacing: -0.02em;
}

h1 {
    font-size: 1.8rem;
    border-bottom: 2px solid var(--accent-light);
    padding-bottom: 0.4rem;
    margin-bottom: 0.5rem;
}

h2 {
    font-size: 1.2rem;
    margin-top: 0;
}

p, span, label, div, .stMarkdown p {
    color: var(--text-secondary);
}

[data-testid="stCaptionContainer"],
[data-testid="stCaptionContainer"] p,
[data-testid="stCaptionContainer"] span {
    color: var(--text-muted) !important;
    opacity: 1 !important;
}

[data-testid="stMetric"] {
    background: var(--bg-surface);
    border: 1px solid var(--border-light);
    border-radius: var(--radius);
    padding: 1rem 1.2rem;
    box-shadow: var(--shadow);
}

[data-testid="stMetricLabel"] > div {
    color: var(--text-secondary);
    font-weight: 600;
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}

[data-testid="stMetricValue"] > div {
    color: var(--text-primary);
    font-weight: 800;
    font-size: 1.6rem;
}

[data-baseweb="input"] > div,
[data-baseweb="select"] > div {
    background-color: var(--bg-surface) !important;
    border: 1px solid var(--border-light) !important;
    border-radius: 8px !important;
    box-shadow: var(--shadow) !important;
}

[data-baseweb="input"] input,
[data-baseweb="input"] input::placeholder {
    color: var(--text-primary) !important;
    opacity: 1 !important;
}

[data-baseweb="input"] > div:focus-within,
[data-baseweb="select"] > div:focus-within {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(201, 168, 76, 0.2) !important;
}

[data-testid="stButton"] > button,
.stButton > button {
    background: linear-gradient(180deg, var(--accent), var(--accent-strong)) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    padding: 0.4rem 1.2rem !important;
    box-shadow: var(--shadow) !important;
    transition: all 0.15s ease !important;
}

[data-testid="stButton"] > button:hover,
.stButton > button:hover {
    background: linear-gradient(180deg, var(--accent-strong), #a07d20) !important;
    box-shadow: 0 2px 8px rgba(201, 168, 76, 0.3) !important;
}

[data-testid="stTabs"] {
    background: var(--bg-surface);
    border-radius: var(--radius);
    box-shadow: var(--shadow);
    padding: 0.25rem 0.25rem 0 0.25rem;
}

[data-testid="stTab"] button {
    color: var(--text-secondary) !important;
    font-weight: 600;
    font-size: 0.85rem;
    padding: 0.5rem 1rem;
    border-radius: 8px 8px 0 0 !important;
}

[data-testid="stTab"] button[aria-selected="true"] {
    color: var(--accent-strong) !important;
    background: rgba(201, 168, 76, 0.08);
    border-bottom: 2px solid var(--accent) !important;
}

[data-testid="stDataFrame"] {
    background: var(--bg-surface);
    border: 1px solid var(--border-light);
    border-radius: var(--radius);
    box-shadow: var(--shadow);
}

[data-testid="stDataFrame"] * {
    color: var(--text-primary) !important;
}

.streamlit-expanderHeader {
    background: var(--bg-surface);
    border: 1px solid var(--border-light);
    border-radius: var(--radius);
    font-weight: 600;
    color: var(--text-primary);
}

.streamlit-expanderContent {
    background: var(--bg-surface);
    border: 1px solid var(--border-light);
    border-top: none;
    border-radius: 0 0 var(--radius) var(--radius);
}

#MainMenu, footer, [data-testid="stHeader"] {
    visibility: hidden;
}

[data-testid="collapsedControl"] {
    background-color: var(--accent-light);
    border: 1px solid var(--accent);
    border-radius: var(--radius);
}

[data-testid="collapsedControl"] svg {
    fill: var(--accent-strong);
}

.stAlert {
    border-radius: var(--radius);
    border-left: 4px solid;
}

div[data-baseweb="notification"] {
    border-radius: var(--radius);
}

/* ── Preset sidebar buttons: prevent word-break orphans ── */
[data-testid="stSidebar"] [data-testid="column"] [data-testid="stButton"] > button {
    white-space: nowrap !important;
    font-size: 0.75rem !important;
    padding: 0.25rem 0.4rem !important;
    overflow: hidden;
    text-overflow: ellipsis;
}

/* ── Responsive: tablet ── */
@media (max-width: 992px) {
    h1 { font-size: 1.5rem; }
    h2 { font-size: 1.05rem; }
    [data-testid="stMetric"] { padding: 0.7rem 0.8rem; }
    [data-testid="stMetricValue"] > div { font-size: 1.3rem; }
}

/* ── Responsive: mobile ── */
@media (max-width: 640px) {
    .stApp header { padding-top: 0.25rem; }
    [data-testid="stAppViewContainer"] > .main { padding: 0.5rem 0.5rem 2rem; }
    h1 { font-size: 1.2rem; padding-bottom: 0.25rem; }
    h2 { font-size: 0.95rem; }
    [data-testid="stCaptionContainer"] { font-size: 0.75rem; }
    [data-testid="stMetric"] { padding: 0.5rem 0.6rem; }
    [data-testid="stMetricValue"] > div { font-size: 1.1rem; }
    [data-testid="stMetricLabel"] > div { font-size: 0.65rem; }
    [data-testid="stTabs"] { padding: 0.15rem; overflow-x: auto; }
    [data-testid="stTab"] button { font-size: 0.75rem; padding: 0.35rem 0.6rem; }
    [data-testid="stSidebar"] { min-width: 260px; }
}

/* ── Print-friendly ── */
@media print {
    [data-testid="stSidebar"] { display: none !important; }
    .stApp { background: #ffffff !important; }
    h1 { font-size: 1.4rem; border-bottom-color: #ccc; }
    [data-testid="stMetric"] { box-shadow: none; border: 1px solid #ddd; }
    [data-testid="stTabs"] { box-shadow: none; border: 1px solid #ddd; }
}
</style>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------

st.title("LBO Value Creation Bridge")
st.caption("All currency values are shown in USD millions ($mm).")
st.info("For educational purposes only. Not investment advice.", icon="ℹ️")


def format_currency(value: float) -> str:
    if math.isnan(value):
        return "N/M"
    if value < 0:
        return f"-${abs(value):,.0f}"
    return f"${value:,.0f}"


def md_currency(value: float) -> str:
    """Escape dollar signs for use inside st.markdown to avoid LaTeX math mode."""
    return format_currency(value).replace("$", r"\$")


def load_preset(name: str) -> None:
    for key in DEFAULT_ASSUMPTIONS:
        st.session_state[key] = PRESETS[name][key]


# Seed session state from URL query params so users can share scenarios via link
for key in DEFAULT_ASSUMPTIONS:
    if key in st.query_params:
        try:
            st.session_state[key] = float(st.query_params[key])
        except (ValueError, TypeError):
            pass


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------

st.sidebar.header("Inputs")
st.sidebar.caption("Adjust assumptions below. Hover over each field for context.")

st.sidebar.subheader("Scenario Presets")
preset_cols = st.sidebar.columns(2)
for i, name in enumerate(PRESETS):
    with preset_cols[i % 2]:
        if st.button(name, key=f"preset_{name}", width="stretch"):
            load_preset(name)
            st.rerun()

active_preset = None
for name, data in PRESETS.items():
    if all(st.session_state.get(k) == data[k] for k in DEFAULT_ASSUMPTIONS):
        active_preset = name
        break
if active_preset:
    st.sidebar.caption(PRESETS[active_preset]["caption"])

st.sidebar.divider()

if st.sidebar.button("Reset to Defaults", width="stretch"):
    for key, value in DEFAULT_ASSUMPTIONS.items():
        st.session_state[key] = value
    st.rerun()

entry_ebitda = st.sidebar.number_input(
    "Entry EBITDA ($ Millions)",
    value=DEFAULT_ASSUMPTIONS["entry_ebitda"],
    step=5.0,
    format="%.2f",
    key="entry_ebitda",
    help=(
        "The target company\u2019s earnings before interest, taxes, depreciation, "
        "and amortization at the time of acquisition."
    ),
)
entry_multiple = st.sidebar.number_input(
    "Entry EV/EBITDA Multiple",
    value=DEFAULT_ASSUMPTIONS["entry_multiple"],
    step=0.25,
    format="%.2f",
    key="entry_multiple",
    help=(
        "The purchase price expressed as a multiple of EBITDA "
        "(Enterprise Value \u00f7 EBITDA). A higher multiple means a more expensive acquisition."
    ),
)
initial_debt = st.sidebar.number_input(
    "Initial Debt ($ Millions)",
    value=DEFAULT_ASSUMPTIONS["initial_debt"],
    step=10.0,
    format="%.2f",
    key="initial_debt",
    help=(
        "The debt used to finance the acquisition. "
        "Higher leverage magnifies equity returns (and losses)."
    ),
)
exit_ebitda = st.sidebar.number_input(
    "Exit EBITDA ($ Millions)",
    value=DEFAULT_ASSUMPTIONS["exit_ebitda"],
    step=5.0,
    format="%.2f",
    key="exit_ebitda",
    help=(
        "The projected EBITDA at the time of sale. "
        "Growth from entry reflects operational improvement."
    ),
)
exit_multiple = st.sidebar.number_input(
    "Exit EV/EBITDA Multiple",
    value=DEFAULT_ASSUMPTIONS["exit_multiple"],
    step=0.25,
    format="%.2f",
    key="exit_multiple",
    help=(
        "The multiple at which the company is sold. "
        "Can differ from entry due to market conditions or company profile changes."
    ),
)
debt_paydown = st.sidebar.number_input(
    "Debt Paydown ($ Millions)",
    value=DEFAULT_ASSUMPTIONS["debt_paydown"],
    step=10.0,
    format="%.2f",
    key="debt_paydown",
    help=(
        "Positive = debt paid down during the holding period. "
        "Negative = additional borrowing, which increases net debt and reduces equity value."
    ),
)
holding_period_years = st.sidebar.number_input(
    "Holding Period (Years)",
    min_value=1.0,
    value=DEFAULT_ASSUMPTIONS["holding_period_years"],
    step=0.25,
    format="%.2f",
    key="holding_period_years",
    help=(
        "The time between acquisition and exit. "
        "A longer period allows more operational improvement (or decay)."
    ),
)

st.sidebar.divider()
if st.sidebar.button(
    "🔗 Copy Shareable Link",
    width="stretch",
    help="Updates the URL with your current inputs so you can share this scenario.",
):
    for key in DEFAULT_ASSUMPTIONS:
        st.query_params[key] = str(st.session_state.get(key, DEFAULT_ASSUMPTIONS[key]))
    st.toast("🔗 Link updated! Copy the URL from your browser to share this scenario.", icon="🔗")

# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

validation_errors = []
if entry_multiple < 0 or exit_multiple < 0:
    validation_errors.append("Multiples cannot be negative.")
if holding_period_years < 1:
    validation_errors.append("Holding Period must be at least 1 year.")
if entry_ebitda < 0 or exit_ebitda < 0:
    st.warning(
        "Warning: Negative EBITDA indicates a distressed scenario; "
        "multiples may not be meaningful."
    )

for error_message in validation_errors:
    st.error(f"Error: {error_message}")

if validation_errors:
    st.stop()

# ---------------------------------------------------------------------------
# Core calculations
# ---------------------------------------------------------------------------

entry_ev = entry_ebitda * entry_multiple
exit_ev = exit_ebitda * exit_multiple

entry_equity = entry_ev - initial_debt
exit_net_debt = initial_debt - debt_paydown
exit_equity = exit_ev - exit_net_debt

ebitda_growth_impact = (exit_ebitda - entry_ebitda) * entry_multiple
multiple_expansion_impact = entry_ebitda * (exit_multiple - entry_multiple)
interaction_effect = (exit_ebitda - entry_ebitda) * (exit_multiple - entry_multiple)

if debt_paydown >= 0:
    debt_label = "Debt Paydown"
    debt_effect = debt_paydown
else:
    debt_label = "Additional Borrowing"
    debt_effect = debt_paydown

components = [
    ebitda_growth_impact,
    multiple_expansion_impact,
    interaction_effect,
    debt_effect,
]
component_labels = [
    "EBITDA Growth Impact",
    "Multiple Expansion Impact",
    "Interaction Effect",
    debt_label,
]

reconciliation_check = round(exit_equity - (entry_equity + sum(components)), 2)

invalid_capital_structure = entry_equity <= 0

moic = float("nan")
irr = float("nan")
if not invalid_capital_structure and entry_equity != 0:
    moic = exit_equity / entry_equity
if not math.isnan(moic) and moic > 0 and holding_period_years > 0:
    irr = moic ** (1.0 / holding_period_years) - 1.0

moic_display = (
    f"{moic:,.2f}x" if (not math.isnan(moic) and not invalid_capital_structure) else "N/M"
)
irr_display = (
    f"{irr * 100:,.1f}%" if (not math.isnan(irr) and not invalid_capital_structure) else "N/M"
)

# Dynamic table labels
if exit_net_debt >= 0:
    exit_debt_cash_label = "Exit Net Debt"
    exit_debt_cash_value = exit_net_debt
else:
    exit_debt_cash_label = "Exit Net Cash"
    exit_debt_cash_value = abs(exit_net_debt)

# Additional intermediate values used in tabs
delta_ebitda = exit_ebitda - entry_ebitda
delta_multiple = exit_multiple - entry_multiple
delta_ev = exit_ev - entry_ev
entry_leverage = initial_debt / entry_ev if entry_ev != 0 else float("nan")
exit_leverage = exit_net_debt / exit_ev if exit_ev != 0 else float("nan")

# ---------------------------------------------------------------------------
# KPI bar
# ---------------------------------------------------------------------------

st.subheader("Key Metrics")
kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
with kpi_col1:
    st.metric("Entry Equity", format_currency(entry_equity))
with kpi_col2:
    st.metric("Exit Equity", format_currency(exit_equity))
with kpi_col3:
    st.metric("MOIC", moic_display)
    if invalid_capital_structure:
        st.caption("Entry equity \u2264 0 \u2014 not meaningful")
with kpi_col4:
    st.metric("IRR", irr_display)
    st.caption("Single-exit, no interim dividends")

# ---------------------------------------------------------------------------
# Tabs
# ---------------------------------------------------------------------------

bridge_tab, data_tab, summary_tab, how_tab = st.tabs(
    ["Bridge", "Detailed Data", "Executive Summary", "How It Works"]
)

# ---------------------------------------------------------------------------
# Tab 1: Bridge (waterfall chart)
# ---------------------------------------------------------------------------

with bridge_tab:
    x_labels = ["Entry Equity", *component_labels, "Exit Equity"]
    measure = ["absolute", "relative", "relative", "relative", "relative", "total"]
    y_values = [entry_equity, *components, exit_equity]

    waterfall = go.Figure(
        go.Waterfall(
            name="Equity Bridge",
            orientation="v",
            measure=measure,
            x=x_labels,
            y=y_values,
            connector={"line": {"color": "#d4ccc0", "width": 1.5}},
            increasing={"marker": {"color": "#c9a84c"}},
            decreasing={"marker": {"color": "#c62828"}},
            totals={"marker": {"color": "#1a1a2e"}},
            text=[
                f"{v:,.0f}" if abs(v) >= 1 else f"{v:,.2f}" for v in y_values
            ],
            textposition="outside",
            textfont={
                "size": 13,
                "color": "#1a1a2e",
                "family": "Inter, sans-serif",
            },
            hoverinfo="x+y",
            hoverlabel={
                "bgcolor": "#ffffff",
                "bordercolor": "#d4ccc0",
                "font": {
                    "family": "Inter, sans-serif",
                    "size": 13,
                    "color": "#1a1a2e",
                },
            },
        )
    )

    waterfall.update_layout(
        title={
            "text": "LBO Equity Value Creation Bridge",
            "font": {
                "size": 18,
                "family": "Inter, sans-serif",
                "color": "#1a1a2e",
            },
        },
        yaxis_title={
            "text": "USD Millions ($mm)",
            "font": {"size": 13, "family": "Inter, sans-serif", "color": "#5b5b6b"},
        },
        xaxis={
            "tickfont": {
                "size": 12,
                "family": "Inter, sans-serif",
                "color": "#5b5b6b",
            },
            "tickangle": 0,
        },
        showlegend=False,
        plot_bgcolor="#faf8f5",
        paper_bgcolor="#faf8f5",
        margin={"l": 50, "r": 30, "t": 50, "b": 40},
        hovermode="x",
        font={"family": "Inter, sans-serif"},
    )

    waterfall.update_xaxes(gridcolor="#f0ebe3", showgrid=False, zeroline=False)
    waterfall.update_yaxes(
        gridcolor="#f0ebe3",
        showgrid=True,
        zeroline=True,
        zerolinecolor="#d4ccc0",
        zerolinewidth=1,
    )

    st.plotly_chart(waterfall, width="stretch")

    if invalid_capital_structure:
        st.error(
            "Invalid Capital Structure: Equity Value is zero or negative. "
            "Adjust Debt or Multiples."
        )

# ---------------------------------------------------------------------------
# Tab 2: Detailed Data
# ---------------------------------------------------------------------------

with data_tab:
    total_equity_change = exit_equity - entry_equity

    def pct_contrib(val):
        if total_equity_change == 0:
            return "0%"
        return f"{abs(val) / abs(total_equity_change) * 100:,.0f}%"

    summary_rows = [
        ("Key Values", ""),
        ("Entry EV", format_currency(entry_ev)),
        ("Entry Equity", format_currency(entry_equity)),
        ("Exit EV", format_currency(exit_ev)),
        (exit_debt_cash_label, format_currency(exit_debt_cash_value)),
        ("Exit Equity", format_currency(exit_equity)),
        ("Returns", ""),
        ("MOIC", moic_display),
        ("IRR", irr_display),
        ("Intermediate", ""),
        ("Delta EBITDA (Exit \u2212 Entry)", format_currency(delta_ebitda)),
        ("Delta Multiple (Exit \u2212 Entry)", f"{delta_multiple:+.2f}x"),
        ("Delta EV (Exit \u2212 Entry)", format_currency(delta_ev)),
        (
            "Entry Leverage (Debt / EV)",
            f"{entry_leverage * 100:,.0f}%" if not math.isnan(entry_leverage) else "N/M",
        ),
        (
            "Exit Leverage (Net Debt / EV)",
            f"{exit_leverage * 100:,.0f}%" if not math.isnan(exit_leverage) else "N/M",
        ),
        ("Bridge Components", ""),
        ("EBITDA Growth Impact", format_currency(ebitda_growth_impact)),
        ("Multiple Expansion Impact", format_currency(multiple_expansion_impact)),
        ("Interaction Effect", format_currency(interaction_effect)),
        (debt_label, format_currency(debt_effect)),
        ("Contribution %", ""),
        ("EBITDA Growth Contribution", pct_contrib(ebitda_growth_impact)),
        ("Multiple Expansion Contribution", pct_contrib(multiple_expansion_impact)),
        ("Interaction Contribution", pct_contrib(interaction_effect)),
        (f"{debt_label} Contribution", pct_contrib(debt_effect)),
        ("Model Integrity", ""),
        (
            "Reconciliation Check (Tolerance < $0.01)",
            format_currency(reconciliation_check),
        ),
    ]

    summary_df = pd.DataFrame(summary_rows, columns=["Metric", "Value"])
    st.dataframe(summary_df, width="stretch", hide_index=True)

    is_balanced = abs(reconciliation_check) < 0.01
    if is_balanced:
        st.success("Model Balanced \u2013 All inputs reconcile correctly.")
    else:
        st.error("Check Math \u2013 Model does not reconcile.")

# ---------------------------------------------------------------------------
# Tab 3: Executive Summary
# ---------------------------------------------------------------------------

with summary_tab:
    value_creation = exit_equity - entry_equity
    driver_candidates = {
        "EBITDA Growth": ebitda_growth_impact,
        "Multiple Expansion": multiple_expansion_impact,
        "Interaction Effect": interaction_effect,
        debt_label: debt_effect,
    }

    st.subheader("Executive Summary")

    if invalid_capital_structure:
        st.write("Transaction structure is invalid for standard LBO analysis.")
    elif value_creation > 0:
        primary_driver = max(driver_candidates, key=driver_candidates.get)
        primary_driver_value = driver_candidates[primary_driver]
        st.markdown(
            f"The deal **created {md_currency(abs(value_creation))} million** "
            f"in equity value. The primary driver was **{primary_driver}**, "
            f"contributing {md_currency(primary_driver_value)} million."
        )
    elif value_creation < 0:
        primary_driver = min(driver_candidates, key=driver_candidates.get)
        primary_driver_value = abs(driver_candidates[primary_driver])
        st.markdown(
            f"The deal **eroded {md_currency(abs(value_creation))} million** "
            f"in equity value. The primary driver of value loss was "
            f"**{primary_driver}**, reducing equity by "
            f"{md_currency(primary_driver_value)} million."
        )
    else:
        st.write("Net equity value was unchanged over the holding period.")

    if not invalid_capital_structure and not math.isnan(moic) and moic < 1.0:
        st.warning("The transaction results in a capital loss (MOIC < 1.0x).")

    st.divider()

    st.subheader("Contribution Breakdown")

    comp_col1, comp_col2 = st.columns(2)

    driver_info = [
        ("EBITDA Growth", ebitda_growth_impact, "Operational performance improvement."),
        ("Multiple Expansion", multiple_expansion_impact, "Change in market valuation."),
        (
            "Interaction Effect",
            interaction_effect,
            "Combined effect of growth and re-rating.",
        ),
        (debt_label, debt_effect, "Leverage / deleveraging impact."),
    ]

    for i, (label, val, desc) in enumerate(driver_info):
        col = comp_col1 if i < 2 else comp_col2
        with col:
            if val > 0:
                badge = "\u2705"
                prefix = "+"
            elif val < 0:
                badge = "\u274c"
                prefix = "\u2212"
            else:
                badge = "\u2796"
                prefix = ""
            st.markdown(
                f"{badge} **{label}**: "
                f"{prefix}{md_currency(abs(val))} mm"
            )
            st.caption(desc)

    st.divider()

    st.subheader("Relative Contribution")

    contrib_data = pd.DataFrame({
        "Component": component_labels,
        "Value": components,
    })
    contrib_data["Abs Value"] = contrib_data["Value"].abs()
    contrib_data["Color"] = contrib_data["Value"].apply(
        lambda v: "#2e7d32" if v >= 0 else "#c62828"
    )

    contrib_fig = go.Figure()
    for _, row in contrib_data.iterrows():
        contrib_fig.add_trace(
            go.Bar(
                x=[row["Abs Value"]],
                y=[row["Component"]],
                orientation="h",
                marker_color=row["Color"],
                text=f"{format_currency(abs(row['Value']))} mm",
                textposition="outside",
                showlegend=False,
                hovertemplate="%{y}: %{text}<extra></extra>",
            )
        )

    contrib_fig.update_layout(
        xaxis_title="Absolute Contribution ($mm)",
        xaxis={
            "tickfont": {"family": "Inter, sans-serif", "color": "#5b5b6b"},
            "gridcolor": "#f0ebe3",
            "zeroline": False,
        },
        yaxis={
            "tickfont": {"family": "Inter, sans-serif", "color": "#1a1a2e", "size": 13},
        },
        plot_bgcolor="#faf8f5",
        paper_bgcolor="#faf8f5",
        margin={"l": 10, "r": 80, "t": 10, "b": 10},
        height=200,
        font={"family": "Inter, sans-serif"},
        barmode="group",
    )
    contrib_fig.update_xaxes(showgrid=True, gridcolor="#f0ebe3")
    contrib_fig.update_yaxes(showgrid=False)

    st.plotly_chart(contrib_fig, width="stretch")

# ---------------------------------------------------------------------------
# Tab 4: How It Works
# ---------------------------------------------------------------------------

with how_tab:
    st.subheader("How the LBO Value Creation Bridge Works")

    st.markdown(
        "A leveraged buyout (LBO) creates (or destroys) equity value through "
        "four channels. This tool decomposes the total change in equity into its "
        "additive components so you can see exactly what drove returns."
    )

    with st.expander("1. Core Enterprise & Equity Values", expanded=True):
        st.markdown(
            f"""
**Enterprise Value (EV)** = EBITDA \u00d7 Multiple

- **Entry EV**: {entry_ebitda:,.0f} \u00d7 {entry_multiple:.0f}x = **{md_currency(entry_ev)}**
- **Exit EV**: {exit_ebitda:,.0f} \u00d7 {exit_multiple:.0f}x = **{md_currency(exit_ev)}**

**Equity Value** = Enterprise Value \u2212 Net Debt

- **Entry Equity**:
  {md_currency(entry_ev)} \u2212 {md_currency(initial_debt)}
  = **{md_currency(entry_equity)}**
- **Exit Equity**:
  {md_currency(exit_ev)} \u2212 {md_currency(exit_net_debt)}
  = **{md_currency(exit_equity)}**
        """
        )

    with st.expander("2. The Three-Part EV Bridge (Algebraic Identity)"):
        st.markdown(
            """
The change in enterprise value (\u0394EV) can be broken into three additive components.
This is a **mathematical identity** \u2014 it always holds:

\u0394**EV = EBITDA Growth + Multiple Expansion + Interaction Effect**

| Component | Formula | Current Value |
|-----------|---------|---------------|
| **EBITDA Growth** | (Exit EBITDA \u2212 Entry EBITDA) \u00d7 Entry Multiple | |
| **Multiple Expansion** | Entry EBITDA \u00d7 (Exit Multiple \u2212 Entry Multiple) | |
| **Interaction Effect** |
  (Exit EBITDA \u2212 Entry EBITDA) \u00d7 (Exit Multiple \u2212 Entry Multiple) | |

The interaction effect captures what happens when *both* EBITDA and the multiple change
simultaneously. If you grew EBITDA and expanded the multiple, the interaction effect
is the additional value created beyond what each would have generated alone.
        """
        )
        st.markdown(
            f"""
**With your numbers:**

| Component | Calculation | Value |
|-----------|------------|-------|
| EBITDA Growth |
  ({exit_ebitda:,.0f} \u2212 {entry_ebitda:,.0f}) \u00d7 {entry_multiple:.0f}x
  | **{md_currency(ebitda_growth_impact)}** |
| Multiple Expansion |
  {entry_ebitda:,.0f} \u00d7 ({exit_multiple:.0f}x \u2212 {entry_multiple:.0f}x)
  | **{md_currency(multiple_expansion_impact)}** |
| Interaction Effect |
  ({exit_ebitda:,.0f} \u2212 {entry_ebitda:,.0f})
  \u00d7 ({exit_multiple:.0f}x \u2212 {entry_multiple:.0f}x)
  | **{md_currency(interaction_effect)}** |
| **Total \u0394EV** | | **{md_currency(delta_ev)}** |
        """
        )

    with st.expander("3. Debt Component & Full Equity Bridge"):
        st.markdown(
            f"""
Equity value also changes when debt is paid down (or added). Every dollar of debt paydown
flows directly to equity holders.

- **{debt_label}**: {md_currency(debt_effect)}

**Full Bridge Identity:**

> Exit Equity = Entry Equity + EBITDA Growth + Multiple Expansion
> + Interaction Effect + Debt Component

**Reconciliation Check:** {md_currency(reconciliation_check)}
        """
        )
        if abs(reconciliation_check) < 0.01:
            st.success("\u2713 The model balances perfectly.")
        else:
            st.error("\u2717 The model does not balance.")

    with st.expander("4. Return Metrics"):
        st.markdown(
            f"""
**MOIC** (Multiple of Invested Capital) = Exit Equity \u00f7 Entry Equity

- MOIC = {md_currency(exit_equity)} \u00f7 {md_currency(entry_equity)} = **{moic_display}**

**IRR** (Internal Rate of Return) = MOIC^(1/n) \u2212 1, where n = holding period

- IRR = {moic_display}^(1 \u00f7 {holding_period_years:,.0f}) \u2212 1 = **{irr_display}**
- *Assumes a single terminal cash flow and no interim dividends.*
        """
        )

    with st.expander("5. Key Intuitions"):
        st.markdown(
            """
- **EBITDA Growth** reflects operational performance
  — the company's earnings power increased.
- **Multiple Expansion** reflects market sentiment
  — investors pay more for each dollar of earnings.
- **The Interaction Effect** is the "double count" of
  simultaneous growth and re-rating — largest when
  both move significantly in the same direction.
- **Debt Paydown** directly increases equity
  — leverage amplifies both gains and losses.
- If the model is balanced (reconciliation < $0.01), the math is correct.
        """
        )

# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------

st.divider()
st.markdown(
    """
    <div style="text-align:center; color:#8f8f9f; font-size:0.8rem; padding: 1rem 0;">
        Built by an MBA student ·
        <a href="https://github.com/KaramelBytes/LBO-learning-sim" target="_blank" style="color:#8f8f9f; text-decoration:underline;">View source on GitHub</a> ·
        MIT Licensed
    </div>
    """,
    unsafe_allow_html=True,
)
