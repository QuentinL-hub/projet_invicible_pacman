from nodes import Node

class BFS_cheby():
  def __init__(self, m, gate):
    self.map = m
    self.gate = gate
  #exemple : 30, 30  -> 90, 60
  def Distance(self, x1,y1,x2,y2):
    return abs(((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5)

  def check_take_tp(self, startx1, starty1, goalx2, goaly2):
    tmp_distance = 0
    tmp_tup =   None
    tmp_i = 0
    for i in range(len(self.gate)):
        
        d1 = self.Distance(startx1, starty1, self.gate[i][0], self.gate[i][1]) 
        d2 = 0
        d3 = self.Distance(startx1, starty1, goalx2, goaly2) 
        if(i%2 == 0):
          d2 = self.Distance(self.gate[i+1][0], self.gate[i+1][1],  goalx2, goaly2)
                 
        else:
          d2 = self.Distance(self.gate[i-1][0], self.gate[i-1][1],  goalx2, goaly2)
          
        
        if((d1 + d2) < d3):
          if(tmp_distance == None):
            
            tmp_distance = d3 - (d1+d2)
            tmp_i = i
          else:
            if(tmp_distance < (d3 - (d1 + d2))):
              
              tmp_distance = d3 - (d1+d2)
              tmp_i = i
    if(tmp_distance == 0):
      return None
    else:
      return tmp_i
      

  def best_first_search(self, start, end):
    go_to_tp = self.check_take_tp(start[0], start[1], end[0], end[1])
    if(go_to_tp != None):
      dl = self.best_first_search(start, (self.gate[go_to_tp][0], self.gate[go_to_tp][1]))
      if(go_to_tp % 2 == 0):
        dr = self.best_first_search((self.gate[go_to_tp+1][0], self.gate[go_to_tp+1][1]), end)
      else:
        dr = self.best_first_search(start, (self.gate[go_to_tp][0], self.gate[go_to_tp][1])) + self.best_first_search((self.gate[go_to_tp-1][0], self.gate[go_to_tp-1][1]), end)  
      if(dl == None):
        return dr
      elif(dr == None):
        return dl
      else:
        return dl + dr
    # Create lists for open nodes and closed nodes
    open = []
    closed = []
   

    # Create a start node and an goal node
    start_node = Node(start, None)
    goal_node = Node(end, None)
    # Add the start node
    open.append(start_node)
    
    # Loop until the open list is empty
    while len(open) > 0:
        open.sort()
        # Get the node with the lowest cost
        current_node = open.pop(0)
     
        closed.append(current_node)
        if current_node == goal_node:
            path = []
            while current_node != start_node:
                path.append(current_node.position)
                current_node = current_node.parent
            
            return path[::-1]
        
        (x, y) = current_node.position
        # Get neighbors
        neighbors = self.map[current_node.position]["neighboor"]
       
       
        # Loop neighbors
        for next in neighbors:
            # Get value from map
           
            map_value = self.map.get(next.position)
           
            # Check if the node is a wall
            if(map_value == None):
              continue
            if(map_value["signe"] == "="):
              
                continue
            # Create a neighbor node
            neighbor = Node(next.position, current_node)
           
            # Check if the neighbor is in the closed list
            if(neighbor in closed):
                continue
            
            neighbor.g = max(abs(neighbor.position[0] - start_node.position[0]), abs(neighbor.position[1] - start_node.position[1]))
            neighbor.h = max(abs(neighbor.position[0] - goal_node.position[0]), abs(neighbor.position[1] - goal_node.position[1]))
            neighbor.f = neighbor.h
           
            if(add_to_open(open, neighbor) == True):
               
                open.append(neighbor)
    # Return None, no path is found
    return None
# Check if a neighbor should be added to open list
def add_to_open(open, neighbor):
    for node in open:
        if (neighbor == node and neighbor.f >= node.f):
            return False
    return True