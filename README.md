# 🤖 AI-Powered Customer Support Triage Engine

An automated operations pipeline designed to optimize customer success workflows by ingesting raw, unstructured text communications and outputting highly structured, prioritized routing data.

## 🛠️ System Architecture & Workflow
1. **Data Ingestion:** Reads incoming support requests from a flat ledger (`support_tickets.csv`).
2. **Analysis Layer:** Leverages the `google-genai` SDK and `gemini-2.5-flash` with a strict low-temperature configuration (`0.2`) to evaluate text sentiment and intent.
3. **Structured Storage:** Enforces absolute validation via structured JSON objects and commits the processed, actionable flags to a production-ready database ledger (`resolved_tickets.csv`).

## 📊 Automated Categorization Schema
The engine evaluates and maps every incoming ticket to a rigid matrix:
* **Category Routing:** Classifies text into `Refund`, `Shipping`, `Tech Bug`, or `General Inquiry`.
* **Dynamic Priority Scoring:** Flags urgency dynamically (`Low`, `Medium`, `High`, `Urgent`).
* **Human-Escalation Flares:** Automatically triggers a `true` boolean flag if a customer displays severe dissatisfaction or financial frustration, alerting human account managers instantly.
* **Contextual Response Generation:** Pre-drafts a personalized, professional reply tailored to the customer's specific grievance.

## 🚀 How to Run
1. Ensure your dependencies are installed: `pip install google-genai`
2. Add your Google AI Studio API key to the `MY_API_KEY` variable in `main.py`.
3. Execute the script from your terminal:
   ```bash
   python main.py