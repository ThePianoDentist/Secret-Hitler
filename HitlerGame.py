from HitlerBoard import HitlerBoard
from HitlerConstants import Endings, Teams
from HitlerPlayer import DumbPlayer
from random import randint


class HitlerGame(object):
    def __init__(self, playernum=0):
        """Stuff"""
        self.playernum = playernum or int(input("How many players?\n"))
        self.hitler = None
        self.board = HitlerBoard(self.playernum)
        self.board.assign_players()

    def play(self):
        """Main game loop"""
        self.inform_fascists()
        self.choose_first_president()

        while not self.game_ended:
            self.turn()

        #print("Game's over!")

    @property
    def game_ended(self):
        return self.policy_win() or self.hitler.is_dead or self.hitler_chancellor_win()

    def turn(self):
        """
        Take a turn.
        """
        # First, pass on the presidency
        self.set_next_president()

        # Ask the president to nominate a chancellor
        self.board.chancellor = self.nominate_chancellor()

        # Ask the players to vote whether they want this pairing
        voted = self.voting()

        if not voted:
            #print("Vote failed!")
            action_enacted = self.vote_failed()
        else:
            # Possibility to win if Hitler is chancellor and more than 2 fascist policies enacted.
            if self.hitler_chancellor_win():
                return

            action_enacted = self.vote_passed()

        if action_enacted:
            self.perform_vote_action()

    def inform_fascists(self):
        """
        Inform the fascists who the other fascists are.
        If there are 5 players, Hitler knows who the other fascist is.
        """

        for fascist in self.board.players[Teams.FASCIST]:
            # Every fascist knows who Hitler is
            fascist.hitler = self.hitler
            if self.playernum in [5, 6]:
                # Hitler knows about the other fascist
                fascist.fascists = self.board.players[Teams.FASCIST]
            elif not fascist.is_hitler:
                # Hitler doesn't know about the other fascists
                fascist.fascists = self.board.players[Teams.FASCIST]

    def choose_first_president(self):
        """
        Choose a random player to be the 'zeroth' president, the first president will
        be the next person after them.
        """
        self.board.president = self.board.players[randint(0, len(self.board.players) - 1)]

    def set_next_president(self):
        self.board.president = self.board.players[(self.board.president.id + 1) % len(self.board.players)]
        if self.board.president.is_dead:
            self.set_next_president()

    def nominate_chancellor(self):
        chancellor = self.board.chancellor
        while (chancellor == self.board.chancellor or
               chancellor == self.board.president or
               (self.playernum in [5, 6] and
                chancellor == self.board.ex_president) or
               chancellor.is_dead):
            chancellor = self.board.president.nominate_chancellor()

        return chancellor

    def voting(self):
        """
        Get votes for the current pairing from all players.
        :returns: Whether the vote succeeded
        """
        self.board.last_votes = []
        for player in self.board.players:
            if not player.is_dead:
                self.board.last_votes.append(player.vote())

        positivity = 0

        for vote in self.board.last_votes:
            if vote:
                positivity += 1
            else:
                positivity -= 1

        return positivity > 0

    def vote_failed(self):
        #print("Vote failed!")
        self.board.failed_votes += 1

        if self.board.failed_votes == 3:
            self.board.failed_votes = 0

            #print("Too many failed votes! Citizens are taking action into their own hands")
            return self.board.enact_policy(self.board.draw_policy(1)[0])

        else:
            # Not enacting a vote, take another turn
            return False

    def vote_passed(self):
        """
        The vote has passed! Get the president and chancellor to do their thang.
        """
        #print("Vote passed!")

        (take, discard) = self.board.president.filter_policies(self.board.draw_policy(3))
        self.board.discards.append(discard)

        if (self.board.veto and
                self.board.chancellor.chancellor_veto(take) and
                self.board.president.president_veto()):
            #print("Vote vetoed!")
            return self.vote_failed()

        (enact, discard) = self.board.chancellor.enact_policy(take)
        self.board.discards.append(discard)
        return self.board.enact_policy(enact)

    def hitler_chancellor_win(self):
        return (self.board.fascist_track >= 3 and
                self.board.chancellor == self.hitler)

    def policy_win(self):
        return self.board.liberal_track == 5 or self.board.fascist_track == 6

    def perform_vote_action(self):
        action = self.board.fascist_track_actions[self.board.fascist_track - 1]
        if action is None:
            #print("No action")
            return

        #print("Performing vote action: %s" % action)

        if action == "policy":
            top_three = self.board.draw_policy(3)
            self.board.president.view_policies(top_three)
            self.board.return_policy(top_three)

        elif action == "kill":
            killed_player = self.board.president.kill()
            while killed_player.is_dead or killed_player == self.board.president:
                killed_player = self.board.president.kill()
            killed_player.is_dead = True

        elif action == "inspect":
            inspect = self.board.president.inspect_player()
            while inspect.is_dead or inspect == self.board.president:
                self.board.president.inspected_players[inspect] = inspect.role.party_membership

        elif action == "choose":
            chosen = self.board.president
            while chosen == self.board.president or chosen.is_dead:
                chosen = self.board.president.choose_next()

            self.board.president = chosen

        else:
            assert False, "Unrecognised action!"

    @property
    def game_result(self):
        if self.hitler_chancellor_win():
            #print("Fascists win by electing Hitler!")
            return Endings.HITLER_CHANCELLOR

        elif self.policy_win():
            if self.board.liberal_track == 5:
                #print("Liberals win by policy!")
                return Endings.LIBERAL_POLICY
            else:
                #print("Fascists win by policy!")
                return Endings.FASCIST_POLICY

        elif self.hitler.is_dead:
            #print("Liberals win by shooting Hitler!")
            return Endings.HITLER_DEAD


def newgame():
    game = HitlerGame(10)
    game.play()
    return game.game_result


if __name__ == "__main__":
    games = {
        Endings.HITLER_CHANCELLOR: 0,
        Endings.FASCIST_POLICY: 0,
        Endings.LIBERAL_POLICY: 0,
        Endings.HITLER_DEAD: 0
    }
    for ii in range(100000):
        result = newgame()
        games[result] += 1

    print(games)
    print(str(games[Endings.LIBERAL_POLICY] + games[Endings.HITLER_DEAD]) + ":" +
          str(games[Endings.FASCIST_POLICY] + games[Endings.HITLER_CHANCELLOR]))
