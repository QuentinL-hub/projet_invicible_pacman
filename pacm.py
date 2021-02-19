import pygame, sys
from pygame.locals import *
import time
BLOCK_SIZE = 30
class Pacman(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__() 
        self.image = pygame.image.load("images/pacman_o.png")
        self.surf = pygame.Surface((30, 30))
        self.rect = self.surf.get_rect()
        self.score = 0
        self.dx = 0
        self.dy = 0
        self.rot = 0
        self.score = 0
        self.dir = None
        self.x = x*BLOCK_SIZE
        self.y = y*BLOCK_SIZE
        self.register_parcour = []
        

    

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def blocks_ahead_of_pacman(self, dx, dy, map_modal):
        """Return a list of tiles at this position + delta"""
        x = self.x + dx
        y = self.y + dy
        if( self.x // 30 == 0 or self.y // 30 == 0 or self.x //30 == 19 or self.y//30 == 19):
          return []
        # Find integer block pos, using floor (so 4.7 becomes 4)
        ix, iy = int(x // BLOCK_SIZE), int(y // BLOCK_SIZE)
        if(ix < 0 or iy < 0 or iy>19 or ix> 19):
          return []
        # # Remainder let's us check adjacent blocks
        if(self.x % 30 == 0 and self.x//30 != 0):
          
          if(map_modal[((x//30), y//30)]["signe"] == "=" and dx < 0):
            return ['=']
        rx, ry = x % BLOCK_SIZE, y % BLOCK_SIZE
        blocks = [map_modal[(ix, iy)]["signe"]]
        if rx: blocks.append(map_modal[(ix+1, iy)]["signe"])
        if ry: blocks.append(map_modal[(ix, iy+1)]["signe"])
        if rx and ry: blocks.append(map_modal[(ix+1, iy+1)]["signe"])

        return blocks


    def eat_food(self, map_food, scre):
        ix, iy = int(self.x / BLOCK_SIZE), int(self.y / BLOCK_SIZE)
        has_eat = False
        if (ix, iy) in map_food:
            map_food.remove((ix, iy))
            scre += 1
            has_eat = True
            # print("scoreeat = ", score)
        #pacman.powerup = POWER_UP_START
        #set_banner("Power Up!", 5)
        #for g in ghosts: new_ghost_direction(g)
        #pacman.score += 5
        if(has_eat == True):
          return (scre, tuple((ix, iy)))
        else:
          return (scre, None)

    def alternate(self, option1, option2):
        if time.time() % 1 <= (0.5):
            return option2
        else:
            return option1

    def load_image(self, image1, image2, angle):
        return pygame.transform.rotate(pygame.image.load(self.alternate(image1, image2)), angle)
    def update_image(self):
        if self.dir == "D":
            self.image = self.load_image("images/pacman_o.png", "images/pacman_c.png", 270)
        if self.dir == "L":
            self.image = self.load_image("images/pacman_or.png", "images/pacman_cr.png", 180)
        if self.dir == "R":
            self.image = self.load_image("images/pacman_o.png", "images/pacman_c.png", 0)
        if self.dir == "U":
            self.image = self.load_image("images/pacman_o.png", "images/pacman_c.png", 90)
   
    def update2(self, map_mod, map_food, sc):
        print("sc = ", sc)
        t = self.eat_food(map_food, sc)
        sc = t[0]
        print(t)
        print(t[0])
        pressed_keys = pygame.key.get_pressed()
        storedx = 0
        storedy = 0
        

        if pressed_keys[K_UP] or self.dir == "U":
            storedy = -5
            storedx = 0
            self.dir = "U"
            
            if self.y==0:
                storedy=570
        
        if pressed_keys[K_DOWN] or self.dir == "D":
            storedy = 5
            storedx = 0
            self.dir = "D"
            if self.y==570:
                storedy=-570
         
        if pressed_keys[K_LEFT] or self.dir == "L":
            storedx = -5
            storedy = 0
            self.dir = "L"
           
            if self.x==0:
                self.x = 570

        if pressed_keys[K_RIGHT] or self.dir == "R":
           
            storedx = 5
            storedy = 0
            self.dir = "R"
            if self.x==570:
                self.x=5


        if self.dir is not None:
            
            good = True
          
            for g in self.blocks_ahead_of_pacman(storedx, storedy, map_mod):
             
              if(g == "="):
                good = False
            if(good):
              self.dx = storedx
              self.dy = storedy
            else:
              for g in self.blocks_ahead_of_pacman(self.dx, self.dy, map_mod):
                if(g == "="):
                  self.dx = 0
                  self.dy = 0
                  break
            
            
            

        self.update_image()
        self.x = self.x + self.dx
        self.y = self.y + self.dy
        self.rect.move_ip(self.x, self.y)
        return sc

 
    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))     


class IAPacmanHungry(Pacman):
  def update2(self, tab_mod, heigt, food_map, score):
        
        choices = [5, -5]
        self.x += self.dx
        self.y += self.dy

        tmpx = self.x // BLOCK_SIZE
        tmpy = self.y // BLOCK_SIZE

        moduloX = self.x % BLOCK_SIZE
        moduloY = self.y % BLOCK_SIZE

        if(self.x >= (len(tab_mod) / heigt) * 30 - 30):
          self.x = 5
         
        elif(self.x <= 0):
          self.x = ((len(tab_mod)/ heigt) * BLOCK_SIZE)  - BLOCK_SIZE - 5
          
        elif(self.y >= heigt*30-30):
          self.y = 10
          
        elif(self.y <= 0):
          self.y = heigt*30-30-10
         
        else:

          nh = tab_mod[(tmpx, tmpy)]["neighboor"]
          if(moduloX or moduloY):
            pass
          else:
            
            nh = tab_mod[(tmpx, tmpy)]["neighboor"]
            possible_pos = [ n for n in nh if(tab_mod[n.position]["signe"] != "=")]
            if(len(possible_pos) == 2): # possible ligne  droite
              n1 = possible_pos[0].position
              n2 = possible_pos[1].position
              if( n1[0] == n2[0] or n1[1] == n2[1] ): # on rentre dans le use case d'un ligne droite horizontal ou vertical
                if(self.dx == 0 and self.dy == 0): # si le fantome s'est arreter
                  self.dx = 0
                  self.dy = 0
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
        if self.dx == 5:
            self.dir = "R"

        elif self.dx == -5:
            self.dir = "L"
        elif self.dy == 5:
            self.dir = "U"
        elif self.dy == -5:
            self.dir = "D"
        else:
            self.dir = None
        self.update_image()
        score = self.eat_food(food_map, score)
        # print(score)

        # print(self.dx, "  ", self.dy)
        self.rect.move_ip(self.x + self.dx, self.y + self.dy)
        # print("score = ", score)

        return score
        


class IANaive(Pacman):

  def update2(self, tab_mod, heigt, food_map, score):
        
        choices = [5, -5]
      

        tmpx = self.x // BLOCK_SIZE
        tmpy = self.y // BLOCK_SIZE

        moduloX = self.x % BLOCK_SIZE
        moduloY = self.y % BLOCK_SIZE

        if(self.x >= (len(tab_mod) / heigt) * 30 - 30):
          self.x = 5
         
        elif(self.x <= 0):
          self.x = ((len(tab_mod)/ heigt) * BLOCK_SIZE)  - BLOCK_SIZE - 5
          
        elif(self.y >= heigt*30-30):
          self.y = 10
          
        elif(self.y <= 0):
          self.y = heigt*30-30-10
         
        else:

          nh = tab_mod[(tmpx, tmpy)]["neighboor"]
          if(moduloX or moduloY):
            pass
          else:
            
            nh = tab_mod[(tmpx, tmpy)]["neighboor"]
            possible_pos = [ n for n in nh if(tab_mod[n.position]["signe"] != "=")]
            if(len(possible_pos) == 2): # possible ligne  droite
              n1 = possible_pos[0].position
              n2 = possible_pos[1].position
              if( n1[0] == n2[0] or n1[1] == n2[1] ): # on rentre dans le use case d'un ligne droite horizontal ou vertical
                if(self.dx == 0 and self.dy == 0): # si le fantome s'est arreter
                  self.dx = 0
                  self.dy = 0
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
        if self.dx == 5:
            self.dir = "R"

        elif self.dx == -5:
            self.dir = "L"
        elif self.dy == 5:
            self.dir = "U"
        elif self.dy == -5:
            self.dir = "D"
        else:
            self.dir = None
        self.update_image()
        score = self.eat_food(food_map, score)
        # print("bbbb")
        # print(score)
        # print(self.dx, "  ", self.dy)
        self.x += self.dx
        self.y += self.dy
        self.rect.move_ip(self.x, self.y)
        # print("score = ", score)

        return score