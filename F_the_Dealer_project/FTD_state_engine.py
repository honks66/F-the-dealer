''' TimeStamp 27.07.2022 '''


import os, time
import pygame
import pygame.mouse
import pygame.time
from pygame.locals import *
import random
import numpy as np
import pandas as pd


''' Määritetään luokka Button '''

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
                print('CLICKED')
                print('Klikattiin: ', self.number)
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False





        # draw button on screen
        # g.screen.blit(self.image, (self.rect.x, self.rect.y))

        return action



class State():
    def __init__(self, game):
        self.game = game
        self.prev_state = None

    def update(self, delta_time, actions):
        pass

    def render(self, surface):
        pass

    def enter_state(self):
        if len(self.game.state_stack) > 1:
            self.prev_state = self.game.state_stack[-1]
        self.game.state_stack.append(self)

    def exit_state(self):
        self.game.state_stack.pop()




class TitleScreen(State):
    def __init__(self, game):
        State.__init__(self, game)


    def update(self, delta_time, actions):
        if actions['start']:
            new_state = KortinValinta(self.game)
            new_state.enter_state()
        self.game.reset_keys()

    def render(self, display):
        display.fill((255,255,255))
        self.game.draw_text(display, 'Tervetuloa Fuck the Dealeriin', (0,0,0), g.screen.get_width()/2, g.screen.get_height()/2)


