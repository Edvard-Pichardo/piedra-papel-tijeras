# Juego Piedra, Papel o Tijeras

![Nivel](https://img.shields.io/badge/Nivel-Intermedio-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Tests](https://img.shields.io/badge/Tests-18%20passed-success?logo=pytest)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


## Descripción

Estos archivos muestran el clásico juego de “Piedra, Papel o Tijeras”  
Pero, se aplicó principios SOLID, POO, persistencia, manejo de excepciones, tipado estático, logging y pruebas unitarias exhaustivas.

Por lo que se tiene una aplicación de consola que 
**juega contra una IA, guarda el historial en JSON, calcula estadísticas y registra cada evento en logs profesionales**. 

## Tech Stack

- **Lenguaje:** Python 3.10+
- **Librerías estándar:** `enum`, `abc`, `pathlib`, `json`, `logging`, `typing`, `random`, `datetime`
- **Testing:** `pytest` (con `monkeypatch` y fixtures `tmp_path`)
- **Empaquetado:** `pyproject.toml` (PEP 621)
- **Contenedor opcional:** Docker

## Instalación y ejecución

```bash
# Clonar el repositorio (asumiendo que es parte de tu monorepo)
cd piedra-papel-tijeras

# Crear entorno virtual y activarlo
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
.venv\Scripts\activate      # Windows

# Instalar dependencias (solo pytest para desarrollo)
pip install -e ".[dev]"

# Ejecutar el juego
python -m src.main

# Ejecutar pruebas unitarias
pytest -v

Se verá algo como:
tests/test_modelos.py::TestJugadorHumano::test_elegir_valida PASSED
tests/test_juego.py::TestJuego::test_gana_jugador1 PASSED
...
======================= 18 passed in 0.25s =======================
```

## Demostración:

$ python -m src.main

Humano, elige (piedra/papel/tijeras): papel

Resultado: Humano [papel] vs IA [piedra]
¡Ganó Humano!

¿Jugar otra vez? (s/n): s

Humano, elige (piedra/papel/tijeras): tijeras

Resultado: Humano [tijeras] vs IA [papel]
¡Ganó Humano!

¿Jugar otra vez? (s/n): n
¡Gracias por jugar!

📊 Estadísticas de todas las partidas jugadas:
Victorias por jugador:
  - Humano: 2
  - IA: 0
Elección más usada: 'papel' (2 veces)
Porcentaje de empates: 0.00% (0 de 2)
