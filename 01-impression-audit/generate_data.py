import pandas as pd
import numpy as np
import random

random.seed(42)
np.random.seed(42)

screens = [f"SCR_{str(i).zfill(3)}" for i in range(1, 51)]
campaigns = ["CAMP_A", "CAMP_B", "CAMP_C", "CAMP_D", "CAMP_E"]
dates = pd.date_range("2024-01-01", "2024-01-30")

rows = []
for date in dates:
    for campaign in campaigns:
        for screen in random.sample(screens, 20):
            booked = random.choice([3000, 4000, 5000, 6000])
            roll = random.random()
            if roll < 0.08:
                delivered = int(booked * random.uniform(0.5, 0.88))
            elif roll < 0.12:
                delivered = int(booked * random.uniform(1.06, 1.20))
            else:
                delivered = int(booked * random.uniform(0.91, 1.04))
            rows.append({
                "screen_id": screen,
                "campaign_id": campaign,
                "date": date.strftime("%Y-%m-%d"),
                "booked_impressions": booked,
                "delivered_impressions": delivered
            })

df = pd.DataFrame(rows)
df.to_csv("data/play_log.csv", index=False)
print(f"Generated {len(df)} rows")