# Week 2: Personalized customer greetings
# Generates a different greeting for VIPs vs regular customers

customers = ["Lisa BlackPink", "Jennie BlackPink", "Jisoo BlackPink", "Rose BlackPink", "Eden BlackPink", "Josie BlackPink", "Lily BlackPink", "Sophie BlackPink", "Mia BlackPink", "Ella BlackPink"]
vip_customers = ["Lisa BlackPink", "Jisoo BlackPink"]

print("=== Customer Outreach List ===")
print("")  # blank line for spacing

for customer in customers:
    if customer in vip_customers:
        print("Hi " + customer + ", thanks for being a valued customer! Got a moment to connect this week?")
    else:
        print("Hello " + customer + ", checking in — how are things going?")

print("")
print("=== End of list ===")