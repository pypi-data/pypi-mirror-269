import pyspiel
import os
import LiteEFG

def NodeName(node):
    if isinstance(node, str):
        return node.replace("\n", "/")
    return node.serialize().replace("\n", "/").replace(" ", "_")

def InfosetName(node, idx):
    infoset = node.information_state_string().replace("\n", "/")
    infoset = "pl%d_%d__"%(node.current_player()+1, idx) + infoset
    return infoset.replace(" ", "_")

class OpenSpielEnv(LiteEFG.FileEnv):
    def __init__(self, game: pyspiel.Game, traverse_type="Enumerate"):
        if not isinstance(game, pyspiel.Game):
            raise ValueError("game must be an instance of pyspiel.Game")
        
        game_name = game.get_type().short_name
        infosets = {}
        num_infosets = [0 for _ in range(game.num_players())]
        queue = [game.new_initial_state()]

        game_full_name = game_name
        for k in game.get_parameters():
            game_full_name += "_%s=%s"%(k, game.get_parameters()[k])

        current_directory = os.path.dirname(os.path.abspath(__file__))
        for i in range(3):
            current_directory = os.path.dirname(current_directory)
        os.makedirs(os.path.join(current_directory, "GameInstances"), exist_ok=True)
        file_name = os.path.join(current_directory, "GameInstances", game_full_name + ".openspiel")

        if os.path.exists(file_name):
            super().__init__(file_name, traverse_type=traverse_type)
            return
        
        print("Generating %s.openspiel instance from OpenSpiel"%(game_full_name))
        file = open(file_name, "w")

        print("# %s instance with parameters:"%game_name, file=file)
        print("#", file=file)
        print("# Opt {", file=file)
        print("#     openspiel,", file=file)
        for k in game.get_parameters():
            print("#     %s: %s,"%(k, game.get_parameters()[k]), file=file)
        if "players" not in game.get_parameters():
            print("#     players: %d,"%game.num_players(), file=file)
        print("# }", file=file)
        print("#", file=file)

        while len(queue) > 0:
            node = queue.pop()
            
            if node.is_terminal():
                print("node %s leaf payoffs"%NodeName(node), end='', file=file)
                for player, reward in enumerate(node.returns()):
                    print(" %d=%f"%(player+1, reward), end='', file=file)
                print(file=file)
                continue

            if node.is_chance_node():
                print("node %s chance actions"%NodeName(node), end='', file=file)
                for action, prob in node.chance_outcomes():
                    child = node.clone()
                    child.apply_action(action)
                    queue.append(child)
                    print(" %s=%.8f"%(NodeName(child.serialize()), prob), end='', file=file)
                print(file=file)
            else:
                print("node %s player %d actions"%(NodeName(node), node.current_player()+1), end='', file=file)
                for action in node.legal_actions():
                    child = node.clone()
                    child.apply_action(action)
                    queue.append(child)
                    print(" %s"%NodeName(child.serialize()), end='', file=file)
                print(file=file)

                infoset = node.information_state_string()
                if infoset not in infosets:
                    infosets[infoset] = [InfosetName(node, num_infosets[node.current_player()])]
                    num_infosets[node.current_player()] += 1
                infosets[infoset].append(node.serialize())

        for infoset in infosets:
            print("infoset %s nodes"%infosets[infoset][0], end='', file=file)
            for node in infosets[infoset][1:]:
                print(" %s"%NodeName(node), end='', file=file)
            print(file=file)
        
        file.close()
        super().__init__(file_name, traverse_type=traverse_type)

if __name__ == "__main__":
    OpenSpielEnv(pyspiel.load_game("dark_hex(board_size=2,gameversion=adh)"))