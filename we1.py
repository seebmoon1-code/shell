import os, re, requests, urllib3, hashlib, time, sys, json
from bs4 import BeautifulSoup

# [v54.0-stable] - robot brain architect with inference engine
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

def spider_engine(target, limit, word):
    global last_topic
    last_topic = target
    headers = {'user-agent': 'mozilla/5.0 (linux; android 11)'}
    target = target.replace('"', '').replace("'", "")
    
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
        print(f"{c['orange']}  ┃ extracted {len(data.split())} words of knowledge.{c['reset']}")
        return data
    except: return ""

def update_db(content):
    if not content: return
    db_file = "robot_brain.json"
    h = hashlib.sha256(content.encode()).hexdigest()
    
    entry = {
        "topic": last_topic,
        "sha256": h,
        "timestamp": time.ctime(),
        "data": content
    }
    
    db = []
    if os.path.exists(db_file):
        with open(db_file, "r") as f:
            try: db = json.load(f)
            except: db = []
            
    if any(item['sha256'] == h for item in db):
        print(f"{c['red']}## duplicate knowledge (sha match). skipped.{c['reset']}")
    else:
        db.append(entry)
        with open(db_file, "w") as f:
            json.dump(db, f, indent=4)
        print(f"{c['orange']}## knowledge anchored to {db_file}.{c['reset']}")

def bot_ask(query):
    db_file = "robot_brain.json"
    if not os.path.exists(db_file):
        print(f"{c['red']}## robot has no brain yet. use db.add first.{c['reset']}")
        return

    with open(db_file, "r") as f:
        db = json.load(f)
    
    # جستجوی کلمه کلیدی در دیتابیس
    results = [item for item in db if query.lower() in item['data'].lower()]
    
    if results:
        print(f"{c['gold']}◈ robot found {len(results)} records about '{query}':{c['reset']}")
        # نمایش اولین نتیجه یافت شده (خلاصه)
        context = results[0]['data']
        start = context.lower().find(query.lower())
        snippet = context[max(0, start-100):start+400]
        print(f"{c['white']}...{snippet}...{c['reset']}")
    else:
        print(f"{c['red']}## i haven't learned anything about '{query}' yet.{c['reset']}")

def execute_logic(u_in):
    global bridge_data
    u_in = u_in.strip()
    if not u_in: return

    # logic chain: cmd1 :: cmd2
    if "::" in u_in and "google" not in u_in:
        for p in u_in.split("::"): execute_logic(p.strip())
        return

    # google syntax
    google_match = re.search(r"google\s*\((.*?)\[(\d+)\]\)\s*::\s*\{(.*?)\}\.do", u_in, re.IGNORECASE)
    if google_match:
        bridge_data = spider_engine(google_match.group(1), google_match.group(2), google_match.group(3))
        if "::" in u_in:
            rem = u_in.split(".do", 1)[1].strip()
            if rem.startswith("::"): execute_logic(rem[2:].strip())
        return

    low_in = u_in.lower()
    if low_in == "db.add": update_db(bridge_data)
    elif low_in.startswith("bot.ask "): bot_ask(u_in[8:].strip())
    elif low_in == "sha.check":
        print(f"{c['gold']}◈ bridge sha256: {hashlib.sha256(bridge_data.encode()).hexdigest()}{c['reset']}")
    elif u_in.startswith(". "): os.system(f"python {u_in[2:].strip()}")
    elif u_in.startswith(".. "):
        with open(u_in[3:].strip(), "w") as f: f.write(bridge_data)
        print(f"{c['orange']}## poured.{c['reset']}")
    elif u_in.startswith("... "):
        p = u_in[4:].split()
        if len(p) >= 2: os.rename(p[0], p[1]); print(f"{c['orange']}## moved.{c['reset']}")
    else:
        if low_in in ["clear", "exit", "ls"]: 
            if low_in == "exit": sys.exit()
            os.system(low_in)
        else: os.system(u_in)

def main():
    os.system("clear")
    print(f"{c['red']}◈ we.py v54.0-stable | brain system ◈{c['reset']}")
    while True:
        try:
            cwd = os.getcwd().split('/')[-1] or "root"
            u_in = input(f"{c['white']}{cwd.lower()} {c['orange']}◈ {c['reset']}")
            execute_logic(u_in)
        except KeyboardInterrupt: break

if __name__ == "__main__": main()
