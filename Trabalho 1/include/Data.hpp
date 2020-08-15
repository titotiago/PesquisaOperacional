#ifndef _DATA_H_
#define _DATA_H_

#include <vector>
#include <stdio.h>

class Data
{
   private:

      int nb_foods;
      int nb_nutrients;
      std::vector<std::vector<double> > food_nutr_levels;
      std::vector<double > min_nutr_levels;
      std::vector<double > food_costs;

   public:

      Data(char* filePath);

      int getNbFoods();

      int getNbNutrients();

      double getFoodNutritionalLevel(int food, int nutrient);

      double getFoodCost(int food);

      double getMinNutritionalLevel(int nutrient);
};

#endif

