#!/home/cees/.virtualenvs/magic/bin/python
import os
import sys

# add the parent dir of this script to the python path
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))

from google_scripts.models import MtgStatsManager


def main(prog_args):
    manager = MtgStatsManager()
    print(manager.decks)
    for key, battle in manager.battles.items():
        decks_info = []
        for deck_name, wins in battle['decks'].items():
            decks_info.append("{}: {}% ({})".format(deck_name, round(wins/battle['total_games'] * 100), wins))
        print("{}: {}".format(key, ", ".join(decks_info)))


if __name__ == '__main__':
    sys.exit(main(sys.argv))
