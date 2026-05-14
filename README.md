# Finance Credit Follow-Up Email Agent

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status: MVP](https://img.shields.io/badge/Status-MVP-green.svg)]()

**An AI-powered automation tool that generates professional follow-up emails for overdue invoices with progressive tone escalation.**

> Reduce DSO (Days Sales Outstanding), maintain client relationships, and save 10+ hours per week on manual follow-ups.

---

## 🎯 Overview

This agent automates the Finance team's follow-up process by:

- ✅ **Automatically identifying** overdue invoices
- ✅ **Generating personalized** emails with escalating tone
- ✅ **Logging every action** for compliance and audit
- ✅ **Escalating intelligently** to legal after 30 days
- ✅ **Running locally** with no cloud API costs

---

## 🚀 Quick Start

### Installation

```bash
cd C:\Users\ky805\Downloads\TCIEXPRESS
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Run

```bash
python finance_agent.py
```

---

## 📊 How It Works

### Escalation Stages

| Stage | Days Overdue | Tone | Action |
|-------|---|---|---|
| 1 | 1-7 | Warm & Friendly | Gentle reminder |
| 2 | 8-14 | Polite but Firm | Request confirmation |
| 3 | 15-21 | Formal & Serious | Mention consequences |
| 4 | 22-30 | Stern & Urgent | Final reminder |
| Legal | 30+ | N/A | Flag for legal review |

### Features

✅ **Automatic Escalation** - Deterministic, no bias  
✅ **Personalized Emails** - Client name, amount, due date  
✅ **Complete Audit Trail** - JSON log with timestamps  
✅ **Security** - Local processing, .env configuration  
✅ **Configurable** - Swap LLM models, CPU/GPU selection  

---

## 📁 Project Structure

```
finance_agent.py        ← Main application
requirements.txt        ← Dependencies
.env                   ← Configuration
.env.example          ← Template
README.md             ← This file
ARCHITECTURE.md       ← Technical design
DEMO_SCRIPT.md       ← Demo instructions
PRESENTATION.md      ← Slide deck
audit_log.json       ← Sample output
```

---

## 📊 Sample Output

```json
{
  "generated_emails": 4,
  "escalated_to_legal": 1,
  "audit_log": [
    {
      "invoice_id": "INV-2024-001",
      "stage": 1,
      "timestamp": "2026-05-14T14:19:00",
      "status": "generated",
      "source": "llm"
    }
  ]
}
```

---

## 🔒 Security

✅ Local processing (no cloud transmission)  
✅ .env for credentials  
✅ .gitignore prevents leaks  
✅ Input sanitization  
✅ Complete audit trail  

---

## 📚 Documentation

- [ARCHITECTURE.md](ARCHITECTURE.md) - Technical design
- [DEMO_SCRIPT.md](DEMO_SCRIPT.md) - How to demo
- [PRESENTATION.md](PRESENTATION.md) - 8-10 slides

---

## ✅ Requirements Met

| Feature | Status |
|---------|--------|
| Data Ingestion | ✅ |
| Tone Escalation (4 stages) | ✅ |
| Email Generation (LLM) | ✅ |
| Audit Trail | ✅ |
| Escalation Cap (30+ days) | ✅ |
| Security Documentation | ✅ |
| Technical Stack Documentation | ✅ |

---

**Version:** 1.0 (MVP)  
**Status:** ✅ Production Ready

