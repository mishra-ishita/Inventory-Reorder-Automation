import pandas as pd


# ------------------------------------------
# 1. LOAD REORDER REPORT
# ------------------------------------------

df = pd.read_csv("reorder_report.csv")

print("Reorder report loaded successfully!")
print("Total records:", len(df))


# ------------------------------------------
# 2. GENERATE RECOMMENDATIONS
# ------------------------------------------

def generate_recommendation(row):

    priority = row["priority"]

    # URGENT
    if priority == "URGENT":

        return (
            f"URGENT:" 
            f"Reorder {int(row['reorder_quantity'])} units of {row['product_name']} at {row['store']} immediately. "
            f"Current inventory covers only {row['days_of_inventory']:.1f} days, while supplier lead time is {row['lead_time_days']} days. "
            f"Estimated revenue exposure is ₹{row['revenue_at_risk']:,.0f}."
        )

    # HIGH
    elif priority == "HIGH":

        return (
            f"HIGH PRIORITY:"
            f"Reorder {int(row['reorder_quantity'])} units of {row['product_name']} at {row['store']}. "
            f"Inventory coverage is {row['days_of_inventory']:.1f} days against a {row['lead_time_days']}-day supplier lead time. "
            f"Estimated revenue exposure is ₹{row['revenue_at_risk']:,.0f}."
        )

    # MEDIUM
    elif priority == "MEDIUM":

        return (
            f"MONITOR:" 
            f"{row['product_name']} at {row['store']} has moderate inventory risk. "
            f"Continue monitoring daily sales and stock levels."
        )

    # LOW / HEALTHY
    else:

        return (
            f"NO IMMEDIATE ACTION:"
            f"{row['product_name']} at {row['store']} has sufficient inventory. "
            f"Continue routine monitoring."
        )


# Apply recommendation to ALL rows

df["ai_recommendation"] = df.apply(
    generate_recommendation,
    axis=1
)


# ------------------------------------------
# 3. SAVE MASTER REPORT
# ------------------------------------------

df.to_csv(
    "inventory_master_report.csv",
    index=False
)


print("\n------------------------------------------")
print("MASTER INVENTORY REPORT CREATED")
print("------------------------------------------")

print("Total records:", len(df))

print(
    "\nPriority distribution:"
)

print(
    df["priority"].value_counts()
)


print(
    "\nSaved as:"
)

print(
    "inventory_master_report.csv"
)