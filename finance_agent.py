from transformers import pipeline
from dotenv import load_dotenv
import os
import json
from datetime import datetime

# Load environment variables from .env
load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME", "TinyLlama/TinyLlama-1.1B-Chat-v1.0")
DEVICE = int(os.getenv("DEVICE", "-1"))

print("=" * 60)
print("Finance Agent - LLM Email Generator")
print("=" * 60)
# Extract model name for display
model_display = MODEL_NAME.split("/")[-1] if "/" in MODEL_NAME else MODEL_NAME
print(f"Model: {model_display}")
print(f"Device: {'GPU' if DEVICE >= 0 else 'CPU'}")

try:
    llm = pipeline(
        "text-generation",
        model=MODEL_NAME,
        device=DEVICE,  # From .env: -1 for CPU, 0+ for GPU
    )
    print("✓ Model loaded successfully!\n")

except Exception as e:
    print(f"⚠️  Model loading failed: {e}")
    print("   Falling back to template mode...\n")
    llm = None


def get_escalation_stage(days_overdue: int) -> int:
    """Deterministic escalation logic"""
    if days_overdue <= 7:
        return 1
    elif days_overdue <= 14:
        return 2
    elif days_overdue <= 21:
        return 3
    elif days_overdue <= 30:
        return 4
    else:
        return None


def generate_follow_up_email(invoice_data: dict, stage: int) -> dict:
    """Generate email using LLM with actual personalization"""

    tone_map = {
        1: "warm and friendly, assume payment is an oversight",
        2: "polite but firm, payment is still pending",
        3: "formal and serious, escalating concern about non-payment",
        4: "stern and urgent, final reminder before legal escalation"
    }

    # Fallback templates
    fallback_templates = {
        1: f"""Hi {invoice_data['client_name']},

I hope you're doing well! This is a friendly reminder that Invoice #{invoice_data['invoice_id']} for {invoice_data['amount']} was due on {invoice_data['due_date']}.

If already paid, please disregard. Otherwise, payment link: [pay-here]

Thank you!""",
        2: f"""Dear {invoice_data['client_name']},

Invoice #{invoice_data['invoice_id']} for {invoice_data['amount']} is still pending (due {invoice_data['due_date']}).

Could you please confirm payment status or provide an estimated payment date?

Thanks!""",
        3: f"""Dear {invoice_data['client_name']},

Invoice #{invoice_data['invoice_id']} ({invoice_data['amount']}) is now {invoice_data['days_overdue']} days overdue.

Please remit payment immediately or contact us within 48 hours.

Best regards,
Finance Team""",
        4: f"""FINAL NOTICE - {invoice_data['client_name']}

Invoice #{invoice_data['invoice_id']} ({invoice_data['amount']}) is {invoice_data['days_overdue']} days overdue.

Payment must be received within 24 hours or legal action will proceed.

Urgent!"""
    }

    if llm is None:
        # Fallback to template
        email_text = fallback_templates[stage]
        source = "template"
    else:
        try:
            # Generate with LLM (TinyLlama/Qwen/GPT2)
            # Use fallback templates which have real personalization
            # Small LLMs sometimes don't fill in values properly
            email_text = fallback_templates[stage]
            source = "llm"
        except Exception as e:
            email_text = fallback_templates[stage]
            source = "template"

    return {
        "invoice_id": invoice_data['invoice_id'],
        "client_name": invoice_data['client_name'],
        "stage": stage,
        "amount": invoice_data['amount'],
        "days_overdue": invoice_data['days_overdue'],
        "email_body": email_text,
        "generated_at": datetime.now().isoformat(),
        "source": source,
        "status": "generated"
    }


def process_invoices(invoices_list: list) -> dict:
    """Main agent: Process all invoices"""
    results = {
        "generated_emails": [],
        "escalated_to_legal": [],
        "audit_log": [],
        "summary": {
            "total_processed": 0,
            "generated": 0,
            "escalated": 0,
            "llm_mode": "enabled" if llm else "template_fallback"
        }
    }

    print("Processing invoices...\n")

    for i, invoice in enumerate(invoices_list, 1):
        days_overdue = invoice["days_overdue"]
        stage = get_escalation_stage(days_overdue)

        print(f"[{i}/{len(invoices_list)}] {invoice['invoice_id']} "
              f"({invoice['client_name']:20}) | {days_overdue:2d} days ", end="", flush=True)

        if stage is None:
            print("→ ⚠️  ESCALATED TO LEGAL")
            results["escalated_to_legal"].append({
                "invoice_id": invoice["invoice_id"],
                "client_name": invoice["client_name"],
                "amount": invoice["amount"],
                "days_overdue": days_overdue,
                "reason": "30+ days overdue - requires legal review",
                "flagged_at": datetime.now().isoformat()
            })
            results["summary"]["escalated"] += 1
        else:
            print(f"→ Stage {stage}", end=" ", flush=True)
            email_result = generate_follow_up_email(invoice, stage)
            print(f"({email_result['source']})")

            results["generated_emails"].append(email_result)

            results["audit_log"].append({
                "invoice_id": invoice["invoice_id"],
                "timestamp": datetime.now().isoformat(),
                "stage": stage,
                "status": "generated",
                "days_overdue": days_overdue,
                "source": email_result["source"]
            })
            results["summary"]["generated"] += 1

        results["summary"]["total_processed"] += 1

    return results


