import os, re, requests, urllib3, hashlib, time, sys, json

# [v60.0-stable] - anti-shell-error edition
urllib3.disable_warnings()

# castle standard colors
c = {
    "red": "\033[38;5;196m", 
    "orange": "\033[38;5;208m", 
    "gold": "\033[38;5;220m", 
    "white": "\033[38;5;255m", 
    "reset": "\033[0m"
}

def forge_and_test(name, code):
    """automated building and testing with robustness"""
    print(f"{c['orange']}◈ forging: {name}.cpp...{c['reset']}")
    cpp_file = f"{name}.cpp"
    
    # fix for newline issues in shell
    formatted_code = code.replace('\\n', '\n')
    
    try:
        with open(cpp_file, "w", encoding="utf-8") as f:
            f.write(formatted_code)
        
        # -lcrypto added for sha/security projects
        # -O3 for maximum aarch64 performance
        res = os.system(f"clang++ -O3 {cpp_file} -lcrypto -o {name} 2>/dev/null")
        
        if res == 0:
            print(f"{c['gold']}## {name} is forged successfully.{c['reset']}")
            print(f"{c['white']}--- automated execution ---{c['reset']}")
            os.system(f"./{name}")
            print(f"{c['white']}---------------------------{c['reset']}")
        else:
            # fallback if libs are missing
            os.system(f"clang++ -O3 {cpp_file} -o {name}")
            print(f"{c['orange']}## forged without extra libs.{c['reset']}")
    except Exception as e:
        print(f"{c['red']}## forge failed: {str(e).lower()}{c['reset']}")

def execute_logic(u_in):
    u_in = u_in.strip()
    if not u_in: return

    # 1. the ".." command (pour/copy/forge)
    if u_in.startswith(".. "):
        cmd = u_in[3:].strip()
        
        if cmd.startswith("edit "):
            target = cmd[5:].strip()
            os.system(f"vim {target}")
            return
            
        if cmd.startswith("forge "):
            if "|" in cmd:
                try:
                    raw = cmd[6:]
                    name, code = raw.split("|", 1)
                    forge_and_test(name.strip(), code.strip())
                except:
                    print(f"{c['red']}usage: .. forge name | code{c['reset']}")
            else:
                # new feature: forge existing file if no code provided
                name = cmd[6:].strip()
                if os.path.exists(f"{name}.cpp"):
                    forge_and_test(name, open(f"{name}.cpp").read())
            return

    # 2. the "." command (go/execute)
    if u_in.startswith(". "):
        target = u_in[2:].strip()
        if os.path.exists(target):
            cmd = f"python {target}" if target.endswith(".py") else f"./{target}"
            os.system(cmd)
        else:
            # try finding without extension
            if os.path.exists(f"./{target}"):
                os.system(f"./{target}")
            else:
                print(f"{c['red']}[!] target not found.{c['reset']}")
        return

    if u_in.lower() in ["exit", "clear"]:
        if u_in.lower() == "exit": sys.exit()
        os.system(u_in.lower())
        return

    os.system(u_in)

def main():
    os.system("clear")
    print(f"{c['red']}◈ we.py v60.0 | autonomous architect ◈{c['reset']}")
    print(f"{c['gold']}status: engine optimized. forge refined.{c['reset']}")
    
    while True:
        try:
            cwd = os.getcwd().split('/')[-1].lower()
            if not cwd: cwd = "root"
            u_in = input(f"{c['white']}{cwd} {c['orange']}◈ {c['reset']}")
            execute_logic(u_in)
        except KeyboardInterrupt:
            print(f"\n{c['orange']}◈ session paused.{c['reset']}")
            break

if __name__ == "__main__":
    main()
