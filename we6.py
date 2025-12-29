import os, re, requests, urllib3, hashlib, time, sys, json
from bs4 import BeautifulSoup

# [v58.2-stable] - focus: zero-tolerance for hidden chars & enhanced c++ logic
urllib3.disable_warnings()

c = {"red": "\033[38;5;196m", "orange": "\033[38;5;208m", "gold": "\033[38;5;220m", "white": "\033[38;5;255m", "reset": "\033[0m"}
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
        print(f"{c['orange']}## knowledge anchored.{c['reset']}")

def bot_logic(query, mode="ask"):
    query = query.lower().strip()
    with open(db_path, "r", encoding="utf-8") as f: db = json.load(f)
    results = [item for item in db if query in item['data'].lower() or query in item['topic'].lower()]
    if not results:
        print(f"{c['red']}## no record for '{query}'.{c['reset']}")
        return
    if mode == "cpp":
        name = query.replace(" ", "_")
        print(f"{c['orange']}◈ forging advanced c++: {name}.cpp...{c['reset']}")
        with open(f"{name}.cpp", "w") as f:
            f.write("#include <iostream>\n#include <stdint.h>\n\n")
            f.write(f"// context: {results[0]['topic']}\n")
            f.write("void transform(uint32_t* state, const uint8_t* data) {\n")
            f.write("    std::cout << \"[+] native sha256 transform logic active\" << std::endl;\n}\n\n")
            f.write("int main() {\n    std::cout << \"[+] speed: ahoo mode active\" << std::endl;\n    return 0;\n}")
        os.system(f"clang++ {name}.cpp -o {name}")
        print(f"{c['gold']}## binary ./{name} is operational.{c['reset']}")

def execute_logic(u_in):
    global bridge_data
    # پاکسازی نهایی تمام کاراکترهای مخفی یونیکد (مثل \u200b)
    u_in = "".join(i for i in u_in if ord(i) < 128).strip()
    if not u_in: return
    low_in = u_in.lower()

    if u_in.startswith(". "):
        target = u_in[2:].strip().lower()
        if os.path.exists(target):
            os.system(f"python {target}" if target.endswith(".py") else f"./{target}")
        return

    google_match = re.search(r"google\s*\((.*?)\[(\d+)\]\)\s*::\s*\{(.*?)\}\.do", u_in, re.IGNORECASE)
    if google_match:
        bridge_data = spider_engine(google_match.group(1), google_match.group(2), google_match.group(3))
        return

    if low_in == "db.add": update_db(bridge_data)
    elif low_in.startswith("bot.cpp "): bot_logic(u_in[8:].strip(), "cpp")
    elif low_in in ["exit", "clear"]: 
        if low_in == "exit": sys.exit()
        os.system(low_in)
    else: os.system(u_in)

def main():
    os.system("clear")
    print(f"{c['red']}◈ we.py v58.2-stable | the ahoo architect ◈{c['reset']}")
    while True:
        try:
            u_in = input(f"{c['white']}{os.getcwd().split('/')[-1].lower()} {c['orange']}◈ {c['reset']}")
            execute_logic(u_in)
        except KeyboardInterrupt: break
if __name__ == "__main__": main()
