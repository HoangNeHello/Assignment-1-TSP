from subprocess import Popen

procs = [
    Popen(["python", "MOEA-10.py"]),
    Popen(["python", "MOEA-20.py"]),
    Popen(["python", "MOEA-50.py"]),
]
for p in procs:
    p.wait()
