import pandas as pd
import json

# Read the CSV files
customers = pd.read_csv("customers.csv")
orders = pd.read_csv("orders.csv")
products = pd.read_csv("products.csv")

# Filter orders with status "Delivered"
delivered_orders = orders[orders["Status"] == "Delivered"]

# Merge delivered orders with products on ProductID to get Price
orders_products = pd.merge(delivered_orders, products, on="ProductID", how="inner")

# Calculate total spent per order line: Quantity * Price
orders_products["LineTotal"] = orders_products["Quantity"] * orders_products["Price"]

# Aggregate total spent per CustomerID
total_spent_per_customer = orders_products.groupby("CustomerID")["LineTotal"].sum()

# Find the CustomerID with the maximum total spent
max_customer_id = total_spent_per_customer.idxmax()
max_total_spent = total_spent_per_customer.loc[max_customer_id]

# Get customer details
customer = customers[customers["CustomerID"] == max_customer_id].iloc[0]

# Prepare output dictionary
output = {
    "FirstName": customer["FirstName"],
    "LastName": customer["LastName"],
    "City": customer["City"],
    "TotalSpent": round(max_total_spent, 2)
}

# Print JSON output
print(json.dumps(output))