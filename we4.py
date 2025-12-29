import os, re, requests, urllib3, hashlib, time, sys, json
from bs4 import BeautifulSoup

# [v57.0-stable] - focus: Correct, Complete & Operational Code Generation
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
    last_topic = target
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
    h = hashlib.sha256(content.encode()).hexdigest()
    entry = {"topic": last_topic, "sha256": h, "timestamp": time.ctime(), "data": content}
    db = []
    if os.path.exists(db_path):
        with open(db_path, "r") as f:
            try: db = json.load(f)
            except: db = []
    if not any(item['sha256'] == h for item in db):
        db.append(entry)
        with open(db_path, "w") as f: json.dump(db, f, indent=4)
        print(f"{c['orange']}## knowledge anchored to {db_path}.{c['reset']}")

def bot_logic(query, mode="ask"):
    if not os.path.exists(db_path):
        print(f"{c['red']}## brain not found.{c['reset']}")
        return
    with open(db_path, "r") as f: db = json.load(f)
    results = [item for item in db if query.lower() in item['data'].lower()]
    
    if not results:
        print(f"{c['red']}## no record for '{query}'.{c['reset']}")
        return

    if mode == "ask":
        context = results[0]['data']
        start = context.lower().find(query.lower())
        print(f"{c['gold']}◈ robot analysis:{c['reset']}\n{c['white']}...{context[max(0, start-100):start+500]}...{c['reset']}")
    
    elif mode == "make":
        print(f"{c['orange']}◈ forging professional tool: pro_{query}.py...{c['reset']}")
        script_name = f"pro_{query}.py"
        with open(script_name, "w") as f:
            f.write(f"import os, hashlib, time\n\n# topic: {query}\n# generated for android independence\n\ndef run_tool():\n")
            if "sha" in query.lower() or "hash" in query.lower():
                f.write("    print('[+] sha256 integrity monitor active')\n")
                f.write("    for file in os.listdir('.'):\n        if os.path.isfile(file) and not file.endswith('.py'):\n")
                f.write("            content = open(file, 'rb').read()\n")
                f.write("            h = hashlib.sha256(content).hexdigest()\n")
                f.write("            print(f'   {file} -> {h}')\n")
            else:
                f.write(f"    print('[+] auto-generated logic for {query} based on robot brain')\n")
                f.write("    # logic block extracted from brain\n")
                f.write(f"    context = \"\"\"{results[0]['data'][:300]}...\"\"\"\n")
                f.write("    print(f'   knowledge context: {context}')\n")
            f.write("\nif __name__ == '__main__':\n    run_tool()")
        print(f"{c['gold']}## tool '{script_name}' is correct and ready.{c['reset']}")

def execute_logic(u_in):
    global bridge_data
    u_in = re.sub(r'[^\x20-\x7E]', '', u_in).strip()
    if not u_in: return
    low_in = u_in.lower()
    
    if u_in.startswith("... "):
        p = u_in[4:].split()
        if len(p) >= 2:
            try: os.rename(p[0], p[1]); print(f"{c['orange']}## moved.{c['reset']}")
            except: print(f"{c['red']}## failed.{c['reset']}")
        return
    if u_in.startswith(".. "):
        with open(u_in[3:].strip(), "w") as f: f.write(bridge_data)
        print(f"{c['orange']}## poured.{c['reset']}")
        return
    if u_in.startswith(". "):
        os.system(f"python {u_in[2:].strip()}")
        return
    
    google_match = re.search(r"google\s*\((.*?)\[(\d+)\]\)\s*::\s*\{(.*?)\}\.do", u_in, re.IGNORECASE)
    if google_match:
        bridge_data = spider_engine(google_match.group(1), google_match.group(2), google_match.group(3))
        if "::" in u_in:
            rem = u_in.split(".do", 1)[1].strip()
            if rem.startswith("::"): execute_logic(rem[2:].strip())
        return

    if low_in == "db.add": update_db(bridge_data)
    elif low_in.startswith("bot.ask "): bot_logic(u_in[8:].strip(), "ask")
    elif low_in.startswith("bot.make "): bot_logic(u_in[9:].strip(), "make")
    elif low_in in ["clear", "exit", "ls"]: 
        if low_in == "exit": sys.exit()
        os.system(low_in)
    else: os.system(u_in)

def main():
    os.system("clear")
    print(f"{c['red']}◈ we.py v57.0-stable | the operational architect ◈{c['reset']}")
    while True:
        try:
            cwd = os.getcwd().split('/')[-1] or "root"
            u_in = input(f"{c['white']}{cwd.lower()} {c['orange']}◈ {c['reset']}")
            execute_logic(u_in)
        except KeyboardInterrupt: break

if __name__ == "__main__": main()
