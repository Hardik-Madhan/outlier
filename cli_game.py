#!/usr/bin/env python3
"""
ChoreQuest CLI: Play Fast. Clean Real. (Terminal Edition)
Run fast-paced terminal games that execute real chores in the background.
"""

import sys
import time
import random
import json
from pathlib import Path

# ANSI colors
CYAN = "\033[96m"
PINK = "\033[95m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"

MOCK_EMAILS = [
    {"subject": "🔥 80% OFF EVERYTHING - 2 HOURS LEFT!", "sender": "deals@megastore.com", "type": "SPAM"},
    {"subject": "Amit, you have 14 new notifications", "sender": "alerts@socialnet.com", "type": "NOTIFICATION"},
    {"subject": "Weekly Tech & AI Digest #241", "sender": "digest@substack.com", "type": "NEWSLETTER"},
    {"subject": "Quick inquiry about your services", "sender": "coldlead@salesoutreach.biz", "type": "SPAM"},
    {"subject": "Invoice for Cloud Hosting Services ($14.20)", "sender": "billing@aws.amazon.com", "type": "VIP"},
    {"subject": "Dinner reservations confirmation", "sender": "concierge@opentable.com", "type": "VIP"},
]

MOCK_FILES = [
    {"name": "installer_chrome_setup_2024.exe", "size": "85 MB", "cat": "trash"},
    {"name": "Screenshot_2026-10-21_at_14.00.png", "size": "4.2 MB", "cat": "media"},
    {"name": "quarterly_financial_report.pdf", "size": "1.8 MB", "cat": "docs"},
    {"name": "node_modules_backup_temp.zip", "size": "450 MB", "cat": "trash"},
    {"name": "presentation_final_deck.pptx", "size": "22 MB", "cat": "docs"},
]

MOCK_SUBS = [
    {"name": "Forgotten Gym Membership", "cost": 59.99, "desc": "Haven't visited in 7 months"},
    {"name": "Abandoned Cloud Server", "cost": 112.50, "desc": "Running idle in us-west-2"},
    {"name": "4K StreamFlix Family Tier", "cost": 22.99, "desc": "No one watched in 90 days"},
    {"name": "Monthly Domain Auto-Renew", "cost": 15.00, "desc": "Abandoned pet project from 2023"},
]

def clear_screen():
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()

def print_banner():
    clear_screen()
    print(f"""{CYAN}{BOLD}
   ██████╗██╗  ██╗ ██████╗ ██████╗ ███████╗ ██████╗ ██╗   ██╗███████╗███████╗████████╗
  ██╔════╝██║  ██║██╔═══██╗██╔══██╗██╔════╝██╔═══██╗██║   ██║██╔════╝██╔════╝╚══██╔══╝
  ██║     ███████║██║   ██║██████╔╝█████╗  ██║   ██║██║   ██║█████╗  ███████╗   ██║   
  ██║     ██╔══██║██║   ██║██╔══██╗██╔══╝  ██║▄▄ ██║██║   ██║██╔══╝  ╚════██║   ██║   
  ╚██████╗██║  ██║╚██████╔╝██║  ██║███████╗╚██████╔╝╚██████╔╝███████╗███████║   ██║   
   ╚═════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝ ╚══▀▀═╝  ╚═════╝ ╚══════╝╚══════╝   ╚═╝   
{RESET}{YELLOW}                  ★ PLAY FAST. CLEAN REAL. (TERMINAL ARCADE) ★{RESET}
""")

