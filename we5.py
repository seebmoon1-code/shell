import os, re, requests, urllib3, hashlib, time, sys, json
from bs4 import BeautifulSoup

# [v58.0-stable] - focus: python & c++ integration for android independence
urllib3.disable_warnings()

c = {
    "red": "\033[38;5;196m",
    "orange": "\033[38;5;208m",
    "gold": "\033[38;5;220m",
    "white": "\033[38;5;255m",
    "reset": "\033[0m"
}

bridge_data = ""
last_topic = "general"
db_path = "workshop/robot_brain.json"

if not os.path.exists("workshop"): os.makedirs("workshop")

def spider_engine(target, limit, word):
    global last_topic
    last_topic = target.lower()
    headers = {'user-agent': 'mozilla/5.0 (linux; android 11)'}
    print(f"{c['gold']}◈ scouting {target}...{c['reset']}")
    try:
        res = requests.get(f"https://html.duckduckgo.com/html/?q={target}", headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        links = [l['href'] for l in soup.find_all('a', class_='result__a', href=True)]
        collected = []
        for url in links[:int(limit)]:
            if "uddg=" in url: url = requests.utils.unquote(url.split("uddg=")[1].split("&")[0])
            try:
                s_res = requests.get(url, headers=headers, timeout=5)
                s_soup = BeautifulSoup(s_res.text, 'html.parser')
                text = s_soup.get_text().replace('\n', ' ')
                relevant = [s.strip() for s in re.split(r'(?<=[.!?]) +', text) if word.lower() in s.lower()]
                if relevant: collected.append(" ".join(relevant))
            except: continue
        data = " ".join(list(set(collected)))
        print(f"{c['orange']}  ┃ extracted {len(data.split())} words.{c['reset']}")
        return data
    except: return ""

def update_db(content):
    if not content: return
    h = hashlib.sha256(content.encode()).hexdigest().lower()
    entry = {"topic": last_topic, "sha256": h, "timestamp": time.ctime(), "data": content}
    db = []
    if os.path.exists(db_path):
        with open(db_path, "r", encoding="utf-8") as f:
            try: db = json.load(f)
            except: db = []
    if not any(item['sha256'] == h for item in db):
        db.append(entry)
        with open(db_path, "w", encoding="utf-8") as f:
            json.dump(db, f, indent=4, ensure_ascii=False)
        print(f"{c['orange']}## knowledge anchored to {db_path}.{c['reset']}")

def bot_logic(query, mode="ask"):
    if not os.path.exists(db_path):
        print(f"{c['red']}## brain not found.{c['reset']}")
        return
    with open(db_path, "r", encoding="utf-8") as f: db = json.load(f)
    results = [item for item in db if query.lower() in item['data'].lower() or query.lower() in item['topic'].lower()]
    
    if not results:
        print(f"{c['red']}## no record for '{query}'.{c['reset']}")
        return

    if mode == "ask":
        context = results[0]['data']
        print(f"{c['gold']}◈ robot analysis ({results[0]['topic']}):{c['reset']}\n{c['white']}{context[:600]}...{c['reset']}")
    
    elif mode == "make":
        name = query.lower().replace(" ", "_")
        print(f"{c['orange']}◈ forging python tool: pro_{name}.py...{c['reset']}")
        with open(f"pro_{name}.py", "w") as f:
            f.write(f"# topic: {query}\nimport os, hashlib\n\ndef run():\n    print('[+] python logic active')\n    print(f'   knowledge: {results[0]['data'][:100]}...')\n\nif __name__ == '__main__': run()")
        print(f"{c['gold']}## tool pro_{name}.py ready.{c['reset']}")

    elif mode == "cpp":
        name = query.lower().replace(" ", "_")
        print(f"{c['orange']}◈ forging c++ tool: {name}.cpp...{c['reset']}")
        cpp_file = f"{name}.cpp"
        with open(cpp_file, "w") as f:
            f.write("#include <iostream>\n#include <string>\n\nint main() {\n")
            f.write(f"    std::cout << \"[+] swift c++ tool for {name} active\" << std::endl;\n")
            f.write("    return 0;\n}")
        print(f"{c['gold']}◈ compiling with clang++...{c['reset']}")
        os.system(f"clang++ {cpp_file} -o {name}")
        print(f"{c['orange']}## binary ./{name} is operational.{c['reset']}")

def execute_logic(u_in):
    global bridge_data
    u_in = u_in.strip()
    if not u_in: return
    low_in = u_in.lower()
    
    if u_in.startswith("... "):
        p = u_in[4:].split()
        if len(p) >= 2:
            try: os.rename(p[0], p[1]); print(f"{c['orange']}## moved.{c['reset']}")
            except: print(f"{c['red']}## failed.{c['reset']}")
        return
    if u_in.startswith(".. "):
        with open(u_in[3:].strip().lower(), "w") as f: f.write(bridge_data)
        print(f"{c['orange']}## poured.{c['reset']}")
        return
    if u_in.startswith(". "):
        os.system(f"python {u_in[2:].strip().lower()}")
        return
    
    google_match = re.search(r"google\s*\((.*?)\[(\d+)\]\)\s*::\s*\{(.*?)\}\.do", u_in, re.IGNORECASE)
    if google_match:
        bridge_data = spider_engine(google_match.group(1), google_match.group(2), google_match.group(3))
        return

    if low_in == "db.add": update_db(bridge_data)
    elif low_in.startswith("bot.ask "): bot_logic(u_in[8:].strip(), "ask")
    elif low_in.startswith("bot.make "): bot_logic(u_in[9:].strip(), "make")
    elif low_in.startswith("bot.cpp "): bot_logic(u_in[8:].strip(), "cpp")
    elif low_in in ["clear", "exit", "ls"]: 
        if low_in == "exit": sys.exit()
        os.system(low_in)
    else: os.system(u_in)

def main():
    os.system("clear")
    print(f"{c['red']}◈ we.py v58.0-stable | python & c++ architect ◈{c['reset']}")
    while True:
        try:
            cwd = os.getcwd().split('/')[-1] or "root"
            u_in = input(f"{c['white']}{cwd.lower()} {c['orange']}◈ {c['reset']}")
            execute_logic(u_in)
        except KeyboardInterrupt: break
        except Exception as e: print(f"{c['red']}## error: {e}{c['reset']}")

if __name__ == "__main__": main()
