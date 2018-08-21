from enum import Enum


class Endings(Enum):
    HITLER_CHANCELLOR = "Hitler Chancellor"
    HITLER_DEAD = "Hitler Dead"
    FASCIST_POLICY = "Fascist Policy"
    LIBERAL_POLICY = "Liberal Policy"


class Teams(Enum):
    LIBERAL = "Liberal"
    FASCIST = "Fascist"


players = {
    5: {
        "liberal": 3,
        "fascist": 2,
        "track": [
            None,
            None,
            "policy",
            "kill",
            "kill",
            None
        ]
    },
    6: {
        "liberal": 4,
        "fascist": 2,
        "track": [
            None,
            None,
            "policy",
            "kill",
            "kill",
            None
        ]
    },
    7: {
        "liberal": 4,
        "fascist": 3,
        "track": [
            None,
            "inspect",
            "choose",
            "kill",
            "kill",
            None
        ]
    },
    8: {
        "liberal": 5,
        "fascist": 3,
        "track": [
            None,
            "inspect",
            "choose",
            "kill",
            "kill",
            None
        ]
    },
    9: {
        "liberal": 5,
        "fascist": 4,
        "track": [
            "inspect",
            "inspect",
            "choose",
            "kill",
            "kill",
            None
        ]
    },
    10: {
        "liberal": 6,
        "fascist": 4,
        "track": [
            "inspect",
            "inspect",
            "choose",
            "kill",
            "kill",
            None
        ]
    },
}

board = {
    "policy": {
        "liberal": 6,
        "fascist": 11
    }
}