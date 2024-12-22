LEVELS = {
    1: {
        "enemy_types": [Enemy],
        "enemy_spawn_rate": 2,  # Enemies spawn every 2 seconds
        "unlock": True,  # The first level is unlocked by default
    },
    2: {
        "enemy_types": [Enemy],
        "enemy_spawn_rate": 1.5,  # Faster spawning
        "unlock": False,
    },
    3: {
        "enemy_types": [Enemy, fast_enemy],
        "enemy_spawn_rate": 2,
        "unlock": False,
    },
    4: {
        "enemy_types": [Enemy, fast_enemy],
        "enemy_spawn_rate": 1.5,
        "unlock": False,
    },
    5: {
        "enemy_types": [Enemy, fast_enemy],
        "enemy_spawn_rate": 1,
        "unlock": False,
    },
    6: {
        "enemy_types": [Enemy, shooter_rastreio],
        "enemy_spawn_rate": 2,
        "unlock": False,
    },
    7: {
        "enemy_types": [Enemy, shooter_rastreio],
        "enemy_spawn_rate": 1,
        "unlock": False,
    },
    8: {
        "enemy_types": [Enemy, fast_enemy, shooter_rastreio],
        "enemy_spawn_rate": 2,
        "unlock": False,
    },
    9: {
        "enemy_types": [Enemy, fast_enemy, shooter_rastreio],
        "enemy_spawn_rate": 1.5,
        "unlock": False,
    },
    10: {
        "enemy_types": [Enemy, fast_enemy],
        "enemy_spawn_rate": 2,
        "unlock": False,
    },
}