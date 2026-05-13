import pandas as pd

df = pd.read_csv("data/play_log.csv")

# Step 1: calculate delivery rate
df["delivery_rate"] = df["delivered_impressions"] / df["booked_impressions"]

# Step 2: flag status
def flag_status(rate):
    if rate < 0.90:
        return "UNDER-DELIVERY"
    elif rate > 1.05:
        return "OVER-DELIVERY"
    else:
        return "ON TRACK"

df["status"] = df["delivery_rate"].apply(flag_status)

# Step 3: calculate impression deficit / surplus
df["impression_diff"] = df["delivered_impressions"] - df["booked_impressions"]

# Step 4: summary by campaign
summary = df.groupby("campaign_id").agg(
    total_booked=("booked_impressions", "sum"),
    total_delivered=("delivered_impressions", "sum"),
    under_delivery_days=("status", lambda x: (x == "UNDER-DELIVERY").sum()),
    over_delivery_days=("status", lambda x: (x == "OVER-DELIVERY").sum()),
    on_track_days=("status", lambda x: (x == "ON TRACK").sum())
).reset_index()

summary["overall_delivery_rate"] = (
    summary["total_delivered"] / summary["total_booked"] * 100
).round(2)

# Step 5: make-good calculation
makegood = df[df["status"] == "UNDER-DELIVERY"].copy()
makegood["impressions_owed"] = makegood["booked_impressions"] - makegood["delivered_impressions"]

makegood_summary = makegood.groupby("campaign_id").agg(
    total_impressions_owed=("impressions_owed", "sum"),
    screens_affected=("screen_id", "nunique"),
    days_affected=("date", "nunique")
).reset_index()

# Step 6: export results
df.to_csv("outputs/full_audit.csv", index=False)
summary.to_csv("outputs/campaign_summary.csv", index=False)
makegood_summary.to_csv("outputs/makegood_schedule.csv", index=False)

print("=== AUDIT COMPLETE ===")
print(f"Total rows audited: {len(df)}")
print(f"\nStatus breakdown:")
print(df["status"].value_counts())
print(f"\nCampaign summary:")
print(summary.to_string(index=False))
print(f"\nMake-good required:")
print(makegood_summary.to_string(index=False))