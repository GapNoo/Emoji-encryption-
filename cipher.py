import base64
import os
import time
import sys
import re

# استایل‌دهی رنگی (سازگار با ترموکس)
BLUE = '\033[94m'
WHITE = '\033[97m'
CYAN = '\033[96m'
RED = '\033[91m'
BOLD = '\033[1m'
RESET = '\033[0m'

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def get_mapping():
    # نقشه کاراکترهای Base64 به ایموجی‌های خاص
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
    emojis = [
        "🌌","🌊","🔥","🌙","⚡","💎","🚀","🏹","🛡️","🔑","🗝️","🔮","🌀","🔱","🪐","☄️",
        "🛰️","🛸","👮","🔓","🎯","🎭","🎰","🎬","🎤","🎧","🎨","🎪","🎫","🎟️","🎲","🎱",
        "🥇","🥈","🥉","💎","🛡️","⚔️","🏹","📜","🗝️","🔓","🔒","🔐","🔍","🔎","💡","🔦",
        "🔌","💻","🖥️","🖨️","🖱️","🖲️","🕹️","🗂️","📁","📂","📅","📆","📋","📌","📍","📎",
        "📏","🔗"
    ]
    return dict(zip(chars, emojis)), dict(zip(emojis, chars))

def loading_bar():
    print(f"{BLUE}INITIALIZING SYSTEM...", end="")
    for i in range(10):
        time.sleep(0.1)
        sys.stdout.write(f"{WHITE}█")
        sys.stdout.flush()
    print(f"{RESET}\n")

def main():
    clear_screen()
    print(f"{BLUE}{BOLD}╔════════════════════════════════════════════╗")
    print(f"{BLUE}║{WHITE}        EMOJI ENCRYPTION ENGINE v1.0        {BLUE}║")
    print(f"{BLUE}╚════════════════════════════════════════════╝{RESET}")
    
    loading_bar()
    
    # احراز هویت
    password = input(f"{WHITE}🔑 ENTER MASTER KEY: {RESET}")
    if password != "Aa12345678":
        print(f"{RED}❌ ACCESS DENIED! SYSTEM LOCKED.{RESET}")
        return

    print(f"{CYAN}✅ AUTHENTICATION SUCCESSFUL.{RESET}")
    time.sleep(1)

    c_to_e, e_to_c = get_mapping()

    while True:
        print(f"\n{BLUE}--- MAIN MENU ---")
        print(f"{WHITE}[1] ENCRYPT MESSAGE (متن به ایموجی)")
        print(f"{WHITE}[2] DECRYPT MESSAGE (ایموجی به متن)")
        print(f"{WHITE}[3] EXIT SYSTEM")
        
        choice = input(f"\n{CYAN}SELECT OPTION > {RESET}")

        if choice == '1':
            text = input(f"{WHITE}ENTER PLAIN TEXT: {RESET}")
            if text:
                # تبدیل به Base64 و سپس ایموجی
                b64 = base64.b64encode(text.encode('utf-8')).decode()
                encoded = "".join(c_to_e.get(char, char) for char in b64)
                print(f"\n{BLUE}🔒 ENCRYPTED CODE:{RESET}")
                print(f"{WHITE}{encoded}{RESET}")
                print(f"\n{BLUE}(You can copy the emojis above){RESET}")

        elif choice == '2':
            cipher = input(f"{WHITE}PASTE EMOJI CODE: {RESET}")
            if cipher:
                # استخراج ایموجی‌ها (پشتیبانی از کاراکترهای چندبایتی)
                emoji_pattern = re.compile(r'[^\s\w]|_', re.UNICODE)
                emoji_list = emoji_pattern.findall(cipher)
                
                try:
                    b64_decoded = "".join(e_to_c.get(emo, "") for emo in emoji_list)
                    # اگر ایموجی نبود (مثلاً مساوی در انتهای Base64)، خودش را اضافه کن
                    if not b64_decoded and "=" in cipher:
                         b64_decoded = "".join(e_to_c.get(emo, emo) for emo in emoji_list)
                    
                    original = base64.b64decode(b64_decoded).decode('utf-8')
                    print(f"\n{CYAN}🔓 DECRYPTED MESSAGE:{RESET}")
                    print(f"{WHITE}{original}{RESET}")
                except Exception as e:
                    print(f"{RED}❌ ERROR: INVALID EMOJI CODE OR CORRUPTED DATA.{RESET}")

        elif choice == '3':
            print(f"{BLUE}SHUTTING DOWN SYSTEM...{RESET}")
            break
        else:
            print(f"{RED}INVALID SELECTION!{RESET}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{RED}SYSTEM TERMINATED BY USER.{RESET}")
        sys.exit()
