import json,os

from numba.misc.appdirs import system

with open("system.txt", "r", encoding="utf-8")as f: #opens config file and loads into memory
    sys= f.read()

def load(file):
    try:
        if os.path.getsize(file) == 0:
            return []  # empty file = empty memory
        else:
            with open(file, "r", encoding="utf-8")as m:
                memory= json.load(m)
                SYSTEM_PROMPT = {
                    "role": "system",
                    "content": sys
                }

                memory.insert(0, SYSTEM_PROMPT)
                return memory
    except Exception as e:
        print(f"something went wrong loading the memory. error code ({e})")
        return "error", "memory_load"


def save(file, role, content,max):
    try:
        if os.path.getsize(file) == 0:
            memory = []
        else:
            with open(file, "r", encoding="utf-8") as sm:
                memory = json.load(sm)
                system = memory[0]
                rest = memory[1:][-max:]
                memory = [system] + rest
                memory.append({"role":role, "content":content})
                memory = memory[-max:]

        with open(file, "w", encoding="utf-8") as sm:
            json.dump(memory, sm, indent=2)
            print(f"saved {role} message")

    except Exception as e:
        print(f"something went wrong saving to memory. error code ({e})")
        return "error", "memory_save"



