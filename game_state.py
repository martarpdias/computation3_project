import json
import os
import time


class GameState:
    def __init__(self):
        self.save_file = "game_save.json"
        self.default_state = {
            "score": 0,
            "current_round": 1,
            "player_health": 100,
            "last_saved": None
        }

    def save_game(self, score, current_round, player_health):
        """Save the current game state to a JSON file"""
        state = {
            "score": score,
            "current_round": current_round,
            "player_health": player_health,
            "last_saved": time.strftime("%Y-%m-%d %H:%M:%S")
        }

        try:
            save_path = os.path.abspath(self.save_file)
            print(f"Saving game state - Score: {score}, Round: {current_round}, Health: {player_health}")

            with open(save_path, 'w') as f:
                json.dump(state, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving game state: {e}")
            return False

    def load_game(self):
        """Load the game state from the JSON file"""
        try:
            save_path = os.path.abspath(self.save_file)

            if os.path.exists(save_path):
                with open(save_path, 'r') as f:
                    state = json.load(f)

                print(
                    f"Loaded saved game - Score: {state['score']}, Round: {state['current_round']}, Health: {state['player_health']}")
                return state  # Retorna o estado carregado
            else:
                print("Save file not found, returning default state.")
                return self.default_state.copy()  # Retorna o estado padrão se não houver arquivo
        except Exception as e:
            print(f"Error loading game state: {e}")
            return self.default_state.copy()  # Retorna o estado padrão em caso de erro
