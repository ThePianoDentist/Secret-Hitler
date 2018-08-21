from HitlerConstants import players, board, Teams
from random import shuffle
import HitlerPolicy
import HitlerRole
from HitlerPlayer import DumbPlayer


class HitlerBoard(object):
    def __init__(self, playercount):
        self.num_players = playercount
        self.num_liberals = players[self.num_players]["liberal"]
        self.num_fascists = players[self.num_players]["fascist"]
        self.fascist_track_actions = players[self.num_players]["track"]

        self.policies = ([HitlerPolicy.Liberal()] * board["policy"]["liberal"] +
                         [HitlerPolicy.Fascist()] * board["policy"]["fascist"])
        shuffle(self.policies)
        self.liberal_track = 0
        self.fascist_track = 0
        self.failed_votes = 0
        self.president = None
        self.ex_president = None
        self.chosen_president = None
        self.chancellor = None
        self.most_recent_policy = None
        self.last_votes = []
        self.players = {Teams.FASCIST: [],
                        Teams.LIBERAL: []}
        self.veto = False
        self.discards = []
        self.previous = []

    def shuffled_roles(self):
        all_roles = ([HitlerRole.Liberal()] * self.num_liberals +
                     [HitlerRole.Fascist(False)] * (self.num_fascists - 1) +
                     [HitlerRole.Fascist(True)])
        shuffle(all_roles)

        return all_roles

    def assign_players(self):
        roles = self.shuffled_roles()

        for i, role in enumerate(roles):
            # name = raw_input("Player #%d's name?\n" % num)
            name = "Bot %d" % i
            player = DumbPlayer(i,
                                name,
                                role,
                                self)

            if player.is_hitler:
                # Keep track of Hitler
                self.hitler = player

            self.players[Teams.LIBERAL].append(player) if role.is_liberal else self.players[Teams.FASCIST].append(player)

    def draw_policy(self, num):
        """
        Draw cards from the policy pile
        :param num: Number to draw
        :return: HitlerPolicy objects
        """
        if len(self.policies) >= num:
            drawn = self.policies[:num]
            self.policies = self.policies[num:]
            return drawn
        else:
            # Shuffle the discard and add them to the policies pile again
            #print("Draw pile is empty! Shuffling discards and putting into draw pile")
            shuffle(self.discards)
            #print("Discards: %s" % self.discards)
            self.policies = self.policies + self.discards
            self.discards = []
            #print ("New policy pile: %s" % self.policies)
            assert len(self.policies) > num
            return self.draw_policy(num)

    def discard(self, cards):
        """
        Discard the card we've been given, assert that they're Policy cards!
        :param cards: Policy or list of Policies
        """
        if not isinstance(cards, list):
            cards = [cards]

        for card in cards:
            assert isinstance(card, HitlerPolicy.Policy)
            self.discards.append(card)

    def return_policy(self, policies):
        """
        Return the card we've been given to the policy pile, assert that they're Policy cards!
        :param cards: Policy or list of Policies
        """
        if not isinstance(policies, list):
            policies = [policies]

        for policy in policies:
            assert isinstance(policy, HitlerPolicy.Policy)

        self.policies = policies + self.policies

    def enact_policy(self, policy):
        if policy.type == "liberal":
            self.liberal_track += 1
        else:
            self.fascist_track += 1
            if self.fascist_track_actions[self.fascist_track - 1] is not None:
                return True

        return False

if __name__ == "__main__":
    h = HitlerBoard(5)
    #print(h.shuffle_roles())
    #print(h.policies)
    #print(h.state.fascist_track)

    #print("Drawing three cards")
    #print(h.draw_policy(3))
    #print(h.policies)