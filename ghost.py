import pygame, sys
from pygame.locals import *
BLOCK_SIZE = 30
import time
import random
from bfs import *

class Ghost(pygame.sprite.Sprite):
      def __init__(self, x, y, signe):
        super().__init__()
        self.id = time.time()
        # print(self.id)
        self.image = pygame.image.load(signe)
        self.surf = pygame.Surface((30, 30))
        self.rect = self.surf.get_rect()
        self.dx = 0
        self.dy = 0
        self.x = x*BLOCK_SIZE
        self.y = y*BLOCK_SIZE
        self.signe = signe
        self.rot = 0
        self.busted = False
        self.tab_chemin = []
        self.last_dir = None

      
          # elif(self.dx > 0): #go on right
          # elif(self.dy >  0): #go down
          # else: #go top

        # else:
       
          # g.dy = random.choice([-GHOST_SPEED, GHOST_SPEED])
        
      def getId(self):
        return self.id

      def getX(self):
        return self.x

      def getY(self):
        return self.y

      def isBusting(self):
        return self.busted

      def isRandom(self):
        if(len(self.tab_chemin) == 0):
          return True
        else:
          return False

      def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))
        for t in self.tab_chemin:
          surface.blit(pygame.image.load("images/marker.png"), (t[0]*BLOCK_SIZE, t[1]*BLOCK_SIZE))


      def __str__(self):  
        return "From x= %s, y = %s" % (self.x, self.y)  




class IAPhantomNaive(Ghost):
  def update(self, tab_mod, heigt, pacman_pos):
        choices = [5, -5]
    
        

        tmpx = self.x // BLOCK_SIZE
        tmpy = self.y // BLOCK_SIZE

        moduloX = self.x % BLOCK_SIZE
        moduloY = self.y % BLOCK_SIZE
        tp = False
        if (self.x >= (len(tab_mod) / heigt) * 30 - 30):
            self.x = 5
        elif (self.x <= 0):
            self.x = ((len(tab_mod) / heigt) * BLOCK_SIZE) - BLOCK_SIZE - 5

        elif (self.y >= (heigt) * 30 - 30):
            self.y = 5

        elif (self.y <= 0):
            self.y = (heigt * BLOCK_SIZE) - BLOCK_SIZE - 5
        else:

          nh = tab_mod[(tmpx, tmpy)]["neighboor"]
          if(moduloX == 0 and moduloY == 0):

            
          
            
            nh = tab_mod[(tmpx, tmpy)]["neighboor"]
            possible_pos = [ n for n in nh if(tab_mod[n.position]["signe"] != "=")]
            if(len(possible_pos) == 2): # possible ligne  droite
              n1 = possible_pos[0].position
              n2 = possible_pos[1].position
              if( n1[0] == n2[0] or n1[1] == n2[1] ): # on rentre dans le use case d'un ligne droite horizontal ou vertical
                if(self.dx == 0 and self.dy == 0): # si le fantome est arreter (AU DÉ)
                  
                  if(n1[0] == n2[0]): #c'est vertical  
                    self.dy = random.choice(choices);
                  else:
                    self.dx = random.choice(choices);
              else:
               #on rentre dans le use case d'un angle
                self.dx = 0
                self.dy = 0
                tn = [n1, n2]
                n3 = random.choice(tn)
                
                if(tmpx - n3[0] > 0):
                  self.dx = -5
                  
                elif(tmpx - n3[0] < 0):
                  self.dx = 5

                elif(tmpy - n3[1] < 0):
                  self.dy = 5
                else:
                  self.dy = -5

            else:
              randy = random.choice(possible_pos)
              nrandy = randy.position
              self.dx = 0
              self.dy = 0
              if(tmpx - nrandy[0] > 0):
                  self.dx = -5
                  
              elif(tmpx - nrandy[0] < 0):
                self.dx = 5

              elif(tmpy - nrandy[1] < 0):
                self.dy = 5
              else:
                self.dy = -5
          if(self.dx == -5):
            self.last_dir = "LEFT"
          elif(self.dx == 5):
            self.last_dir = "RIGHT"
          elif(self.dy == 5):
            self.last_dir = "BOT"
          else:
            self.last_dir = "TOP"
          
          
          self.x += self.dx
          self.y += self.dy
          self.rect.move_ip(self.x, self.y)


