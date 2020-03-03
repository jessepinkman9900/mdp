from task1 import MDP, Game


if __name__=="__main__":
  mdp = MDP(gamma=0.99,delta=0.001)
  game = Game(mdp,shootCost=-0.25,rechargeCost=-2.5,dodgeCost=-2.5)
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
  #tag: B final round 
  # mdp.round()
  # mdp.checkStatesAndUtilities()
  # print('Iterations for Convergence: '+str(iterNum-1)+"\nDONE")

