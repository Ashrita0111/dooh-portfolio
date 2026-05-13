import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("outputs/full_audit.csv")
summary = pd.read_csv("outputs/campaign_summary.csv")
mg = pd.read_csv("outputs/makegood_schedule.csv")

# --- Chart 1: status breakdown per campaign ---
fig, ax = plt.subplots(figsize=(10, 5))
x = range(len(summary))
width = 0.25

ax.bar([i - width for i in x], summary["on_track_days"],
       width, label="On track", color="#1D9E75")
ax.bar(list(x), summary["under_delivery_days"],
       width, label="Under-delivery", color="#E24B4A")
ax.bar([i + width for i in x], summary["over_delivery_days"],
       width, label="Over-delivery", color="#EF9F27")

ax.set_xticks(list(x))
ax.set_xticklabels(summary["campaign_id"])
ax.set_xlabel("Campaign")
ax.set_ylabel("Days")
ax.set_title("Delivery status by campaign (30-day period)")
ax.legend()
plt.tight_layout()
plt.savefig("outputs/chart_status_breakdown.png", dpi=150)
plt.close()
print("Chart 1 saved")

# --- Chart 2: overall delivery rate per campaign ---
fig, ax = plt.subplots(figsize=(8, 4))
colors = ["#E24B4A" if r < 90 else "#1D9E75"
          for r in summary["overall_delivery_rate"]]
ax.bar(summary["campaign_id"], summary["overall_delivery_rate"], color=colors)
ax.axhline(y=90, color="#E24B4A", linestyle="--", linewidth=1, label="90% min threshold")
ax.axhline(y=105, color="#EF9F27", linestyle="--", linewidth=1, label="105% max threshold")
ax.set_ylim(85, 110)
ax.set_ylabel("Delivery rate (%)")
ax.set_title("Overall delivery rate by campaign")
ax.legend()
plt.tight_layout()
plt.savefig("outputs/chart_delivery_rate.png", dpi=150)
plt.close()
print("Chart 2 saved")

# --- Chart 3: make-good impressions owed ---
fig, ax = plt.subplots(figsize=(8, 4))
ax.bar(mg["campaign_id"], mg["total_impressions_owed"], color="#534AB7")
for i, (val, screens) in enumerate(zip(mg["total_impressions_owed"],
                                        mg["screens_affected"])):
    ax.text(i, val + 500, f"{val:,}\n({screens} screens)",
            ha="center", fontsize=9, color="#26215C")
ax.set_ylabel("Impressions owed")
ax.set_title("Make-good impressions required per campaign")
plt.tight_layout()
plt.savefig("outputs/chart_makegood.png", dpi=150)
plt.close()
print("Chart 3 saved")

print("\nAll charts saved to outputs/")