class IAPhantomBFS(IAPhantomNaive):
  
  def check_line(self, posx_line, posy_line, vecteur,pac_pos,tab_mod, h_map):
    while(True):
      if(posx_line == pac_pos[0] and posy_line== pac_pos[1]):
        return True
      if(posx_line < 0 or posy_line < 0):
        return False
      if(posy_line >= h_map):
        return False
      if(posx_line >= len(tab_mod)//h_map):
        return False  
      if(tab_mod[(posx_line + vecteur[0], posy_line + vecteur[1])]["signe"] == "="):
        return False
    
        
        
      posx_line += vecteur[0]
      posy_line += vecteur[1]

    return False

  def init_tab_chemin(self, goal_case, map_case, bfobj):
        
        self.tab_chemin = bfobj.best_first_search((self.x//BLOCK_SIZE, self.y // BLOCK_SIZE), goal_case)
        if(self.tab_chemin == None):
          if(self.x % BLOCK_SIZE != 0 or self.y % BLOCK_SIZE != 0):
            self.tab_chemin = [(self.x//BLOCK_SIZE, self.y // BLOCK_SIZE)] + self.tab_chemin
     
        if(self.tab_chemin == None):
          self.tab_chemin = []

  def continue_chemin(self):
    if(len(self.tab_chemin) != 0):
      mycaseX = self.x // BLOCK_SIZE
      mycaseY = self.y // BLOCK_SIZE
      obj = self.tab_chemin[0]
      if(self.x % BLOCK_SIZE == 0 and self.y % BLOCK_SIZE == 0):
        
        if(mycaseX  == obj[0] and mycaseY  == obj[1]): #on est sur la case désiré, on supprime du tableau et on relance
          self.tab_chemin.pop(0)
         
          return self.continue_chemin()
        else:
          if(self.x  < obj[0]*BLOCK_SIZE):
            self.dx = 5
            self.dy = 0
          elif(self.x > obj[0] * BLOCK_SIZE):
            self.dx = -5
            self.dy = 0
          elif(self.y < obj[1]*BLOCK_SIZE):
            self.dx = 0
            self.dy = 5
          else:
            self.dx = 0
            self.dy = -5
      

      self.x = self.x + self.dx
      self.y = self.y + self.dy   
        




  def update(self, tab_mod, heigt, pacman_pos, Bf):
    
      
    pac_pos_x_reel = pacman_pos[0]
    pac_pos_y_reel = pacman_pos[1]
    pac_pos_x = pac_pos_x_reel // BLOCK_SIZE
    pac_pos_y = pac_pos_y_reel // BLOCK_SIZE
    busted = False
    mycaseX = self.x // BLOCK_SIZE
    mycaseY = self.y // BLOCK_SIZE
    
    if(self.x < pacman_pos[0]  and  self.dx > 0 and ((self.y <= pac_pos_y_reel <= self.y + BLOCK_SIZE) or (self.y <= pac_pos_y_reel+30 <= self.y + BLOCK_SIZE)) ): #je regarde a droite et il y'a potentiellement pacman -> coup de calcul en moins si pacman est a ca gauche par exemple
      
      busted = self.check_line(mycaseX, mycaseY, (1, 0), (pac_pos_x, mycaseY), tab_mod, heigt)
    elif(self.x > pacman_pos[0] and self.dx < 0 and ((self.y <= pac_pos_y_reel <= self.y + BLOCK_SIZE) or (self.y <= pac_pos_y_reel+30 <= self.y + BLOCK_SIZE)) ):
      
      busted = self.check_line(mycaseX, mycaseY, (-1, 0), (pac_pos_x, mycaseY), tab_mod, heigt)
    elif(self.y > pac_pos_y_reel and self.dy < 0 and ((self.x <= pac_pos_x_reel <= self.x + BLOCK_SIZE) or (self.x <= pac_pos_x_reel+30 <= self.x + BLOCK_SIZE)) ): #je suis en bas et je remonte
      
     
      busted = self.check_line(mycaseX, mycaseY, (0, -1), (mycaseX,pac_pos_y), tab_mod, heigt)
      
      
    elif(self.y < pacman_pos[1] and self.dy > 0 and ((self.x <= pac_pos_x_reel <= self.x + BLOCK_SIZE) or (self.x <= pac_pos_x_reel+30 <= self.x + BLOCK_SIZE)) ):
     
      busted = self.check_line(mycaseX, mycaseY, (0, 1), (mycaseX,pac_pos_y), tab_mod, heigt)
    else:
      pass
    if(busted):
      self.busted = True
      self.init_tab_chemin((pac_pos_x, pac_pos_y), tab_mod, Bf)

      # self.tab_chemin = Bf.best_first_search((mycaseX, mycaseY), (pac_pos_x, pac_pos_y))
    
     
      # print(self.tab_chemin)
      # print((mycaseX, mycaseY), " ", (pac_pos_x, pac_pos_y))
      if(len(self.tab_chemin) != 0):
        self.continue_chemin()
        if(self.x >= (len(tab_mod) // heigt) * 30 - 30 and self.dx > 0):
          self.x = 0
          self.tab_chemin.pop(0)
        elif(self.x <= 0 and self.dx < 0):
          self.x = ((len(tab_mod)// heigt) * BLOCK_SIZE)  - BLOCK_SIZE
          self.tab_chemin.pop(0)
        elif(self.y > (heigt*30)-30  and self.dy > 0):
          self.y = 0
          if(self.tab_chemin[0][1] == heigt-1):
              self.tab_chemin.pop(0)
          
      
        else:
          if(self.y == 0 and self.dy < 0):
            self.y = heigt*30-30
            self.tab_chemin.pop(0)
    else:
      self.busted = False
      if(len(self.tab_chemin) == 0):
        return IAPhantomNaive.update(self, tab_mod, heigt, pacman_pos)
      else:
        self.continue_chemin()
        if(self.x >= (len(tab_mod) // heigt) * 30 - 30 and self.dx > 0):
          self.x = 0
          self.tab_chemin.pop(0)
             
        elif(self.x == 0 and self.dx < 0):
          self.x = ((len(tab_mod)// heigt) * BLOCK_SIZE)  - BLOCK_SIZE
          self.tab_chemin.pop(0)
          
        elif(self.y >= heigt*30-30  and self.dy > 0):
          self.y = 0
          self.tab_chemin.pop(0)
          
      
        else:
          if(self.y <= 0 and self.dy < 0):
            self.y = heigt*30-30
            self.tab_chemin.pop(0)
    
    self.rect.move_ip(self.x, self.y)

    #je continue mon chemin

class IAPhantom(IAPhantomBFS):
  def update(self, tab_mod, heigt, bfobj,fm):
        choices = [5, -5]
    
        

        tmpx = self.x / BLOCK_SIZE
        tmpy = self.y / BLOCK_SIZE

        moduloX = self.x % BLOCK_SIZE
        moduloY = self.y % BLOCK_SIZE
        tp = False
        if (self.x >= (len(tab_mod) / heigt) * 30 - 30):
            self.x = 5
            if(len(self.tab_chemin) != 0):
              self.tab_chemin.pop(0)
        elif (self.x <= 0):
            self.x = ((len(tab_mod) / heigt) * BLOCK_SIZE) - BLOCK_SIZE - 5
            if(len(self.tab_chemin) != 0):
              self.tab_chemin.pop(0)

        elif (self.y >= (heigt) * 30 - 30):
            self.y = 5
            if(len(self.tab_chemin) != 0):
              self.tab_chemin.pop(0)

        elif (self.y <= 0):
            self.y = (heigt * BLOCK_SIZE) - BLOCK_SIZE - 5
            if(len(self.tab_chemin) != 0):
              self.tab_chemin.pop(0)
        else:
            if(len(fm) != 0):
              nourriture = random.choices(fm)[0]
            
              self.init_tab_chemin(nourriture, tab_mod, bfobj)
            #retourne une position de nourritures qui n'as pas était mangé

class IAPhantomBFS2(IAPhantomBFS):




  def update(self, tab_mod, heigt, pacman_pos, Bf):
    
      
    pac_pos_x_reel = pacman_pos[0]
    pac_pos_y_reel = pacman_pos[1]
    pac_pos_x = pac_pos_x_reel // BLOCK_SIZE
    pac_pos_y = pac_pos_y_reel // BLOCK_SIZE
    busted = False
    mycaseX = self.x // BLOCK_SIZE
    mycaseY = self.y // BLOCK_SIZE
    
    if(self.x < pacman_pos[0]  and  self.dx > 0 and ((self.y <= pac_pos_y_reel <= self.y + BLOCK_SIZE) or (self.y <= pac_pos_y_reel+30 <= self.y + BLOCK_SIZE)) ): #je regarde a droite et il y'a potentiellement pacman -> coup de calcul en moins si pacman est a ca gauche par exemple
      
      busted = self.check_line(mycaseX, mycaseY, (1, 0), (pac_pos_x, mycaseY), tab_mod, heigt)
    elif(self.x > pacman_pos[0] and self.dx < 0 and ((self.y <= pac_pos_y_reel <= self.y + BLOCK_SIZE) or (self.y <= pac_pos_y_reel+30 <= self.y + BLOCK_SIZE)) ):
      
      busted = self.check_line(mycaseX, mycaseY, (-1, 0), (pac_pos_x, mycaseY), tab_mod, heigt)
    elif(self.y > pac_pos_y_reel and self.dy < 0 and ((self.x <= pac_pos_x_reel <= self.x + BLOCK_SIZE) or (self.x <= pac_pos_x_reel+30 <= self.x + BLOCK_SIZE)) ): #je suis en bas et je remonte
      
     
      busted = self.check_line(mycaseX, mycaseY, (0, -1), (mycaseX,pac_pos_y), tab_mod, heigt)
      
      
    elif(self.y < pacman_pos[1] and self.dy > 0 and ((self.x <= pac_pos_x_reel <= self.x + BLOCK_SIZE) or (self.x <= pac_pos_x_reel+30 <= self.x + BLOCK_SIZE)) ):
     
      busted = self.check_line(mycaseX, mycaseY, (0, 1), (mycaseX,pac_pos_y), tab_mod, heigt)
    else:
      pass
    if(busted):
      self.busted = True
      if(len(self.tab_chemin) != 0):
        if(self.tab_chemin[-1] != (pac_pos_x, pac_pos_y)):
          self.init_tab_chemin((pac_pos_x, pac_pos_y), tab_mod, Bf)
      else:
          self.init_tab_chemin((pac_pos_x, pac_pos_y), tab_mod, Bf)

      # self.tab_chemin = Bf.best_first_search((mycaseX, mycaseY), (pac_pos_x, pac_pos_y))
    
     
      # print(self.tab_chemin)
      # print((mycaseX, mycaseY), " ", (pac_pos_x, pac_pos_y))
      if(len(self.tab_chemin) != 0):
        self.continue_chemin()
        if(self.x >= (len(tab_mod) // heigt) * 30 - 30 and self.dx > 0):
          self.x = 0
          self.tab_chemin.pop(0)
             
        elif(self.x <= 0 and self.dx < 0):
          self.x = ((len(tab_mod)// heigt) * BLOCK_SIZE)  - BLOCK_SIZE
          self.tab_chemin.pop(0)
        elif(self.y > (heigt*30)-30  and self.dy > 0):
          self.y = 0
          self.tab_chemin.pop(0)
      
        else:
          if(self.y == 0 and self.dy < 0):
            self.y = heigt*30-30
            self.tab_chemin.pop(0)
    else:
      self.busted = False
      if(len(self.tab_chemin) == 0):
        return IAPhantomNaive.update(self, tab_mod, heigt, pacman_pos)
      else:
        self.continue_chemin()
        if(self.x >= (len(tab_mod) // heigt) * 30 - 30 and self.dx > 0):
          self.x = 0
          self.tab_chemin.pop(0)
        elif(self.x == 0 and self.dx < 0):
          self.x = ((len(tab_mod)// heigt) * BLOCK_SIZE)  - BLOCK_SIZE
          self.tab_chemin.pop(0)
        elif(self.y >= heigt*30-30  and self.dy > 0):
          self.y = 0
          self.tab_chemin.pop(0)
      
        else:
          if(self.y <= 0 and self.dy < 0):
            self.y = heigt*30-30
            self.tab_chemin.pop(0)
    self.rect.move_ip(self.x, self.y)


class IAPhantomBFS3(IAPhantomBFS2):

  def __init__(self, x, y, signe, food_in_map):
    super().__init__( x, y, signe)
    self.food_in_map = food_in_map


  def update(self, tab_mod, heigt, pacman_pos, Bf):
    
      
    pac_pos_x_reel = pacman_pos[0]
    pac_pos_y_reel = pacman_pos[1]
    pac_pos_x = pac_pos_x_reel // BLOCK_SIZE
    pac_pos_y = pac_pos_y_reel // BLOCK_SIZE
    busted = False
    mycaseX = self.x // BLOCK_SIZE
    mycaseY = self.y // BLOCK_SIZE
    
    if(self.x < pacman_pos[0]  and  self.dx > 0 and ((self.y <= pac_pos_y_reel <= self.y + BLOCK_SIZE) or (self.y <= pac_pos_y_reel+30 <= self.y + BLOCK_SIZE)) ): #je regarde a droite et il y'a potentiellement pacman -> coup de calcul en moins si pacman est a ca gauche par exemple
      
      busted = self.check_line(mycaseX, mycaseY, (1, 0), (pac_pos_x, mycaseY), tab_mod, heigt)
    elif(self.x > pacman_pos[0] and self.dx < 0 and ((self.y <= pac_pos_y_reel <= self.y + BLOCK_SIZE) or (self.y <= pac_pos_y_reel+30 <= self.y + BLOCK_SIZE)) ):
      
      busted = self.check_line(mycaseX, mycaseY, (-1, 0), (pac_pos_x, mycaseY), tab_mod, heigt)
    elif(self.y > pac_pos_y_reel and self.dy < 0 and ((self.x <= pac_pos_x_reel <= self.x + BLOCK_SIZE) or (self.x <= pac_pos_x_reel+30 <= self.x + BLOCK_SIZE)) ): #je suis en bas et je remonte
      
     
      busted = self.check_line(mycaseX, mycaseY, (0, -1), (mycaseX,pac_pos_y), tab_mod, heigt)
      
      
    elif(self.y < pacman_pos[1] and self.dy > 0 and ((self.x <= pac_pos_x_reel <= self.x + BLOCK_SIZE) or (self.x <= pac_pos_x_reel+30 <= self.x + BLOCK_SIZE)) ):
     
      busted = self.check_line(mycaseX, mycaseY, (0, 1), (mycaseX,pac_pos_y), tab_mod, heigt)
    else:
      pass
    if(busted):
      self.busted = True
      if(len(self.tab_chemin) != 0):
        if(self.tab_chemin[-1] != (pac_pos_x, pac_pos_y)):
          self.init_tab_chemin((pac_pos_x, pac_pos_y), tab_mod, Bf)
      else:
          self.init_tab_chemin((pac_pos_x, pac_pos_y), tab_mod, Bf)

      # self.tab_chemin = Bf.best_first_search((mycaseX, mycaseY), (pac_pos_x, pac_pos_y))
    
     
      # print(self.tab_chemin)
      # print((mycaseX, mycaseY), " ", (pac_pos_x, pac_pos_y))
      if(len(self.tab_chemin) != 0):
        self.continue_chemin()
        if(self.x >= (len(tab_mod) // heigt) * 30 - 30 and self.dx > 0):
          self.x = 0
          self.tab_chemin.pop(0)
             
        elif(self.x <= 0 and self.dx < 0):
          self.x = ((len(tab_mod)// heigt) * BLOCK_SIZE)  - BLOCK_SIZE
          self.tab_chemin.pop(0)
        elif(self.y > (heigt*30)-30  and self.dy > 0):
          self.y = 0
          self.tab_chemin.pop(0)
          
      
        else:
          if(self.y == 0 and self.dy < 0):
            self.y = heigt*30-30
            self.tab_chemin.pop(0)
    else:
      self.busted = False
      if(len(self.tab_chemin) == 0):
        return IAPhantom.update(self, tab_mod, heigt, Bf, self.food_in_map)
      else:
        self.continue_chemin()
        if(self.x >= (len(tab_mod) // heigt) * 30 - 30 and self.dx > 0):
          self.x = 0
          self.tab_chemin.pop(0)
             
        elif(self.x == 0 and self.dx < 0):
          self.x = ((len(tab_mod)// heigt) * BLOCK_SIZE)  - BLOCK_SIZE
          self.tab_chemin.pop(0)
        elif(self.y >= heigt*30-30  and self.dy > 0):
          self.y = 0
          self.tab_chemin.pop(0)
      
        else:
          if(self.y <= 0 and self.dy < 0):
            self.y = heigt*30-30
            self.tab_chemin.pop(0)
    self.rect.move_ip(self.x, self.y)

    #je continue mon chemin

