from __future__ import print_function
from ortools.linear_solver import pywraplp

def main():
  f = open("instance.txt")
  n = int(f.readline())
  m = int(f.readline())
  B = int(f.readline())
  T = int(f.readline())
  F = int(f.readline())

  line = []

  tabela = [[0 for i in range(n+2)] for i in range(m+4)]

  #setando os dados iniciais da tabela 
  for i in range(0,int(m)):
   line = f.readline()
   j = 0
   for s in line.split(' '):
    num = float(s)
    tabela[i][j] = num
    j += 1

  for i in range(m, int(m+4)):
   line = f.readline()
   j = 0
   for s in line.split(' '):
    num = float(s)
    tabela[i][j] = num
    j += 1

  # Create the mip solver with the CBC backend.
  solver = pywraplp.Solver.CreateSolver('simple_mip_program', 'CBC')

  infinity = solver.infinity()
  precos = tabela[m+3] #preços finais



  #variaveis do solver
  produtos = [0 for i in range(n)] #quantidades de cada produto
  n_lotes = [0 for i in range(m)] #numero de lotes de cada material
  booleanos = [0 for i in range(n)] #Variaveis bool
  
  for i in range(n):
    booleanos[i] = solver.IntVar(0,1,'bool'+str(i))

  for i in range(0,n):
   produtos[i] = solver.IntVar(0.0, infinity, str(i))
  
  for i in range(m):
   n_lotes[i] = solver.IntVar(0.0,infinity, '')
  

  # Definindo Booleanos
  for i in range(n): # dmax*booleanos >= produtos
   constraint = solver.RowConstraint(0,infinity,'')
   constraint.SetCoefficient(produtos[i],-1)
   constraint.SetCoefficient(booleanos[i],tabela[m+2][i])

  for i in range(n): # produtos >= booleanos
    constraint = solver.RowConstraint(-infinity,0,'')
    constraint.SetCoefficient(booleanos[i],1)
    constraint.SetCoefficient(produtos[i],-1)



  #Restrições de demanda

  for i in range(n): #restrições de demanda max -- produtos[i] <= dmax
   constraint = solver.RowConstraint(0, tabela[m+2][i], '')  
   constraint.SetCoefficient(produtos[i], 1)


  for i in range(n): #restrições de demanda min -- produtos[i] >= dmin*booleano
    constraint = solver.RowConstraint(0,infinity,'')
    constraint.SetCoefficient(produtos[i],1)
    constraint.SetCoefficient(booleanos[i],-tabela[m+1][i])



  #Restrição do somatório de horas
  constraint = solver.RowConstraint(0,B,'')
  for i in range(n):
   constraint.SetCoefficient(booleanos[i],T)  #Decrementando quando troca de produção
   constraint.SetCoefficient(produtos[i],tabela[m][i])
  

  # Restrição de quantidade de cada material
  for i in range(m):  #produto*qtd_material <= N_lotes*tamanho_lote 
    constraint = solver.RowConstraint(0,tabela[i][n]-1,'')
    constraint.SetCoefficient(n_lotes[i],-tabela[i][n])
    for j in range(n):
     constraint.SetCoefficient(produtos[j],tabela[i][j])


  #Função objetivo
  #max SVx*px - F - SN_lotes*Cx 
  objective = solver.Objective()
  for i in range(n):
   objective.SetCoefficient(produtos[i], precos[i])

  for i in range(m):
   objective.SetCoefficient(n_lotes[i], -tabela[i][n+1])
  
  #Solve
  objective.SetMaximization()
  status = solver.Solve()

  if status == pywraplp.Solver.OPTIMAL:
   Solucao = solver.Objective().Value() - F
   print ("----------- SOLUÇÃO -----------")
   if(Solucao >= 0):
    print('Lucro =', Solucao, "Reais")
   else:
     print('Prejuizo = ', Solucao)
   print("\n")
   horas = 0
   horas_troca = 0
   for j in range(n):
    horas_prod = produtos[j].solution_value()*tabela[m][j]
    horas_troca += T*booleanos[j].solution_value()
    horas+= horas_prod 
    print("> Produto ", produtos[j].name(), ' = ', produtos[j].solution_value(),"Unidades produzidas", " - Horas Utilizadas:", horas_prod)
   print("\n")
   for i in range(m):
    print("> Foram comprados",n_lotes[i].solution_value(), "lotes do material", i)
  
   print("\nHoras fazendo trocas:", horas_troca)
   print("\nTotal de Horas: ", horas+horas_troca, "/", B )
   print()
   print('Problem solved in %f milliseconds' % solver.wall_time())
   print('Problem solved in %d iterations' % solver.iterations())
   print('Problem solved in %d branch-and-bound nodes' % solver.nodes())
  else:
   print('The problem does not have an optimal solution.')


  
if __name__ == '__main__':
  main()
