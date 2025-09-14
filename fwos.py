#!/usr/bin/env python3
"""
Fam Word Operating System Shell (fwos.py)
Author: Fatehali Abbasali Moknojiya
"""

import os, sys, shlex, shutil, subprocess, glob, time, re, tkinter as tk
from tkinter.scrolledtext import ScrolledText
from datetime import datetime
import threading

PROMPT = "fwos> "
_CLEAR_SENTINEL = "__FWOS_CLEAR__"
APP = None  # set to the FWOSApp instance when GUI starts

# ----------------- COMMAND IMPLEMENTATIONS -----------------

def man(args):
    helptext = {
        "pwd":"pwd - print working directory",
        "cd":"cd DIR - change directory",
        "ls":"ls [path] - list files",
        "mkdir":"mkdir DIR - create dir",
        "rmdir":"rmdir DIR - remove empty dir",
        "cp":"cp SRC DST - copy file",
        "mv":"mv SRC DST - move file",
        "rm":"rm FILE - remove file",
        "cat":"cat FILE - show file",
        "more":"more FILE - paged view",
        "chmod":"chmod MODE FILE - change perms",
        "diff":"diff A B - compare files",
        "grep":"grep PATTERN FILES - search text",
        "wc":"wc FILE - count lines/words/chars",
        "ps":"ps - show processes",
        "kill":"kill PID - kill process",
        "nice":"nice +N CMD - run with priority",
        "sleep":"sleep N - wait N seconds",
        "batch":"batch SCRIPT - run in bg",
        "at":"at 'YYYY-MM-DD HH:MM' CMD - run later",
        "touch":"touch FILE - create empty file or update timestamp",
        "vi":"vi FILE - open simple text editor",
        "clear":"clear - clear the screen"
    }
    if not args:
        return "Commands:\n" + "\n".join(
            f"{cmd}\t{desc}" for cmd, desc in helptext.items()
        ) + "\n"
    else:
        return helptext.get(args[0], f"No help for {args[0]}\n")

def pwd(args): return os.getcwd()+"\n"

def cd(args):
    try:
        os.chdir(args[0] if args else os.path.expanduser("~"))
        return ""
    except Exception as e:
        return f"Error: {e}\n"

def ls(args):
    out = []
    for p in (args or ["."]):
        for f in glob.glob(p):
            if os.path.isdir(f):
                out.append("\n".join(os.listdir(f)))
            else:
                out.append(f)
    return ("\n".join(out) + "\n") if out else ""

def mkdir(args):
    try:
        [os.makedirs(d, exist_ok=False) for d in args]
        return ""
    except Exception as e:
        return f"Error: {e}\n"

def rmdir(args):
    try:
        [os.rmdir(d) for d in args]
        return ""
    except Exception as e:
        return f"Error: {e}\n"

def cp(args):
    try:
        shutil.copy2(args[0], args[1])
        return ""
    except Exception as e:
        return f"Error: {e}\n"

def mv(args):
    try:
        shutil.move(args[0], args[1])
        return ""
    except Exception as e:
        return f"Error: {e}\n"

def rm(args):
    try:
        [os.remove(f) for f in args]
        return ""
    except Exception as e:
        return f"Error: {e}\n"

def cat(args):
    out = []
    for f in args:
        try:
            out.append(open(f).read())
        except Exception as e:
            out.append(f"Error reading {f}: {e}\n")
    return "".join(out)

def more(args):
    out = []
    for f in args:
        try:
            with open(f) as fh:
                lines = fh.readlines()
                for i in range(0,len(lines),20):
                    out.append("".join(lines[i:i+20]))
                    if i+20 < len(lines): out.append("--More--\n")
        except Exception as e:
            out.append(f"Error reading {f}: {e}\n")
    return "".join(out)

def chmod(args):
    try:
        os.chmod(args[1], int(args[0],8))
        return ""
    except Exception as e:
        return f"Error: {e}\n"

