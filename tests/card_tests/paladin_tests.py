import random
import unittest
from hsgame.agents.basic_agents import PredictableBot, DoNothingBot
from tests.testing_agents import *
from tests.testing_utils import generate_game_for
from hsgame.replay import SavedGame

from hsgame.cards import *

__author__ = 'Daniel'

class TestPaladin(unittest.TestCase):

    def setUp(self):
        random.seed(1857)


    def testPaladinPower(self):
        game = generate_game_for(AvengingWrath, MogushanWarden, PredictableBot, DoNothingBot)

        for turn in range(0, 3):
            game.play_single_turn()

        self.assertEqual(1, len(game.current_player.minions))
        self.assertEqual(1, game.current_player.minions[0].attack_power)
        self.assertEqual(1, game.current_player.minions[0].defense)
        self.assertEqual("Silver Hand Recruit", game.current_player.minions[0].card.name)


    def testAvengingWrath(self):
        game = generate_game_for(MogushanWarden, AvengingWrath, MinionPlayingAgent, SpellTestingAgent)

        for turn in range(0, 12):
            game.play_single_turn()

        #The random numbers work so that Avenging Wrath hits the player once, first minion once, second minion four times and third minion two times (total of eight hits)
        self.assertEqual(29, game.other_player.health)
        self.assertEqual(3, len(game.other_player.minions))
        self.assertEqual("Mogu'shan Warden", game.other_player.minions[0].card.name)
        self.assertEqual("Mogu'shan Warden", game.other_player.minions[1].card.name)
        self.assertEqual("Mogu'shan Warden", game.other_player.minions[2].card.name)
        self.assertEqual(6, game.other_player.minions[0].defense)
        self.assertEqual(3, game.other_player.minions[1].defense)
        self.assertEqual(5, game.other_player.minions[2].defense)

    def testBlessedChampion(self):
        game = generate_game_for(BlessedChampion, StonetuskBoar, EnemyMinionSpellTestingAgent, MinionPlayingAgent)
        
        for turn in range(0, 9):
            game.play_single_turn()

        self.assertEqual(2, game.other_player.minions[0].attack_power)
        self.assertEqual(1, game.other_player.minions[0].defense)
        self.assertEqual(1, game.other_player.minions[0].max_defense)

        #Test that this spell is being silenced properly as well
        game.other_player.minions[0].silence()
        self.assertEqual(1, game.other_player.minions[0].attack_power)
        self.assertEqual(1, game.other_player.minions[0].defense)
        self.assertEqual(1, game.other_player.minions[0].max_defense)
        
    def testBlessingOfKings(self):
        game = generate_game_for(BlessingOfKings, StonetuskBoar, EnemyMinionSpellTestingAgent, MinionPlayingAgent)
        
        for turn in range(0, 7):
            game.play_single_turn()

        self.assertEqual(5, game.other_player.minions[0].attack_power)
        self.assertEqual(5, game.other_player.minions[0].defense)
        self.assertEqual(5, game.other_player.minions[0].max_defense)

        #Test that this spell is being silenced properly as well
        game.other_player.minions[0].silence()
        self.assertEqual(1, game.other_player.minions[0].attack_power)
        self.assertEqual(1, game.other_player.minions[0].defense)
        self.assertEqual(1, game.other_player.minions[0].max_defense)

    def testBlessingOfMight(self):
        game = generate_game_for(StonetuskBoar, BlessingOfMight, MinionPlayingAgent, EnemyMinionSpellTestingAgent)
        
        for turn in range(0, 2):
            game.play_single_turn()

        self.assertEqual(4, game.other_player.minions[0].attack_power)
        self.assertEqual(1, game.other_player.minions[0].defense)
        self.assertEqual(1, game.other_player.minions[0].max_defense)

        #Test that this spell is being silenced properly as well
        game.other_player.minions[0].silence()
        self.assertEqual(1, game.other_player.minions[0].attack_power)
        self.assertEqual(1, game.other_player.minions[0].defense)
        self.assertEqual(1, game.other_player.minions[0].max_defense)

    def testBlessingOfWisdom(self):
        game = SavedGame("tests/replays/card_tests/BlessingOfWisdom.rep")
        game.start()
        self.assertEqual(3, len(game.current_player.minions))
        # 7 cards have been drawn.
        # 3 for starting first, 3 for new turn and 1 for minion attack with Blessing of Wisdom (the second minion who had it got silenced)
        self.assertEqual(23, game.other_player.deck.left)

    def testConsecration(self):
        game = generate_game_for(StonetuskBoar, Consecration, MinionPlayingAgent, SpellTestingAgent)

        for turn in range(0, 7):
            game.play_single_turn()
            
        self.assertEqual(30, game.players[0].health)
        self.assertEqual(4, len(game.players[0].minions))
        game.play_single_turn()
        self.assertEqual(28, game.players[0].health)
        self.assertEqual(0, len(game.players[0].minions))
        
    def testDivineFavor(self):
        game = generate_game_for(StonetuskBoar, DivineFavor, DoNothingBot, SpellTestingAgent)

        for turn in range(0, 5):
            game.play_single_turn()
        
        # Cheat
        for cheat in range(0, 4):
            game.players[0].draw()
        
        self.assertEqual(10, len(game.players[0].hand))
        self.assertEqual(6, len(game.players[1].hand))
        game.play_single_turn()
        self.assertEqual(10, len(game.players[0].hand))
        self.assertEqual(10, len(game.players[1].hand))
        # The following test is if we have 10 cards in hand already. Casting Divine Favor should count as being down to 9 again, and then draw a 10th card
        game.play_single_turn()
        self.assertEqual(10, len(game.players[0].hand))
        self.assertEqual(10, len(game.players[1].hand))
        game.play_single_turn() # New turn, p2 draws a card that is discarded (10), cast Divine Favor (9), draws a new card (10)
        self.assertEqual(10, len(game.players[0].hand))
        self.assertEqual(10, len(game.players[1].hand))
        
    def testEquality(self):
        game = generate_game_for(MogushanWarden, Equality, MinionPlayingAgent, SpellTestingAgent)

        for turn in range(0, 3):
            game.play_single_turn()
        
        self.assertEqual(0, len(game.players[0].minions))
        self.assertEqual(0, len(game.players[1].minions))
        self.assertEqual(5, len(game.players[1].hand))
        game.play_single_turn() # SpellTestingAgent should draw a card, have 2 mana and try to cast Equality, which it shouldn't be able to do (no minions), so hand should be 6
        self.assertEqual(0, len(game.players[0].minions))
        self.assertEqual(0, len(game.players[1].minions))
        self.assertEqual(6, len(game.players[1].hand))
        
        for turn in range(0, 3):
            game.play_single_turn()
            
        # Make sure there's a minion on the playfield
        self.assertEqual(1, len(game.players[0].minions))
        self.assertEqual(7, game.players[0].minions[0].defense)
        self.assertEqual(7, game.players[0].minions[0].max_defense)
        game.play_single_turn() # Equality should be played this turn
        self.assertEqual(1, len(game.players[0].minions))
        self.assertEqual(1, game.players[0].minions[0].defense)
        self.assertEqual(1, game.players[0].minions[0].max_defense)
        # Test it again to make sure the minion stays at 1 health
        game.play_single_turn() # A new minion should be played
        game.play_single_turn() # And Equality should be played here
        self.assertEqual(2, len(game.players[0].minions))
        self.assertEqual(1, game.players[0].minions[0].defense)
        self.assertEqual(1, game.players[0].minions[0].max_defense)
        self.assertEqual(1, game.players[0].minions[1].defense)
        self.assertEqual(1, game.players[0].minions[1].max_defense)

    def testHammerOfWrath(self):
        game = generate_game_for(MogushanWarden, HammerOfWrath, DoNothingBot, SpellTestingAgent)
        
        for turn in range(0, 7):
            game.play_single_turn()

        self.assertEqual(30, game.players[0].health)
        self.assertEqual(7, len(game.players[1].hand))
        game.play_single_turn() # Hammer of Wrath should be played
        self.assertEqual(27, game.players[0].health)
        self.assertEqual(8, len(game.players[1].hand))

    def testHandOfProtection(self):
        game = generate_game_for(StonetuskBoar, HandOfProtection, MinionPlayingAgent, SpellTestingAgent)
        
        game.play_single_turn() # Stonetusk Boar should be played
        self.assertEqual(1, len(game.players[0].minions))
        self.assertEqual("Stonetusk Boar", game.players[0].minions[0].card.name)
        self.assertFalse(game.players[0].minions[0].divine_shield)
        game.play_single_turn() # Hand of Protection should be played here, and the only available target should be the enemy minion
        self.assertEqual(0, len(game.players[1].minions))
        self.assertEqual(1, len(game.players[0].minions))
        self.assertEqual("Stonetusk Boar", game.players[0].minions[0].card.name)
        self.assertTrue(game.players[0].minions[0].divine_shield)

    def testHolyLight(self):
        game = generate_game_for(StonetuskBoar, HolyLight, DoNothingBot, SpellTestingAgent)
        
        for turn in range(0, 3):
            game.play_single_turn()
        
        game.players[0].health = 20
        game.play_single_turn() # Holy Light should be played
        self.assertEqual(26, game.players[0].health)
        game.play_single_turn()
        game.play_single_turn() # Holy Light should be played
        self.assertEqual(30, game.players[0].health)

    def testHolyWrath(self):
        game = generate_game_for(StonetuskBoar, HolyWrath, DoNothingBot, SpellTestingAgent)
        
        for turn in range(0, 9):
            game.play_single_turn()
        
        self.assertEqual(30, game.players[0].health)
        game.play_single_turn() # Holy Wrath should be played that will draw Holy Wrath that costs 5 mana, thus dealing 5 damage
        self.assertEqual(25, game.players[0].health)

    def testHumility(self):
        game = generate_game_for(BloodfenRaptor, Humility, MinionPlayingAgent, SpellTestingAgent)
        
        game.play_single_turn()
        game.play_single_turn() # No targets for Humility
        game.play_single_turn() # Bloodfen Raptor should be played
        self.assertEqual(1, len(game.players[0].minions))
        self.assertEqual("Bloodfen Raptor", game.players[0].minions[0].card.name)
        self.assertEqual(3, game.players[0].minions[0].attack_power)
        self.assertEqual(2, game.players[0].minions[0].defense)
        game.play_single_turn() # Humility should be played, and target the enemy Bloodfen Raptor
        self.assertEqual(1, len(game.players[0].minions))
        self.assertEqual("Bloodfen Raptor", game.players[0].minions[0].card.name)
        self.assertEqual(1, game.players[0].minions[0].attack_power)
        self.assertEqual(2, game.players[0].minions[0].defense)

    def testLayOnHands(self):
        game = generate_game_for(StonetuskBoar, LayOnHands, DoNothingBot, SpellTestingAgent)
        
        for turn in range(0, 15):
            game.play_single_turn()
        
        game.players[0].health = 20
        # Put back some cards from hand, for testing purpose
        for putback in range(0, 5):
            game.players[1].put_back(game.players[1].hand[0])
        self.assertEqual(5, len(game.players[1].hand))
        game.play_single_turn() # Lay on Hands should be played
        self.assertEqual(28, game.players[0].health)
        self.assertEqual(8, len(game.players[1].hand))
        game.play_single_turn()
        game.play_single_turn() # Lay on Hands should be played, and a card be discarded since we have 8 already
        self.assertEqual(30, game.players[0].health)
        self.assertEqual(10, len(game.players[1].hand))

    def testAldorPeacekeeper(self):
        game = generate_game_for(AldorPeacekeeper, BloodfenRaptor, MinionPlayingAgent, MinionPlayingAgent)
        for turn in range(0, 4):
            game.play_single_turn()

        self.assertEqual(1, len(game.players[1].minions))
        self.assertEqual(2, game.players[1].minions[0].defense)
        self.assertEqual(3, game.players[1].minions[0].attack_power)
        self.assertEqual("Bloodfen Raptor", game.players[1].minions[0].card.name)
        game.play_single_turn() # Aldor Peacekeeper should be played
        self.assertEqual(1, len(game.players[1].minions))
        self.assertEqual(2, game.players[1].minions[0].defense)
        self.assertEqual(1, game.players[1].minions[0].attack_power)
        self.assertEqual("Bloodfen Raptor", game.players[1].minions[0].card.name)
        self.assertEqual(1, len(game.players[0].minions))
        self.assertEqual(3, game.players[0].minions[0].defense)
        self.assertEqual(3, game.players[0].minions[0].attack_power)
        self.assertEqual("Aldor Peacekeeper", game.players[0].minions[0].card.name)
        game.players[1].minions[0].silence()
        self.assertEqual(2, game.players[1].minions[0].defense)
        self.assertEqual(3, game.players[1].minions[0].attack_power)
        
    def testArgentProtector(self):
        game = generate_game_for(ArgentProtector, BloodfenRaptor, MinionPlayingAgent, MinionPlayingAgent)
        for turn in range(0, 2):
            game.play_single_turn()

        self.assertEqual(0, len(game.players[0].minions))
        game.play_single_turn() # Argent Protector should be played
        self.assertEqual(1, len(game.players[0].minions))
        self.assertEqual("Argent Protector", game.players[0].minions[0].card.name)
        self.assertFalse(game.players[0].minions[0].divine_shield)
        game.play_single_turn()
        game.play_single_turn() # Argent Protector should be played, and the previous AP should get Divine Shield
        self.assertEqual(2, len(game.players[0].minions))
        self.assertTrue(game.players[0].minions[1].divine_shield)
        game.players[0].minions[1].silence()
        self.assertFalse(game.players[0].minions[1].divine_shield)
        
    def testGuardianOfKings(self):
        game = generate_game_for(GuardianOfKings, BloodfenRaptor, MinionPlayingAgent, DoNothingBot)
        for turn in range(0, 12):
            game.play_single_turn()

        game.players[0].health = 20

        self.assertEqual(0, len(game.players[0].minions))
        game.play_single_turn() # Guardian of Kings should be played
        self.assertEqual(1, len(game.players[0].minions))
        self.assertEqual("Guardian of Kings", game.players[0].minions[0].card.name)
        self.assertEqual(26, game.players[0].health)
