import numpy as np
import pandas as pd


def stats_print(name: str, series: pd.Series) -> pd.Series:
    """Print descriptive stats and impute missing values using mean or median."""
    skewness = series.skew()
    n_missing = series.isnull().sum()

    print(f"\n--- {name} ---")
    print(f"  Mean   : {series.mean():.4f}")
    print(f"  Median : {series.median():.4f}")
    print(f"  Std    : {series.std():.4f}")
    print(f"  Skew   : {skewness:.4f}")
    print(f"  Missing: {n_missing} ({n_missing / len(series) * 100:.1f}%)")

    if abs(skewness) > 1:
        fill_value = series.median()
        strategy = "median (skewed)"
    else:
        fill_value = series.mean()
        strategy = "mean (symmetric)"

    print(f"  Strategy: {strategy} → fill with {fill_value:.4f}")
    return series.fillna(fill_value)


def impute_from_distribution(series: pd.Series, seed: int = 42) -> pd.Series:
    """Impute NaN by random sampling from the observed (non-NaN) distribution."""
    observed = series.dropna().values
    missing_mask = series.isnull()
    n_missing = missing_mask.sum()

    if n_missing == 0:
        return series

    rng = np.random.default_rng(seed)
    fills = rng.choice(observed, size=n_missing, replace=True)
    result = series.copy()
    result.loc[missing_mask] = fills
    return result