def play_inbox_blitz():
    print_banner()
    print(f"{BOLD}{CYAN}═══ GAME 1: CYBER INBOX BLITZ (X-01 INTERCEPTOR) ═══{RESET}")
    print(f"""{CYAN}
         ▲            [ X-01 CYBER INTERCEPTOR ]
       ◄███►          Twin Ionized Afterburners • Dual Plasma Lasers
      ◄█████►         Targeting Unread Cyber-Mail Capsules
     ◄█▲███▲█►
    {RESET}""")
    print("Incoming unread mail capsules are descending through sub-space!")
    print(f"Commands: {BOLD}[D]{RESET} Plasma Blast (Delete), {BOLD}[U]{RESET} EMP Wave (Unsubscribe), {BOLD}[K]{RESET} Tractor Shield (Keep VIP)")
    print("Press Enter to initiate intercept run...")
    input()

    score = 0
    purged = 0
    time_start = time.time()

    for i in range(10):
        email = random.choice(MOCK_EMAILS)
        clear_screen()
        print(f"{YELLOW}Score: {score}  |  Emails Purged: {purged}  |  Time: {int(time.time() - time_start)}s{RESET}\n")
        
        # Stylized Cyber Mail Capsule
        type_badge = f"{RED}[ 💀 PROMO SPAM ]{RESET}" if email['type'] == 'SPAM' else f"{PINK}[ ⚡ NEWSLETTER ]{RESET}" if email['type'] == 'NEWSLETTER' else f"{YELLOW}[ 💎 VIP INVOICE ]{RESET}"
        
        print(f"[{i+1}/10] ╔═════════════════ CYBER-MAIL CAPSULE ═════════════════╗")
        print(f"      ║ STATUS: {type_badge}  SEAL: LOCKED 2.4MB             ║")
        print(f"      ║ {BOLD}Subject:{RESET} {email['subject']:<43}║")
        print(f"      ║ {DIM}Sender:{RESET}  {email['sender']:<43}║")
        print(f"      ╚══════════════════════════════════════════════════════╝\n")

        action = input(f"{BOLD}Interceptor Action [ (D) Blast / (U) EMP Unsub / (K) Tractor Save / (Q) Quit ]: {RESET}").strip().upper()
        if action == 'Q':
            break

        if email['type'] == 'VIP':
            if action == 'K':
                print(f"{GREEN}⭐ Tractor Beam locked! VIP receipt protected and starred! (+250 pts){RESET}")
                score += 250
            else:
                print(f"{RED}⚠️ VIP Receipt deflected! Starred anyway to prevent loss.{RESET}")
        elif email['type'] == 'NEWSLETTER':
            if action == 'U':
                print(f"{PINK}⚡ EMP shockwave fired! Auto-unsubscribed & purged! (+250 pts){RESET}")
                score += 250
                purged += 1
            else:
                print(f"{YELLOW}💥 Archived newsletter! (+100 pts){RESET}")
                score += 100
                purged += 1
        else:
            if action == 'D':
                print(f"{CYAN}💥 Dual Plasma Lasers hit! Promotional noise shredded & deleted! (+120 pts){RESET}")
                score += 120
                purged += 1
            else:
                print(f"Ignored and bypassed.")

        time.sleep(0.4)

    print(f"\n{BOLD}{GREEN}🎉 Round Complete! Final Score: {score} | Total Emails Purged: {purged}{RESET}")
    time_saved = purged * 4.5
    print(f"⏱️ You saved approx {time_saved:.1f} seconds of manual inbox clicking!")
    input("\nPress Enter to return to menu...")

def play_conveyor_sorter():
    print_banner()
    print(f"{BOLD}{PINK}═══ GAME 2: CONVEYOR OF CHAOS (FILE SORTER) ═══{RESET}")
    print("Loose desktop/download files are rolling in!")
    print(f"Keys: {BOLD}[1]{RESET} Trash, {BOLD}[2]{RESET} Documents, {BOLD}[3]{RESET} Media Vault, {BOLD}[4]{RESET} Keep")
    print("Press Enter to begin...")
    input()

    freed_mb = 0
    sorted_files = 0

    for i in range(6):
        f = random.choice(MOCK_FILES)
        clear_screen()
        print(f"{PINK}Sorted: {sorted_files}  |  Storage Reclaimed: {freed_mb:.1f} MB{RESET}\n")
        print(f"[{i+1}/6] 📦 CONVEYOR ITEM:")
        print(f"  {BOLD}File:{RESET} {f['name']}")
        print(f"  {DIM}Size:{RESET} {f['size']}")
        print()

        action = input(f"{BOLD}Chute [ (1) Trash / (2) Docs / (3) Media / (4) Keep ]: {RESET}").strip()
        if action == '1':
            print(f"{RED}🔥 Incinerated junk installer / archive! Freed {f['size']}{RESET}")
            freed_mb += float(f['size'].split()[0])
            sorted_files += 1
        elif action == '2':
            print(f"{CYAN}📑 Moved to Documents archive!{RESET}")
            sorted_files += 1
        elif action == '3':
            print(f"{PINK}🖼️ Vaulted to Media Screenshots!{RESET}")
            sorted_files += 1
        elif action == '4':
            print(f"{GREEN}📌 Pinned to Desktop!{RESET}")
            sorted_files += 1

        time.sleep(0.4)

    print(f"\n{BOLD}{GREEN}✨ Cleanup Finished! Total Disk Space Reclaimed: {freed_mb:.1f} MB!{RESET}")
    input("\nPress Enter to return to menu...")

