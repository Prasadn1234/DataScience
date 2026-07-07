# ============================================================================
# WEEK 2.3: EXPLORATORY DATA ANALYSIS
# ============================================================================
#
# Assumes `all_docs_flat` (from week2_process_all.py) is already in scope.

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set style
plt.style.use('seaborn-v0_8-whitegrid')

print("EXPLORATORY DATA ANALYSIS")
print("=" * 60)

# Fixed categorical palette (CVD-validated order): one color per contract
# category, keyed by name so it stays stable across charts and any future
# re-filtering, rather than being assigned by sort rank.
CATEGORY_COLORS = {
    "master_level_agreements": "#2a78d6",
    "transaction_contracts": "#1baf7a",
    "commercial_documents": "#eda100",
    "financial_and_billing": "#008300",
    "operational_documents": "#4a3aa7",
    "compliance_documents": "#e34948",
    "negotiation_history": "#e87ba4",
    "governance": "#eb6834",
}
DEFAULT_COLOR = "#898781"  # muted gray, for any category outside the 8 (e.g. the sample fallback)

# Create a DataFrame from all_docs_flat
df = pd.DataFrame(all_docs_flat)

if df.empty:
    print("No documents to analyze - all_docs_flat is empty.")
else:
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Visualization 1: Category distribution
    category_counts = df['category'].value_counts()
    bar_colors = [CATEGORY_COLORS.get(cat, DEFAULT_COLOR) for cat in category_counts.index]
    axes[0, 0].bar(category_counts.index, category_counts.values, color=bar_colors)
    axes[0, 0].set_title('Document Count by Category')
    axes[0, 0].set_xlabel('Category')
    axes[0, 0].set_ylabel('Number of Documents')
    axes[0, 0].tick_params(axis='x', rotation=45)
    for label in axes[0, 0].get_xticklabels():
        label.set_ha('right')

    # Visualization 2: Word count distribution
    axes[0, 1].hist(df['word_count'], bins=15, color="#2a78d6", edgecolor="white")
    axes[0, 1].set_title('Word Count Distribution')
    axes[0, 1].set_xlabel('Word Count')
    axes[0, 1].set_ylabel('Number of Documents')

    # Visualization 3: Word count by category (box plot)
    category_order = category_counts.index.tolist()
    palette = [CATEGORY_COLORS.get(cat, DEFAULT_COLOR) for cat in category_order]
    sns.boxplot(
        data=df, x='category', y='word_count', order=category_order,
        hue='category', palette=palette, legend=False, ax=axes[1, 0],
    )
    axes[1, 0].set_title('Word Count by Category')
    axes[1, 0].set_xlabel('Category')
    axes[1, 0].set_ylabel('Word Count')
    axes[1, 0].tick_params(axis='x', rotation=45)
    for label in axes[1, 0].get_xticklabels():
        label.set_ha('right')

    # Visualization 4: Summary statistics
    axes[1, 1].axis('off')
    summary_lines = [
        f"Total documents:   {len(df)}",
        f"Categories:        {df['category'].nunique()}",
        f"Total words:       {df['word_count'].sum():,}",
        f"Mean words/doc:    {df['word_count'].mean():.1f}",
        f"Median words/doc:  {df['word_count'].median():.1f}",
        f"Min words/doc:     {df['word_count'].min()}",
        f"Max words/doc:     {df['word_count'].max()}",
    ]
    axes[1, 1].text(
        0.05, 0.95, "\n".join(summary_lines),
        transform=axes[1, 1].transAxes, va='top', ha='left',
        fontsize=12, family='monospace',
    )
    axes[1, 1].set_title('Summary Statistics')

    plt.tight_layout()
    plt.savefig('contract_eda.png', dpi=150, bbox_inches='tight')
    plt.show()

    print("\nEDA visualizations saved to contract_eda.png")