class KortinValinta(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.name = 'KortinValinta'
        g.kortin_valinta() # valitsee kortin randomilla

    def update(self, delta_time, actions):
        self.arvaukset = []
        for button in g.buttons:
            if button.clicked == True:
                self.arvaukset.append(button.number)
                if button.number == g.sarake:
                    new_state = Oikein(self.game)
                    new_state.enter_state()
                if button.number < g.sarake:
                    new_state = Suurempi(self.game)
                    new_state.enter_state()
                if button.number > g.sarake:
                    new_state = Pienempi(self.game)
                    new_state.enter_state()
                # self.player.update(delta_time, actions)

    def render(self, display):
        # piirrä pokerin värinen rect
        pygame.draw.rect(display, (51, 102, 77), pygame.Rect((0, 0), (g.screen.get_width(), g.screen.get_height())))
        # piirrä kortit
        # screenin mitat
        WIDTHX = g.screen.get_width()
        HEIGHTY = g.screen.get_height()
        self.game.draw_text(display, 'Valitse kortti!', (255, 255, 255), g.screen.get_width() / 2, g.screen.get_height() / 2)
        x_coords = [(WIDTHX - 1040) / 2]  # 13 * (kortin leveys + 10) = 1040
        for i in range(0, 12):
            x_coords.append(x_coords[i] + 80)

        # tehdään dictionary, missä on jokaisen kortin järjestysluku sekä x-koordinaatti
        lista_koordinaatit = list(np.array(
            [4 * [x_coords[0]], 4 * [x_coords[1]], 4 * [x_coords[2]], 4 * [x_coords[3]], 4 * [x_coords[4]],
             4 * [x_coords[5]], 4 * [x_coords[6]], 4 * [x_coords[7]], 4 * [x_coords[8]], 4 * [x_coords[9]],
             4 * [x_coords[10]], 4 * [x_coords[11]], 4 * [x_coords[12]]]).flatten())

        dictX = {}
        for i, j in zip(g.vapaat_kortit_copy, lista_koordinaatit):
            dictX[i] = j
        # make y_coords
        y_coords = [HEIGHTY / 10]
        for i in range(0, 3):
            y_coords.append(y_coords[i] + 35)

        # määritä oikealle kortille oikea koordinaatti
        # jokulista = np.array(g.kortti_tulkki(g.kortit, g.korttitulkki_df))
        jokulista = np.array(g.kortti_tulkki())
        korttien_maarat = []
        uniques = np.array(list(set(jokulista)))

        for i in range(0, len(jokulista)):
            homo = uniques[np.where(uniques == jokulista[i])]
            korttien_maarat.append(jokulista[0:i + 1].tolist().count(homo))

        # piirtää kortit oikeisiin koordinaatteihin
        if len(g.kortit) > 1:
            for i, j in zip(g.kortit[0:len(g.kortit)-1], korttien_maarat):

                if j == 1:
                    y = y_coords[0]
                if j == 2:
                    y = y_coords[1]
                if j == 3:
                    y = y_coords[2]
                if j == 4:
                    y = y_coords[3]
                display.blit(g.KORTIT[g.dict1[i]], (dictX[i], y))


        for button in g.buttons:
            display.blit(button.image, (button.rect.x, button.rect.y))
            button.draw()



class KortinValinta2(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.name = 'KortinValinta2'
        self.prev_state = self.game.state_stack[-1]

    def update(self, delta_time, actions):
        for button in g.buttons:
            if button.clicked == True:
                if button.number == g.sarake:
                    new_state = Oikein(self.game)
                    new_state.enter_state()
                if button.number != g.sarake:
                    new_state = Vaarin(self.game)
                    new_state.enter_state()

                # self.player.update(delta_time, actions)

    def render(self, display):
        # piirrä pokerin värinen rect
        pygame.draw.rect(display, (51, 102, 77), pygame.Rect((0, 0), (g.screen.get_width(), g.screen.get_height())))
        # piirrä kortit
        # screenin mitat
        WIDTHX = g.screen.get_width()
        HEIGHTY = g.screen.get_height()
        self.game.draw_text(display, 'Valitse kortti!', (255, 255, 255), g.screen.get_width() / 2, g.screen.get_height() / 2)
        x_coords = [(WIDTHX - 1040) / 2]  # 13 * (kortin leveys + 10) = 1040
        for i in range(0, 12):
            x_coords.append(x_coords[i] + 80)

        # tehdään dictionary, missä on jokaisen kortin järjestysluku sekä x-koordinaatti
        lista_koordinaatit = list(np.array(
            [4 * [x_coords[0]], 4 * [x_coords[1]], 4 * [x_coords[2]], 4 * [x_coords[3]], 4 * [x_coords[4]],
             4 * [x_coords[5]], 4 * [x_coords[6]], 4 * [x_coords[7]], 4 * [x_coords[8]], 4 * [x_coords[9]],
             4 * [x_coords[10]], 4 * [x_coords[11]], 4 * [x_coords[12]]]).flatten())

        dictX = {}
        for i, j in zip(g.vapaat_kortit_copy, lista_koordinaatit):
            dictX[i] = j
        # make y_coords
        y_coords = [HEIGHTY / 10]
        for i in range(0, 3):
            y_coords.append(y_coords[i] + 35)

        # määritä oikealle kortille oikea koordinaatti
        # jokulista = np.array(g.kortti_tulkki(g.kortit, g.korttitulkki_df))
        jokulista = np.array(g.kortti_tulkki())
        korttien_maarat = []
        uniques = np.array(list(set(jokulista)))

        for i in range(0, len(jokulista)):
            homo = uniques[np.where(uniques == jokulista[i])]
            korttien_maarat.append(jokulista[0:i + 1].tolist().count(homo))

        # piirtää kortit oikeisiin koordinaatteihin
        if len(g.kortit) > 1:
            for i, j in zip(g.kortit[0:len(g.kortit)-1], korttien_maarat):

                if j == 1:
                    y = y_coords[0]
                if j == 2:
                    y = y_coords[1]
                if j == 3:
                    y = y_coords[2]
                if j == 4:
                    y = y_coords[3]
                display.blit(g.KORTIT[g.dict1[i]], (dictX[i], y))

        if self.prev_state.name == 'Pienempi':
            for button in g.buttons:
                if button.number < self.prev_state.prev_state.arvaukset[-1]:
                    display.blit(button.image, (button.rect.x, button.rect.y))
                    button.draw()


        if self.prev_state.name == 'Suurempi':
            for button in g.buttons:
                if button.number > self.prev_state.prev_state.arvaukset[-1]:
                    print('Suurempi')
                    display.blit(button.image, (button.rect.x, button.rect.y))
                    button.draw()






class Pienempi(State):
    def __init__(self, game):
        self.game = game
        State.__init__(self, game)
        self.name = 'Pienempi'
        self.prev_state = self.game.state_stack[-1]
        # self.tulosteksti()

    def update(self, delta_time, actions):
        if actions['start']:
            new_state = KortinValinta2(self.game)
            new_state.enter_state()
            print('Entry onnistui!')
        self.game.reset_keys()

    def render(self, display):
        self.prev_state.render(display)
        pygame.draw.rect(display, (51, 102, 77), pygame.Rect((0, 0), (g.screen.get_width(), g.screen.get_height())))
        if self.prev_state.name == 'KortinValinta':
            self.game.draw_text(display, 'Pienempi!', (255, 255, 255), g.screen.get_width() / 2, g.screen.get_height() / 2)
            self.game.draw_text(display, 'Paina ENTER jatkaaksesi!', (0, 0, 0), g.screen.get_width() / 2, g.screen.get_height() / 1.5)


class Suurempi(State):
    def __init__(self, game):
        self.game = game
        State.__init__(self, game)
        self.name = 'Suurempi'
        self.prev_state = self.game.state_stack[-1]
        # self.tulosteksti()

    def update(self, delta_time, actions):
        if actions['start']:
            new_state = KortinValinta2(self.game)
            new_state.enter_state()
            print('Entry onnistui!')
        self.game.reset_keys()

    def render(self, display):
        self.prev_state.render(display)
        pygame.draw.rect(display, (51, 102, 77), pygame.Rect((0, 0), (g.screen.get_width(), g.screen.get_height())))
        if self.prev_state.name == 'KortinValinta':
            self.game.draw_text(display, 'Suurempi!', (0, 0, 0), g.screen.get_width() / 2, g.screen.get_height() / 2)
            self.game.draw_text(display, 'Paina ENTER jatkaaksesi!', (0, 0, 0), g.screen.get_width() / 2,
                                g.screen.get_height() / 1.5)


class Oikein(State):
    def __init__(self, game):
        self.game = game
        State.__init__(self, game)
        self.name = 'Oikein'
        # self.tulosteksti()



    def update(self, delta_time, actions):
        if actions['start']:
            new_state = KortinValinta(self.game)
            new_state.enter_state()
            print('Entry onnistui!')
        self.game.reset_keys()

    def render(self, display):
        self.prev_state.render(display)
        pygame.draw.rect(display, (51, 102, 77), pygame.Rect((0, 0), (g.screen.get_width(), g.screen.get_height())))
        if self.prev_state.name == 'KortinValinta':
            self.game.draw_text(display, 'Oikein!', (0,0,0), g.screen.get_width()/2, g.screen.get_height()/2)
            self.game.draw_text(display, 'Paina ENTER jatkaaksesi!', (0, 0, 0), g.screen.get_width() / 2, g.screen.get_height() / 1.5)
        if self.prev_state.name == 'KortinValinta2':
            self.game.draw_text(display, 'Oikein!', (0, 0, 0), g.screen.get_width() / 2, g.screen.get_height() / 2)
            self.game.draw_text(display, 'Paina ENTER jatkaaksesi!', (0, 0, 0), g.screen.get_width() / 2, g.screen.get_height() / 1.5)

            # pygame.time.delay(2000)

        # display.blit(self.menu_img, self.menu_rect)

    # def tulosteksti(self):
    #     if self.prev_state.name == 'KortinValinta':
    #         font = pygame.font.SysFont('comicsans', 60)
    #         draw_text = font.render('Oikein', 1, (0, 0, 0))
    #         g.screen.blit(draw_text, (g.screen.get_width() / 2 - draw_text.get_width() / 2, g.screen.get_height() / 1.5 - draw_text.get_height() / 1.5))


class Vaarin(State):
    def __init__(self, game):
        self.game = game
        State.__init__(self, game)
        self.name = 'Väärin'

    def update(self, delta_time, actions):
        if actions['start']:
            new_state = KortinValinta(self.game)
            new_state.enter_state()
            print('Entry onnistui!')
        self.game.reset_keys()

    def render(self, display):
        self.prev_state.render(display)
        pygame.draw.rect(display, (51, 102, 77), pygame.Rect((0, 0), (g.screen.get_width(), g.screen.get_height())))
        if self.prev_state.name == 'KortinValinta2':
            self.game.draw_text(display, 'Väärin!', (0, 0, 0), g.screen.get_width() / 2, g.screen.get_height() / 2)
            self.game.draw_text(display, 'Paina ENTER jatkaaksesi!', (0, 0, 0), g.screen.get_width() / 2, g.screen.get_height() / 1.5)






class Game():
   def __init__(self):
       pygame.init()
       # self.GAME_W, self.GAME_H = 480, 270
       self.GAME_W, self.GAME_H = 1530, 750
       self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 1530, 750
       self.game_canvas = pygame.Surface((self.GAME_W, self.GAME_H))
       self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.RESIZABLE)

       self.kortit_width = 100*0.9
       self.kortit_height = 140*0.9

       self.buttonit_width = 100*0.9
       self.buttonit_height = 140*0.9

       self.button_x_coords = [(self.screen.get_width() - 13*(self.kortit_width+18))/ 2]  # 13 * (kortin leveys + 10) = 1040
       self.running, self.playing = True, True
       self.actions = {'left':False, 'right':False, 'up':False, 'down':False, 'action1':False, 'action2':False, 'start':False}
       self.dt, self.prev_time = 0, 0
       self.state_stack = []

       self.maat = ['hearts', 'diamonds', 'spades', 'clubs']
       self.numerot = ['ace', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'jack', 'queen', 'king']
       self.KORTIT = {}
       self.btn_nimet = ['ace', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'jack', 'queen','king']
       self.BUTTONIT = {}
       self.load_assets()
       self.load_states()
       self.x_coords_calc()
       self.button_y = 140
       self.ace_button = Button(self.button_x_coords[0], self.screen.get_height() - self.button_y, self.BUTTONIT['ace'], 1)
       self.two_button = Button(self.button_x_coords[1], self.screen.get_height() - self.button_y, self.BUTTONIT['two'], 2)
       self.three_button = Button(self.button_x_coords[2], self.screen.get_height() - self.button_y, self.BUTTONIT['three'], 3)
       self.four_button = Button(self.button_x_coords[3], self.screen.get_height() - self.button_y, self.BUTTONIT['four'], 4)
       self.five_button = Button(self.button_x_coords[4], self.screen.get_height() - self.button_y, self.BUTTONIT['five'], 5)
       self.six_button = Button(self.button_x_coords[5], self.screen.get_height() - self.button_y, self.BUTTONIT['six'], 6)
       self.seven_button = Button(self.button_x_coords[6], self.screen.get_height() - self.button_y, self.BUTTONIT['seven'], 7)
       self.eight_button = Button(self.button_x_coords[7], self.screen.get_height() - self.button_y, self.BUTTONIT['eight'], 8)
       self.nine_button = Button(self.button_x_coords[8], self.screen.get_height() - self.button_y, self.BUTTONIT['nine'], 9)
       self.ten_button = Button(self.button_x_coords[9], self.screen.get_height() - self.button_y, self.BUTTONIT['ten'], 10)
       self.jack_button = Button(self.button_x_coords[10], self.screen.get_height() - self.button_y, self.BUTTONIT['jack'], 11)
       self.queen_button = Button(self.button_x_coords[11], self.screen.get_height() - self.button_y, self.BUTTONIT['queen'], 12)
       self.king_button = Button(self.button_x_coords[12], self.screen.get_height() - self.button_y, self.BUTTONIT['king'], 13)

       self.buttons = [self.ace_button, self.two_button, self.three_button, self.four_button, self.five_button, self.six_button, self.seven_button, self.eight_button, self.nine_button, self.ten_button, self.jack_button, self.queen_button, self.king_button]

       # korttien järjestyslukujen luominen
       self.vapaat_kortit = [*range(0, 52)]
       self.yksi = [*range(0, 52, 13)]
       self.kaksi = [*range(1, 52, 13)]
       self.kolme = [*range(2, 52, 13)]
       self.nelja = [*range(3, 52, 13)]
       self.viisi = [*range(4, 52, 13)]
       self.kuusi = [*range(5, 52, 13)]
       self.seitseman = [*range(6, 52, 13)]
       self.kahdeksan = [*range(7, 52, 13)]
       self.yhdeksan = [*range(8, 52, 13)]
       self.kymmenen = [*range(9, 52, 13)]
       self.yksitoista = [*range(10, 52, 13)]
       self.kaksitoista = [*range(11, 52, 13)]
       self.kolmetoista = [*range(12, 52, 13)]
       self.vapaat_kortit_copy = list(np.array([self.yksi, self.kaksi, self.kolme, self.nelja, self.viisi, self.kuusi, self.seitseman, self.kahdeksan, self.yhdeksan, self.kymmenen, self.yksitoista, self.kaksitoista,self.kolmetoista]).flatten())
       self.vapaat_kortit = np.transpose(np.array([self.yksi, self.kaksi, self.kolme, self.nelja, self.viisi, self.kuusi, self.seitseman, self.kahdeksan, self.yhdeksan, self.kymmenen, self.yksitoista, self.kaksitoista, self.kolmetoista]))
       self.vapaat_kortit = pd.DataFrame(self.vapaat_kortit, columns=range(1, 14))
       self.korttitulkki_df = self.vapaat_kortit



       # testikortit
       # self.kortit = [*range(0, 52)]
       self.kortit = []

       self.korttien_listaus()


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
                if event.key == pygame.K_a:
                    self.actions['left'] = True
                if event.key == pygame.K_d:
                    self.actions['right'] = True
                if event.key == pygame.K_w:
                    self.actions['up'] = True
                if event.key == pygame.K_s:
                    self.actions['down'] = True
                if event.key == pygame.K_p:
                    self.actions['action1'] = True
                if event.key == pygame.K_o:
                    self.actions['action2'] = True
                if event.key == pygame.K_RETURN:
                    self.actions['start'] = True

          if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.actions['left'] = False
                if event.key == pygame.K_d:
                    self.actions['right'] = False
                if event.key == pygame.K_w:
                    self.actions['up'] = False
                if event.key == pygame.K_s:
                    self.actions['down'] = False
                if event.key == pygame.K_p:
                    self.actions['action1'] = False
                if event.key == pygame.K_o:
                    self.actions['action2'] = False
                if event.key == pygame.K_RETURN:
                    self.actions['start'] = False

   def update(self):
       self.state_stack[-1].update(self.dt, self.actions)


   def render(self):
       self.state_stack[-1].render(self.game_canvas)
       self.screen.blit(pygame.transform.scale(self.game_canvas, (self.screen.get_width(), self.screen.get_height())), (0,0))
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

       for numero in self.numerot:
           for maa in self.maat:
               self.KORTIT['{}_of_{}'.format(numero, maa)] = pygame.transform.smoothscale(pygame.image.load(os.path.join('PNG-cards-1.3', '{}_of_{}.png'.format(numero, maa))),(self.kortit_width, self.kortit_height))

       for nimi in self.btn_nimet:
           self.BUTTONIT[nimi] = pygame.transform.smoothscale(pygame.image.load(os.path.join('PNG-numbers', '{}.png'.format(nimi))), (self.buttonit_width, self.buttonit_height))

       self.font = pygame.font.SysFont('comicsans', 50)

   def load_states(self):
       self.title_screen = TitleScreen(self)
       self.state_stack.append(self.title_screen)


   def reset_keys(self):
       for action in self.actions:
           self.actions[action] = False

   def x_coords_calc(self):
       for i in range(0, 12):
           self.button_x_coords.append(self.button_x_coords[i] + 110)

   def korttien_listaus(self):

       # tehdään lista, jossa korttien nimet
       lista2 = []
       for numero in self.numerot:
           for maa in self.maat:
               lista2.append('{}_of_{}'.format(numero, maa))
       # print(lista2)

       # tehdään dictionary, jossa kortin numero sekä kortin nimi
       self.dict1 = {}

       for i, j in zip(self.vapaat_kortit_copy, lista2):
           self.dict1[i] = j

   def kortti_tulkki(self):
       if type(self.kortit) == list:
           cards = []
           for i in self.kortit:
               check = self.korttitulkki_df[self.korttitulkki_df.isin([i])].stack().index.to_list()
               jep = [item for t in check for item in t][1]
               cards.append(jep)
           return cards
       else:
           check = self.korttitulkki_df[self.korttitulkki_df.isin([self.kortit])].stack().index.to_list()
           jep = [item for t in check for item in t][1]
           return jep

   def kortin_valinta(self):
       # satunnaisen kortin valinta
       self.kortti = random.choice(self.vapaat_kortit.values[self.vapaat_kortit.values < 9999])
       print('Kortin järjestysluku on: ', self.kortti)
       # kortin numeron etsiminen järjestysluvun perusteella
       self.sarake = self.vapaat_kortit.columns[np.where(self.vapaat_kortit == self.kortti)[1]][0]
       self.vapaat_kortit = self.vapaat_kortit.replace(self.kortti, 9999)
       print(self.vapaat_kortit)
       self.kortit.append(self.kortti)
       print('Random kortti oli:', self.sarake)
       # running = False


# if __name__ == '__FTD_state_engine__:
g = Game()
while g.running:
    g.game_loop()




