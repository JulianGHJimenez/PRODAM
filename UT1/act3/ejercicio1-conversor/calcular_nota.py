from pathlib import Path
import hashlib
import re
import subprocess
import unicodedata
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
REPORTS = ROOT / "target" / "surefire-reports"
TARGET = ROOT / "target"

PESO_CODIGO = 8.0
PESO_DIBUJO = 1.0
PESO_COLOCACION = 1.0

HASH_RESPUESTAS = {'A': 'e980e67bc2f06641f23e62a14329c883c6e31203df3cf26a4c364df2e5d9d081', 'B': '7393ee5acb010aa7a8a05683c98fcaa0b57d6d5008029abacea3fadfe18cb55e', 'C': '796e0b15b4217aae21fccba864f5e4301b886669be9e3c908bc6bbdeab232d17', 'D': '0cba7a87ff53669cf8c7808d5ae760bd519edf4ae51a241a19a2f398becadd6d', 'E': '37aaee4ff55365357ba1a540d9d740ff4cf882634623e9889c8a4a7b4181f8bd', 'F': 'a383bcb77c832a8ff52caace0f4efa8f1639b56b3ad5e32df3c35e8e2ca88f92'}

def normalizar(texto: str) -> str:
    texto = unicodedata.normalize("NFD", texto.lower().strip())
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    return re.sub(r"\s+", " ", texto)

def ejecutar_tests():
    try:
        subprocess.run(
            ["mvn", "-q", "test"],
            cwd=ROOT,
            check=False
        )
        return None
    except FileNotFoundError:
        return "No se ha encontrado Maven (mvn) en el sistema"

def leer_tests():
    total = passed = failed = 0
    for report in REPORTS.glob("TEST-*.xml"):
        try:
            suite = ET.parse(report).getroot()
        except ET.ParseError:
            continue

        tests = int(suite.attrib.get("tests", 0))
        fallos = (
            int(suite.attrib.get("failures", 0))
            + int(suite.attrib.get("errors", 0))
            + int(suite.attrib.get("skipped", 0))
        )
        total += tests
        failed += fallos
        passed += max(0, tests - fallos)

    nota = 0.0 if total == 0 else passed / total * PESO_CODIGO
    return round(nota, 2), total, passed, failed

def puntuacion_dibujo():
    archivo = ROOT / "diagrama.mmd"
    if not archivo.exists():
        return 0.0, ["No existe diagrama.mmd"]

    texto = archivo.read_text(encoding="utf-8")
    t = normalizar(texto)
    puntos = 0.0
    obs = []

    # 0,20: declaración del diagrama
    if re.search(r"\bflowchart\b|\bgraph\b", t):
        puntos += 0.20
    else:
        obs.append("Falta la declaración flowchart/graph")

    # 0,20: inicio y fin con forma de terminador Mermaid ([...])
    tiene_inicio = bool(re.search(r"\(\[\s*inicio\s*\]\)", t))
    tiene_fin = bool(re.search(r"\(\[\s*fin\s*\]\)", t))
    if tiene_inicio and tiene_fin:
        puntos += 0.20
    else:
        obs.append("INICIO y FIN deben estar representados como terminadores")

    # 0,20: entradas/salidas
    entradas = ["mostrar menu", "leer opcion", "leer valor", "mostrar resultado"]
    if all(x in t for x in entradas):
        puntos += 0.20
    else:
        obs.append("Faltan elementos de entrada/salida")

    # 0,20: cuatro decisiones
    decisiones = [f"opcion = {i}" for i in range(1, 5)]
    if all(x in t for x in decisiones) and t.count("{") >= 4:
        puntos += 0.20
    else:
        obs.append("Faltan las cuatro decisiones o no usan forma de decisión")

    # 0,20: cuatro funciones y conexiones
    funciones = [
        "kmametros",
        "metrosacentimetros",
        "horasaminutos",
        "celsiusafahrenheit",
    ]
    if all(x in t for x in funciones) and texto.count("-->") >= 8:
        puntos += 0.20
    else:
        obs.append("Faltan funciones o conexiones suficientes")

    return round(min(PESO_DIBUJO, puntos), 2), obs

def leer_properties():
    archivo = ROOT / "ejercicio01.properties"
    if not archivo.exists():
        return {}

    datos = {}
    for linea in archivo.read_text(encoding="utf-8").splitlines():
        linea = linea.strip()
        if not linea or linea.startswith("#") or "=" not in linea:
            continue
        clave, valor = linea.split("=", 1)
        datos[clave.strip().upper()] = valor.strip()
    return datos

def puntuacion_colocacion():
    respuestas = leer_properties()
    aciertos = 0
    detalle = []

    for letra, hash_esperado in HASH_RESPUESTAS.items():
        valor = respuestas.get(letra, "")
        hash_obtenido = hashlib.sha256(normalizar(valor).encode()).hexdigest()

        if hash_obtenido == hash_esperado:
            aciertos += 1
            detalle.append(f"{letra}: correcta")
        else:
            detalle.append(f"{letra}: incorrecta")

    nota = (aciertos / len(HASH_RESPUESTAS)) * PESO_COLOCACION
    return round(nota, 2), aciertos, detalle

def main():
    TARGET.mkdir(parents=True, exist_ok=True)
    error_maven = ejecutar_tests()

    nota_codigo, total_tests, passed, failed = leer_tests()
    nota_dibujo, obs_dibujo = puntuacion_dibujo()
    nota_colocacion, aciertos, detalle = puntuacion_colocacion()

    nota_final = nota_codigo + nota_dibujo + nota_colocacion

    lineas = [
        "=== AUTOCORRECCIÓN EJERCICIO 1 ===",
        "",
        "=== CÓDIGO ===",
        *( [f"- {error_maven}"] if error_maven else [] ),
        f"Tests superados: {passed}/{total_tests}",
        f"Tests no superados: {failed}",
        f"Puntuación código: {nota_codigo:.2f}/{PESO_CODIGO:.2f}",
        "",
        "=== DIAGRAMA: DIBUJO ===",
        f"Puntuación dibujo: {nota_dibujo:.2f}/{PESO_DIBUJO:.2f}",
    ]

    for obs in obs_dibujo:
        lineas.append(f"- {obs}")

    lineas += [
        "",
        "=== DIAGRAMA: COLOCACIÓN ===",
        f"Respuestas correctas: {aciertos}/{len(HASH_RESPUESTAS)}",
        f"Puntuación colocación: {nota_colocacion:.2f}/{PESO_COLOCACION:.2f}",
    ]
    lineas.extend(f"- {x}" for x in detalle)

    lineas += [
        "",
        "=== RESUMEN ===",
        f"Código:      {nota_codigo:.2f}/{PESO_CODIGO:.2f}",
        f"Dibujo:      {nota_dibujo:.2f}/{PESO_DIBUJO:.2f}",
        f"Colocación:  {nota_colocacion:.2f}/{PESO_COLOCACION:.2f}",
        f"NOTA FINAL:  {nota_final:.2f}/10.00",
        "",
    ]

    informe = "\n".join(lineas)
    (TARGET / "nota.txt").write_text(informe, encoding="utf-8")
    print(informe)

if __name__ == "__main__":
    main()
