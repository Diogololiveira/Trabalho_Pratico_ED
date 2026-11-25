from datetime import datetime
import json


def parse_data(texto):
    """ pymongo não aceita datetime.date, por isso essa conversão """

    if texto is None or not str(texto).strip():
        return None
    
    return datetime.strptime(str(texto).strip().replace("/", "-"), "%Y-%m-%d")


def legivel(valor):
    if isinstance(valor, datetime):
        if valor.hour == 0 and valor.minute == 0 and valor.second == 0 and valor.microsecond == 0:
            return valor.strftime("%Y-%m-%d")
        return valor.isoformat()
    if isinstance(valor, dict):
        return {k: legivel(v) for k, v in valor.items()}
    if isinstance(valor, list):
        return [legivel(v) for v in valor]
    return valor


def mostrar(rotulo, doc):
    print(f"\n[{rotulo}]")
    
    if doc is None or doc == []:
        print("(nenhum documento)")
    else:
        print(json.dumps(legivel(doc), indent=2, ensure_ascii=False, default=str))