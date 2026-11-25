
import json, os
BASE = os.path.join(os.path.dirname(__file__), "..", "..")
def _load(name):
    p=os.path.join(BASE, name)
    try:
        with open(p, encoding="utf-8") as f: return json.load(f)
    except: return {}
def _save(name, data):
    p=os.path.join(BASE, name)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p,"w",encoding="utf-8") as f: json.dump(data,f,indent=2,ensure_ascii=False)
def get_config(): return _load("config/config.json")
def save_config(c): _save("config/config.json", c)
def get_db(): return _load("database/jesvex.json")
def save_db(d): _save("database/jesvex.json", d)
def get_niveles(): return _load("config/niveles.json")
def save_niveles(n): _save("config/niveles.json", n)

async def setup(bot):
    # esta era la funcion que faltaba, por eso te daba ERROR
    # no cambia nada de lo que ya tenias, solo deja que discord lo cargue
    print("OK sistemas/db.py")
