import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations
from collections import Counter

df = pd.read_csv("Sales_May_2019.csv")
df = df.replace({
    "Order ID": "Order ID",
    "Product": "Product",
    "Quantity Ordered": "Quantity Ordered",
    "Price Each": "Price Each",
    "Order Date": "Order Date",
    "Purchase Address": "Purchase Address"
}, np.nan)
df = df.dropna()

df["Quantity Ordered"] = pd.to_numeric(df["Quantity Ordered"])
df["Price Each"] = pd.to_numeric(df["Price Each"])
df["Sales"] = df["Quantity Ordered"] * df["Price Each"]
df["Date"] = df["Order Date"].str[3:5]
df["City"] = df["Purchase Address"].apply(lambda x: x.split(",")[1]) + "," + df["Purchase Address"].apply(lambda x: x.split(",")[2][:3])
df["Hour"] = df["Order Date"].str[9:11]

# Print highest sale and date on which it occured
print("Highest purchase of {} was done on {} at {}".format(df["Sales"].max(),
                                                           str(df.loc[df["Sales"].max()]["Order Date"])[:8],
                                                           str(df.loc[df["Sales"].max()]["Order Date"])[9:]))  # Highest sale

# Calculate the most oftenly sold together
all_data = df[df["Order ID"].duplicated(keep=False)]
all_data["Grouped"] = df.groupby("Order ID")["Product"].transform(lambda x: ",".join(x))
all_data = all_data[["Order ID", "Grouped"]].drop_duplicates()
count = Counter()
for row in all_data["Grouped"]:
    row_list = row.split(",")
    count.update((Counter(combinations(row_list, 2))))
print(count.most_common(10)[0])  # Most oftenly sold together

# Price of each item
price = df.groupby("Product")["Price Each"].mean()
print(price)

# Plot graph between Date and Sales
date_range = range(1, 32)
df["Date"] = pd.to_numeric(df["Date"])
result_1 = df.groupby("Date").sum()
plt.bar(date_range, result_1["Sales"])
plt.xticks(date_range)
plt.title("Date vs Sales graph")
plt.xlabel("Date")
plt.ylabel("Sales")

plt.show()

# Plot graph between City and Sales
city_range = [city for city, new_df in df.groupby("City")]
result_2 = df.groupby("City").sum()
plt.bar(city_range, result_2["Sales"])
plt.xticks(city_range, rotation="vertical", size=8)
plt.title("City vs Sales")
plt.xlabel("City")
plt.ylabel("Sales")

plt.show()

# Plot graph between Hour and Sales
hour_range = range(0, 24)
result_3 = df.groupby("Hour").sum()
plt.bar(hour_range, result_3["Sales"])
plt.xticks(hour_range)
plt.title("Hour vs Sales")
plt.xlabel("Hour")
plt.ylabel("Sales")

plt.show()

# Plot graph between Product and Product Quantity
product_group = df.groupby("Product")
product_quantity = product_group["Quantity Ordered"].sum()
products = [product for product, all_data in product_group]
plt.bar(products, product_quantity)
plt.xticks(products, rotation="vertical", size=8)
plt.xlabel("Product")
plt.ylabel("Product quantity")

plt.show()