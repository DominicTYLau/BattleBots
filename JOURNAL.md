---
title: "Battle Bot"
author: "Dominic Lau"
description: "Two Battle Bots to break each other"
created_at: "2024-06-01"
---

## May 15, 2025

Highway was announced and it's a great time to make a project that I've always wanted. 2 BattleBots to break each other. The big challenge for this project is to make sure they both work in order to do damage.

I started by watching a lot of BattleBots and trying to find different designs from different weight classes. I then drew a couple designs that I liked.

![ideas](Images/Ideas/ideas.jpeg)

Time Spent: Around 1 hour

## May 16, 2025

Now that I had the idea, I wanted to determine how to build it. I first decided what main components I need to make this idea possible. Each robot needs to be controlled (user feedback), drive, and spin up a weapon system. Once I had an idea of the requirements, I made some high level diagrams to figure how to wire the robots. I also made a power distrubution diagram. This part is quite expensive because different components requires different voltages. In my past experiences, power is the hardest for the projects. This time, I want to wire as neatly as possible. I then broke the BOM into two main sections. Electoronics and Mechanical. After I listed everything I classified them into things I already have and things that I needed to buy. Afterwards, I went on amazon (cheapest and fastest place to get electronics for me) to find the items that I'm missing. I spent a lot of time trying to optimize the budget and keep the cost low. The current buy items are in [BOM.csv](./BOM.csv). 

![High Level Schematic](Images/Schematic/High_Level.jpeg)
![Power Distribution](Images/Schematic/Power.jpeg)
![Electrical BOM](Images/Ideas/Electrical_BOM.jpeg)
![Mechanical BOM](Images/Ideas/Mechanical_BOM.jpeg)

Time Spent: 3 hours

## May 17, 2025

Today I spent a lot of time cading out the design. I first started by 150 mm x 150 mm square and placed each component inside where I think would best fit. After I was happy with it I moved on making it 3D. I worked on the front where I had to learn how to create planes at angles to create the angled ramps at the front of the robot. I also caded up the weapon assembly for bot 1. For bot 2, I took similar layout from bot 1 and changed where the weapon is and its support.

![layout 1](Images/CAD/Layout_1.png)
![frame](Images/CAD/Frame.png)
![base](Images/CAD/Base.png)
![body](Images/CAD/Body.png)

Time Spent: 2.5 hours

## May 18, 2025

Once I had both chasis done, I decided to try and fit the components in the chassis. I followed my original layout and it worked pretty well. I also made the weapon assembly for bot 2. Most of the cad is done for bot 2. For bot 1 I added all the components but as I was adding a top I realized I made the chassis too short so I increased. However, this changed all my other values and so it looks like a mess right now. I’ll fix that for tomorrow and create a schematic.

![cad 1.1](Images/CAD/Full_Cad_1.1.png)
![cad 1.2](Images/CAD/Full_Cad_1.2.png)
![cad 1.3](Images/CAD/Full_Cad_1.3.png)
![problme](Images/CAD/Problem.png)

Time Spent: 3 hours

## May 19, 2025

I fixed up the bot 1 which took a while. I had to go back in the timeline and change a lot of parameters and remake the sketches.

![Robot 2](Images/CAD/Full_Cad_2.png)

Time Spent: 1 hour

## May 20, 2025

I made the schematic for the robot. I had to search a lot of the pinouts and I also finally figured out the motor controller for the drive wheels. I’ll be using the L293D which I already have. I also wrote some of the firmware for the pi and the arduino controller. I learned that it’s not a good idea to have the cg of the weapon away from the point of rotation. As a results, I remade it to change the cg position.

![weapon](Images/CAD/Weapon_1.png)
![Robot Schematic](Images/Schematic/Schematic_Robot.png)

Time Spent: 1.5 hour

## May 22, 2025

I made sure that my cad was correct with the right dimensions. I added some threads to the weapon system. I contacted places to get quotes for the cnc parts. 

![Threads](Images/CAD/Threads.png)

Time Spent: 0.5 hour 


## Jun 8, 2025

I got past the obstacle which was trying to lower the price. I removed some unneecessary parts. I'm still over, but I will pay it out of pocket. I also worked on schematic for the controller and that should be it.

![controller_schematic](Images/Schematic/controller_schematic.png)

Time Spent: 0.5 hour 
