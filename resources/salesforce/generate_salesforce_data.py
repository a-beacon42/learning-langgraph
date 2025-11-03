#!/usr/bin/env python3
"""
Script to generate fake Salesforce data based on the schema from data_catalog.json
Generates 100 accounts, 200 opportunities, and 500 contacts with realistic relationships.
"""

import json
import random
from datetime import datetime, timedelta
from faker import Faker
import uuid

# Initialize Faker
fake = Faker()

def generate_account_id():
    """Generate a Salesforce-style Account ID"""
    return f"001{fake.random_number(digits=15, fix_len=True)}"

def generate_opportunity_id():
    """Generate a Salesforce-style Opportunity ID"""
    return f"006{fake.random_number(digits=15, fix_len=True)}"

def generate_contact_id():
    """Generate a Salesforce-style Contact ID"""
    return f"003{fake.random_number(digits=15, fix_len=True)}"

def generate_accounts(num_accounts=100):
    """Generate fake account data"""
    accounts = []
    
    # Industry options for private equity context
    industries = [
        "Technology", "Healthcare", "Financial Services", "Manufacturing", 
        "Consumer Goods", "Energy", "Real Estate", "Telecommunications",
        "Media & Entertainment", "Retail", "Transportation", "Education",
        "Software", "Biotechnology", "Aerospace", "Automotive"
    ]
    
    # Account stages
    stages = ["Prospect", "Portfolio", "Exited"]
    
    # Owner names (relationship managers)
    owners = [
        "John Smith", "Sarah Johnson", "Michael Chen", "Emily Davis",
        "Robert Wilson", "Lisa Anderson", "David Brown", "Jennifer Garcia",
        "Mark Thompson", "Amanda Martinez", "Chris Lee", "Rachel Taylor"
    ]
    
    for i in range(num_accounts):
        account = {
            "AccountId": generate_account_id(),
            "Name": fake.company(),
            "Industry": random.choice(industries),
            "Revenue": round(random.uniform(1000000, 500000000), 2),  # $1M to $500M
            "OwnerName": random.choice(owners),
            "Stage": random.choice(stages)
        }
        accounts.append(account)
    
    return accounts

def generate_opportunities(num_opportunities=200, account_ids=None):
    """Generate fake opportunity data"""
    opportunities = []
    
    if not account_ids:
        account_ids = [generate_account_id() for _ in range(50)]
    
    # Opportunity stages
    stages = [
        "Prospecting", "Qualification", "Due Diligence", "Term Sheet", 
        "Negotiation", "Closed Won", "Closed Lost"
    ]
    
    # Deal types for private equity
    deal_types = [
        "Growth Capital", "Buyout", "Recapitalization", "Add-on Acquisition",
        "Platform Investment", "Secondary Transaction"
    ]
    
    for i in range(num_opportunities):
        stage = random.choice(stages)
        
        # Set probability based on stage
        probability_map = {
            "Prospecting": random.uniform(10, 30),
            "Qualification": random.uniform(25, 45),
            "Due Diligence": random.uniform(40, 60),
            "Term Sheet": random.uniform(60, 80),
            "Negotiation": random.uniform(70, 90),
            "Closed Won": 100,
            "Closed Lost": 0
        }
        
        # Generate close date
        if stage == "Closed Won":
            close_date = fake.date_between(start_date="-2y", end_date="today")
        elif stage == "Closed Lost":
            close_date = fake.date_between(start_date="-1y", end_date="today")
        else:
            close_date = fake.date_between(start_date="today", end_date="+1y")
        
        opportunity = {
            "OpportunityId": generate_opportunity_id(),
            "Name": f"{random.choice(deal_types)} - {fake.company()}",
            "Amount": round(random.uniform(5000000, 200000000), 2),  # $5M to $200M
            "CloseDate": close_date.isoformat(),
            "Stage": stage,
            "Probability": round(probability_map[stage], 1),
            "AccountId": random.choice(account_ids)  # Link to account
        }
        opportunities.append(opportunity)
    
    return opportunities

def generate_contacts(num_contacts=500, account_ids=None):
    """Generate fake contact data"""
    contacts = []
    
    if not account_ids:
        account_ids = [generate_account_id() for _ in range(50)]
    
    # Job titles common in private equity context
    titles = [
        "CEO", "CFO", "COO", "CTO", "President", "Vice President",
        "Managing Director", "General Partner", "Principal", "Director",
        "Senior Vice President", "Chief Investment Officer", "Head of Strategy",
        "Business Development Director", "Investment Director", "Portfolio Manager",
        "Chief Revenue Officer", "Chief Marketing Officer", "Head of Operations",
        "Senior Analyst", "Investment Analyst", "Associate"
    ]
    
    for i in range(num_contacts):
        first_name = fake.first_name()
        last_name = fake.last_name()
        
        contact = {
            "ContactId": generate_contact_id(),
            "FirstName": first_name,
            "LastName": last_name,
            "Email": f"{first_name.lower()}.{last_name.lower()}@{fake.domain_name()}",
            "Title": random.choice(titles),
            "AccountId": random.choice(account_ids)
        }
        contacts.append(contact)
    
    return contacts

def save_to_json(data, filename):
    """Save data to JSON file with proper formatting"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def main():
    """Main function to generate all Salesforce data"""
    print("Generating fake Salesforce data...")
    
    # Generate accounts first (100)
    print("Generating 100 accounts...")
    accounts = generate_accounts(100)
    account_ids = [account["AccountId"] for account in accounts]
    
    # Generate opportunities (200) linked to accounts
    print("Generating 200 opportunities...")
    opportunities = generate_opportunities(200, account_ids)
    
    # Generate contacts (500) linked to accounts
    print("Generating 500 contacts...")
    contacts = generate_contacts(500, account_ids)
    
    # Save to files
    print("Saving data to JSON files...")
    save_to_json(accounts, "resources/salesforce/accounts.json")
    save_to_json(opportunities, "resources/salesforce/opportunities.json")
    save_to_json(contacts, "resources/salesforce/contacts.json")
    
    print("✅ Data generation complete!")
    print(f"Generated:")
    print(f"  - {len(accounts)} accounts")
    print(f"  - {len(opportunities)} opportunities")
    print(f"  - {len(contacts)} contacts")
    print(f"\nFiles saved to:")
    print(f"  - resources/salesforce/accounts.json")
    print(f"  - resources/salesforce/opportunities.json")
    print(f"  - resources/salesforce/contacts.json")

if __name__ == "__main__":
    main()