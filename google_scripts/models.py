import os

from google_scripts.google_api_client import Client as GoogleClient


class MtgStatsException(Exception):
    pass


class MtgStatsManager(object):
    COLUMN_DATE = 'date'
    COLUMN_WINNER = 'Winner'
    COLUMN_WES = 'Wes'
    COLUMN_PAPS = 'Paps'
    HEADER_ROW = [COLUMN_DATE, COLUMN_WINNER, COLUMN_WES, COLUMN_PAPS]

    def __init__(self):
        self.raw_data = None
        self.decks = set()
        self.data = []
        self.battles = {}
        self.google_client = GoogleClient(
            os.environ['GOOGLE_DRIVE_CLIENT_ID'],
            os.environ['GOOGLE_DRIVE_CLIENT_SECRET'],
            os.environ['MTG_DECKS_DRIVE_FILE_ID'])
        self.load()

    def _from_google_values(self, google_data):
        header_row = google_data.pop(0)
        if header_row != self.HEADER_ROW:
            raise MtgStatsException("Spreadsheet header differs from expected header, can't load data. {} != {}."
                                    .format(header_row, self.HEADER_ROW))
        for row in google_data:
            deck_wes = self.get_value(row, self.COLUMN_WES)
            deck_paps = self.get_value(row, self.COLUMN_PAPS)
            self.decks.add(deck_wes)
            self.decks.add(deck_paps)
            battle_names = [deck_wes, deck_paps]
            battle_names.sort()
            battle_key = '_'.join(battle_names)
            battle = self.battles.get(battle_key)
            if not battle:
                battle = {'decks': {deck_wes: 0, deck_paps: 0}, 'total_games': 0}
                self.battles[battle_key] = battle
            battle['total_games'] += 1
            if self.get_value(row, self.COLUMN_WINNER) == self.COLUMN_WES:
                battle['decks'][deck_wes] += 1
            else:
                battle['decks'][deck_paps] += 1

    def get_value(self, row, column):
        return row[self.HEADER_ROW.index(column)]

    def load(self, overwrite=False):
        if self.raw_data and not overwrite:
            raise MtgStatsException("Data already loaded from google, use the 'overwrite' parameter to load anyway")
        self.raw_data = self.google_client.get_file()
        self._from_google_values(self.raw_data)
        return self.data


class MtgStats(object):

    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        return "<{}: >".format(self.__class__.__name__)

    def __repr__(self) -> str:
        return self.__str__()
