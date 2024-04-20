import os
import datetime
import sys
import subprocess
import psutil

from loguru import logger


def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def RUN():
    if len(sys.argv) < 2:
        print("usage RUN [script_file]")
        return
    script_file = os.path.abspath(sys.argv[1])
    path, name = os.path.split(script_file)
    log_path = os.path.join(path, "log")
    log_file = os.path.join(path, "log", f"{name}.run")
    mkdir(log_path)
    now = datetime.datetime.now()
    if name.endswith(".py"):
        cmd = f"nohup python -Wignore {script_file} &"
    elif name.endswith(".sh"):
        cmd = f"nohup bash {script_file} &"
    else:
        cmd = f"nohup {script_file} &"

    with open(log_file, "a") as f:
        f.write(f"{now} | start run {name}\n")
    subprocess.Popen(
        cmd,
        cwd=path,
        stdout=open(log_file, "a"),
        stderr=open(log_file, "a"),
        shell=True,
    )


def KILL():
    if len(sys.argv) < 2:
        print("usage: KILL [script_file]")
        return
    key = sys.argv[1]
    signal = 9
    for arg in sys.argv[1:]:
        if arg[0] == "-":
            signal = int(arg[1:])
            continue
        key = arg
        break
    for process in psutil.process_iter(["pid", "name", "cmdline"]):
        if process.info["cmdline"] is None:
            continue
        cmdline = " ".join(list(process.info["cmdline"]))
        if key in cmdline:
            pid = process.info["pid"]
            print("kill -{signal} {pid}")
            os.kill(pid, signal)


def TASK():
    if len(sys.argv) < 2:
        print("usage TASK [script_file]")
        return
    bash_file = os.path.expanduser("~/.local/share/mytot/TASK")
    subprocess.run(["bash", bash_file] + sys.argv[1:], check=False)
