import LiteEFG
from tqdm import tqdm
import pyspiel

def train(graph, traverse_type, convergence_type, iter, print_freq, game_env="leduc_poker"):
    game = pyspiel.load_game(game_env)
    env = LiteEFG.OpenSpielEnv(game, traverse_type=traverse_type)
    #env = LiteEFG.FileEnv("GameInstances/kuhn_poker.openspiel", traverse_type=args.traverse_type)
    env.GetGraph(graph)

    for i in tqdm(range(iter)):
        graph.UpdateGraph(env)
        if convergence_type != "default":
            env.UpdateStrategy(graph.Strategy(), update_best=(convergence_type == "best-iterate"))
            
        if i % print_freq == 0:
            print(i, env.Exploitability(graph.Strategy(), convergence_type))

def test():
    import CFR
    import CFRplus
    import DCFR
    import DOMD
    import MMD
    import OS_MCCFR
    import QFR
    alg_list = [CFR.graph(), CFRplus.graph(), DCFR.graph(), DOMD.graph(), MMD.graph(), OS_MCCFR.graph(), QFR.graph()]
    traverse_type_list = ["Enumerate", "Enumerate", "Enumerate", "Enumerate", "Enumerate", "Outcome", "Enumerate"]
    convergence_type_list = ["avg-iterate", "linear-avg-iterate", "last-iterate", "last-iterate", "default", "avg-iterate", "default"]
    alg_name_list = ["CFR", "CFR+", "DCFR", "DOMD", "MMD", "OS-MCCFR", "QFR"]

    for i, alg in enumerate(alg_list):
        train(alg, traverse_type_list[i], convergence_type_list[i], 100001, 100000, "kuhn_poker")
        print(alg_name_list[i] + " finished training")
    print("Test Success")

if __name__ == "__main__":
    test()
