class MDP():
  def __init__(self,gamma,delta):
    self.gamma = gamma
    self.delta = delta
    self.states = []
    self.utility = {}
    self.actionprime = {}
    self.utilityprime = {}

  def isConverged(self):
    ''' return True or False based on convergence of the states '''
    count = 0
    for s in self.states:
      if abs(self.utility[s] - self.utilityprime[s]) <= self.delta:
        count += 1
    return count == len(self.states)
      
  def checkStatesAndUtilities(self):
    ''' print U tab U\' to visually verify change in utility values'''
    for s in self.states:
      print(str(s)+'\t'+str(self.utility[s])+'\t'+str(self.utilityprime[s]))

  
  def copyUtils(self):
    ''' copy U\' to U before update'''
    for s in self.states:
      self.utility[s] = self.utilityprime[s]
  
  def round(self):
    ''' round all util values to 3 decimals - use at end'''
    for state in self.states:
      self.utilityprime[state] = round(self.utilityprime[state],3)
      self.utility[state] = round(self.utility[state],3)


class Game():
  def __init__(self,mdp,shootCost, dodgeCost, rechargeCost):
    #step cost for part (based on def of game in problem statement)
    self.shootCost = shootCost
    self.dodgeCost = dodgeCost
    self.rechargeCost = rechargeCost

    #possible state values
    A = [0,1,2,3]
    S = [0,50,100]
    H = [0,25,50,75,100]

    #initialising U and U'
    mdp.states = [(s,a,h) for s in S for a in A for h in H] 

    for state in mdp.states:
      h = state[2]
      mdp.utility[state] = float(0)
      mdp.utilityprime[state] = float(0)
      if h==0:
        mdp.utilityprime[state] = float(10)


  def getShootVal(self,state,mdp):
    ''' 
      - can shoot only when num of arrows(a) > 0 and stamina(s) > 0 and haven't won game yet
      - poor shooter P(hit) = P(miss) = 0.5
    '''
    s,a,h = state[0],state[1],state[2]
    shootVal=0
    if a in [1,2,3] and s in [50,100] and h in [25,50,75,100]:
      shootVal = (0.5)*float(mdp.utility[(s-50,a-1,h)]) + (0.5)*float(mdp.utility[(s-50,a-1,h-25)])
    return shootVal

  def getDodgeVal(self,state,mdp):
    '''
      - dodge if stamina(s) > 0 
      - if s==100
          - P(s lowered by 50) = 0.8 ; P(s lowered by 100) = 0.2
          - P(picking up arrow) = 0.8; P(not picking an arrow) = 0.2
      - if s==50
          - P(s lowered by 50) = 1
          - P(picking up arrow) = 0.8; P(not picking an arrow) = 0.2
    '''
    s,a,h = state[0],state[1],state[2]
    dodgeVal =0
    if s == 100:
      if a in [0,1,2]:
        shootVal = float((0.8*0.8)*float(mdp.utility[(50,a+1,h)]) + (0.8*0.2)*float(mdp.utility[(50,a,h)]) + (0.2*0.8)*float(mdp.utility[(0,a+1,h)]) + (0.2*0.2)*float(mdp.utility[(0,a,h)]))
      if a == 3:
        shootVal = float((0.8)*float(mdp.utility[(50,a,h)]) + (0.2)*float(mdp.utility[(0,a,h)]) )
    elif s == 50:
      if a in [0,1,2]:
        shootVal = float((0.8)*float(mdp.utility[(0,a+1,h)]) + (0.2)*float(mdp.utility[(0,a,h)]))
      if a == 3:
        shootVal = float((1)*float(mdp.utility[(0,a,h)]) )    
    return dodgeVal

  def getRechargeVal(self,state,mdp):
    '''
      - recharge action result in stamina(s) increasing by 50 or 0
      - P(s increases by 50) = 0.8 ; P(s doesn't increase) = 0.2
    '''
    s,a,h = state[0],state[1],state[2]
    rechargeVal = 0
    if s in [0,50]:
      rechargeVal = (0.8)*float(mdp.utility[(s+50,a,h)]) + (0.2)*float(mdp.utility[(s,a,h)])
    return rechargeVal

  def getAction(self,dodgeVal, shootVal, rechargeVal):
    '''
      - action of that iteration is the action that gives max utility among all possible actions
    '''
    action = ''
    if dodgeVal > shootVal:
      if dodgeVal > rechargeVal:
        action = 'DODGE'
      else:
        action = 'RECHARGE'
    else:
      if shootVal>rechargeVal:
        action = 'SHOOT'
      else:
        action = 'RECHARGE'
    return action

  def updateUtilities(self,mdp):
    for state in mdp.states:
      s,a,h = state[0],state[1],state[2]

      #recharge
      rechargeVal = self.getRechargeVal(state,mdp)
      
      #shoot
      shootVal = self.getShootVal(state,mdp)

      #dodge
      dodgeVal = self.getDodgeVal(state,mdp)

      #action 
      action = self.getAction(dodgeVal, shootVal, rechargeVal)

      # updating
      '''
      ****   please verify once not sure how to handle terminal states   *****
      ****   also verify formula and related calculations once           *****
      '''
      val = float(mdp.gamma * max(self.dodgeCost + dodgeVal,self.shootCost + shootVal, self.rechargeCost + rechargeVal))
      if h==0:
        val = float(10)
        action = '-1'
      mdp.actionprime[state] = action
      mdp.utilityprime[state] = val
      
      print('('+str(int(s/50))+','+str(a)+','+str(int(h/25))+'):'+str(action)+'=['+str(round(mdp.utilityprime[state],3))+']')
      #uncommet for viewing update values tag:A
      # print('('+str(s)+','+str(a)+','+str(h)+'):\t'+str(action)+str(dodgeVal)+'\t'+str(shootVal)+'\t'+str(rechargeVal)+'\t'+str(mdp.utility[state])+'\t'+str(val))
      # print()
    pass


if __name__=="__main__":
  mdp = MDP(gamma=0.99,delta=0.001)
  game = Game(mdp,shootCost=-10, dodgeCost=-10, rechargeCost=-10)
  iterNum=1
  # print('Gamma = '+str(mdp.gamma)+'\tDelta = '+str(mdp.delta))
  while(mdp.isConverged()==False):
    print('iteration='+str(iterNum))

    #uncommet for viewing update values tag:A
    # print("State\t\tDV\tSV\tRV\tU\tVal")

    mdp.copyUtils()
    game.updateUtilities(mdp)
    iterNum+=1
    pass
  # tag: B final round 
  # mdp.round()
  # mdp.checkStatesAndUtilities()
  # print('Iterations for Convergence: '+str(iterNum-1)+"\nDONE")


    




