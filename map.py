from nodes import Node
from group_Ghost import *
from pacm import Pacman
from ghost import *
from bfs import *
class Map():
  def __init__(self):
    self.char_to_image = {
      '.': 'images/dot.png',
      '=': 'images/wall.png',
      '*': 'images/power.png',
      'g': 'images/ghost1.png',
      'G': 'images/ghost3.png',
      'h': 'images/ghost4.png',
      'H': 'images/ghost5.png',
      'M': 'images/marker.png',
      'O': 'images/marker2.png',
    }
    self.w = 0
    self.h = 0
    self.food_left = 0
    self.map_modal = dict()
    self.food_map = []
    self.pacman = None
    self.groupGhost = None
    self.score = 0
    self.test_path_bfs = []
    self.tp = []

  def load_level(self, number):
    file = "level-%s.txt" % number
    self.food_left = 0

    with open(file) as f:
      map_tmp = [[b for b in line.strip()] for line in f]
      self.h = len(map_tmp)
      self.map_modal = {(j, i):{"signe":b, "neighboor":[Node((j-1, i), None), Node((j, i-1), None), Node((j+1, i), None), Node((j, i+1), None)]} for i, l in enumerate(map_tmp)  for j, b in enumerate(l)}
      
      self.food_map = [(j, i) for i, l in enumerate(map_tmp)  for j, b in enumerate(l) if b == "."  ]
      self.food_left = len(self.food_map)

      self.groupGhost= EnsembleOnEstPlusFortV3(self.food_map.copy())
      for k, v in self.map_modal.items():
        if((v["signe"] == "." or v["signe"] == "*") and k[0] == 0):
          v["neighboor"][0].position = (len(map_tmp[0])-1, v["neighboor"][0].position[1])
          print("changed 1")
        if((v["signe"] == "." or v["signe"] == "*") and k[1] == 0):
          v["neighboor"][1].position = (v["neighboor"][0].position[0], self.h - 1)
          print("changed 2")
        if((v["signe"] == "." or v["signe"] == "*") and k[0] == len(map_tmp[0])- 1):
          v["neighboor"][2].position = (0, v["neighboor"][0].position[1])
          print("changed 3")
        if((v["signe"] == "." or v["signe"] == "*") and k[1] == self.h - 1):
          v["neighboor"][3].position = (v["neighboor"][0].position[0], 0)
          print("changed 4")
        if(k[0] == 0 and v["signe"] == "."):
          self.tp += [k]
          self.tp += [((len(self.map_modal)//self.h)-1 , k[1])]
        if(k[1] ==0 and v["signe"] == "."):
          self.tp += [k]
          self.tp += [(k[0], self.h-1)]
         

        if(v["signe"] == "p"):
        
          #self.pacman = IAPacmanHungry(k[0], k[1])
          self.pacman = Pacman(k[0], k[1])
        
        else:
          if(v["signe"] == "g" or v["signe"] == "G" or v["signe"] == "h" or v["signe"] == "H"):
            gosth = IAPhantomBFS3(k[0], k[1], self.char_to_image[v["signe"]], self.food_map)
            self.groupGhost.addToList(gosth)
      for g in self.groupGhost:
        print(g)
          



  
      
  def from_pacman_to_ghost(pos):

    x, y = pos
    i = max(0, int(x / 30))
    j = max(0, int(y / 30))

    return i, j       

  def get_collision(self):
    pcx = self.pacman.getX()
    pcy = self.pacman.getY()
    pac_rect = pygame.Rect(pcx, pcy, BLOCK_SIZE, BLOCK_SIZE)
    for g in self.groupGhost:
      
      gx = g.getX()
      gy = g.getY()
      rect_g = pygame.Rect(gx, gy, BLOCK_SIZE, BLOCK_SIZE)
      if((pac_rect).colliderect(rect_g)):
        return True
    #     """Retourne la liste des rectangles autour de la position (i_start, j_start).
 
    # Vu que le personnage est dans le carré (i_start, j_start), il ne peut
    # entrer en collision qu'avec des blocks dans sa case, la case en-dessous,
    # la case à droite ou celle en bas et à droite. On ne prend en compte que
    # les cases du niveau avec une valeur de 1.
    # """
    
      
    return False  


  def update(self):
    if(len(self.food_map) == 0):
      print("Congrats vous avez gagné")
      exit(1)
    Bf = BFS_cheby(self.map_modal, self.tp)
    # if(isinstance(self.pacman, Pacman)):
    res =self.pacman.update2(self.map_modal, self.food_map, self.score)
    # else:
    #res =self.pacman.update2(self.map_modal, self.h, self.food_map, self.score)
    self.score = res
    # print(self.score)
    if(isinstance(self.groupGhost, EnsembleOnEstPlusFortV3)):

      self.groupGhost.update(self.map_modal, self.h, (self.pacman.getX(), self.pacman.getY()), Bf, self.food_map)
    else:
      self.groupGhost.update(self.map_modal, self.h, (self.pacman.getX(), self.pacman.getY()), Bf)
    
    if(self.get_collision()):
      return False
    else:
      return True

    # is_collision = self.get_collision()
    # if(is_collision):
    #   print("perdu")
    #   exit(1)



  def draw(self, surface):
  
    for k, v in self.map_modal.items():
      if(v["signe"] == "="):
        image = self.char_to_image.get(v["signe"], None)
        if image:
          surface.blit(pygame.image.load(self.char_to_image[v["signe"]]), (k[0]*30, k[1]*30))
    
    for food in self.food_map:
      surface.blit(pygame.image.load(self.char_to_image["."]), (food[0]*30, food[1]*30))
    for pa in self.test_path_bfs:
      
      surface.blit(pygame.image.load(self.char_to_image["M"]), (pa[0]*30, pa[1]*30))
   
    for g in self.groupGhost:
      g.draw(surface)


    






    self.pacman.draw(surface)