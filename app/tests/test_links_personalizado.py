import pytest

from app.controllers.links import *

def test_linkComNumero():
    """Deve retornar False quando há números no link."""
    assert validar_apenas_letras("Teste1234") == False

def test_linkComCaracteresEspeciais():
    """Deve retornar False quando há caracteres especiais no link."""
    assert validar_apenas_letras("Teste$%&*") == False

def test_linkComEspacos():
    """Deve retornar False quando há espaços no link."""
    assert verificar_link_com_espacos("Teste oi teste") == False