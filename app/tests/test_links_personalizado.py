import pytest

from app.controllers.links import *

def test_linkComNumero():
    assert validar_apenas_letras("Teste1234")

def test_linkComCaracteresEspeciais():
    assert validar_apenas_letras("Teste$%&*")

def test_linkComEspacos():
    assert verificar_link_com_espacos("Teste oi teste")