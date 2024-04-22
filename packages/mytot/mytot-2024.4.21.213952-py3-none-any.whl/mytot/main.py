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
    if len(sys.argv) >= 3:
        args = " ".join(sys.argv[2:])
    else:
        args = ""
    script_file = os.path.abspath(sys.argv[1])
    path, name = os.path.split(script_file)
    log_path = os.path.join(path, "log")
    log_file = os.path.join(path, "log", f"{name}.log")
    mkdir(log_path)
    now = datetime.datetime.now()
    if name.endswith(".py"):
        cmd = f"nohup python -Wignore {script_file} {args} &"
    elif name.endswith(".sh"):
        cmd = f"nohup bash {script_file} {args} &"
    else:
        cmd = f"nohup {script_file} {args} &"

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
        if "KILL" in cmdline:
            continue
        if key in cmdline:
            pid = process.info["pid"]
            print(f"kill -{signal} {pid}")
            os.kill(pid, signal)


def today():
    return datetime.datetime.now().strftime("%Y%m%d")


def TASK():
    if len(sys.argv) < 2:
        print("usage TASK [script_file]")
        return
    script_file = os.path.abspath(sys.argv[1])
    # check the pragma
    date = today()
    mkdir(os.path.expanduser("~/.cache/task_log/"))
    task_log = os.path.expanduser(f"~/.cache/task_log/out.{date}")
    for process in psutil.process_iter(["pid", "name", "cmdline"]):
        if process.info["cmdline"] is None:
            continue
        cmdline = " ".join(list(process.info["cmdline"]))
        if script_file in cmdline:
            with open(task_log, "a") as f:
                now = datetime.datetime.now()
                f.write(f"{now} | {script_file} is running\n")
            return
    path, name = os.path.split(script_file)
    log_path = os.path.join(path, "log")
    mkdir(log_path)
    if script_file.endswith(".py"):
        cmd = ["python", "-Wignore", script_file]
    elif script_file.endswith(".sh"):
        cmd = ["bash", script_file]
    else:
        cmd = [script_file]
    if len(sys.argv) >= 3:
        cmd += sys.argv[2:]

    with open(task_log, "a") as f:
        f.write("{} | start run {}\n".format(datetime.datetime.now(), script_file))
        f.write("{} | cmd: {}\n".format(datetime.datetime.now(), " ".join(cmd)))
    log_file = os.path.join(path, "log", f"{name}.log")
    subprocess.run(
        cmd,
        cwd=path,
        stdout=open(log_file, "a"),
        stderr=open(log_file, "a"),
        check=False,
    )
