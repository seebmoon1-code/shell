import os, sys, subprocess

# [pure fortress v1.0] - absolute stability edition
def get_color(code):
    return f"\033[38;5;{code}m"

c = {"gold": get_color(220), "orange": get_color(208), "red": get_color(196), "reset": "\033[0m"}

def run_forge(name, code=None):
    """smart forge: handles direct code or existing files"""
    target = f"{name}.cpp"
    if code:
        # direct injection without shell interference
        with open(target, "w") as f:
            f.write(code.replace('\\n', '\n'))
    
    if not os.path.exists(target):
        print(f"{c['red']}◈ error: {target} not found.{c['reset']}")
        return

    print(f"{c['orange']}◈ forging {name}...{c['reset']}")
    # -lcrypto added for sha projects, -O3 for max speed
    cmd = ["clang++", "-O3", target, "-lcrypto", "-o", name]
    process = subprocess.run(cmd, capture_output=True, text=True)
    
    if process.returncode == 0:
        print(f"{c['gold']}◈ {name} is ready.{c['reset']}")
        print(f"{c['orange']}--- executing ---{c['reset']}")
        os.system(f"./{name}")
    else:
        print(f"{c['red']}◈ forge failed:\n{process.stderr.lower()}{c['reset']}")

def main():
    os.system("clear")
    print(f"{c['gold']}◈ castle v1.0 | pure architect ◈{c['reset']}")
    
    while True:
        try:
            cwd = os.getcwd().split('/')[-1] or "root"
            cmd_in = input(f"{c['orange']}{cwd.lower()} ◈ {c['reset']}").strip()
            
            if not cmd_in: continue
            if cmd_in == "exit": break
            if cmd_in == "clear": os.system("clear"); continue

            # logic for '.' (go)
            if cmd_in.startswith(". "):
                target = cmd_in[2:].strip()
                if os.path.exists(target):
                    os.system(f"./{target}")
                elif os.path.exists(f"{target}.py"):
                    os.system(f"python {target}.py")
                else:
                    print(f"{c['red']}◈ target not found.{c['reset']}")

            # logic for '..' (forge/pour)
            elif cmd_in.startswith(".. "):
                raw = cmd_in[3:].strip()
                if "|" in raw:
                    name, code = raw.split("|", 1)
                    run_forge(name.strip(), code.strip())
                else:
                    run_forge(raw) # forge existing file

            # default: pass to system shell
            else:
                os.system(cmd_in)

        except KeyboardInterrupt:
            print(f"\n{c['orange']}◈ paused.{c['reset']}")
            break

if __name__ == "__main__":
    main()
