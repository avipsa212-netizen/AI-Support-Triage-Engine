import os
import csv
import time
import json
from google import genai
from google.genai import types

# 1. PASTE YOUR API KEY HERE
MY_API_KEY = "YOUR_API_KEY_HERE"

client = genai.Client(api_key=MY_API_KEY)

def analyze_and_save_support(input_csv, output_csv):
    print("🤖 Initializing AI Support Triaging & Storage System...")
    print("-" * 60)
    
    if not os.path.exists(input_csv):
        print(f"❌ Error: Could not find the file at {input_csv}")
        return

    # Open the input file to read tickets, and open the output file to write results
    with open(input_csv, mode='r', encoding='utf-8') as infile, \
         open(output_csv, mode='w', encoding='utf-8', newline='') as outfile:
        
        reader = csv.DictReader(infile)
        
        # Define the structure for our new output spreadsheet
        fieldnames = ['ticket_id', 'customer_email', 'category', 'priority_score', 'escalate_to_human', 'drafted_reply']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader() # Writes the column names at the top

        for row in reader:
            ticket_id = row['ticket_id']
            customer = row['customer_email']
            message = row['raw_message']
            
            print(f"📥 Processing Ticket: {ticket_id} | From: {customer}")
            
            prompt = f"""
            You are an advanced automated customer operations agent. Analyze this incoming ticket:
            "{message}"

            Provide your response strictly in the following JSON format structure:
            {{
                "category": "Must be exactly one of: Refund, Shipping, Tech Bug, General Inquiry",
                "priority_score": "Must be exactly one of: Low, Medium, High, Urgent",
                "sentiment_summary": "A brief description of the customer's emotional state",
                "escalate_to_human": true or false,
                "drafted_reply": "A professional, polite response addressing the customer's issue"
            }}
            """
            
            try:
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        temperature=0.2
                    ),
                )
                
                # Parse the text string from Gemini into a Python dictionary
                data = json.loads(response.text)
                
                # Write the combined data into our new CSV row
                writer.writerow({
                    'ticket_id': ticket_id,
                    'customer_email': customer,
                    'category': data.get('category'),
                    'priority_score': data.get('priority_score'),
                    'escalate_to_human': data.get('escalate_to_human'),
                    'drafted_reply': data.get('drafted_reply')
                })
                print(f"✅ Saved analysis for {ticket_id}")
                
            except Exception as e:
                print(f"⚠️ Error processing {ticket_id}: {e}")
            
            print("-" * 60)
            time.sleep(2)
            
    print(f"\n🎉 Done! All analyzed tickets saved to: {output_csv}")

if __name__ == "__main__":
    # Input source -> Output destination
    analyze_and_save_support("support_tickets.csv", "resolved_tickets.csv")