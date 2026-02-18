# watchtower_training_sim.py

import textwrap
import random
import sys

WRAP = 80

def wrap_print(text):
    print(textwrap.fill(text, WRAP))
    print()

def ask_mcq(question, options, answer_index):
    wrap_print(question)
    for i, opt in enumerate(options, 1):
        print(f"{i}. {opt}")
    print()
    choice = input("Your choice (1-{}): ".format(len(options))).strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(options)):
        wrap_print("Commander Reyes: 'Focus, recruit. That wasn't a valid option.'")
        return False
    correct = (int(choice) - 1) == answer_index
    if correct:
        wrap_print("Reyes nods. 'Correct.'")
    else:
        wrap_print("Reyes: 'Not quite. Study the field notes again.'")
    return correct

def ask_freeform(prompt, model_answer=None):
    wrap_print(prompt)
    input("(Type your answer, then press Enter)
> ")
    if model_answer:
        wrap_print("Model answer for comparison:")
        wrap_print(model_answer)

def flashcard(card):
    q = card["q"]
    a = card["a"]
    wrap_print("Flashcard: " + q)
    input("> ")
    wrap_print("Answer: " + a)

def run_level(level):
    wrap_print("=" * 40)
    wrap_print(f"Entering {level['code']}: {level['title']}")
    wrap_print(level["story"])

    # Field Notes
    wrap_print("FIELD NOTES (skim or read carefully):")
    for line in level["field_notes"]:
        wrap_print("- " + line)
    input("Press Enter to continue to Knowledge Check...")

    xp = 0

    # Knowledge Check (MCQs or short tasks)
    wrap_print("KNOWLEDGE CHECK")
    for item in level.get("knowledge_check_mcq", []):
        if ask_mcq(item["q"], item["options"], item["answer_index"]):
            xp += item.get("xp", 10)

    for item in level.get("knowledge_check_freeform", []):
        ask_freeform(item["q"], item.get("model_answer"))
        xp += item.get("xp", 5)

    # Hard Mode Drill
    if level.get("hard_mode"):
        wrap_print("HARD MODE DRILL")
        ask_freeform(level["hard_mode"]["prompt"],
                     level["hard_mode"].get("model_answer"))

    # Flashcards
    if level.get("flashcards"):
        wrap_print("FLASHCARDS")
        random.shuffle(level["flashcards"])
        for card in level["flashcards"]:
            flashcard(card)

    wrap_print(f"Level complete. XP gained: {xp}")
    return xp

# --- Content derived from your Watchtower PDF (Security+ only) ---

levels = [
    {
        "code": "1.1",
        "title": "Threats, Attacks, and Vulnerabilities",
        "story": (
            "In the perimeter gallery of the Watchtower, Eli watches echoes ripple "
            "across sensors: quiet scans, crafted emails, strange binaries. "
            "Reyes stands beside him. 'Every echo is a story,' he says. "
            "'Learn to tell threat from weakness from weapon.'"
        ),
        "field_notes": [
            "Threat: potential cause of an unwanted impact (an actor or event).",
            "Vulnerability: a weakness that could be exploited.",
            "Exploit: a method or code that takes advantage of a vulnerability.",
            "Risk: the combination of likelihood and impact of a threat exploiting a vulnerability.",
            "Attack surface: all the points where an attacker can try to enter or get data.",
            "Indicators of compromise (IOCs): forensic clues that an attack has occurred.",
            "Common attacks: phishing (including spear/whaling), password attacks, wireless attacks, "
            "web app attacks, supply chain, insider threats.",
            "Malware families: virus, worm, trojan, ransomware, spyware, rootkit, botnet."
        ],
        "knowledge_check_mcq": [
            {
                "q": (
                    "A developer leaves a web admin panel exposed to the internet with a default "
                    "password. An attacker later discovers it via scanning. Which is the "
                    "vulnerability?"
                ),
                "options": [
                    "The attacker scanning the internet",
                    "The exposed admin panel with a default password",
                    "The exploit code the attacker runs",
                    "The business impact of data loss"
                ],
                "answer_index": 1
            },
            {
                "q": (
                    "An employee receives a targeted email that looks like it is from their CEO, "
                    "asking them to urgently pay an invoice to a new account. Which attack type "
                    "best fits?"
                ),
                "options": [
                    "Generic phishing",
                    "Spear phishing",
                    "Whaling",
                    "Insider threat"
                ],
                "answer_index": 2  # whaling (CEO-level target)
            }
        ],
        "knowledge_check_freeform": [
            {
                "q": "In 1–2 sentences, explain the difference between a threat and a vulnerability.",
                "model_answer": (
                    "A threat is a potential cause of harm, such as an attacker or natural disaster. "
                    "A vulnerability is a weakness in a system or process that a threat could exploit."
                )
            },
            {
                "q": (
                    "Scenario: A ransomware group targets a hospital. Describe how the attack "
                    "might flow from reconnaissance to exfiltration using the stages from the book."
                ),
                "model_answer": (
                    "Recon: scan hospital external IPs and staff emails. "
                    "Initial access: phishing email with malicious attachment. "
                    "Privilege escalation: exploit an unpatched server to gain admin rights. "
                    "Lateral movement: spread through file shares and endpoints. "
                    "Exfiltration: steal sensitive data and then encrypt systems."
                )
            }
        ],
        "hard_mode": {
            "prompt": (
                "Teach this chapter to an imaginary new recruit in 90 seconds. "
                "Explain threat, vulnerability, exploit, and give one concrete example tying them together."
            ),
            "model_answer": (
                "Example: A criminal group (threat) targets remote desktop services. "
                "The service is exposed with weak passwords (vulnerability). "
                "They use credential stuffing tools (exploit) to log in, deploy ransomware, and demand payment."
            )
        },
        "flashcards": [
            {
                "q": "Define 'threat' in security.",
                "a": "A potential cause of an unwanted incident, such as an attacker, event, or condition."
            },
            {
                "q": "Define 'vulnerability' in security.",
                "a": "A weakness in a system, process, or control that could be exploited by a threat."
            },
            {
                "q": "Name three common phishing variants.",
                "a": "Generic phishing, spear phishing, and whaling."
            },
            {
                "q": "What is an indicator of compromise (IOC)?",
                "a": "A forensic artifact or clue that suggests a system has been attacked or breached."
            }
        ]
    },
    {
        "code": "1.2",
        "title": "Security Controls and Control Types",
        "story": (
            "Sirens blare as a breach drill begins. On the wall, controls light up in layers: "
            "policies, firewalls, badges, cameras. Eli must choose quickly what to adjust. "
            "Reyes: 'Every control has a job. Know which one you’re turning.'"
        ),
        "field_notes": [
            "Control categories: administrative (policies, procedures, training), "
            "technical (firewalls, encryption, authentication systems), "
            "physical (locks, guards, fences, cameras).",
            "Control functions: preventive (stop), deterrent (discourage), "
            "detective (find), corrective (fix), compensating (alternative), "
            "recovery (return to normal).",
            "Principles: least privilege, defense-in-depth, separation of duties."
        ],
        "knowledge_check_mcq": [
            {
                "q": "Which of the following is a technical preventive control?",
                "options": [
                    "Security awareness training",
                    "A firewall denying inbound traffic by default",
                    "Security guards at the front door",
                    "Video cameras in the server room"
                ],
                "answer_index": 1
            },
            {
                "q": (
                    "Requiring two different people to approve large wire transfers is an example of:"
                ),
                "options": [
                    "Least privilege",
                    "Separation of duties",
                    "Defense-in-depth",
                    "Recovery control"
                ],
                "answer_index": 1
            }
        ],
        "knowledge_check_freeform": [
            {
                "q": "Describe defense-in-depth in one sentence.",
                "model_answer": (
                    "Defense-in-depth uses multiple overlapping security controls so that if one fails, "
                    "others still provide protection."
                )
            }
        ],
        "hard_mode": {
            "prompt": (
                "Design a simple control stack for a small web app: choose one administrative, "
                "one technical, and one physical control; also label each as preventive, "
                "detective, or other function."
            ),
            "model_answer": (
                "Administrative: Acceptable use and password policy (preventive). "
                "Technical: Web app firewall and MFA for admin login (preventive). "
                "Physical: Locked server closet with access logs (preventive/detective)."
            )
        },
        "flashcards": [
            {
                "q": "Name the three main categories of security controls.",
                "a": "Administrative, technical, and physical."
            },
            {
                "q": "What principle limits users to only the access they need to do their job?",
                "a": "Least privilege."
            },
            {
                "q": "What is a detective control?",
                "a": "A control that identifies that an incident has occurred or is occurring (e.g., IDS, logs)."
            }
        ]
    },
    {
        "code": "1.3",
        "title": "Security Governance Basics",
        "story": (
            "In the Policy Hall, each door bears a different plaque: Policy, Standard, "
            "Procedure, Guideline. Eli reaches for the wrong handle. Reyes catches his wrist. "
            "'Choose the wrong one,' he says, 'and the audit will choose you.'"
        ),
        "field_notes": [
            "Policies: high-level statements of management intent (what and why).",
            "Standards: specific requirements that support policies (what exactly must be done).",
            "Procedures: step-by-step instructions for performing tasks (how to do it).",
            "Guidelines: recommended but optional practices.",
            "Risk concepts: likelihood vs impact; qualitative vs quantitative approaches.",
            "Compliance vs security: compliance meets external requirements, "
            "security aims to actually reduce risk; they overlap but are not identical."
        ],
        "knowledge_check_mcq": [
            {
                "q": "'All customer data must be encrypted at rest and in transit.' This is most likely a:",
                "options": [
                    "Policy",
                    "Standard",
                    "Procedure",
                    "Guideline"
                ],
                "answer_index": 0
            },
            {
                "q": (
                    "Which statement best describes the relationship between compliance and security?"
                ),
                "options": [
                    "If you are compliant, you are automatically secure.",
                    "Security is a subset of compliance.",
                    "Compliance focuses on requirements; security focuses on actual risk reduction.",
                    "They are identical."
                ],
                "answer_index": 2
            }
        ],
        "knowledge_check_freeform": [
            {
                "q": "In 1–2 sentences, explain the difference between a policy and a procedure.",
                "model_answer": (
                    "A policy states management’s high-level intent and rules. "
                    "A procedure provides detailed step-by-step instructions to implement those policies."
                )
            }
        ],
        "hard_mode": {
            "prompt": (
                "Write one sentence of a security policy for admin accounts, and one supporting standard "
                "that is measurable and auditable."
            ),
            "model_answer": (
                "Policy: 'All administrative access to production systems must be strongly controlled and monitored.' "
                "Standard: 'All admin accounts must use MFA and unique IDs, and their privileged sessions must be logged for at least one year.'"
            )
        },
        "flashcards": [
            {
                "q": "Define 'policy' in the context of security governance.",
                "a": "A high-level statement of management intent and direction."
            },
            {
                "q": "Define 'procedure'.",
                "a": "A detailed, step-by-step description of how to carry out a specific task."
            },
            {
                "q": "What two factors define risk in basic terms?",
                "a": "Likelihood and impact."
            }
        ]
    }
]

def main():
    wrap_print("The Watchtower Training Sim (Security+ Edition)")
    wrap_print(
        "You are Eli, apprentice to Commander Reyes. "
        "Clear each wing of the Watchtower by mastering its concepts."
    )

    total_xp = 0
    for level in levels:
        total_xp += run_level(level)
        cont = input("Continue to the next level? (y/n): ").strip().lower()
        if cont != "y":
            break

    wrap_print(f"Session complete. Total XP: {total_xp}")
    wrap_print(
        "Commander Reyes: 'Security is a chain of decisions. "
        "Return tomorrow and we will strengthen more links.'"
    )

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(\"\
Training aborted. See you back at the Watchtower.\")
        sys.exit(0)