def play_saas_dungeon():
    print_banner()
    print(f"{BOLD}{YELLOW}═══ GAME 3: ROGUE AUDIT: SAAS DUNGEON ═══{RESET}")
    print("You enter the dungeon of recurring monthly charges...")
    print("Press Enter to engage monsters...")
    input()

    saved_burn = 0
    for sub in MOCK_SUBS:
        clear_screen()
        print(f"{YELLOW}Monthly Burn Rescued: ${saved_burn:.2f}/mo  |  Annual Savings: ${saved_burn*12:.2f}/yr{RESET}\n")
        print(f"⚔️ A WILD VAMPIRE CHARGE APPEARS: {BOLD}{sub['name']}{RESET}")
        print(f"  Cost: {RED}${sub['cost']}/month{RESET}")
        print(f"  Notes: {DIM}{sub['desc']}{RESET}\n")

        print("Actions:")
        print(f"  {BOLD}[1]{RESET} Banish / Cancel Subscription")
        print(f"  {BOLD}[2]{RESET} Approve as Legitimate Business Expense")
        print(f"  {BOLD}[3]{RESET} Dispute / Chargeback")

        act = input(f"\n{BOLD}Choose action: {RESET}").strip()
        if act == '1':
            print(f"{GREEN}⚔️ CRITICAL STRIKE! Cancelled! You save ${sub['cost']}/mo!{RESET}")
            saved_burn += sub['cost']
        elif act == '2':
            print(f"{CYAN}🤝 Approved verified expense for accountant.{RESET}")
        elif act == '3':
            print(f"{YELLOW}⚡ Chargeback dispute filed with bank.{RESET}")

        time.sleep(0.6)

    print(f"\n{BOLD}{GREEN}🏆 Dungeon Cleared! Total Cash Rescued: ${saved_burn:.2f}/mo (${saved_burn*12:.2f}/yr)!{RESET}")
    input("\nPress Enter to return to menu...")

def main():
    while True:
        print_banner()
        print(f"{BOLD}CHOOSE YOUR CHORE ARENA:{RESET}")
        print(f"  {CYAN}[1]{RESET} Cyber Inbox Invaders (Purge 5,000 Unread Emails)")
        print(f"  {PINK}[2]{RESET} Conveyor of Chaos (Sort Messy Downloads Folder)")
        print(f"  {YELLOW}[3]{RESET} Rogue Audit (Slay Forgotten SaaS Charges)")
        print(f"  {GREEN}[4]{RESET} Launch Web Arcade in Browser (Full 60fps Experience)")
        print(f"  {DIM}[Q]{RESET} Quit\n")

        choice = input(f"{BOLD}Select [1-4 or Q]: {RESET}").strip().upper()
        if choice == '1':
            play_inbox_blitz()
        elif choice == '2':
            play_conveyor_sorter()
        elif choice == '3':
            play_saas_dungeon()
        elif choice == '4':
            import webbrowser
            html_path = Path(__file__).parent / "index.html"
            print(f"\nOpening {html_path.resolve()} in default browser...")
            webbrowser.open(html_path.resolve().as_uri())
            time.sleep(1.5)
        elif choice == 'Q':
            print("\nThanks for cleaning with ChoreQuest! Goodbye.")
            break

if __name__ == "__main__":
    main()
