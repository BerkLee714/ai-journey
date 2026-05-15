# Week 4: AI-powered Customer Outreach Tool
# Reads customers from CSV, asks Claude to generate personalized emails for each. 

import csv
import os
from datetime import datetime, date
from dotenv import load_dotenv
from anthropic import Anthropic

USE_AI = True

# === Setup ===
load_dotenv()
client = Anthropic()
MODEL = "claude-sonnet-4-5"

# === Function: days since last contact ===
def days_since_last_contact(last_contact_string):
    last_contact_date = datetime.strptime(last_contact_string, "%Y-%m-%d").date()
    today = date.today()
    return (today - last_contact_date).days

# === Function: build the prompt for a single customer ===
def build_prompt(name, tier, days_since_contact):
    prompt = f"""You are an account manager for a software company. Your job is to write personalized emails to customers based on their tier. 

    Write a brief outreach email to this customer:
    - Customer name: {name}
    - Customer tier: {tier}
    - Days since last contact: {days_since_contact} days

    Guidelines: 
    - Tone: warm but professional
    - Length: 3-4 sentences maximum
    - VIP customers: emphasize valued partnership
    - Trial customers: offer help, ask about their experience
    - Churned customers: acknowledge their departure, ask for feedback on how to improve and win them back
    - Prospect customers: welcome them, offer resources, and encourage them to get started
    - Standard customers: friendly check in, and if they need additional support and we can offer other services to help them grow
    - If days_since_contact > 30 days, add a gentle nudge to encourage re-engagement, and acknowledge that it's been a while since you last connected.

   Reply with ONLY email body. No subject line, no greetings like "Dear", no signature."""
    return prompt

# === Function: generate a template email without AI (for testing) from Week 3 ===
def generate_template_email(name, tier, days_since_contact):
    if tier == "VIP":
        email = f"Hi {name}, thanks for being a valued partner! It's been {days_since_contact} days since we last connected - got a moment to connect this week?"
    elif tier == "Trial": 
        email = f"Hello {name}, hope you're enjoying the trial! Any questions I can help answer? It's been {days_since_contact} days since we last checked in."
    elif tier == "Churned":
        email = f"Hello {name}, we're sorry to see you go. Is there anything we could have done to keep you as a customer? It's been {days_since_contact} days since we last connected, but we'd love to hear any feedback you have on how we can improve."
    elif tier == "Prospect":
        email = f"Hello {name}, thanks for your interest! Can I share some resources to help you get started? It's been {days_since_contact} days since you expressed interest, and we'd love to help you get started."
    else:
        email = f"Hello {name}, checking in — how are things going? It's been {days_since_contact} days since we last connected, so I just wanted to reach out and see if there's anything you need from us right now."
    return email, 0, 0


# === Function: call Claude with the prompt, return the email text ===
def generate_email(prompt):
    response = client.messages.create(
        model=MODEL,
        max_tokens=300,
        messages=[
            {"role": "user", "content": prompt}
        ]       
    )
    email_text = response.content[0].text
    input_tokens = response.usage.input_tokens
    output_tokens = response.usage.output_tokens
    return email_text, input_tokens, output_tokens

# === Main script ===
print("=== AI-powered Customer Outreach Tool ===")
print("")

# Load customers from CSV
customers = []
with open("customers.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        cleaned_row = {key: value.strip() for key, value in row.items()}
        customers.append(cleaned_row)

print (f"loaded {len(customers)} customers from CSV")
print ("")

# === Track usage totals ===
total_input_tokens = 0
total_output_tokens = 0

# Generate and print emails for each customer
for customer in customers:
    name = customer["name"].strip()
    tier = customer["tier"].strip()
    last_contact_string = customer["last_contact"].strip()
    days_since_contact = days_since_last_contact(last_contact_string)
    
    print(f"--- Email for {name} ({tier}, {days_since_contact} days since last contact) ---")
   
    if USE_AI:
        prompt = build_prompt(name, tier, days_since_contact)
        email, input_tokens, output_tokens = generate_email(prompt)
    else: 
        email, input_tokens, output_tokens = generate_template_email(name, tier, days_since_contact)
      
    print(email)
    print("")

    total_input_tokens += input_tokens
    total_output_tokens += output_tokens

# === Cost summary ===
if USE_AI:
    # print the full cost summary
    print("=== Cost Summary ===")
    print(f"total input tokens: {total_input_tokens}")
    print(f"total output tokens: {total_output_tokens}")  

    # === Approximate cost calculation for Sonnet 4.5 ===
    input_cost = (total_input_tokens / 1_000_000) * 3
    output_cost = (total_output_tokens / 1_000_000) * 15
    total_cost = input_cost + output_cost
    print(f"Approximate total cost: ${total_cost:.4f}")
else: 
    print("=== Summary ===")
    print ("Template mode - no API calls, no cost.")
  

