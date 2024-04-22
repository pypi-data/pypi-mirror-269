from l4v1.price_volume_mix import pvm_plot, pvm_table
import polars as pl
import datetime as dt

df = pl.read_parquet("../data/supermarket_sales.parquet").with_columns(
    pl.col(pl.Categorical).cast(pl.Utf8)
)

df1 = df.filter(pl.col("Datetime").dt.week() == 4)
df2 = df.filter(pl.col("Datetime").dt.week() == 5)

df1.columns

# Create the performance volume mix table
pvm_df = pvm_table(
    df_primary=df1,
    df_comparison=df2,
    group_by_columns=["Customer type", "Product line"],
    metrics={"volume": "Quantity", "outcome": "Total"},
)

pvm_df

pvm_plot(
    pvm_table=pvm_df,
    outcome_metric_name="Total",
    primary_label="lala",
    comparison_label="zaza",
)
