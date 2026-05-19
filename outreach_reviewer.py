# Week 5: two-call workflow with structured output (draft → review → JSON)
# Building a tool to generate customer response JSON and 2 calls to the API.

import os
import csv
import json
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

# === Function: build the prompt for a single customer from Week 4 ===
def generate_draft_email(name, tier, days_since_contact):
    # Build the prompt
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
    
    # Call Claude
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
 
# === Function: call Claude to review its own draft and return structured JSON ===
def review_email(email_text):
    review_prompt = f"""You are a senior copywriter reviewing customer outreach emails. Your job is to review the draft of an outreach email and provide feedback on how well it follows the guidelines, and then rewrite it to be more effective if needed. 

    Here is the email to review:
    ---
    {email_text}
    --- 

    Evaluate this email and return a JSON object with these exact fields: 
    {{
        "quality_score": <integer from 1-10, where 10 is excellent>,
        "issues": <list of 1-3 short issues, or empty list if none>,
        "suggested_revision": <a rewritten version of the email that addresses the issues and improves the quality>
    }}

    Reply with ONLY valid JSON. No preamble, no markdown code fences, no explanations."""

    # Call Claude
    response = client.messages.create(
        model=MODEL,
        max_tokens=500,
        messages=[
            {"role": "user", "content": review_prompt}
        ]       
    )

    raw_text = response.content[0].text

    # Parse JSON safely - strip markdown fences if Claude added them
    try:
        review_dict = json.loads(raw_text)
    except json.JSONDecodeError:
        # Try cleaning markdown fences and re-parsing
        cleaned = raw_text.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        elif cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        try:
            review_dict = json.loads(cleaned.strip())
        except json.JSONDecodeError:
            print(f"⚠️ Couldn't parse JSON even after cleaning. Raw: {raw_text[:200]}")
            review_dict = {
                "quality_score": 0,
                "issues": ["JSON parse failed"],
                "suggested_revision": "N/A"
        }
    input_tokens = response.usage.input_tokens
    output_tokens = response.usage.output_tokens    
    return review_dict, input_tokens, output_tokens   

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
    
    print(f"--- {name} ({tier}, {days_since_contact} days since last contact) ---")
   
    # Call 1: generate draft
    draft, in1, out1 = generate_draft_email(name, tier, days_since_contact)
    print("DRAFT:")
    print(draft)
    print("")
    
    # Call 2: review draft
    review, in2, out2 = review_email(draft)
    print(f"REVIEW (score: {review['quality_score']}/10):")
    print(f"Issues: {review['issues']}")
    print(f"Suggested revision:")
    print(review['suggested_revision'])
    print("")

    total_input_tokens += in1 + in2
    total_output_tokens += out1 + out2

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
  

