import os, re, requests, urllib3, hashlib, time, sys, json
from bs4 import BeautifulSoup

# [v58.5-stable] - focus: dynamic c++ arguments & file streaming
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

def bot_logic(query):
    query = query.lower().strip()
    name = query.replace(" ", "_")
    print(f"{c['orange']}◈ forging file-engine: {name}.cpp...{c['reset']}")
    
    # تزریق کد سی‌پلاس‌پلاس با قابلیت پذیرش آرگومان (نام فایل)
    cpp_code = """#include <iostream>
#include <fstream>
#include <chrono>

int main(int argc, char* argv[]) {
    if(argc < 2) {
        std::cout << "[!] error: provide a filename" << std::endl;
        std::cout << "usage: . """ + name + """ <filename>" << std::endl;
        return 1;
    }
    
    std::ifstream file(argv[1], std::ios::binary);
    if(!file) {
        std::cout << "[-] error: file not found: " << argv[1] << std::endl;
        return 1;
    }
    
    char buffer[8192]; // 8KB buffer for maximum speed
    size_t total_bytes = 0;
    
    auto start = std::chrono::high_resolution_clock::now();
    while(file.read(buffer, sizeof(buffer))) { total_bytes += file.gcount(); }
    total_bytes += file.gcount();
    auto end = std::chrono::high_resolution_clock::now();
    
    std::chrono::duration<double> diff = end - start;
    std::cout << "[+] scanned: " << argv[1] << std::endl;
    std::cout << "[+] size: " << total_bytes << " bytes" << std::endl;
    std::cout << "[+] time: " << diff.count() << "s (ahoo speed)" << std::endl;
    
    return 0;
}"""
    
    with open(f"{name}.cpp", "w") as f: f.write(cpp_code)
    res = os.system(f"clang++ -O3 {name}.cpp -o {name}")
    if res == 0:
        print(f"{c['gold']}## binary ./{name} is now a high-speed file engine.{c['reset']}")
    else:
        print(f"{c['red']}## compilation failed. check clang++ installation.{c['reset']}")

def execute_logic(u_in):
    global bridge_data
    # پاکسازی کاراکترهای مخفی و غیرمجاز
    u_in = "".join(i for i in u_in if 31 < ord(i) < 127).strip()
    if not u_in: return
    
    # دستور "." برای اجرا (پشتیبانی از آرگومان)
    if u_in.startswith(". "):
        parts = u_in[2:].split()
        if not parts: return
        target = parts[0]
        args = " ".join(parts[1:])
        if os.path.exists(target):
            os.system(f"python {target} {args}" if target.endswith(".py") else f"./{target} {args}")
        return

    # دستور ".." برای ریختن (Pour)
    if u_in.startswith(".. "):
        target_file = u_in[3:].strip()
        with open(target_file, "w") as f: f.write(bridge_data)
        print(f"{c['gold']}## poured bridge_data into {target_file}.{c['reset']}")
        return

    google_match = re.search(r"google\((.*?)\[(\d+)\]\)::\{(.*?)\}\.do", u_in)
    if google_match:
        bridge_data = spider_engine(google_match.group(1), google_match.group(2), google_match.group(3))
        return

    if u_in.lower() == "db.add": update_db(bridge_data)
    elif u_in.lower().startswith("bot.cpp "): bot_logic(u_in[8:].strip())
    elif u_in.lower() in ["exit", "clear"]: 
        if u_in.lower() == "exit": sys.exit()
        os.system(u_in.lower())
    else: os.system(u_in)

def main():
    os.system("clear")
    print(f"{c['red']}◈ we.py v58.5 | file-stream architect ◈{c['reset']}")
    while True:
        try:
            cwd = os.getcwd().split('/')[-1].lower()
            u_in = input(f"{c['white']}{cwd} {c['orange']}◈ {c['reset']}")
            execute_logic(u_in)
        except KeyboardInterrupt: break
if __name__ == "__main__": main()
