''' TimeStamp 10.01.2023 '''

''' Github version '''



import os, time
import pygame
import pygame.mouse
import pygame.time
from pygame.locals import *
import random
import numpy as np
import pandas as pd
from collections import Counter

def main():
    class Button():
        def __init__(self, x, y, image, number):
            self.number = number
            self.image = image
            self.rect = self.image.get_rect()
            self.rect.topleft = (x, y)
            self.clicked = False
            self.draw()

        def draw(self):
            action = False
            # get mouse position
            pos = pygame.mouse.get_pos()

            # check mouseover and clicked conditions
            if self.rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                    self.clicked = True
                    action = True

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
                action = False

            return action

    class State():
        def __init__(self, game):
            self.game = game
            self.prev_state = None

        def turnCalc(self, x):
            pass

        def update(self, delta_time, actions):
            pass

        def render(self, surface):
            pass

        def renderPlayers(self, surface, actions):
            pass

        def enter_state(self):
            if len(self.game.state_stack) > 1:
                self.prev_state = self.game.state_stack[-1]
            self.game.state_stack.append(self)

        def exit_state(self):
            self.game.state_stack.pop()

    ''' class Button '''

    class endGame(State):
        def __init__(self, game):
            self.game = game
            State.__init__(self, game)
            self.i = 1

        def update(self, delta_time, actions):
            if actions['start']:
                main()
            self.game.reset_keys()

        def render(self, display):
            if g.players_typed == False:
                display.fill((255, 255, 255))

                self.game.draw_text(display, 'Thank you for playing!', (255, 0, 0), g.screen.get_width() / 2,
                                    g.screen.get_height() / 5)
                self.game.draw_text(display, 'Click ENTER to start a new game', (0, 0, 0),
                                    g.screen.get_width() / 2, g.screen.get_height() / 1.4)

    class TitleScreen(State):
        def __init__(self, game):
            self.game = game
            State.__init__(self, game)
            self.i = 1

        def update(self, delta_time, actions):

            if g.start_button.clicked == True:

                g.players_rand()
                if g.players[1] == g.dealers[0]:
                    g.players.append(g.players[0])
                    g.players = g.players[1:]

                print(g.players)
                print(g.dealers)

                g.start_button.clicked = False
                new_state = CardChoosing(self.game)
                new_state.enter_state()
                self.game.reset_keys()

        def render(self, display):
            if g.players_typed == False:
                display.fill((255, 255, 255))

                self.game.draw_text(display, 'Fuck the Dealer', (0, 0, 0), g.screen.get_width() / 2,
                                    g.screen.get_height() / 5)

                base_font = pygame.font.Font(None, 60)

                # inputting player names
                input_rect = pygame.draw.rect(display, (54, 81, 94), pygame.Rect(
                    ((g.screen.get_width() - g.screen.get_width()) + 20, g.screen.get_height() / 1.5), (600, 100)))

                user_text = g.user_text
                text_surface = base_font.render(user_text, True, (0, 0, 0))
                display.blit(text_surface, (input_rect.x + 10, input_rect.y + 35))

                display.blit(g.start_button.image, (g.start_button.rect.x, g.start_button.rect.y))
                g.start_button.draw()

    class CardChoosing(State):
        def __init__(self, game):
            State.__init__(self, game)
            self.name = 'CardChoosing'
            g.card_chooser()  # chooses a card randomly

        def update(self, delta_time, actions):
            self.guesses = []
            for button in g.buttons:
                if button.clicked == True:
                    button.clicked = False  # fixes a weird problem near the end of the game, where cards are chosen automatically
                    self.guesses.append(button.number)
                    if button.number == g.sarake:
                        new_state = Correct(self.game)
                        new_state.enter_state()
                    if button.number < g.sarake:
                        new_state = Larger(self.game)
                        new_state.enter_state()
                    if button.number > g.sarake:
                        new_state = Smaller(self.game)
                        new_state.enter_state()

        def render(self, display):
            # draws a poker table colored rect
            pygame.draw.rect(display, (51, 102, 77), pygame.Rect((0, 0), (g.screen.get_width(), g.screen.get_height())))

            # screen measurements
            WIDTHX = g.screen.get_width()
            HEIGHTY = g.screen.get_height()


            self.game.draw_text(display, 'Choose a card!', (255, 255, 255), g.screen.get_width() / 2,
                                g.screen.get_height() / 2)
            g.font = pygame.font.SysFont('comicsans', 30)
            self.game.draw_text(display, 'Wrong guesses: {}'.format(g.wrong_count), (255, 255, 255), g.screen.get_width() / 6,
                                g.screen.get_height() / 1.5)
            self.game.draw_text(display, 'Player: {}'.format(g.players[1]), (255, 255, 255), g.screen.get_width() / 6,
                                g.screen.get_height() / 1.8)
            self.game.draw_text(display, 'Dealer: {}'.format(g.dealers[0]), (255, 255, 255), g.screen.get_width() / 6,
                                g.screen.get_height() / 2)
            g.font = pygame.font.SysFont('comicsans', 50)
            x_coords = [(WIDTHX - 13 * (g.cards_width + 18)) / 2]  # 13 * (card width + 10) = 1040
            for i in range(0, 12):
                x_coords.append(x_coords[i] + 110)

            # dictionary which holds every cards indetifier number and x-coordinate
            list_coords = list(np.array(
                [4 * [x_coords[0]], 4 * [x_coords[1]], 4 * [x_coords[2]], 4 * [x_coords[3]], 4 * [x_coords[4]],
                 4 * [x_coords[5]], 4 * [x_coords[6]], 4 * [x_coords[7]], 4 * [x_coords[8]], 4 * [x_coords[9]],
                 4 * [x_coords[10]], 4 * [x_coords[11]], 4 * [x_coords[12]]]).flatten())

            dictX = {}
            for i, j in zip(g.cards_available_copy, list_coords):
                dictX[i] = j
            # make y_coords
            y_coords = [HEIGHTY / 10]
            for i in range(0, 3):
                y_coords.append(y_coords[i] + 35)

            # find out quantities of different card numbers played
            quanlist = np.array(g.card_interpreter())
            card_quantities = []
            uniques = np.array(list(set(quanlist)))

            for i in range(0, len(quanlist)):
                uniques_coord = uniques[np.where(uniques == quanlist[i])]
                card_quantities.append(quanlist[0:i + 1].tolist().count(uniques_coord))

            # draws cards to right coordinates
            if len(g.cards_played) > 1:
                for i, j in zip(g.cards_played[0:len(g.cards_played) - 1], card_quantities):

                    if j == 1:
                        y = y_coords[0]
                    if j == 2:
                        y = y_coords[1]
                    if j == 3:
                        y = y_coords[2]
                    if j == 4:
                        y = y_coords[3]
                    display.blit(g.CARDS[g.dict1[i]], (dictX[i], y))

            for button in g.buttons:
                if g.realized_cards[button.number] < 4:
                    display.blit(button.image, (button.rect.x, button.rect.y))
                    button.draw()

    class CardChoosing2(State):
        def __init__(self, game):
            State.__init__(self, game)
            self.name = 'CardChoosing2'
            self.prev_state = self.game.state_stack[-1]

        def update(self, delta_time, actions):
            for button in g.buttons:
                if button.clicked == True:
                    button.clicked = False  # fixes a weird problem near the end of the game, where cards are chosen automatically
                    if button.number == g.sarake:
                        new_state = Correct(self.game)
                        new_state.enter_state()
                    if button.number != g.sarake:
                        new_state = Wrong(self.game)
                        new_state.enter_state()


        def render(self, display):
            # draws a poker table colored rect
            pygame.draw.rect(display, (51, 102, 77), pygame.Rect((0, 0), (g.screen.get_width(), g.screen.get_height())))

            # screen measurements
            WIDTHX = g.screen.get_width()
            HEIGHTY = g.screen.get_height()


            self.game.draw_text(display, 'Choose a card!', (255, 255, 255), g.screen.get_width() / 2,
                                g.screen.get_height() / 2)
            g.font = pygame.font.SysFont('comicsans', 30)
            self.game.draw_text(display, 'Wrong guesses: {}'.format(g.wrong_count), (255, 255, 255), g.screen.get_width() / 6,
                                g.screen.get_height() / 1.5)
            self.game.draw_text(display, 'Players: {}'.format(g.players[1]), (255, 255, 255), g.screen.get_width() / 6,
                                g.screen.get_height() / 1.8)
            self.game.draw_text(display, 'Dealer: {}'.format(g.dealers[0]), (255, 255, 255), g.screen.get_width() / 6,
                                g.screen.get_height() / 2)
            g.font = pygame.font.SysFont('comicsans', 50)
            x_coords = [(WIDTHX - 13 * (g.cards_width + 18)) / 2]  # 13 * (card width + 10) = 1040
            for i in range(0, 12):
                x_coords.append(x_coords[i] + 110)

            # dictionary which holds every cards indetifier number and x-coordinate
            list_coords = list(np.array(
                [4 * [x_coords[0]], 4 * [x_coords[1]], 4 * [x_coords[2]], 4 * [x_coords[3]], 4 * [x_coords[4]],
                 4 * [x_coords[5]], 4 * [x_coords[6]], 4 * [x_coords[7]], 4 * [x_coords[8]], 4 * [x_coords[9]],
                 4 * [x_coords[10]], 4 * [x_coords[11]], 4 * [x_coords[12]]]).flatten())

            dictX = {}
            for i, j in zip(g.cards_available_copy, list_coords):
                dictX[i] = j
            # make y_coords
            y_coords = [HEIGHTY / 10]
            for i in range(0, 3):
                y_coords.append(y_coords[i] + 35)

            quanlist = np.array(g.card_interpreter())
            card_quantities = []
            uniques = np.array(list(set(quanlist)))

            for i in range(0, len(quanlist)):
                uniques_coord = uniques[np.where(uniques == quanlist[i])]
                card_quantities.append(quanlist[0:i + 1].tolist().count(uniques_coord))

            # draws cards to right coordinates
            if len(g.cards_played) > 1:
                for i, j in zip(g.cards_played[0:len(g.cards_played) - 1], card_quantities):

                    if j == 1:
                        y = y_coords[0]
                    if j == 2:
                        y = y_coords[1]
                    if j == 3:
                        y = y_coords[2]
                    if j == 4:
                        y = y_coords[3]
                    display.blit(g.CARDS[g.dict1[i]], (dictX[i], y))

            if self.prev_state.name == 'Smaller':
                for button in g.buttons:
                    if g.realized_cards[button.number] < 4:
                        if button.number < self.prev_state.prev_state.guesses[-1]:
                            display.blit(button.image, (button.rect.x, button.rect.y))
                            button.draw()

            if self.prev_state.name == 'Larger':
                for button in g.buttons:
                    if g.realized_cards[button.number] < 4:
                        if button.number > self.prev_state.prev_state.guesses[-1]:
                            display.blit(button.image, (button.rect.x, button.rect.y))
                            button.draw()

    class Smaller(State):
        def __init__(self, game):
            self.game = game
            State.__init__(self, game)
            self.name = 'Smaller'
            self.prev_state = self.game.state_stack[-1]

        def update(self, delta_time, actions):
            if actions['start']:
                new_state = CardChoosing2(self.game)
                new_state.enter_state()
            self.game.reset_keys()

        def render(self, display):
            self.prev_state.render(display)
            pygame.draw.rect(display, (51, 102, 77), pygame.Rect((0, 0), (g.screen.get_width(), g.screen.get_height())))
            if self.prev_state.name == 'CardChoosing':
                self.game.draw_text(display, 'Smaller!', (255, 255, 255), g.screen.get_width() / 2,
                                    g.screen.get_height() / 2)
                self.game.draw_text(display, 'Press ENTER to continue!', (0, 0, 0), g.screen.get_width() / 2,
                                    g.screen.get_height() / 1.5)

    class Larger(State):
        def __init__(self, game):
            self.game = game
            State.__init__(self, game)
            self.name = 'Larger'
            self.prev_state = self.game.state_stack[-1]

        def update(self, delta_time, actions):
            if actions['start']:
                new_state = CardChoosing2(self.game)
                new_state.enter_state()
            self.game.reset_keys()

        def render(self, display):
            self.prev_state.render(display)
            pygame.draw.rect(display, (51, 102, 77), pygame.Rect((0, 0), (g.screen.get_width(), g.screen.get_height())))
            if self.prev_state.name == 'CardChoosing':
                self.game.draw_text(display, 'Larger!', (0, 0, 0), g.screen.get_width() / 2,
                                    g.screen.get_height() / 2)
                self.game.draw_text(display, 'Press ENTER to continue!', (0, 0, 0), g.screen.get_width() / 2,
                                    g.screen.get_height() / 1.5)

    class Correct(State):
        def __init__(self, game):
            self.game = game
            State.__init__(self, game)
            self.name = 'Correct'
            g.remaining_cards()
            g.reset_wrong_count()

        def update(self, delta_time, actions):
            if actions['start']:
                g.players.append(g.players[0])
                g.players = g.players[1:]
                if g.players[1] == g.dealers[0]:
                    g.players.append(g.players[0])
                    g.players = g.players[1:]

                print(g.players)
                print(g.dealers)
                g.round.append(1)
                if len(g.round) < 52:
                    new_state = CardChoosing(self.game)
                    new_state.enter_state()
                    print(actions['start'])
                else:
                    new_state = endGame(self.game)
                    new_state.enter_state()

            self.game.reset_keys()

        def render(self, display):
            self.prev_state.render(display)
            pygame.draw.rect(display, (51, 102, 77), pygame.Rect((0, 0), (g.screen.get_width(), g.screen.get_height())))
            if self.prev_state.name == 'CardChoosing':
                self.game.draw_text(display, 'Correct!', (0, 0, 0), g.screen.get_width() / 2, g.screen.get_height() / 2)
                self.game.draw_text(display, 'Press ENTER to continue!', (0, 0, 0), g.screen.get_width() / 2,
                                    g.screen.get_height() / 1.5)
                # draw the card on the upper screen
                display.blit(g.CARDS[g.dict1[g.card]],
                             ((g.screen.get_width() - g.cards_width) / 2, g.screen.get_height() / 6))
            if self.prev_state.name == 'CardChoosing2':
                self.game.draw_text(display, 'Correct!', (0, 0, 0), g.screen.get_width() / 2, g.screen.get_height() / 2)
                self.game.draw_text(display, 'Press ENTER to continue!', (0, 0, 0), g.screen.get_width() / 2,
                                    g.screen.get_height() / 1.5)
                # draw the card on the upper screen
                display.blit(g.CARDS[g.dict1[g.card]],
                             ((g.screen.get_width() - g.cards_width) / 2, g.screen.get_height() / 6))

    class Wrong(State):
        def __init__(self, game):
            self.game = game
            State.__init__(self, game)
            self.name = 'Wrong'
            g.remaining_cards()
            g.turnCalc(1)

        def update(self, delta_time, actions):
            if actions['start']:
                g.players.append(g.players[0])
                g.players = g.players[1:]
                if g.players[1] == g.dealers[0]:
                    g.players.append(g.players[0])
                    g.players = g.players[1:]

                print(g.players)
                print(g.dealers)
                g.round.append(1)
                if len(g.round) < 52:
                    new_state = CardChoosing(self.game)
                    new_state.enter_state()
                    print(actions['start'])
                else:
                    new_state = endGame(self.game)
                    new_state.enter_state()
                if g.wrong_count == 3:
                    g.reset_wrong_count()
            self.game.reset_keys()

        def render(self, display):
            self.prev_state.render(display)
            pygame.draw.rect(display, (51, 102, 77), pygame.Rect((0, 0), (g.screen.get_width(), g.screen.get_height())))
            if self.prev_state.name == 'CardChoosing2':
                if g.wrong_count == 3:
                    self.game.draw_text(display, 'Wrong! The dealer changes!', (0, 0, 0), g.screen.get_width() / 2,
                                        g.screen.get_height() / 2)

                    self.game.draw_text(display, 'Press ENTER to continue!', (0, 0, 0), g.screen.get_width() / 2,
                                        g.screen.get_height() / 1.5)
                else:
                    self.game.draw_text(display, 'Wrong!', (0, 0, 0), g.screen.get_width() / 2,
                                        g.screen.get_height() / 2)
                    self.game.draw_text(display, 'Press ENTER to continue!', (0, 0, 0), g.screen.get_width() / 2,
                                        g.screen.get_height() / 1.5)
                # draw the card on the upper screen
                display.blit(g.CARDS[g.dict1[g.card]],
                             ((g.screen.get_width() - g.cards_width) / 2, g.screen.get_height() / 6))

    class Game():
        def __init__(self):
            pygame.init()
            # self.GAME_W, self.GAME_H = 480, 270
            self.GAME_W, self.GAME_H = 1530, 750
            self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 1530, 750
            self.game_canvas = pygame.Surface((self.GAME_W, self.GAME_H))
            self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.RESIZABLE)

            self.cards_width = 100 * 0.9
            self.cards_height = 140 * 0.9
            # creating buttons
            self.buttons_width = 100 * 0.9
            self.buttons_height = 140 * 0.9

            self.button_x_coords = [
                (self.screen.get_width() - 13 * (self.cards_width + 18)) / 2]  # 13 * (card width + 10) = 1040
            self.running, self.playing = True, True
            self.actions = {'left': False, 'right': False, 'up': False, 'down': False, 'aloita_peli': False,
                            'action2': False, 'start': False}
            self.dt, self.prev_time = 0, 0
            self.state_stack = []

            self.suits = ['hearts', 'diamonds', 'spades', 'clubs']
            self.card_names = ['ace', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'jack', 'queen', 'king']
            self.CARDS = {}
            self.btn_names = ['ace', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'jack',
                              'queen', 'king']
            self.BUTTONS = {}
            self.load_assets()
            self.load_states()
            self.x_coords_calc()
            self.button_y = 140
            self.ace_button = Button(self.button_x_coords[0], self.screen.get_height() - self.button_y,
                                     self.BUTTONS['ace'], 1)
            self.two_button = Button(self.button_x_coords[1], self.screen.get_height() - self.button_y,
                                     self.BUTTONS['two'], 2)
            self.three_button = Button(self.button_x_coords[2], self.screen.get_height() - self.button_y,
                                       self.BUTTONS['three'], 3)
            self.four_button = Button(self.button_x_coords[3], self.screen.get_height() - self.button_y,
                                      self.BUTTONS['four'], 4)
            self.five_button = Button(self.button_x_coords[4], self.screen.get_height() - self.button_y,
                                      self.BUTTONS['five'], 5)
            self.six_button = Button(self.button_x_coords[5], self.screen.get_height() - self.button_y,
                                     self.BUTTONS['six'], 6)
            self.seven_button = Button(self.button_x_coords[6], self.screen.get_height() - self.button_y,
                                       self.BUTTONS['seven'], 7)
            self.eight_button = Button(self.button_x_coords[7], self.screen.get_height() - self.button_y,
                                       self.BUTTONS['eight'], 8)
            self.nine_button = Button(self.button_x_coords[8], self.screen.get_height() - self.button_y,
                                      self.BUTTONS['nine'], 9)
            self.ten_button = Button(self.button_x_coords[9], self.screen.get_height() - self.button_y,
                                     self.BUTTONS['ten'], 10)
            self.jack_button = Button(self.button_x_coords[10], self.screen.get_height() - self.button_y,
                                      self.BUTTONS['jack'], 11)
            self.queen_button = Button(self.button_x_coords[11], self.screen.get_height() - self.button_y,
                                       self.BUTTONS['queen'], 12)
            self.king_button = Button(self.button_x_coords[12], self.screen.get_height() - self.button_y,
                                      self.BUTTONS['king'], 13)

            self.buttons = [self.ace_button, self.two_button, self.three_button, self.four_button, self.five_button,
                            self.six_button, self.seven_button, self.eight_button, self.nine_button, self.ten_button,
                            self.jack_button, self.queen_button, self.king_button]

            self.start_button_image = pygame.transform.smoothscale(
                pygame.image.load(os.path.join('peli_painikkeet', 'aloita_peli.png')), (277 * 0.7, 117 * 0.7))
            self.start_button = Button(self.screen.get_width() - 277 * 0.7 - 20, self.screen.get_height() / 2,
                                         self.start_button_image, 14)

            # each card has a unique indetifier from 0 to 51
            self.cards_available = [*range(0, 52)]
            self.one = [*range(0, 52, 13)]
            self.two = [*range(1, 52, 13)]
            self.three = [*range(2, 52, 13)]
            self.four = [*range(3, 52, 13)]
            self.five = [*range(4, 52, 13)]
            self.six = [*range(5, 52, 13)]
            self.seven = [*range(6, 52, 13)]
            self.eight = [*range(7, 52, 13)]
            self.nine = [*range(8, 52, 13)]
            self.ten = [*range(9, 52, 13)]
            self.eleven = [*range(10, 52, 13)]
            self.twelve = [*range(11, 52, 13)]
            self.thirteen = [*range(12, 52, 13)]
            self.cards_available_copy = list(np.array(
                [self.one, self.two, self.three, self.four, self.five, self.six, self.seven, self.eight,
                 self.nine, self.ten, self.eleven, self.twelve, self.thirteen]).flatten())
            self.cards_available = np.transpose(np.array(
                [self.one, self.two, self.three, self.four, self.five, self.six, self.seven, self.eight,
                 self.nine, self.ten, self.eleven, self.twelve, self.thirteen]))
            self.cards_available = pd.DataFrame(self.cards_available, columns=range(1, 14))
            self.card_interpreter_data = self.cards_available

            self.players = []
            self.outcomes = [0, 0, 0]
            self.wrong_count = 0

            # pelaajien syöttäminen
            self.user_text = 'Type a player name'

            self.players_typed = False
            self.players = []
            self.dealers = 0
            self.round = []

            self.cards_played = []

            self.listing_cards()
            self.remaining_cards()
            print(pygame.font.get_fonts())

        def game_loop(self):
            while self.playing:
                self.get_dt()
                self.get_events()
                self.update()
                self.render()

        def get_events(self):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.playing = False
                    self.running = False
                if event.type == VIDEORESIZE:
                    pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.playing = False
                        self.running = False

                    if event.key == pygame.K_RETURN:
                        self.actions['start'] = True
                        if self.state_stack[-1] == self.title_screen:
                            self.players.append(self.user_text)
                            self.user_text = 'Type a player name'
                            print(self.players)
                            print(self.state_stack[-1])

                    if event.key == pygame.K_BACKSPACE:
                        self.user_text = self.user_text[:-1]
                    else:
                        if event.key != pygame.K_RETURN:
                            self.user_text += event.unicode

                if event.type == pygame.KEYUP:

                    if event.key == pygame.K_RETURN:
                        self.actions['start'] = False

        def update(self):
            self.state_stack[-1].update(self.dt, self.actions)

        def render(self):
            self.state_stack[-1].render(self.game_canvas)
            self.screen.blit(
                pygame.transform.scale(self.game_canvas, (self.screen.get_width(), self.screen.get_height())), (0, 0))
            pygame.display.flip()

        def get_dt(self):
            now = time.time()
            self.dt = now - self.prev_time
            self.prev_time = now

        def draw_text(self, surface, text, color, x, y):
            text_surface = self.font.render(text, True, color)
            text_rect = text_surface.get_rect()
            text_rect.center = (x, y)
            surface.blit(text_surface, text_rect)

        def load_assets(self):

            for card_name in self.card_names:
                for suit in self.suits:
                    self.CARDS['{}_of_{}'.format(card_name, suit)] = pygame.transform.smoothscale(
                        pygame.image.load(os.path.join('PNG-cards-1.3', '{}_of_{}.png'.format(card_name, suit))),
                        (self.cards_width, self.cards_height))

            for btn_name in self.btn_names:
                self.BUTTONS[btn_name] = pygame.transform.smoothscale(
                    pygame.image.load(os.path.join('PNG-numbers', '{}.png'.format(btn_name))),
                    (self.buttons_width, self.buttons_height))

            self.font = pygame.font.SysFont('malgungothic', 90)

        def load_states(self):
            self.title_screen = TitleScreen(self)
            self.state_stack.append(self.title_screen)

        def reset_keys(self):
            for action in self.actions:
                self.actions[action] = False

        def x_coords_calc(self):
            for i in range(0, 12):
                self.button_x_coords.append(self.button_x_coords[i] + 110)

        def listing_cards(self):

            # list with card names
            lista2 = []
            for card_name in self.card_names:
                for suit in self.suits:
                    lista2.append('{}_of_{}'.format(card_name, suit))
            # print(lista2)

            # dictionary with card name and identifier number
            self.dict1 = {}

            for i, j in zip(self.cards_available_copy, lista2):
                self.dict1[i] = j

        def card_interpreter(self):
            if type(self.cards_played) == list:
                cards = []
                for i in self.cards_played:
                    check = self.card_interpreter_data[self.card_interpreter_data.isin([i])].stack().index.to_list()
                    jep = [item for t in check for item in t][1]
                    cards.append(jep)
                return cards
            else:
                check = self.card_interpreter_data[self.card_interpreter_data.isin([self.cards_played])].stack().index.to_list()
                jep = [item for t in check for item in t][1]
                return jep

        def card_chooser(self):

            # choosing a random card
            self.card = random.choice(self.cards_available.values[self.cards_available.values < 9999])
            # finding the card by indentifier number
            self.sarake = self.cards_available.columns[np.where(self.cards_available == self.card)[1]][0]
            self.cards_available = self.cards_available.replace(self.card, 9999)
            self.cards_played.append(self.card)

        def remaining_cards(self):
            self.realized_cards = self.card_interpreter()
            self.realized_cards = Counter(self.realized_cards)

        def turnCalc(self, x):
            self.outcomes.append(x)

            if sum(self.outcomes[-3:]) < 3:
                self.wrong_count = sum(self.outcomes[-3:])

            if sum(self.outcomes[-3:]) == 3:
                self.wrong_count = sum(self.outcomes[-3:])
                self.dealers.append(self.dealers[0])
                self.dealers = self.dealers[1:]

        def players_rand(self):
            random.shuffle(self.players)
            self.dealers = self.players.copy()

        def reset_wrong_count(self):
            self.outcomes.append(0);
            self.outcomes.append(0);
            self.outcomes.append(0)
            self.wrong_count = 0

        # def pelaajien_syottaminen(self):
        #     pygame.draw.rect(display, (68, 85, 90), pygame.Rect((800, 800), (120, 500)))

    # if __name__ == '__FTD_state_engine__:
    g = Game()
    while g.running:
        g.game_loop()

main()