def diff(args):
    if len(args) != 2:
        return "Usage: diff FILE1 FILE2\n"
    try:
        with open(args[0]) as f1, open(args[1]) as f2:
            l1, l2 = f1.readlines(), f2.readlines()
        out = []
        for i,(a,b) in enumerate(zip(l1,l2),1):
            if a!=b:
                out.append(f"Line {i}:\n- {a}+ {b}")
        if len(l1)>len(l2):
            out.extend(f"Extra in {args[0]}: {x}" for x in l1[len(l2):])
        elif len(l2)>len(l1):
            out.extend(f"Extra in {args[1]}: {x}" for x in l2[len(l1):])
        return "".join(out) if out else "Files are identical\n"
    except Exception as e:
        return f"Error: {e}\n"

def grep(args):
    try:
        pat, *files = args
    except ValueError:
        return "Usage: grep PATTERN FILES\n"
    rgx = re.compile(pat)
    out=[]
    for f in files:
        try:
            for i,l in enumerate(open(f),1):
                if rgx.search(l): out.append(f"{f}:{i}:{l}")
        except Exception as e:
            out.append(f"Error reading {f}: {e}\n")
    return "".join(out)

def wc(args):
    out=[]
    for f in args:
        try:
            data=open(f,"rb").read()
            out.append(f"{data.count(b'\\n')} {len(data.split())} {len(data)} {f}\n")
        except Exception as e:
            out.append(f"Error reading {f}: {e}\n")
    return "".join(out)

def ps(args):
    try:
        if os.name == "nt":  # Windows
            return subprocess.getoutput("tasklist") + "\n"
        else:
            return subprocess.getoutput("ps aux") + "\n"
    except Exception as e:
        return f"Error: {e}\n"

def kill(args):
    try:
        pid = int(args[0])
        if os.name == "nt":
            return subprocess.getoutput(f"taskkill /PID {pid} /F") + "\n"
        else:
            os.kill(pid, 9)
            return f"Killed {pid}\n"
    except Exception as e:
        return f"Error: {e}\n"

def nice(args):
    try:
        if os.name == "nt":
            return "nice is not supported on Windows\n"
        os.nice(int(args[0]))
        subprocess.run(args[1:])
        return ""
    except Exception as e:
        return f"Error: {e}\n"

def sleep_cmd(args):
    try:
        time.sleep(float(args[0]))
        return ""
    except Exception as e:
        return f"Error: {e}\n"

def batch(args):
    try:
        script = args[0]
        if os.name == "nt":
            subprocess.Popen(["cmd", "/c", script])
        else:
            subprocess.Popen(["sh", script])
        return f"Started batch {script}\n"
    except Exception as e:
        return f"Error: {e}\n"

def at(args):
    try:
        t = datetime.fromisoformat(args[0])
        cmd = args[1:]
        def job():
            while datetime.now() < t:
                time.sleep(1)
            subprocess.run(cmd)
        threading.Thread(target=job, daemon=True).start()
        return f"Scheduled {' '.join(cmd)} at {t}\n"
    except Exception as e:
        return f"Error: {e}\n"

def touch(args):
    try:
        for f in args:
            with open(f, "a"): os.utime(f, None)
        return ""
    except Exception as e:
        return f"Error: {e}\n"

# New: GUI editor (vi)
def vi(args):
    if not args:
        return "Usage: vi FILE\n"
    fname = args[0]
    if APP is None:
        return "Error: GUI not initialized\n"

    done = threading.Event()
    result = {}

    def opener():
        try:
            _open_vi_window(fname, done, result)
        except Exception as e:
            result['msg'] = f"Error opening editor: {e}\n"
            done.set()

    APP.after(0, opener)
    done.wait()
    return result.get('msg', '')

