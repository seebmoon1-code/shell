import os, re, requests, urllib3, hashlib, time, sys, json

# [v59.0-stable] - The Complete Castle Core
urllib3.disable_warnings()

# رنگ‌های استاندارد قلعه
c = {
    "red": "\033[38;5;196m", 
    "orange": "\033[38;5;208m", 
    "gold": "\033[38;5;220m", 
    "white": "\033[38;5;255m", 
    "reset": "\033[0m"
}

def forge_and_test(name, code):
    """ساخت، کامپایل و تست خودکار کدهایی که من (Gemini) می‌دهم"""
    print(f"{c['orange']}◈ forging: {name}.cpp...{c['reset']}")
    cpp_file = f"{name}.cpp"
    formatted_code = code.replace('\\n', '\n')
    
    with open(cpp_file, "w", encoding="utf-8") as f:
        f.write(formatted_code)
    
    # کامپایل با بالاترین سطح بهینه‌سازی برای موبایل
    res = os.system(f"clang++ -O3 {cpp_file} -o {name}")
    
    if res == 0:
        print(f"{c['gold']}## {name} is alive. starting automated test...{c['reset']}")
        print(f"{c['white']}--- OUTPUT ---{c['reset']}")
        os.system(f"./{name}")
        print(f"{c['white']}--------------{c['reset']}")
    else:
        print(f"{c['red']}## forge failed. check blueprint syntax.{c['reset']}")

def execute_logic(u_in):
    u_in = u_in.strip()
    if not u_in: return

    # ۱. دستور ".." برای ریختن/کپی یا عملیات ویژه
    if u_in.startswith(".. "):
        cmd = u_in[3:].strip()
        
        # قابلیت ویرایش سریع با ویم
        if cmd.startswith("edit "):
            target = cmd[5:].strip()
            os.system(f"vim {target}")
            return
            
        # قابلیت فورج خودکار (برای اینکه خسته نشوی)
        if cmd.startswith("forge "):
            try:
                raw = cmd[6:]
                name, code = raw.split("|", 1)
                forge_and_test(name.strip(), code.strip())
            except:
                print(f"{c['red']}usage: .. forge name | code{c['reset']}")
            return

    # ۲. دستور "." برای اجرای سریع (برو)
    if u_in.startswith(". "):
        target = u_in[2:].strip()
        if os.path.exists(target):
            # اگر پایتون بود با پایتون، اگر نبود مستقیم اجرا کن
            cmd = f"python {target}" if target.endswith(".py") else f"./{target}"
            os.system(cmd)
        else:
            print(f"{c['red']}[!] target not found.{c['reset']}")
        return

    # ۳. دستورات خروج و پاکسازی
    if u_in.lower() in ["exit", "clear"]:
        if u_in.lower() == "exit": sys.exit()
        os.system(u_in.lower())
        return

    # ۴. اجرای مستقیم دستورات شل
    os.system(u_in)

def main():
    os.system("clear")
    print(f"{c['red']}◈ we.py v59.0 | autonomous architect ◈{c['reset']}")
    print(f"{c['gold']}status: system stable. bridge active.{c['reset']}")
    
    while True:
        try:
            # نمایش دایرکتوری فعلی برای تسلط بیشتر
            cwd = os.getcwd().split('/')[-1].lower()
            if not cwd: cwd = "root"
            
            u_in = input(f"{c['white']}{cwd} {c['orange']}◈ {c['reset']}")
            execute_logic(u_in)
        except KeyboardInterrupt:
            print(f"\n{c['orange']}◈ session paused. type 'exit' to close.{c['reset']}")
            break

if __name__ == "__main__":
    main()
