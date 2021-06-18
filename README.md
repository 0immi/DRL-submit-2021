Autonomous Driving based on DQN

1. How to run the main file
- python ./main.py
<br>   
   
2. Dependencies
- Ubuntu 18.04
- PyTorch
- pygame
- matplotlib

<br> 
3. Description 
- main.py : main file for learning based on DQN<br> 
- env.py : overall autonmous driving environment based on pygame<br>
- GenerateCar.py : generate ego vehicle and update the states based on action learnt by DQN<br> 
- GenerateOtherCar.py : generate other vehicle and update the states based on each behavior(lane keep/slow)
<br> 
<br> 
4. Requirement
<br> for showing pygame simulation, need to download the images and modify the each directory in the code. <br> 
- bg.png: env.py -> line 35 <br> 
- car.png: GenerateCar.py -> line.26<br> 
- oppponent_car: GenerateOtherCar.py -> line.19<br> 
