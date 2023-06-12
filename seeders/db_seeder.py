import importlib


def seed():
    seeders = [
        'role_seeder'
    ]

    for seeder in seeders:
        module = importlib.import_module('seeders.' + seeder)
        if hasattr(module, 'seed') and callable(getattr(module, 'seed')):
            module.seed()
