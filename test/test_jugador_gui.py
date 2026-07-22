import pytest
from src.jugador_gui import JugadorTkinter
from src.modelos import Eleccion

def test_jugador_tkinter_elegir_despues_de_seleccionar():
    j = JugadorTkinter("Test")
    j.seleccionar(Eleccion.PAPEL)
    assert j.elegir() == Eleccion.PAPEL
    # Después de elegir se resetea, por lo que la siguiente llamada sin seleccionar lanza error
    with pytest.raises(RuntimeError):
        j.elegir()