#include "../include/Data.hpp"
#include <stdio.h>
#include <iostream>
#include <ilcplex/ilocplex.h>

void solve(Data& data);

int main(int argc, char** argv)
{
    if(argc != 2)
    {
        printf("Usage:\n./diet instance\n");
        return 0;
    }

    Data data(argv[1]);
    solve(data);

    return 0;
}

void solve(Data& data)
{
    IloEnv env;
    IloModel modelo(env);

    IloNumVarArray x(env, data.getNbFoods(), 0, IloInfinity);

    //adiciona a variavel x ao modelo
    for(int i = 0; i < data.getNbFoods(); i++)
    {
        char name[100];
        sprintf(name, "X(%d)", i);
        x[i].setName(name);
        modelo.add(x[i]);
    }

    ////////////////////////////////////////////////////////
    //Criando a Função Objetivo (FO) 
    IloExpr obj(env);
    for(int i = 0; i < data.getNbFoods(); i++)
    {
        obj += data.getFoodCost(i)*x[i];
    }
    // Adicionando a FO
    modelo.add(IloMinimize(env, obj));
    //////////////////////////////////////////////////////////

    ////////////////////////////////////////////////////////
    //Restricoes

    for(int i = 0; i < data.getNbNutrients(); i++) 
    {
        IloExpr sumX(env);
        for(int j = 0; j < data.getNbFoods(); j++)
        {
            sumX += data.getFoodNutritionalLevel(j,i)*x[j];
        }

        IloRange r = (sumX >= data.getMinNutritionalLevel(i));
        char name[100];
        sprintf(name, "NUTRIENT(%d)", i);
        r.setName(name);
        modelo.add(r);
    }


    //fim das restricoes
    ////////////////////////////////////////////////////////

    //resolve o modelo
    IloCplex diet(modelo);
    diet.setParam(IloCplex::TiLim, 2*60*60);
    diet.setParam(IloCplex::Threads, 1);
    diet.exportModel("modelo.lp");

    try
    {
        diet.solve();
    }
    catch(IloException& e)
    {
        std::cout << e;
    }

    std::cout << "status:" << diet.getStatus() << std::endl;
    std::cout << "custo da dieta:" << diet.getObjValue() << std::endl;
    for(int i = 0; i < data.getNbFoods(); i++) 
    {
        double value = diet.getValue(x[i]);
        if(value > 0.00001)
        {
            std::cout << "food " << i << ": " << value << std::endl;
        }
    }
}
