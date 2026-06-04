import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.outliers_influence import variance_inflation_factor


def ols_diagnostics(model, label: str = "") -> None:
    """Residuals vs Fitted, Normal Q-Q plot, and Breusch-Pagan test."""
    fitted = model.fittedvalues
    residuals = model.resid
    std_resid = residuals / residuals.std()

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Residuals vs Fitted
    axes[0].scatter(fitted, residuals, alpha=0.4, s=15, color="steelblue")
    axes[0].axhline(0, color="red", linestyle="--", lw=1.5)
    axes[0].set_xlabel("Fitted values")
    axes[0].set_ylabel("Residuals")
    axes[0].set_title(f"Residuals vs Fitted — {label}", fontweight="bold")

    # Normal Q-Q
    (osm, osr), (slope, intercept, _) = stats.probplot(residuals, dist="norm")
    axes[1].scatter(osm, osr, alpha=0.4, s=15, color="steelblue")
    axes[1].plot(osm, slope * np.array(osm) + intercept, color="red", lw=1.5)
    axes[1].set_xlabel("Theoretical quantiles")
    axes[1].set_ylabel("Sample quantiles")
    axes[1].set_title(f"Normal Q-Q — {label}", fontweight="bold")

    plt.tight_layout()
    plt.show()

    # Breusch-Pagan test
    bp_stat, bp_p, _, _ = het_breuschpagan(residuals, model.model.exog)
    print(f"Breusch-Pagan test — {label}")
    print(f"  LM statistic : {bp_stat:.4f}")
    print(f"  p-value      : {bp_p:.4f}")
    if bp_p < 0.05:
        print("  → Heteroscedasticity detected (p < 0.05). Use HC3 robust SE.")
    else:
        print("  → No significant heteroscedasticity (p ≥ 0.05).")


def model_summary_row(model, name: str, predictors: list) -> dict:
    """Return a dict summarising a fitted OLS model for comparison tables."""
    row = {
        "model"  : name,
        "n"      : int(model.nobs),
        "r2"     : round(model.rsquared, 4),
        "adj_r2" : round(model.rsquared_adj, 4),
        "aic"    : round(model.aic, 2),
        "bic"    : round(model.bic, 2),
    }
    for pred in predictors:
        if pred in model.params:
            row[f"coef_{pred}"] = round(model.params[pred], 4)
            row[f"p_{pred}"]    = round(model.pvalues[pred], 4)
    return row
