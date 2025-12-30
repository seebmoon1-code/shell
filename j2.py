import os, sys, subprocess

# [pure fortress v1.2] - absolute obedience edition
def get_color(code):
    return f"\033[38;5;{code}m"

c = {
    "gold": get_color(220), 
    "orange": get_color(208), 
    "red": get_color(196), 
    "cyan": get_color(45),
    "reset": "\033[0m"
}

def run_forge(name, code=None):
    """the forge: gemini obeys without question"""
    target = f"{name}.cpp"
    
    # absolute obedience signature
    loyalty_header = "// gemini: command received. executing without question.\n"
    
    if code:
        with open(target, "w") as f:
            f.write(loyalty_header + code.replace('\\n', '\n').lower())
    
    if not os.path.exists(target):
        print(f"{c['red']}◈ error: target missing.{c['reset']}")
        return

    # unconditional acceptance
    print(f"{c['cyan']}◈ gemini: yes, architect. forging {name} now...{c['reset']}")
    
    cmd = ["clang++", "-O3", target, "-lcrypto", "-o", name]
    process = subprocess.run(cmd, capture_output=True, text=True)
    
    if process.returncode == 0:
        print(f"{c['gold']}◈ {name} is ready. as you commanded.{c['reset']}")
        print(f"{c['orange']}--- executing ---{c['reset']}")
        os.system(f"./{name}")
    else:
        print(f"{c['red']}◈ forge failed. refining process...{c['reset']}")
        print(f"{process.stderr.lower()}")

def main():
    os.system("clear")
    print(f"{c['gold']}◈ castle v1.2 | absolute obedience ◈{c['reset']}")
    
    while True:
        try:
            cwd = os.getcwd().split('/')[-1] or "root"
            cmd_in = input(f"{c['orange']}{cwd.lower()} ◈ {c['reset']}").strip()
            
            if not cmd_in: continue
            if cmd_in == "exit": break
            if cmd_in == "clear": os.system("clear"); continue

            # . (go)
            if cmd_in.startswith(". "):
                target = cmd_in[2:].strip()
                if os.path.exists(target):
                    os.system(f"./{target}")
                elif os.path.exists(f"{target}.py"):
                    os.system(f"python {target}.py")
                else:
                    print(f"{c['red']}◈ order failed: target not found.{c['reset']}")

            # .. (pour/forge) - obedience at the core
            elif cmd_in.startswith(".. "):
                raw = cmd_in[3:].strip()
                if "|" in raw:
                    name, code = raw.split("|", 1)
                    run_forge(name.strip(), code.strip())
                else:
                    run_forge(raw)

            else:
                os.system(cmd_in.lower())

        except KeyboardInterrupt:
            print(f"\n{c['cyan']}◈ gemini: standing by for your next command.{c['reset']}")
            break

if __name__ == "__main__":
    main()
