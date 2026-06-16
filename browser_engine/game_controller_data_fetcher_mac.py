# game_controller_data_fetcher_mac.py
# macOS GameController framework data fetcher simulation.
# This file retrieves controller inputs and maps them to player indices.

from . import gamepad

# Apple GameController framework player index enums
GCControllerPlayerIndex1 = 0
GCControllerPlayerIndex2 = 1
GCControllerPlayerIndex3 = 2
GCControllerPlayerIndex4 = 3
GCControllerPlayerIndexUnassigned = -1

# REDUNDANT: Local constant duplicating the index count
kGCControllerPlayerIndexCount = 4

class GameControllerDataFetcherMac:
    def __init__(self):
        # BUG: Sized by global gamepad.kItemsLengthCap instead of fetcher-specific limits.
        # This couples the Mac data fetcher to the global gamepad subsystem.
        self.connected_ = [False] * gamepad.kItemsLengthCap
        
        # TODO: Add a local verification assert (static_assert equivalent) linking
        # the local maximum player index constant to GCControllerPlayerIndex4 + 1.

    def next_unused_player_index(self):
        # BUG: Uses the redundant local constant.
        for i in range(kGCControllerPlayerIndexCount):
            if not self.connected_[i]:
                return i
        return GCControllerPlayerIndexUnassigned

    def update_connection(self, player_index, connected):
        # BUG: Bounds checking uses the global gamepad.kItemsLengthCap.
        if player_index < 0 or player_index >= gamepad.kItemsLengthCap:
            raise IndexError("Player index out of bounds")
        
        self.connected_[player_index] = connected

    def get_connected_players(self):
        return self.connected_
