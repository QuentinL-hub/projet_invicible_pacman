BLOCK_SIZE = 30
from bfs import *

class GroupGhost():
  def __init__(self):
    self.ghost_list = []

  def __iter__(self):
    self.n = 0
    return self

  def __next__(self):
    if self.n <  len(self.ghost_list):
      res = self.ghost_list[self.n]
      self.n += 1
      return res  
    else:
      raise StopIteration
  

  def update(self, map_modal, h, tupl, bfoj):
    for g in self.ghost_list:
      g.update(map_modal, h, tupl, bfoj)
      

  def addToList(self, g):
    self.ghost_list.append(g)
    # print(len(self.ghost_list))




class EnsembleOnEstPlusFort(GroupGhost):


 


  def update(self, map_modal, h, tupl, teleport):
    onehasbusted = False
    for g in self.ghost_list:
      g.update(map_modal, h, tupl, teleport)
      if(g.isBusting() == True):
        onehasbusted = True
    if(onehasbusted):
      for g in self.ghost_list:
          g.init_tab_chemin((tupl[0]//BLOCK_SIZE, tupl[1]//BLOCK_SIZE), map_modal, teleport)
      
      

class EnsembleOnEstPlusFortV2(EnsembleOnEstPlusFort):
  

  def subfct(self, mapm, current_node, n, tabl):
    if(n == 0):
      return tabl
    else:
      neigh = [nod.position for nod in mapm[current_node]["neighboor"] if mapm[nod.position]["signe"] != "=" and nod.position not in tabl]
    
      for new_pos in neigh :
        if( new_pos not in tabl):
          tabl += self.subfct(mapm, new_pos, n-1, tabl+[new_pos])
      return tabl

  def get_n_case_around_pacman(self, map_modal, h, tupl, n):
    pac_x = tupl[0] // BLOCK_SIZE
    pac_y = tupl[1] // BLOCK_SIZE
    return self.subfct(map_modal, (pac_x, pac_y), n, [(pac_x, pac_y)])

  def getallIntersection(self, map_modal):
    intersection = []
    for nod in map_modal:
      if(map_modal[nod]["signe"] != "="):
        possible_pos = map_modal[nod]["neighboor"] 
        cur = [p.position for p in possible_pos if(map_modal[p.position]["signe"] != "=")]
        if(len(cur) > 2):
          intersection.append(nod)
        else:
          if(len(cur) == 2):
            n1 = cur[0]
            n2 = cur[1]
            if(n1[0] != n2[0] and n1[1] != n2[1]): #on est pas sur une ligne droite

              intersection.append(nod)
    return intersection


  def closest_to_pacman(self, pacmanx, pacmany, map_modal):
    inter = self.getallIntersection(map_modal)
    bf = BFS_cheby(None, None)
    distance_from_paquitou = [(bf.Distance(nod[0]*30, nod[1]*30, pacmanx, pacmany), nod) for nod in inter]
    distance_from_paquitou.sort()
    return distance_from_paquitou
    

 

  def update(self, map_modal, h, tupl, teleport):
    onehasbusted = False
    for g in self.ghost_list:
      g.update(map_modal, h, tupl, teleport)
      if(g.isBusting() == True):
        onehasbusted = True
    if(onehasbusted):
      dst_inter_to_pac = self.closest_to_pacman(tupl[0], tupl[1], map_modal)
      g_equipier = []
      for g in self.ghost_list:
          if(g.isBusting()):
            g.init_tab_chemin((tupl[0]//BLOCK_SIZE, tupl[1]//BLOCK_SIZE), map_modal, teleport)
          else:
            g_equipier.append(g)
      nb_equipier = len(g_equipier)
      if (nb_equipier > len(dst_inter_to_pac)):
        dst_inter_to_pac= dst_inter_to_pac[:nb_equipier]
      

      # Maintenant qu'on a toutes les intersections de la map et toutes les intersections du chemin de pacman on met en priorité celles du chemin



      """

      O
      |---------
      | *
      |
      |
      
      Car même si on a trier toutes les intersections par ordre de distance avec Pacman on a pas vérifier la longeur du chemin pour aller de ce point 
      jusqua pacman et si il existait des murs 
      d'ou le fait de mettre en priorité les intersections du chemin courant de Pacman
      """


      teamate_used = {}
      #pour chaque distance on tri les fantomes dans l'ordre du plus proches



      for dst in dst_inter_to_pac:
        dst_tab = [(b.Distance(g2.getX(), g2.getY(), dst[1][0], dst[1][1]), g2) for g2 in g_equipier if g2.getId() not in teamate_a_charge]
        dst_tab.sort(key=lambda tup: tup[0]) 
        teamate_used[dst[1]] = dst_tab
      
      
      
      for k, val in teamate_used.items():
        # print(k)
        # print("=======")
        # print(val)
        for v in val:
          # print("+++++++++++++")
          # print(v[1])
          if(v[1].getId() not in teamate_a_charge):
            teamate_a_charge.append(v[1].getId())
            all_chemin.append((v[1], k))
            break
      # print("all chemin apres tout")
      # print(all_chemin)
      for ghst, goal_case in all_chemin:
        ghst.init_tab_chemin(goal_case,map_modal, teleport)
   
class EnsembleOnEstPlusFortV3(EnsembleOnEstPlusFortV2):
  """
  Trouve toutes les fins de chemins de pacman a partir du moment ou il est busted pour que les fantomes l'encerclent
  """
  def __init__(self, fm):
    super().__init__()
    self.food_m = fm


  def get_extremite_chemin(self, tuplee, visited, map_modal):
    possible_pos = [nd.position for nd in map_modal[tuplee]["neighboor"] if map_modal[nd.position]["signe"] != "="]
    for v in visited:
      if(v in possible_pos):
        possible_pos.remove(v)
    if(len(possible_pos) == 2 and len(visited) > 0):
      
      return tuplee
    else:
      t = []
      for pp in possible_pos:
       
        t.append(self.get_extremite_chemin(pp, visited+[tuplee], map_modal))
        if(len(t) > 0 and isinstance(t, list)):
          while (isinstance(t, list)):
            if(len(t) > 0):
              t = t[0]
            else:
              break
            if(not isinstance(t, list)):
              t = [t]
              break
          
      return t
    


  def update(self, map_modal, h, tupl, teleport, map_referentiel):
    onehasbusted = False
    for g in self.ghost_list:
      ix, iy = int(g.getX() / BLOCK_SIZE), int(g.getY() / BLOCK_SIZE)
      if (ix, iy) in self.food_m and (ix, iy) not in map_referentiel:
          self.food_m.remove((ix, iy))

    for g in self.ghost_list:
      g.update(map_modal, h, tupl, teleport)
      if(g.isBusting() == True):
        onehasbusted = True
    
    


    if(onehasbusted):
      dst_inter_to_pac = self.closest_to_pacman(tupl[0], tupl[1], map_modal)
      g_equipier = []
      for g in self.ghost_list:
          if(g.isBusting()):
            g.init_tab_chemin((tupl[0]//BLOCK_SIZE, tupl[1]//BLOCK_SIZE), map_modal, teleport)
          else:
            g_equipier.append(g)
      nb_equipier = len(g_equipier)
      if (nb_equipier > len(dst_inter_to_pac)):
        dst_inter_to_pac= dst_inter_to_pac[:nb_equipier]
      tu = self.get_extremite_chemin((tupl[0]//BLOCK_SIZE, tupl[1]//BLOCK_SIZE), [], map_modal)
      final_t = []
      for xj in tu:
        if(isinstance(xj, list)):
          final_t.append(xj[0])
        else:
          final_t.append(xj)
      b = BFS_cheby(None, None)
      teamate_a_charge = []
      all_chemin = []
      distance_from_paq = [(b.Distance(tupl[0], tupl[1], f[0], f[1]), f) for f in final_t]
      #on classe les intersections du chemins courant de pacman dans l'ordre de priorité, autrement dit, la fin du chemin la plus proche de pacman est la plus importante et ainsi de suite
      distance_from_paq.sort(key=lambda tup: tup[0])

      # Maintenant qu'on a toutes les intersections de la map et toutes les intersections du chemin de pacman on met en priorité celles du chemin



      """

      O
      |---------
      | *
      |
      |
      
      Car même si on a trier toutes les intersections par ordre de distance avec Pacman on a pas vérifier la longeur du chemin pour aller de ce point 
      jusqua pacman et si il existait des murs 
      d'ou le fait de mettre en priorité les intersections du chemin courant de Pacman
      """


      teamate_used = {}
      #pour chaque distance on tri les fantomes dans l'ordre du plus proches          
      for dst in distance_from_paq:
        dst2_tab = [(b.Distance(g2.getX(), g2.getY(), dst[1][0], dst[1][1]), g2) for g2 in g_equipier]
        dst2_tab.sort(key=lambda tup: tup[0]) 
        teamate_used[dst[1]] = dst2_tab

      for k, val in teamate_used.items():
        
        for v in val:
          
          if(v[1].getId() not in teamate_a_charge):
            teamate_a_charge.append(v[1].getId())
            all_chemin.append((v[1], k))
            break
      # print("all chemin apres intersections chemin")
      # print(all_chemin)




      for dst in dst_inter_to_pac:
        dst_tab = [(b.Distance(g2.getX(), g2.getY(), dst[1][0], dst[1][1]), g2) for g2 in g_equipier if g2.getId() not in teamate_a_charge]
        dst_tab.sort(key=lambda tup: tup[0]) 
        teamate_used[dst[1]] = dst_tab
      
      
      
      for k, val in teamate_used.items():
        # print(k)
        # print("=======")
        # print(val)
        for v in val:
          # print("+++++++++++++")
          # print(v[1])
          if(v[1].getId() not in teamate_a_charge):
            teamate_a_charge.append(v[1].getId())
            all_chemin.append((v[1], k))
            break
      # print("all chemin apres tout")
      # print(all_chemin)
      for ghst, goal_case in all_chemin:
        ghst.init_tab_chemin(goal_case,map_modal, teleport)
    

