import os, re, requests, urllib3, hashlib, time
from bs4 import BeautifulSoup

# [v51.2-Stable] - Optimized for GitHub Backup
urllib3.disable_warnings()

c = {
    "red": "\033[38;5;196m",
    "orange": "\033[38;5;208m",
    "gold": "\033[38;5;220m",
    "white": "\033[38;5;255m",
    "reset": "\033[0m"
}

bridge_data = ""

def spider_engine(target, limit, word):
    headers = {'user-agent': 'mozilla/5.0 (linux; android 11)'}
    is_media = any(ext in word.lower() for ext in ['.jpg', '.png', '.jpeg'])
    target = target.replace('"', '').replace("'", "")
    word = word.replace('"', '').replace("'", "")
    
    print(f"{c['gold']}◈ scouting {'media' if is_media else 'targets'}...{c['reset']}")
    
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
                if is_media:
                    for img in s_soup.find_all('img', src=True):
                        src = img['src']
                        if word.replace('*','') in src.lower():
                            if src.startswith('//'): src = 'https:' + src
                            elif src.startswith('/'): src = url.split('.com')[0] + '.com' + src
                            collected.append(src)
                else:
                    text = s_soup.get_text().replace('\n', ' ')
                    relevant = [s.strip() for s in re.split(r'(?<=[.!?]) +', text) if word.lower() in s.lower()]
                    if relevant: collected.append(f"[{url}]: " + " ".join(relevant))
            except: continue
        
        data = "\n".join(list(set(collected)))
        print(f"{c['orange']}  ┃ found {len(list(set(collected)))} items.{c['reset']}")
        return data
    except: return ""

def downloader():
    global bridge_data
    if not bridge_data or "http" not in bridge_data: 
        print(f"{c['red']}## bridge is empty!{c['reset']}")
        return
    
    if not os.path.exists("downloads"): os.makedirs("downloads")
    links = [l for l in bridge_data.split('\n') if l.startswith('http')]
    print(f"{c['gold']}◈ downloading {len(links)} files...{c['reset']}")
    
    count = 0
    for link in links:
        try:
            ext = ".jpg" if ".png" not in link.lower() else ".png"
            name = f"downloads/img_{int(time.time())}_{count}{ext}"
            r = requests.get(link, timeout=10)
            if r.status_code == 200:
                with open(name, 'wb') as f: f.write(r.content)
                count += 1
                print(f"{c['white']}  ┃ progress: {count}/{len(links)}{c['reset']}", end='\r')
        except: continue
    print(f"\n{c['orange']}## session finished. {count} files in /downloads{c['reset']}")

def execute_logic(u_in):
    global bridge_data
    u_in = u_in.strip()
    if not u_in: return

    # فیلتر اختصاصی برای جلوگیری از خطای سینتکس در اندروید
    google_match = re.search(r"google\s*\((.*?)\[(\d+)\]\)\s*::\s*\{(.*?)\}\.do", u_in, re.IGNORECASE)
    
    if google_match:
        bridge_data = spider_engine(google_match.group(1), google_match.group(2), google_match.group(3))
        if "::" in u_in:
            rem = u_in.split(".do", 1)[1].strip()
            if rem.startswith("::"): execute_logic(rem[2:].strip())
        return

    if "::" in u_in:
        for p in u_in.split("::"): execute_logic(p.strip())
        return

    # توابع داخلی
    low_in = u_in.lower()
    if low_in == "download.all": downloader()
    elif low_in == "sha.check":
        h = hashlib.sha256(bridge_data.encode()).hexdigest()
        print(f"{c['gold']}◈ sha256: {h}{c['reset']}")
        bridge_data = f"sha256: {h}\n" + bridge_data
    elif u_in.startswith(".. "):
        with open(u_in[3:].strip(), "w") as f: f.write(bridge_data)
        print(f"{c['orange']}## poured.{c['reset']}")
    elif u_in.startswith("... "):
        p = u_in[4:].split()
        if len(p)>=2: 
            try: os.rename(p[0], p[1]); print(f"{c['orange']}## moved.{c['reset']}")
            except: print(f"{c['red']}## failed.{c['reset']}")
    else:
        if low_in in ["clear", "exit"]: os.system(low_in) if low_in!="exit" else exit()
        else: os.system(u_in)

def main():
    os.system("clear")
    print(f"{c['red']}◈ we.py v51.2-stable ◈{c['reset']}")
    while True:
        try:
            cwd = os.getcwd().split('/')[-1] or "root"
            u_in = input(f"{c['white']}{cwd.lower()} {c['orange']}◈ {c['reset']}")
            execute_logic(u_in)
        except KeyboardInterrupt: break

if __name__ == "__main__": main()
