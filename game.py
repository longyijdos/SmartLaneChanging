import json
import argparse
from players import Player1, Player2


def change_success(args, a1, a2):
    distance = (args.v1 - args.v2) * args.t + 0.5 * (a1 - a2) * args.t ** 2
    print(f"Distance: {distance}")
    return distance > 1.5 * args.l or distance < -1.5 * args.l


def game(args):
    with open(args.para_path, 'r') as file:
        data = json.load(file)

    player1 = Player1(data["player1"], args)
    player2 = Player2(data["player2"], args)

    payoff1 = {}
    a1 = {}
    payoff1["acceleration"], a1["acceleration"] = player1.payoff("acceleration", args.v2, args.t)
    payoff1["constant"], a1["constant"] = player1.payoff("constant", args.v2, args.t)
    print(f"Player1 Payoffs: {payoff1}")

    sorted_keys1 = sorted(payoff1, key=lambda k: payoff1[k], reverse=True)

    while True:
        for i in sorted_keys1:
            payoff2 = {}
            a2 = {}
            payoff2["acceleration"], a2["acceleration"] = player2.payoff("acceleration", args.v1, a1[i], args.t, args.l)
            payoff2["constant"], a2["constant"] = player2.payoff("constant", args.v1, a1[i], args.t, args.l)
            payoff2["deceleration"], a2["deceleration"] = player2.payoff("deceleration", args.v1, a1[i], args.t, args.l)
            print(f"Player2 Payoffs: {payoff2}")

            sorted_keys2 = sorted(payoff2, key=lambda k: payoff2[k], reverse=True)

            j = sorted_keys2[0]

            if change_success(args, a1[i], a2[j]):
                print(
                    f"Successfully change the lane, player1 choose {i} with {a1[i]} m/s^2, player2 choose {j} with {a2[j]} m/s^2")
                return

        player2.shrink(j)
        print(f"Shrink {j} choice, new C values: {player2.C}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--para_path", type=str, help="path to json file", default="setting舒适_效率.json")
    parser.add_argument("--v1", type=float, help="v1", default=12)
    parser.add_argument("--v2", type=float, help="v2", default=10)
    parser.add_argument("--a1_min", type=int, help="minimum a of player1", default=-5)
    parser.add_argument("--a1_max", type=int, help="maximum a of player1", default=7)
    parser.add_argument("--a2_min", type=int, help="minimum a of player2", default=-5)
    parser.add_argument("--a2_max", type=int, help="maximum a of player2", default=7)
    parser.add_argument("--type1", type=str, choices=["comfort", "efficient"], help="type of player1",
                        default="comfort")
    parser.add_argument("--type2", type=str, choices=["comfort", "efficient"], help="type of player2",
                        default="comfort")
    parser.add_argument("--t", type=float, help="time", default=1)
    parser.add_argument("--l", type=float, help="length of the car", default=1)
    args = parser.parse_args()
    game(args)