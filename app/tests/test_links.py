import pytest

from app.controllers.links import *

def test_verificacaoURL():
    assert verificacaoURL("https://g1.globo.com/")
    assert verificacaoURL("https://portal.ifro.edu.br/")

def test_verificacaoTextoURL():
    assert verificacaoTextoURL("Fonte: https://g1.globo.com/")

def test_variarPossibilidades():
    assert variarPossibilidades("https://portal.ifro.edu.br/")