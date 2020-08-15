#include "../include/Data.hpp"
#include <stdlib.h>

Data::Data(char* filePath)
{
    FILE* f = fopen(filePath, "r");

    if(!f)
    {
        printf("Problem while reading instance 1.\n");
        exit(1);
    }

    if(fscanf(f, "%d %d", &nb_foods, &nb_nutrients) != 2)
    {
        printf("Problem while reading instance.2\n");
        exit(1);
    }

    //reading costs
    food_costs = std::vector<double>(nb_foods);
    for(int i = 0; i < nb_foods; i++)
    {
        if(fscanf(f, "%lf", &food_costs[i]) != 1)
        {
            printf("Problem while reading instance.3\n");
            exit(1);
        }
    }

    //reading minimum nutritional levels
    min_nutr_levels = std::vector<double>(nb_nutrients);
    for(int i = 0; i < nb_nutrients; i++)
    {
        if(fscanf(f, "%lf", &min_nutr_levels[i]) != 1)
        {
            printf("Problem while reading instance.4\n");
            exit(1);
        }
    }

    //reading food X nutrient matrix
    food_nutr_levels = std::vector<std::vector<double> >(nb_foods, std::vector<double>(nb_nutrients));
    for(int i = 0; i < nb_foods; i++)
    {
        for(int j = 0; j < nb_nutrients; j++)
        {
            if(fscanf(f, "%lf", &food_nutr_levels[i][j]) != 1)
            {
                printf("Problem while reading instance.5\n");
                exit(1);
            }
        }
    }

    fclose(f);
}

int Data::getNbFoods()
{
    return nb_foods;
}

int Data::getNbNutrients()
{
    return nb_nutrients;
}

double Data::getFoodNutritionalLevel(int food, int nutrient)
{
    return food_nutr_levels[food][nutrient];
}

double Data::getFoodCost(int food)
{
    return food_costs[food];
}

double Data::getMinNutritionalLevel(int nutrient)
{
    return min_nutr_levels[nutrient];
}
