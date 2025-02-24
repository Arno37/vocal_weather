# test_service_city.py (convention de nommage des fichiers de test : test_*.py)
import pytest
from service_city import postal_code_to_city

def test_postal_code_to_city():
    postal_code = "37000"

    ville = postal_code_to_city(postal_code)

    assert ville == "tours", "La ville doit être égale à 'tours'"

@pytest.fixture # Le décorateur @pytest.fixture marque la fonction sample_postal_code comme une fixture pytest
def sample_postal_code():
    return "37000"

def test_postal_code_to_city(sample_postal_code):
    ville = postal_code_to_city(sample_postal_code) # la valeur fournie par la fixture sample_postal_code est injectée automatiquement
    assert ville == "tours", "La ville doit être égale à 'tours'"

def test_postal_code_to_city_among_known_cities(sample_postal_code):
    ville = postal_code_to_city(sample_postal_code)
    assert ville in ["bordeaux", "brest", "paris", "tours"], f"La ville '{ville}' devrait être parmi les villes connues"

@pytest.mark.parametrize("postal_code, expected_city", [
    ("29200", "brest"),
    ("33000", "bordeaux"),
    ("37000", "tours"),
    ("75000", "paris"),
    ("99999", None)  # Cas où le code postal n'est pas défini dans le dictionnaire
])
def test_postal_code_to_city_parametrized(postal_code, expected_city):
    result = postal_code_to_city(postal_code)
    assert result == expected_city, f"Pour le code postal {postal_code}, la ville retournée devrait être '{expected_city}', mais obtenue '{result}'."