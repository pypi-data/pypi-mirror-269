from l4v1.impact_analysis import impact_plot, impact_table
import polars as pl

df = pl.scan_parquet("data/supermarket_sales.parquet").with_columns(
    pl.col(pl.Categorical).cast(pl.Utf8)
)

sales_week5 = df.filter(pl.col("Datetime").dt.week() == 5)
sales_week6 = df.filter(pl.col("Datetime").dt.week() == 6)

impact_table_df = impact_table(
    df_primary=sales_week6,
    df_comparison=sales_week5,
    group_by_columns=["Branch", "Product line"],
    volume_metric_name="Quantity",
    outcome_metric_name="Total",
)

impact_plot(
    impact_table=impact_table_df,
    format_data_labels="{:,.0f}",
    primary_total_label="Test1",
    comparison_total_label="Test2",
    title="Detailed Impact Analysis"
)
