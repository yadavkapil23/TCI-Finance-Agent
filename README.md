# Finance Credit Follow-Up Email Agent
**Open-Source HF LLM (Mistral 7B) - Working Prototype**

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Agent
```bash
python finance_agent.py
```

**First run:** ~3-5 minutes (downloads Mistral 7B model ~14GB)
**Subsequent runs:** ~1-2 minutes for 5 invoices

### 3. Output
- Console output with generated emails
- `audit_log.json` with structured results

---

## 📋 What It Does

**Input:** List of overdue invoices with:
- Invoice ID
- Client name
- Amount due
- Days overdue

**Processing:**
1. Determines escalation stage based on days overdue
2. Generates personalized follow-up email using Mistral 7B
3. Escalates to legal if 30+ days overdue
4. Logs all actions to audit trail

**Output:**
- Personalized emails at 4 escalation levels (Warm → Stern)
- Legal escalation flags
- Complete audit log in JSON format

---

## 🔄 Escalation Stages

| Stage | Days Overdue | Tone | CTA |
|-------|---|---|---|
| 1 | 1-7 | Warm & Friendly | Pay now link |
| 2 | 8-14 | Polite but Firm | Confirm payment date |
| 3 | 15-21 | Formal & Serious | Respond within 48 hrs |
| 4 | 22-30 | Stern & Urgent | Pay immediately or call |
| ⚠️ Legal | 30+ | — | Manual review required |

---

## 📊 Example Run

```bash
$ python finance_agent.py

INV-2024-001 | Rajesh Kumar        | ₹45,000   | 5 days overdue → Stage 1
INV-2024-002 | Priya Sharma        | ₹75,000   | 10 days overdue → Stage 2
INV-2024-003 | Arjun Patel         | ₹1,20,000 | 20 days overdue → Stage 3
INV-2024-004 | Neha Gupta          | ₹55,000   | 28 days overdue → Stage 4
INV-2024-005 | Vikram Singh        | ₹2,10,000 | 45 days overdue → ESCALATED TO LEGAL

Generated Emails: 4
Escalated to Legal: 1
Audit Log: audit_log.json
```

---

## 🔧 Tech Stack

- **LLM:** Mistral 7B Instruct v0.2 (HuggingFace)
- **Framework:** Transformers pipeline (direct, no deployment)
- **Data:** Mock invoice data (pandas-ready format)
- **Logging:** JSON audit trail

---

## 🛡️ Security

✅ **Local Processing:** No cloud API calls
✅ **No API Keys:** Mistral runs locally  
✅ **Data Privacy:** All invoice data stays on your machine
✅ **Structured Output:** Parsed JSON with validation

---

## 📝 Code Structure

```
finance_agent.py
├── get_escalation_stage()     # Deterministic logic
├── generate_follow_up_email() # LLM email generation
├── process_invoices()         # Main agent loop
├── print_results()            # Output formatting
└── mock_invoices              # Sample data
```

---

## ⚠️ Requirements

- **RAM:** 16GB+ (recommended)
- **GPU:** Optional (uses CPU if unavailable, but slower)
- **Storage:** ~15GB for Mistral 7B model cache
- **Python:** 3.8+

---

## 🔮 Next Steps (Week 1 Improvements)

1. **Structured Output:** Add JSON parsing for reliable email format
2. **Email Sending:** Integrate SMTP for dry-run mode
3. **Data Input:** Load invoices from CSV
4. **Dashboard:** Simple Streamlit UI to visualize results
5. **Prompt Tuning:** Refine email tone and personalization

---

**Built with ❤️ using open-source tools**
