# Week 2 Stretch: Three-tiered customer greetings with counter summary
# Handles VIPs, trial customers, and standdard customers separately
# Prints a tally at the end so we know what was sent

# === Customer lists ===
customers = ["Lisa BlackPink", "Jennie BlackPink", "Jisoo BlackPink", "Rose BlackPink", "Eden BlackPink", "Josie BlackPink", "Lily BlackPink", "Sophie BlackPink", "Mia BlackPink", "Ella BlackPink"]
vip_customers = ["Lisa BlackPink", "Jisoo BlackPink"]
trial_customers = ["Sophie BlackPink", "Mia BlackPink"]
churn_customers = ["Lily BlackPink", "Ella BlackPink"]

# === Counters (start at zero, increase inside the loop) ===
vip_count = 0
trial_count = 0
standard_count = 0
churn_count = 0

# === Print the greetings ===
print ("=== Customer Outreach List ===")
print ("")
for customer in customers:
    if customer in vip_customers:
        print("Hi " + customer + ", thanks for being a valued partner! Got a moment to connect this week?")
        vip_count += 1
    elif customer in trial_customers:
        print("Hello " + customer + ", hope you're enjoying the trial! Any questions I can help answer?")
        trial_count += 1
    elif customer in churn_customers:
        print("Hello " + customer + ", we're sorry to see you go. Is there anything we could have done to keep you as a customer?")
        churn_count += 1
    else:
        print("Hello " + customer + ", checking in — how are things going?")
        standard_count += 1
print ("")
print ("=== End of list ===")
print ("")

# === Summary ===
print ("=== Summary ===")
print ("VIPS contacted: " + str(vip_count))
print ("Trial customers contacted: " + str(trial_count))
print ("Standard customers contacted: " + str(standard_count))
print ("Churned customer contacted: " + str(churn_count))

#Bonus: total check
total_contacted = vip_count + trial_count + standard_count + churn_count
print ("Total customers contacted: " + str(total_contacted))