from subprocess import Popen

procs = [
    Popen(["python3", "MOEA-10.py"]),
    Popen(["python3", "MOEA-20.py"]),
    Popen(["python3", "MOEA-50.py"]),
]
for p in procs:
    p.wait()
