import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def plot_distributions(df: pd.DataFrame, biomarkers: list, group_col: str, ncols: int = 4) -> None:
    """Plot KDE distributions for each biomarker, stratified by group_col."""
    nrows = -(-len(biomarkers) // ncols)  # ceiling division
    fig, axes = plt.subplots(nrows, ncols, figsize=(ncols * 4, nrows * 3.5))
    axes = axes.flatten()

    for i, col in enumerate(biomarkers):
        for group, subset in df.groupby(group_col):
            axes[i].hist(subset[col].dropna(), bins=30, alpha=0.5, label=str(group), density=True)
        axes[i].set_title(col, fontweight="bold")
        axes[i].set_xlabel(col)
        axes[i].set_ylabel("Density")
        if i == 0:
            axes[i].legend(title=group_col)

    for j in range(len(biomarkers), len(axes)):
        axes[j].set_visible(False)

    plt.suptitle(f"Biomarker distributions by {group_col}", fontsize=13, fontweight="bold")
    plt.tight_layout()
    plt.show()


def plot_regplots(df: pd.DataFrame, predictors: list, target: str, title: str = "") -> None:
    """Scatter plots with LOWESS regression line for each predictor vs target."""
    ncols = 3
    nrows = -(-len(predictors) // ncols)
    fig, axes = plt.subplots(nrows, ncols, figsize=(ncols * 4.5, nrows * 4))
    axes = axes.flatten()

    for i, pred in enumerate(predictors):
        sns.regplot(
            data=df, x=pred, y=target,
            ax=axes[i], lowess=True,
            scatter_kws={"alpha": 0.3, "s": 12},
            line_kws={"color": "tomato", "lw": 2},
        )
        axes[i].set_title(f"{pred} vs {target}", fontweight="bold")

    for j in range(len(predictors), len(axes)):
        axes[j].set_visible(False)

    if title:
        plt.suptitle(title, fontsize=13, fontweight="bold")
    plt.tight_layout()
    plt.show()


def plot_correlation_heatmap(df: pd.DataFrame, biomarkers: list) -> None:
    """Pearson correlation heatmap for the given biomarkers."""
    corr = df[biomarkers].corr()
    mask = pd.DataFrame(False, index=corr.index, columns=corr.columns)
    for i in range(len(mask)):
        for j in range(i):
            mask.iloc[i, j] = True

    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(
        corr, mask=mask, annot=True, fmt=".2f",
        cmap="coolwarm", center=0, linewidths=0.5,
        square=True, ax=ax,
    )
    ax.set_title("Pearson correlation matrix — biomarkers", fontsize=13, fontweight="bold")
    plt.tight_layout()
    plt.show()
