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

def boss_battle(boss_data):
    wrap_print("=" * 40)
    wrap_print(f"!!! BOSS BATTLE: {boss_data['name']} !!!")
    wrap_print(boss_data["intro"])
    
    health = boss_data["health"]
    for i, phase in enumerate(boss_data["phases"]):
        wrap_print(f"Phase {i+1}: {phase['description']}")
        if ask_mcq(phase["q"], phase["options"], phase["answer_index"]):
            wrap_print(f"You struck a blow! {boss_data['name']} health: {health - 1}")
            health -= 1
        else:
            wrap_print(f"The boss countered! You took damage, but you're still in the fight.")
    
    if health <= 0:
        wrap_print(f"VICTORY! You have defeated {boss_data['name']}.")
        return True
    else:
        wrap_print(f"DEFEAT... {boss_data['name']} stands tall. Study and try again.")
        return False

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

    # Boss Battle
    if level.get("boss"):
        if boss_battle(level["boss"]):
            xp += 50
        else:
            wrap_print("Reyes: 'Rest up. We'll face this threat again when you're ready.'")

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

# --- Content derived from your Watchtower PDF (Security+ Domains 1-4) ---

levels = [
    {
        "code": "1.1",
        "title": "Threats and Malware",
        "story": "Eli enters the perimeter. A swarm of malware variants is clouding the sensors.",
        "field_notes": [
            "Malware: Virus, Worm, Trojan, Ransomware, Spyware, Rootkit, Botnet.",
            "Social Engineering: Phishing, Vishing, Smishing, Tailgating, Impersonation."
        ],
        "boss": {
            "name": "The Shadow Swarm (Malware Collective)",
            "health": 2,
            "intro": "The sensors scream as a polymorphic threat approaches. It's changing shape every second!",
            "phases": [
                {
                    "description": "The swarm attempts to bypass the firewall by masquerading as a harmless system utility.",
                    "q": "What type of malware is a program that appears useful but contains malicious code?",
                    "options": ["Virus", "Worm", "Trojan", "Rootkit"],
                    "answer_index": 2
                },
                {
                    "description": "The swarm has breached! It's now encrypting files and demanding payment.",
                    "q": "What is the primary goal of Ransomware?",
                    "options": ["Stealing passwords", "Gaining remote access", "Extorting money via encryption", "Spreading to other networks"],
                    "answer_index": 2
                }
            ]
        },
        "knowledge_check_mcq": [
            {
                "q": "Which social engineering attack uses voice calls?",
                "options": ["Phishing", "Vishing", "Smishing", "Shoulder Surfing"],
                "answer_index": 1
            }
        ]
    },
    {
        "code": "2.1",
        "title": "Secure Architecture",
        "story": "Eli reaches the Sky Vault. The cloud infrastructure is under siege.",
        "field_notes": [
            "Zero Trust: Never trust, always verify.",
            "Cloud Models: SaaS, PaaS, IaaS.",
            "Defense-in-Depth: Layered security."
        ],
        "boss": {
            "name": "Nexus (The Corrupted Hypervisor)",
            "health": 2,
            "intro": "The very ground of the virtual vault begins to shift. Nexus has taken control of the physical hosts!",
            "phases": [
                {
                    "description": "Nexus is trying to break out of its virtual machine to attack other VMs.",
                    "q": "What is this type of virtualization attack called?",
                    "options": ["VM Sprawl", "VM Escape", "Side-channel attack", "Privilege Escalation"],
                    "answer_index": 1
                },
                {
                    "description": "Nexus is flooding the control plane, trying to disconnect the Sky Vault.",
                    "q": "In which cloud model is the provider responsible for the hypervisor security?",
                    "options": ["SaaS only", "PaaS only", "IaaS and PaaS", "SaaS, PaaS, and IaaS"],
                    "answer_index": 3
                }
            ]
        }
    }
]

def main():
    wrap_print("The Watchtower Training Sim (Security+ Edition)")
    wrap_print("You are Eli, apprentice to Commander Reyes. Clear the Watchtower!")

    total_xp = 0
    for level in levels:
        total_xp += run_level(level)
        cont = input("Continue to the next level? (y/n): ").strip().lower()
        if cont != "y":
            break

    wrap_print(f"Session complete. Total XP: {total_xp}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(\"\
Training aborted.\")
        sys.exit(0)
