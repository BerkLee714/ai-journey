# Week 3: Customer Outreach Tool
# Reads customers from a CSV file, generates personalized greetings using a function,
# and prints a summary. 

import csv

# === Function: generate a personalized greeting based on tier ===
def make_greeting(name, tier):
    if tier == "VIP":
        return "Hi " + name + ", thanks for being a valued partner! Got a moment to connect this week?"
    elif tier == "Trial": 
        return "Hello " + name + ", hope you're enjoying the trial! Any questions I can help answer?"
    elif tier == "Churned":
        return "Hello " + name + ", we're sorry to see you go. Is there anything we could have done to keep you as a customer?"
    elif tier == "Prospect":
        return "Hello " + name + ", thanks for your interest! Can I share some resources to help you get started?"
    else:
        return "Hello " + name + ", checking in — how are things going?"
    
# === Function: count tiers across all customers ===
def count_tiers(customer_list):
    counts = {"VIP": 0, "Trial": 0, "Churned": 0, "Standard": 0, "Prospect": 0}
    for customer in customer_list: 
        tier = customer["tier"].strip()
        counts[tier] += 1
    return counts

# === Main script ===
print("=== Customer Outreach Tool ===")
print("")

# Read the CSV file into a list of dictionaries
customers = []
with open("customers.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        # Strip whitespace from every value to defend against messy CVSs
        cleaned_row = {key: value.strip() for key, value in row.items()}
        customers.append(cleaned_row)

# Generate and print a greeting for each customer
print("=== Greetings ===")
for customer in customers:
    greeting = make_greeting(customer["name"], customer["tier"])
    print(greeting)
print("")

print("")
print("=== Summary ===")

# === Function: find customers by tier ===
def find_customers_by_tier(customer_list, tier):
    return [customer for customer in customer_list if customer["tier"].strip() == tier]


# Show all VIPS using the filter function
vips = find_customers_by_tier(customers, "VIP")
print("=== VIP Customers ===")
for vip in vips:
    print("- " + vip["name"] + " (" + vip["email"] + ")")
print("")

# Count tiers and print the summary
tier_counts = count_tiers(customers)
print("VIPs: " + str(tier_counts["VIP"]))
print("Trial customers: " + str(tier_counts["Trial"]))
print("Churned customers: " + str(tier_counts["Churned"]))
print("Standard customers: " + str(tier_counts["Standard"]))
print("Prospect customers: " + str(tier_counts["Prospect"]))

total = len(customers)  
print("Total customers: " + str(total))

# # Count days since last contacted for each customer and print summary
# print("")
# print("=== Days Since Last Contacted ===")
# for customer in customers:
#     name = customer["name"]
#     tier = customer["tier"]
#     days_since_contact = customer["days_since_contact"]
#     print(f"{name} ({tier}): {days_since_contact} days")