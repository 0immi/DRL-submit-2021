Autonomous Driving based on DQN

1. Run the main file
   python ./main.py
   
   
2.Dependencies
- Ubuntu 18.04
- PyTorch
- pygame
- matplotlib


3. Description 
- main.py : main file for learning based on DQN
- env.py : overall autonmous driving environment based on pygame
- GenerateCar.py : generate ego vehicle and update the states based on action learnt by DQN
- GenerateOtherCar.py : generate other vehicle and update the states based on each behavior(lane keep/slow)

**for showing pygame simulation, need to download the images and modify the each directory in the code. 
**bg.png: env.py -> line 35 
**car.png: GenerateCar.py -> line.26
**oppponent_car: GenerateOtherCar.py -> line.19
