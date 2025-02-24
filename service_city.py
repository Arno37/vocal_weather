def postal_code_to_city(postal_code):
    # Dictionnaire associant les codes postaux aux villes
    postal_code_map = {
        "29200": "brest",
        "33000": "bordeaux",
        "37000": "tours",
        "75000": "paris"
    }

    # Retourne la ville qui correspond au code postal, ou None si non trouvé
    return postal_code_map.get(postal_code, None)