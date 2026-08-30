import pandas as pd

# ==========================================
# 1. LOAD DATA
# ==========================================

df = pd.read_csv("inventory_data_500.csv")

print("Inventory dataset loaded successfully!")

print("\nDataset Shape:")
print(df.shape)

# ==========================================
# 2. DATA QUALITY CHECK
# ==========================================

print("\nMissing Values:")
print(df.isnull().sum())

# ==========================================
# 3. DAYS OF INVENTORY
# ==========================================

df["days_of_inventory"] = (df["current_stock"] / df["avg_daily_sales"]).round(2)

# ==========================================
# 4. LEAD-TIME DEMAND
# ==========================================

df["lead_time_demand"] = (df["avg_daily_sales"] * df["lead_time_days"]).round(0)

# ==========================================
# 5. TARGET STOCK
# ==========================================

TARGET_DAYS = 7

df["target_stock"] = (df["avg_daily_sales"] * TARGET_DAYS).round(0)

# ==========================================
# 6. REORDER QUANTITY
# ==========================================

df["reorder_quantity"] = (df["target_stock"] - df["current_stock"]).clip(lower=0)

# ==========================================
# 7. INVENTORY STATUS
# ==========================================

def inventory_status(row):

    if row["days_of_inventory"] <= row["lead_time_days"]:
        return "CRITICAL"

    elif row["days_of_inventory"] <= row["lead_time_days"] + 2:
        return "WARNING"

    else:
        return "HEALTHY"

df["status"] = df.apply(inventory_status,axis=1)

# ==========================================
# 8. STOCKOUT RISK
# ==========================================

df["stockout_risk"] = (df["current_stock"] < df["lead_time_demand"])

# ==========================================
# 9. REORDER VALUE
# ==========================================

df["reorder_value"] = (df["reorder_quantity"] * df["unit_cost"]).round(2)

# ==========================================
# 10. INVENTORY VALUE
# ==========================================

df["current_inventory_value"] = (df["current_stock"] * df["unit_cost"]).round(2)

# ==========================================
# 11. POTENTIAL REVENUE AT RISK
# ==========================================

df["revenue_at_risk"] = (df["avg_daily_sales"] * df["selling_price"] *df["lead_time_days"]).round(2)

# ==========================================
# 12. PRIORITY
# ==========================================

def calculate_priority(row):

    if row["stockout_risk"] and row["status"] == "CRITICAL":
        return "URGENT"

    elif row["status"] == "CRITICAL":
        return "HIGH"

    elif row["status"] == "WARNING":
        return "MEDIUM"

    else:
        return "LOW"

df["priority"] = df.apply(calculate_priority,axis=1)

# ==========================================
# 13. REORDER REQUIRED
# ==========================================

df["reorder_required"] = (df["reorder_quantity"] > 0)

# ==========================================
# 14. DISPLAY TOP PRIORITY PRODUCTS
# ==========================================

print("\n========== TOP PRIORITY PRODUCTS ==========")

priority_order = {
    "URGENT": 1,
    "HIGH": 2,
    "MEDIUM": 3,
    "LOW": 4
}

df["priority_rank"] = df["priority"].map(priority_order)

top_products = (df.sort_values(["priority_rank", "revenue_at_risk"],ascending=[True, False]).head(15))

print(
    top_products[
        [
            "product_name",
            "store",
            "current_stock",
            "avg_daily_sales",
            "lead_time_days",
            "days_of_inventory",
            "reorder_quantity",
            "reorder_value",
            "revenue_at_risk",
            "priority"
        ]
    ].to_string(index=False))

# ==========================================
# 15. OVERALL SUMMARY
# ==========================================

print("\n========== INVENTORY SUMMARY ==========")

print("Total Records:", len(df))

print("Critical:",(df["status"] == "CRITICAL").sum())

print("Warning:",(df["status"] == "WARNING").sum())

print("Healthy:",(df["status"] == "HEALTHY").sum())

print("Stockout Risk:",df["stockout_risk"].sum())

print("Reorder Required:",df["reorder_required"].sum())

print("Total Reorder Value: ₹",round(df["reorder_value"].sum(), 2))

print("Revenue at Risk: ₹",round(df["revenue_at_risk"].sum(), 2))

print("========================================")

# ==========================================
# 16. SAVE REPORT
# ==========================================

df = df.drop(columns=["priority_rank"])

df.to_csv("reorder_report.csv",index=False)

print("\nReorder report saved successfully!")