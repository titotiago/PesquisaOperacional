from __future__ import print_function
from ortools.linear_solver import pywraplp
def main():
  f = open("instance7.txt")
  num_vertices = int(f.readline())
  num_arcos = int(f.readline())
  inic = int(f.readline())
  fim = int(f.readline())

  line = []
  supplies = []
  
  capacidades = [[0 for i in range(num_vertices)] for i in range(num_vertices)]
  variaveis = [[0 for i in range(num_vertices)] for i in range(num_vertices)]
  restricoes_arcos = [[0 for i in range(num_vertices)] for i in range(num_vertices)]
  fluxo = [0 for i in range(num_vertices)]
  unit_costs = [[0 for i in range(num_vertices)] for i in range(num_vertices)]

  #definindo a oferta e a demanda no começo e fim
  for i in range(0, num_vertices):
    if i == fim-1:
        supplies.append(99999)
    elif i == inic-1:
      supplies.append(-99999)
    else: 
      supplies.append(0)
  
  #Setando as infos 
  for i in range(0,int(num_arcos)):
      words = f.readline()
      for word in words.split():
        line.append(word)
      capacidades[int(line[0])-1][int(line[1])-1] = int(line[2])
      line = []
  
  solver = pywraplp.Solver('LinearProgrammingExample', pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)
  
  #adicionando o arco e colocando uma capacidade infinita + custo alto
  unit_costs[fim-1][inic-1] = -1
  capacidades[fim-1][inic-1] = solver.infinity()

  #definindo as variaveis no or tools
  for i in range(0,int(num_vertices)):
    for j in range(0,int(num_vertices)):
      if(capacidades[i][j] > 0): #se existe um arco
        variaveis[i][j] = solver.NumVar(0,solver.infinity(),'')


  # RESTRIÇÕES!
  #restrições de capacidade nos arcos    Xab < capacidade
  for i in range (0,int(num_vertices)):
    for j in range(0,int(num_vertices)):
      if(capacidades[i][j] > 0):
        restricoes_arcos[i][j] = solver.Constraint(0,capacidades[i][j])
        restricoes_arcos[i][j].SetCoefficient(variaveis[i][j],1)
  
  #restrições de conservação de fluxo
  for i in range (0, int(num_vertices)):
    #demanda do nó
    fluxo[i] = solver.Constraint(0, 0)
    
    # o que sai do nó
    for x in range (0, int(num_vertices)):
      if(capacidades[i][x] > 0 ): 
        fluxo[i].SetCoefficient(variaveis[i][x], -1)
   
    # o que entra no nó
    for y in range (0, int(num_vertices)):
      if(capacidades[y][i] > 0 ):
        fluxo[i].SetCoefficient(variaveis[y][i], 1)
    
  
  # FUNÇÃO OBJETIVO:
  objective = solver.Objective()
  for i in range(0, int(num_vertices)):
    for j in range(0, int(num_vertices)):
      if(capacidades[i][j] > 0):
        objective.SetCoefficient(variaveis[i][j], unit_costs[i][j])

  objective.SetMinimization()

  opt_solution = 0


  #solving
  status = solver.Solve()
  if status == solver.OPTIMAL:
    for i in range(0, int(num_vertices)):
      for j in range(0, int(num_vertices)):
        if(i!=fim-1 | j!=inic-1):
          if(capacidades[i][j] > 0 ):
              print('arco:',i+1,'-',j+1,' valor: ',variaveis[i][j].solution_value(), 'capacidade: ', capacidades[i][j] )
            
        opt_solution = variaveis[fim-1][inic-1].solution_value()
        
    # The value of each variable in the solution.
    print('Solution:')
    # The objective value of the solution.
    print('Optimal objective value =', opt_solution)
  
  else: 
    print("Sem solução")


  
if __name__ == '__main__':
  main()