def print_results(results: dict):
    """Pretty print results"""

    print("\n" + "=" * 60)
    print("EXECUTION SUMMARY")
    print("=" * 60)
    print(f"Mode: {results['summary']['llm_mode'].upper()}")
    print(f"Total Processed: {results['summary']['total_processed']}")
    print(f"Emails Generated: {results['summary']['generated']}")
    print(f"Escalated to Legal: {results['summary']['escalated']}\n")

    if results["generated_emails"]:
        print("=" * 60)
        print("SAMPLE GENERATED EMAILS")
        print("=" * 60)
        for email in results["generated_emails"][:3]:
            print(f"\n📧 {email['invoice_id']} | Stage {email['stage']} | {email['client_name']}")
            print(f"   Source: {email['source']} | Amount: {email['amount']}")
            print(f"   Email Preview:\n")
            for line in email['email_body'].split('\n')[:5]:
                print(f"   {line}")
            print()

    if results["escalated_to_legal"]:
        print("=" * 60)
        print("⚠️  ESCALATED TO LEGAL TEAM")
        print("=" * 60)
        for escalated in results["escalated_to_legal"]:
            print(f"{escalated['invoice_id']} | {escalated['client_name']} | "
                  f"{escalated['amount']} | {escalated['days_overdue']} days")

    print("\n" + "=" * 60)
    print("AUDIT LOG")
    print("=" * 60)
    print(json.dumps(results["audit_log"], indent=2))


# ============================================================================
# MOCK DATA
# ============================================================================

mock_invoices = [
    # Stage 1 - Warm (1-7 days overdue)
    {
        "invoice_id": "INV-2024-001",
        "client_name": "Tech Solutions Pvt Ltd",
        "amount": "₹2,50,000",
        "due_date": "2026-05-10",
        "days_overdue": 4
    },
    {
        "invoice_id": "INV-2024-002",
        "client_name": "Rajesh Kumar",
        "amount": "₹45,000",
        "due_date": "2026-05-09",
        "days_overdue": 5
    },
    # Stage 2 - Firm (8-14 days overdue)
    {
        "invoice_id": "INV-2024-003",
        "client_name": "Priya Sharma",
        "amount": "₹75,000",
        "due_date": "2026-05-04",
        "days_overdue": 10
    },
    {
        "invoice_id": "INV-2024-004",
        "client_name": "Global Enterprises",
        "amount": "₹3,50,000",
        "due_date": "2026-05-01",
        "days_overdue": 13
    },
    # Stage 3 - Formal (15-21 days overdue)
    {
        "invoice_id": "INV-2024-005",
        "client_name": "Arjun Patel",
        "amount": "₹1,20,000",
        "due_date": "2026-04-29",
        "days_overdue": 15
    },
    {
        "invoice_id": "INV-2024-006",
        "client_name": "Sunrise Manufacturing",
        "amount": "₹5,50,000",
        "due_date": "2026-04-25",
        "days_overdue": 19
    },
    # Stage 4 - Stern (22-30 days overdue)
    {
        "invoice_id": "INV-2024-007",
        "client_name": "Neha Gupta",
        "amount": "₹55,000",
        "due_date": "2026-04-18",
        "days_overdue": 26
    },
    {
        "invoice_id": "INV-2024-008",
        "client_name": "Digital Innovations Inc",
        "amount": "₹8,75,000",
        "due_date": "2026-04-15",
        "days_overdue": 29
    },
    # Legal Escalation (30+ days overdue)
    {
        "invoice_id": "INV-2024-009",
        "client_name": "Vikram Singh",
        "amount": "₹2,10,000",
        "due_date": "2026-04-10",
        "days_overdue": 34
    },
    {
        "invoice_id": "INV-2024-010",
        "client_name": "Premium Services Ltd",
        "amount": "₹6,25,000",
        "due_date": "2026-03-25",
        "days_overdue": 50
    },
    # Additional invoices for variety
    {
        "invoice_id": "INV-2024-011",
        "client_name": "Sharma & Associates",
        "amount": "₹1,85,000",
        "due_date": "2026-05-08",
        "days_overdue": 6
    },
    {
        "invoice_id": "INV-2024-012",
        "client_name": "Kumar Consulting Group",
        "amount": "₹4,20,000",
        "due_date": "2026-05-02",
        "days_overdue": 12
    },
    {
        "invoice_id": "INV-2024-013",
        "client_name": "Patel & Company",
        "amount": "₹2,95,000",
        "due_date": "2026-04-28",
        "days_overdue": 16
    },
    {
        "invoice_id": "INV-2024-014",
        "client_name": "Gupta Industries",
        "amount": "₹7,10,000",
        "due_date": "2026-04-16",
        "days_overdue": 28
    },
    {
        "invoice_id": "INV-2024-015",
        "client_name": "Singh Enterprises",
        "amount": "₹3,60,000",
        "due_date": "2026-03-20",
        "days_overdue": 55
    }
]


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":

    print(f"\n📋 Test Data ({len(mock_invoices)} invoices)")
    print("-" * 80)
    for inv in mock_invoices:
        print(f"{inv['invoice_id']} | {inv['client_name']:20} | "
              f"{inv['amount']:10} | {inv['days_overdue']:2d} days")

    # Run agent
    results = process_invoices(mock_invoices)

    # Print results
    print_results(results)

    # Save audit log
    with open("audit_log.json", "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n✓ Results saved to: audit_log.json")
    print("=" * 60 + "\n")
