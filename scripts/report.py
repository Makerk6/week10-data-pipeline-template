import pandas as pd
import os
import logging
import sys

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logging.info("Start of execution")

try:
    # Ensure output directory exists
    os.makedirs("output", exist_ok=True)

    logging.info("Loading data...")
    try:
        df = pd.read_parquet("data/sample_data.parquet")
    except FileNotFoundError:
        logging.exception("Missing file error: data/sample_data.parquet was not found")
        sys.exit(1)
    except Exception:
        logging.exception("Data loading failure: unable to read data/sample_data.parquet")
        sys.exit(1)

    logging.info("Processing data...")
    df["revenue"] = df["price"] * df["qty"]

    # Compute summary
    summary = df.groupby("category").agg(
        total_revenue=("revenue", "sum"),
        total_quantity=("qty", "sum"),
        avg_price=("price", "mean"),
        transaction_count=("category", "size")
    ).reset_index()

    summary = summary[[
        "category",
        "total_revenue",
        "total_quantity",
        "avg_price",
        "transaction_count",
    ]]

    logging.info("Report generation step")
    summary.to_csv("output/report.csv", index=False)

    logging.info("Completion message: report generated at output/report.csv")
except Exception:
    logging.exception("Unexpected runtime error while generating the report")
    sys.exit(1)