def _open_vi_window(fname, done_event, result_container):
    top = tk.Toplevel(APP)
    top.title(f"Edit: {fname}")
    top.geometry("800x600")

    txt = ScrolledText(top)
    txt.pack(fill='both', expand=True)

    try:
        if os.path.exists(fname):
            with open(fname, 'r') as fh:
                content = fh.read()
        else:
            content = ''
    except Exception as e:
        content = f"Error reading {fname}: {e}\n"

    txt.insert('1.0', content)

    btn_frame = tk.Frame(top)
    btn_frame.pack(fill='x')

    def save():
        try:
            with open(fname, 'w') as fh:
                fh.write(txt.get('1.0', 'end-1c'))
            result_container['msg'] = f"Saved {fname}\n"
        except Exception as e:
            result_container['msg'] = f"Error saving {fname}: {e}\n"
        finally:
            try: top.grab_release()
            except Exception: pass
            top.destroy()
            done_event.set()

    def cancel():
        result_container['msg'] = "Quit without saving\n"
        try: top.grab_release()
        except Exception: pass
        top.destroy()
        done_event.set()

    tk.Button(btn_frame, text='Save (Ctrl-S)', command=save).pack(side='left', padx=6, pady=6)
    tk.Button(btn_frame, text='Cancel (Ctrl-Q)', command=cancel).pack(side='left', padx=6, pady=6)

    top.bind('<Control-s>', lambda e: save())
    top.bind('<Control-q>', lambda e: cancel())

    top.transient(APP)
    top.grab_set()
    txt.focus_set()

def clear(args): return _CLEAR_SENTINEL

# ----------------- COMMAND DICTIONARY -----------------
COMMANDS={
    "man":man,"pwd":pwd,"cd":cd,"ls":ls,"mkdir":mkdir,"rmdir":rmdir,
    "cp":cp,"mv":mv,"rm":rm,"cat":cat,"more":more,"chmod":chmod,"diff":diff,
    "grep":grep,"wc":wc,"ps":ps,"kill":kill,"nice":nice,"sleep":sleep_cmd,
    "batch":batch,"at":at,"touch":touch,"vi":vi,"clear":clear
}

# ----------------- EXECUTION -----------------
def fwos_command(cmdline):
    args = shlex.split(cmdline)
    if not args: return ""
    cmd,*rest=args
    if cmd=="exit":
        raise SystemExit
    try:
        return COMMANDS[cmd](rest)
    except KeyError:
        return f"Unknown: {cmd}\n"
    except Exception as e:
        return f"Error: {e}\n"

# ----------------- GUI APP -----------------
class FWOSApp(tk.Tk):
    def __init__(self):
        super().__init__()
        global APP
        APP = self
        self.title("Fam Word OS")
        self.geometry("900x600")
        self.config(bg="black")
        self.show_splash()

    def show_splash(self):
        lbl = tk.Label(self, text="Fam Word", font=("Arial", 48, "bold"), fg="white", bg="black")
        lbl.pack(expand=True)
        self.after(2000, self.show_welcome)

    def show_welcome(self):
        for widget in self.winfo_children():
            widget.destroy()
        lbl = tk.Label(self, text="Welcome to\nFatehali Abbasali Moknojiya\nOperating System",
                       font=("Arial", 28), fg="cyan", bg="black")
        lbl.pack(expand=True)
        self.after(3000, self.show_terminal)

    def show_terminal(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.text = ScrolledText(self, bg="black", fg="white", insertbackground="white")
        self.text.pack(fill="both", expand=True)
        self.text.insert(tk.END, PROMPT)
        self.text.bind("<Return>", self.on_enter)
        self.text.bind("<Control-c>", lambda e: None)

    def on_enter(self, event):
        line = self.text.get("insert linestart", "insert lineend")
        if line.startswith(PROMPT):
            cmdline = line[len(PROMPT):].strip()
        else:
            cmdline = line.strip()

        self.text.insert(tk.END, "\n")
        if not cmdline:
            self.text.insert(tk.END, PROMPT)
            return "break"

        threading.Thread(target=self.run_command, args=(cmdline,)).start()
        return "break"

    def run_command(self, cmdline):
        try:
            output = fwos_command(cmdline)
        except SystemExit:
            self.after(0, self.destroy)
            return
        except Exception as e:
            output = f"Error: {e}\n"

        def finish():
            if output == _CLEAR_SENTINEL:
                self.text.delete("1.0", tk.END)
                self.text.insert(tk.END, PROMPT)
            else:
                if output:
                    self.text.insert(tk.END, output)
                self.text.insert(tk.END, PROMPT)
                self.text.see(tk.END)

        self.text.after(0, finish)

# ----------------- MAIN -----------------
if __name__ == "__main__":
    app = FWOSApp()
    app.mainloop()
