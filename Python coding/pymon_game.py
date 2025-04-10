


import random


# Random generator to generate random numbers to assign the Pymon to random locations
def generate_random_number(max_number = 1):
    r = random.randint(0,max_number)
    return r 

# Exception class for directions containing no locations
class InvalidDirectionException(Exception):
    def __init__(self, direction):
        self.message=f"The selected {direction} direction has no location attached to it!"
        super().__init__(self.message)

# Exception class for invalid format of the input file   
class InvalidInputFileFormat(Exception):
    def __init__(self, filename):
        self.message=f"Invalid content or in incorrect format in {filename}!"
        super().__init__(self.message)

# Class for creature
class Creature:
    def __init__(self, name, description,adoptable, current_location=''):
        self.name=name
        self.description=description
        self.current_location=current_location
        self.adoptable=adoptable
    def get_name(self):
        return self.name
    def get_location(self):
        return self.current_location

from datetime import datetime
#Class for Pymon
class Pymon(Creature):
    def __init__(self, name = "The player",description='',current_location='',energy=3):
        super().__init__(name,description, current_location)        
        self.energy=energy
        self.move_count=0
        self.battle_record=[]
        self.total_win_counts=0
        self.total_draws_counts=0
        self.total_lose_counts=0
    
    # Helps to increase the step count
    def add_move_count(self, step):
        self.move_count=self.move_count+step
    
    def get_energy(self):
        return self.energy
    
    def set_energy(self,energy):
        self.energy=energy
    
    #Function used to move the Pymon to different locations
    def move(self, direction = None):
        
        if self.current_location != None:          
            comp="None"  
            if self.current_location.doors[direction].strip().lower() != comp.strip().lower():
                
                loc=self.current_location.doors[direction]                
                for location in Record.locations:                               
                    if location.name.strip().lower()==loc.strip().lower():                        
                        self.current_location.remove_creature(self)
                        self.current_location=location      
                        location.add_creature(self)  
                        self.add_move_count(1) 

                        #Helps to reduce energy after every 2 moves 
                        if self.move_count%2==0:
                            self.energy=self.energy-1      
                        return 1
            else:
                raise InvalidDirectionException(direction)
                
        
        
    
    def pymon_stats(self):
        print(f"Hi Player. My name is {self.name}. I am{self.description}. My energy is {self.energy}/3. What can I do to help you?")

    #Used to spawn the pymon to random locations           
    def spawn(self, loc):
        if loc != None:
            loc.add_creature(self)
            self.current_location = loc
            self.current_location.add_creature(self)

    #Generating battle statistics for each pymon
    def battle_stats(self,opponent_name,draws_count,lose_count,wins_count):
        date_of_battle=datetime.now().strftime("%d/%m/%Y %I:%M %p")

        battle_log={
            "Date":date_of_battle,
            "Opponent":opponent_name,
            "W":wins_count,
            "D":draws_count,
            "L":lose_count
        }
        self.battle_record.append(battle_log)

        self.total_win_counts+=wins_count
        self.total_lose_counts+=lose_count
        self.total_draws_counts+=draws_count

    #Displaying the battle statistics
    def display_battle_stats(self):
        battle_no=1
        print(f"Pymon Nickname: {self.name}")
        for battle in self.battle_record:
            print(f"Battle {battle_no}, {battle['Date'] } Opponent: {battle['Opponent'] }, W: {battle['W'] }, D: {battle['D'] }, L: {battle['L'] }")
            battle_no+=1
        
        print(f"Total: W: {self.total_win_counts}, D: {self.total_draws_counts}, L: {self.total_lose_counts},")
    
    

            
    


    
        

# Class for location          
class Location:
    def __init__(self, name = "New room",description='', w = None, n = None , e = None, s = None):
        self.name = name
        self.description=description
        self.doors = {}
        self.doors["west"] = w
        self.doors["north"] = n
        self.doors["east"] = e
        self.doors["south"] = s
        self.creatures = []
        self.items = []        
        
    def add_creature(self, creature):
        self.creatures.append(creature)
        
             
    def get_creatures(self):
        return self.creatures
    
    #Helps to remove creatures from the list
    def remove_creature(self,creature):
        self.creatures.remove(creature)

    #Function helps to add items to the list  
    def add_item(self, item):
        self.items.append(item)
    
    #Function helps to remove items to the list 
    def remove_item(self, item):
        self.items.remove(item)
       
    
    def get_items(self):
        return self.items
        
    def connect_east(self, another_room):
        self.doors["east"] = another_room 
        another_room.doors["west"]  = self;
        
    def connect_west(self, another_room):
        self.doors["west"] = another_room 
        another_room.doors["east"]  = self;
    
    def connect_north(self, another_room):
        self.doors["north"] = another_room 
        another_room.doors["south"]  = self;
        
    def connect_south(self, another_room):
        self.doors["south"] = another_room 
        another_room.doors["north"]  = self;
        
    def get_name(self):
        return self.name
        
    

#Class for items
class Item:
    def __init__(self, name, description, pickable,consumable):
        self.name=name
        self.description=description
        self.pickable=pickable
        self.consumable=consumable
    def get_name(self):
        return self.name

    def get_pickable(self):
        return self.pickable
        
#Class for records  of creatures, items, inventory and location     
class Record:
    def __init__(self):
        self.location_temp=[]
        Record.locations = []
        Record.creatures=[]
        Record.items=[]
        Record.inventory=[]
        Record.pymon_list=[]
        #This copy list was used so as to keep track of all the Pymons ever captured so as to generate its Battle statistics
        Record.pymon_list_copy=[]
        Record.potion_status=0


    def import_location(self):

        i=0
        #IMporting from the locations csv file
        import os        
        directory=directory = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__))).replace("\\","/")
        location=directory+"/"+  "locations.csv"
        with open(os.path.join(directory, location), mode='r', newline='') as source:
            p=0
            #Making sure that the format is right and the header row is not read in
            for l in source:    
                if p==0:
                    location_check = l.strip().split(',') 
                    correct_format_location=['name', 'description', 'west', 'north', 'east', 'south']
                    
                    if location_check!=correct_format_location:
                        raise InvalidInputFileFormat("locations.csv")
                    p=1
                    continue   
                else:
                    location_name = l.strip().split(',')      
                    self.location_temp.append(location_name)                
                    self.location_temp[i][2].replace(" ","").strip()
                    self.location_temp[i][3].replace(" ","").strip()  
                    self.location_temp[i][4].replace(" ","").strip()             
                    self.location_temp[i][5].replace(" ","").strip()  
                    

                    temp1=Location(self.location_temp[i][0],self.location_temp[i][1],self.location_temp[i][2],self.location_temp[i][3],self.location_temp[i][4],self.location_temp[i][5])
                    Record.locations.append(temp1)
                    i+=1
           

        
    def get_locations(self):
        return Record.locations
    

    def import_creatures(self):
        i=0
        self.creatures=[]
        import os        
        directory=directory = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__))).replace("\\","/")
        creature=directory+"/"+  "creatures.csv"
        #To import the creatures csv file
        with open(os.path.join(directory, creature), mode='r', newline='') as source:
            p=0
            for l in source:  
                #To make sure that the header format is right and the header is not read in
                if p==0:
                    creature_check = l.strip().split(',') 
                    correct_format_creature=['name', ' description', ' adoptable']
                    if creature_check!=correct_format_creature:
                        raise InvalidInputFileFormat("creatures.csv")
                    p=1
                    continue   
                else:                             
                    creature_name = l.strip().split(',') 
                    self.creatures.append(creature_name)
                    if self.creatures[i][0]=="Kitimon":
                        for location in Record.locations:
                            if location.name=="Playground":
                                temp1=Creature(self.creatures[i][0],self.creatures[i][1],self.creatures[i][2],location)
                                location.add_creature(temp1)
                                Record.creatures.append(temp1)
                    elif self.creatures[i][0]=="Sheep":
                        for location in Record.locations:
                            if location.name=="Beach":
                                temp1=Creature(self.creatures[i][0],self.creatures[i][1],self.creatures[i][2],location)
                                location.add_creature(temp1)
                                Record.creatures.append(temp1)
                    elif self.creatures[i][0]=="Marimon":
                        for location in Record.locations:
                            if location.name=="School":
                                temp1=Creature(self.creatures[i][0],self.creatures[i][1],self.creatures[i][2],location)
                                location.add_creature(temp1)
                                Record.creatures.append(temp1)
                    i+=1

        

    def import_items(self):
        
        i=0
        self.items=[]
        import os        
        directory=directory = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__))).replace("\\","/")
        items=directory+"/"+  "items.csv"
        #To import the items csv file
        with open(os.path.join(directory, items), mode='r', newline='') as source:
            p=0
            for l in source:
                #To make sure that the header format is right and the header is not read in
                if p==0:
                    items_check = l.strip().split(',') 
                    correct_format_items=['name', ' description', ' pickable', ' consumable']
                    if items_check!=correct_format_items:
                        raise InvalidInputFileFormat("items.csv")
                    p=1
                    continue   
                else:                                
                    item_name = l.strip().split(',') 
                    self.items.append(item_name)
                    if self.items[i][0].lower()=="tree" or self.items[i][0].lower()=="potion":
                        for location in Record.locations:
                            if location.name=="Playground":
                                temp1=Item(self.items[i][0],self.items[i][1],self.items[i][2],self.items[i][3])
                                location.add_item(temp1)
                                Record.items.append(temp1)
                    elif self.items[i][0].lower()=="apple":
                        for location in Record.locations:
                            if location.name=="Beach":
                                temp1=Item(self.items[i][0],self.items[i][1],self.items[i][2],self.items[i][3])
                                location.add_item(temp1)
                                Record.items.append(temp1)
                    elif self.items[i][0]=="binocular":
                        for location in Record.locations:
                            if location.name=="School":
                                temp1=Item(self.items[i][0],self.items[i][1],self.items[i][2],self.items[i][3])
                                location.add_item(temp1)
                                Record.items.append(temp1)
                    i+=1
        

#Class for operations such as battle between Pymons
class Operation:

    def __init__(self):
        self.locations = []
        self.current_pymon = Pymon("Kimimon"," white and yellow with a square face")
        
    
    def battle(self):
        
        flag=0
        #List keeps the three moves of the oponents which is chosen randomly
        
        oponent_attacks=['paper','rock','scissor']
        option_creature=input("Which creature do you want to battle?: ")
        for creature in Pymon.get_location(self.current_pymon).get_creatures():                    
                    if (option_creature.lower()==creature.get_name().lower()) and ("Pymon" in creature.description):
                        print("")
                        print(f"{creature.name} has accepted your battle challenge! Ready for the battle!")
                        print("The Pymon to win 2 of the encounters will win the battle!")                        
                        print("")         
                        flag=1              

                        print("")
                        break
                    elif ("Pymon" not in creature.description):
                        print("Creature cannot be challenged!")
                        print("") 
                        break
                    else:
                        print("Creature not present at the location!")   
                            
                        print("") 
                        break
        if flag==1:


            i=0
            score=0
            draw_count=0
            lose_count=0
            win_count=0
            
            
            while i <=3:
                a_random_attack = generate_random_number(len(oponent_attacks)-1)

                oponent_input=oponent_attacks[a_random_attack]
                print("Encounter begins....")
                #User can enter starting letter or the whole word as input
                game_input=input("Your turn (r)ock),(p)aper), or (s)cissor)?: ")
                if game_input.lower()=="r" or game_input.lower()=="rock":
                    print("You issued a rock!")
                elif game_input.lower()=="p" or game_input.lower()=="paper":
                    print("You issued a paper!")
                elif game_input.lower()=="s" or game_input.lower()=="scissor":
                    print("You issued a scissor!")
                

                

                print(f"Your opponent issued a {oponent_input}!")
                
                #For draw the outcome is noted
                if (game_input.lower()=="r" or game_input.lower()=="rock") and (oponent_input=="rock"):
                    game_input="rock"
                    outcome_round="draw"
                    draw_count+=1
                #For losing outcome the energy is decreased by one if there is no magic potion in play and score is reduced by 1
                elif (game_input.lower()=="r" or game_input.lower()=="rock") and (oponent_input=="paper"):
                    game_input="rock"
                    outcome_round="lose"
                    if Record.potion_status==1:
                        print("1 energy will not be reduced as Pymon is Potion Protected!")
                        Record.potion_status=0
                    else:
                        self.current_pymon.set_energy(self.current_pymon.get_energy()-1)
                    i+=1
                    score-=1
                    lose_count+=1
                #For winning outcome the energy is increased by one and score is increased by 1
                elif (game_input.lower()=="r" or game_input.lower()=="rock") and (oponent_input=="scissor"):
                    game_input="rock"
                    outcome_round="win"
                    i+=1
                    score+=1
                    win_count+=1
                elif (game_input.lower()=="p" or game_input.lower()=="paper") and (oponent_input=="paper"):
                    game_input="paper"
                    outcome_round="draw"
                    draw_count+=1
                elif (game_input.lower()=="p" or game_input.lower()=="paper") and (oponent_input=="rock"):
                    game_input="paper"
                    outcome_round="win"
                    i+=1
                    score+=1
                    win_count+=1
                elif (game_input.lower()=="p" or game_input.lower()=="paper") and (oponent_input=="scissor"):
                    game_input="paper"
                    outcome_round="lose"
                    if Record.potion_status==1:
                        print("1 energy will not be reduced as Pymon is Potion Protected!")
                        Record.potion_status=0
                    else:
                        self.current_pymon.set_energy(self.current_pymon.get_energy()-1)
                    i+=1
                    score-=1
                    lose_count+=1
                elif (game_input.lower()=="s" or game_input.lower()=="scissor") and (oponent_input=="scissor"):
                    game_input="scissor"
                    outcome_round="draw"
                    draw_count+=1
                elif (game_input.lower()=="s" or game_input.lower()=="scissor") and (oponent_input=="rock"):
                    game_input="scissor"
                    outcome_round="lose"
                    if Record.potion_status==1:
                        print("1 energy will not be reduced as Pymon is Potion Protected!")
                        Record.potion_status=0
                    else:
                        self.current_pymon.set_energy(self.current_pymon.get_energy()-1)
                    i+=1
                    score-=1
                    lose_count+=1
                elif (game_input.lower()=="s" or game_input.lower()=="scissor") and (oponent_input=="paper"):
                    game_input="scissor"
                    outcome_round="win"
                    i+=1
                    score+=1
                    win_count+=1
                
                if outcome_round=="win":
                    print(f"{game_input} vs {oponent_input}: {game_input} wins! You have won this encounter!")
                elif outcome_round=="lose":
                    print(f"{game_input} vs {oponent_input}: {oponent_input} wins! You have lost this encounter and lost 1 energy!")
                elif outcome_round=="draw":
                    print(f"{game_input} vs {oponent_input}: Draw! One more encounter!")
                
                if score==2 and i==2:
                    print("You won two encounters!")
                    print(f"Congrats! You have won the battle and adopted a new Pymon called {creature.name}!")
                    #Making sure the potins effect is taken off with this flag
                    if Record.potion_status==1:
                        Record.potion_status=0
                    self.current_pymon.battle_stats(option_creature,draw_count,lose_count,win_count)
                    new_pymon=Pymon(creature.name,creature.description)
                    #Adding the new defeated Pymon to the list
                    Record.pymon_list.append(new_pymon)
                    Record.pymon_list_copy.append(new_pymon)

                    #Removing theacquired Pymon from its current location
                    for location in Record.locations:                                        
                        if location.name==Pymon.get_location(self.current_pymon).name:
                            creature.current_location.remove_creature(creature)                            
                    break
                if score>0 and i==3:
                    print(f"Congrats! You have won the battle and adopted a new Pymon called {creature.name}!")
                    self.current_pymon.battle_stats(option_creature,draw_count,lose_count,win_count)
                    new_pymon=Pymon(creature.name,creature.description)
                    #Adding the new defeated Pymon to the list
                    Record.pymon_list.append(new_pymon)
                    Record.pymon_list_copy.append(new_pymon)
                    #Making sure the potins effect is taken off with this flag
                    if Record.potion_status==1:
                        Record.potion_status=0
                    
                    #Removing theacquired Pymon from its current location
                    for location in Record.locations:                    
                        if location.name==Pymon.get_location(self.current_pymon).name:
                            creature.current_location.remove_creature(creature)                    
                    break
                        
                if (score<0 and (i==2 or i==3)) or self.current_pymon.get_energy()==0:
                    print(f"You have lost the battle and released your current Pymon to the wild!")
                    self.current_pymon.battle_stats(option_creature,draw_count,lose_count,win_count)

                    #Removing the Pymon from the list since it lost
                    Record.pymon_list.remove(self.current_pymon)

                    #Assigning the current location to the Pymon left in the list
                    if len(Record.pymon_list)>0:
                        Record.pymon_list[0].current_location=self.current_pymon.current_location

                    #Making sure the potins effect is taken off with this flag
                    if Record.potion_status==1:
                        Record.potion_status=0
                    
                    #Current Pymon is moved to a random locatin into the wild with energy=3
                    a_random_number = generate_random_number(len(self.locations)-1)        
                    spawned_loc = self.locations[a_random_number]
                    self.current_pymon.set_energy(3)
                    self.current_pymon.current_location.remove_creature(self.current_pymon)
                    self.current_pymon.spawn(spawned_loc)

                    #Assigning the next Pymon if available as the current Pymon
                    if len(Record.pymon_list)>0:
                        self.current_pymon=Record.pymon_list[0]
                        self.current_pymon.current_location.add_creature(self.current_pymon)
                    else:
                        print("Game Over!!!!!")
                        sys.exit()
                    break

    


        

    #Function for game menu
    def handle_menu(self):
        Operation.flag=0
        while Operation.flag==0:                   
            print("Please issue a command to your Pymon:")
            print("1) Inspect Pymon")
            print("2) Inspect current location")
            print("3) Move")
            print("4) Pick an Item")
            print("5) View inventory")
            print("6) Challenge a creature")
            print("7) Generate stats")
            print("8) Exit the program")
            
            
            option=input("Your command:")
            
            #If string input is given it redirects the user to give correct input            
            try:
                option=int(option)
            except:
                option=100

            #Option for inspecting the current Pymon and to see the list of all the available Pymons
            if option==1:
                print("")
                print("1) Inspect current Pymon")
                print("2) List and select a benched Pymon to use")
                option_sub=int(input("Your command:"))

                if option_sub==1:
                    Pymon.pymon_stats(self.current_pymon)

                elif option_sub==2:
                    print("The avaialble Pymmons are: ")
                    for creatures in Record.pymon_list:
                        print(creatures.name)
                    if len(Record.pymon_list)>1:
                        t=0

                        #To swap the Pymon
                        while t==0:
                            choice=input("Do you want to swap(y/n)?")

                            if choice.lower() =='y':
                                pymon_chosen=input("Which Pymon would you like to swap to?: ")

                                #To assign the current Pymon location to the chosen swap Pymon, also removing the current Pymon from the location and adding the selected Pymon to the location
                                creature_flag=0
                                for creatures in Record.pymon_list:
                                    if pymon_chosen.lower()==creatures.name.lower():
                                        location_temp=self.current_pymon.current_location
                                        self.current_pymon.current_location.remove_creature(self.current_pymon)                                         
                                        self.current_pymon=creatures  
                                        self.current_pymon.current_location=location_temp
                                        self.current_pymon.current_location.add_creature(self.current_pymon)     
                                        creature_flag=1                                 
                                        break
                                if creature_flag==0:
                                    print("Creature not present!")
                                print("")
                                print("Swap successful!")

                                t=1

                            elif choice.lower()=='n':
                                print("Sure! Swap not done!")
                                t=1
                            else:
                                print("Type correct input!")
                else:
                    Operation.handle_menu(self)

            #To get information on the current location such as creatures present, items in location  
            elif option==2:
                location=Pymon.get_location(self.current_pymon)
                print(f"You are at a {self.current_pymon.current_location.get_name()}, {self.current_pymon.current_location.description}")
                print("")
                print(f"Creatures in this location:")
                set_temp=set(self.current_pymon.current_location.get_creatures())
                for creatures in set_temp:                    
                    print(creatures.get_name())
                print("")
                
                print(f"Items in this location:")
                for items in self.current_pymon.current_location.get_items():                    
                    print(items.get_name())
                print("")

            #To move the Pymon to a different location
            elif option==3:
                option_direction=input("Moving to which direction?:")
                pymon_creature=self.current_pymon  

                try:
                    flg=Pymon.move(pymon_creature,option_direction.lower())                    
                    if flg==1:
                        
                        print(f"You travelled {option_direction} and arrived at a {Pymon.get_location(self.current_pymon).get_name()}")
                        print("")
                
                    #To make sure that the current pymon is removed and moved to a random location if its energy equals zero
                    if self.current_pymon.energy==0:
                        Record.pymon_list.remove(self.current_pymon)
                        if len(Record.pymon_list)>0:
                            Record.pymon_list[0].current_location=self.current_pymon.current_location
                        a_random_number = generate_random_number(len(self.locations)-1)        
                        spawned_loc = self.locations[a_random_number]
                        self.current_pymon.set_energy(3)
                        self.current_pymon.current_location.remove_creature(self.current_pymon)
                        self.current_pymon.spawn(spawned_loc)

                        if len(Record.pymon_list)>0:
                            self.current_pymon=Record.pymon_list[0]
                            self.current_pymon.current_location.add_creature(self.current_pymon)
                        else:
                            print("Game Over!!!!!")
                            sys.exit()

                #Raising an exception if there is no location attached to the direction  
                except InvalidDirectionException as error:
                    print(error)
                    print("")
                    
            #To pick an item from a location that is pickable
            elif option==4:
                option_item=input("What item would you like to pick?: ")
                for items in Pymon.get_location(self.current_pymon).get_items():                    
                    if option_item==items.get_name() and items.get_pickable().strip()=="yes":
                        Record.inventory.append(items)
                        print(f"You picked up a {option_item}!")
                        Pymon.get_location(self.current_pymon).remove_item(items)
                        print("")
                        break

                    elif option_item==items.get_name() and items.get_pickable().strip()!="yes":
                        print("The item is not pickable!")
                        print("")

                    else:
                        print("The item is not at the location!")       
                        print("")  

            #To see the items that was picked which was added into a list
            elif option==5:
                print("The items you are carrying: ")
                for items in Record.inventory:                    
                    print(items.get_name())
                print("")
                
                #To select an item from the list if there are any items present in the list
                if len(Record.inventory)>0:
                    option_item_selected=input("Select item to use: ")
                    for items in Record.inventory:   

                        #Apple gives one bar of energy if the energy is not equal to 3                 
                        if option_item_selected.lower()==items.name.lower():
                            if option_item_selected.lower()=="apple":
                                
                                if self.current_pymon.energy==3:
                                    print("Energy full and cannot be increased!")
                                else:
                                    Record.inventory.remove(items)
                                    self.current_pymon.energy=self.current_pymon.energy+1
                                    print("Energy restored by one!")
                                    print("")
                                
                            #Magic potion gives immunity for one encounter loss with the help of th epotion_status flag
                            elif option_item_selected.lower()=="potion":
                                Record.potion_status=1
                                Record.inventory.remove(items)
                                print("Magic potion activated for next battle!")
                                print("")

                            #Binocular helps to get a summary of the current location or other connected locations
                            elif option_item_selected.lower()=="binocular":
                                print("Current")
                                print("West")
                                print("North")
                                print("East")
                                print("South")
                                binocular_option=input("Select which would yo like to see more of?: ")
                                items_temp=[]
                                creature_temp=[]
                                dir_temp=[]

                                if binocular_option.lower()=="current":                                    
                                    for items in self.current_pymon.current_location.get_items():   
                                        items_temp.append(items.get_name())       
                                    set_temp=set(self.current_pymon.current_location.get_creatures())
                                    for creatures in set_temp: 
                                        if creatures.get_name().lower()!=self.current_pymon.name.lower():
                                            creature_temp.append(creatures.get_name())           
                                    
                                    #This helps to add only locations which has locations attached to it
                                    if self.current_pymon.current_location.doors["west"].strip()!="None":
                                        temp="West: "+ self.current_pymon.current_location.doors["west"]
                                        dir_temp.append(temp)
                                    if self.current_pymon.current_location.doors["east"].strip()!="None":
                                        temp="East: "+ self.current_pymon.current_location.doors["east"]
                                        dir_temp.append(temp)
                                    if self.current_pymon.current_location.doors["north"].strip()!="None":
                                        temp="North: "+ self.current_pymon.current_location.doors["north"]
                                        dir_temp.append(temp)
                                    if self.current_pymon.current_location.doors["south"].strip()!="None":
                                        temp="South: "+ self.current_pymon.current_location.doors["south"]
                                        dir_temp.append(temp)                                        
                
                                    print(f"Location contains the items {items_temp}, creatures {creature_temp}, different locations at {dir_temp}")
                                
                                #Helps to see information in the west side of the current location
                                elif binocular_option.lower()=="west": 
                                    if self.current_pymon.current_location.doors["west"].strip()!="None":
                                        for location in Record.locations:   
                                            if location.name.strip().lower()==self.current_pymon.current_location.doors["west"].strip().lower():
                                                temp_name_loc=location

                                        #Items in the west side of the location
                                        for items in temp_name_loc.get_items():
                                            items_temp.append(items.get_name())       
                                        set_temp=set(temp_name_loc.get_creatures())

                                        #Creatures in the west side of the location
                                        for creatures in set_temp: 
                                            if creatures.get_name().lower()!=self.current_pymon.name.lower():
                                                creature_temp.append(creatures.get_name())  

                                        print(f"The west leads to {temp_name_loc.name} and contains the items {items_temp}, creatures {creature_temp}")

                                    elif self.current_pymon.current_location.doors["west"].strip()=="None":
                                        print("This direction leads nowhere!")
                                
                                #Helps to see information in the east side of the current location
                                elif binocular_option.lower()=="east": 
                                    if self.current_pymon.current_location.doors["east"].strip()!="None":
                                        for location in Record.locations:   
                                            if location.name.strip().lower()==self.current_pymon.current_location.doors["east"].strip().lower():
                                                temp_name_loc=location

                                        #Items in the east side of the location
                                        for items in temp_name_loc.get_items():
                                            items_temp.append(items.get_name())       
                                        set_temp=set(temp_name_loc.get_creatures())

                                        #Creatures in the east side of the location
                                        for creatures in set_temp: 
                                            if creatures.get_name().lower()!=self.current_pymon.name.lower():
                                                creature_temp.append(creatures.get_name())  

                                        print(f"The east leads to {temp_name_loc.name} and contains the items {items_temp}, creatures {creature_temp}")

                                    elif self.current_pymon.current_location.doors["east"].strip()=="None":
                                        print("This direction leads nowhere!")

                                #Helps to see information in the north side of the current location
                                elif binocular_option.lower()=="north": 
                                    if self.current_pymon.current_location.doors["north"].strip()!="None":
                                        for location in Record.locations:   
                                            if location.name.strip().lower()==self.current_pymon.current_location.doors["north"].strip().lower():
                                                temp_name_loc=location

                                        #Items in the north side of the location
                                        for items in temp_name_loc.get_items():
                                            items_temp.append(items.get_name())       
                                        set_temp=set(temp_name_loc.get_creatures())

                                        #Creatures in the north side of the location
                                        for creatures in set_temp: 
                                            if creatures.get_name().lower()!=self.current_pymon.name.lower():
                                                creature_temp.append(creatures.get_name())  

                                        print(f"The north leads to {temp_name_loc.name} and contains the items {items_temp}, creatures {creature_temp}")

                                    elif self.current_pymon.current_location.doors["north"].strip()=="None":
                                        print("This direction leads nowhere!")

                                #Helps to see information in the south side of the current location
                                elif binocular_option.lower()=="south": 
                                    if self.current_pymon.current_location.doors["south"].strip()!="None":
                                        for location in Record.locations:   
                                            if location.name.strip().lower()==self.current_pymon.current_location.doors["south"].strip().lower():
                                                temp_name_loc=location

                                        #Items in the south side of the location
                                        for items in temp_name_loc.get_items():
                                            items_temp.append(items.get_name())       
                                        set_temp=set(temp_name_loc.get_creatures())

                                        #Creatures in the south side of the location
                                        for creatures in set_temp: 
                                            if creatures.get_name().lower()!=self.current_pymon.name.lower():
                                                creature_temp.append(creatures.get_name())  

                                        print(f"The south leads to {temp_name_loc.name} and contains the items {items_temp}, creatures {creature_temp}")

                                    elif self.current_pymon.current_location.doors["south"].strip()=="None":
                                        print("This direction leads nowhere!")
                                
            #To battle with a Pymon in the location which can be fought with
            elif option==6:
                Operation.battle(self)

            elif option==7:
                print("----------------------")
                for pymon in Record.pymon_list_copy:
                    pymon.display_battle_stats()
                    print("----------------------")

            #To exit the program
            elif option==8:
                Operation.flag=1
            
            else:
                print("Enter correct input!")
               
    
      
    def setup(self):
        record = Record()
        try:
            record.import_location()
            record.import_creatures()
            record.import_items()
        except InvalidInputFileFormat as error:
            print(error)
            print("Exiting program please check file and do the needful!")
            sys.exit()

        for location in record.get_locations():
            self.locations.append(location)

        a_random_number = generate_random_number(len(self.locations)-1)

        spawned_loc = self.locations[a_random_number]
        

        self.current_pymon.spawn(spawned_loc)

    
    #Start the game with text and menu
    def start_game(self):
        print("Welcome to Pymon World\n")
        print("It's just you and your loyal Pymon roaming around to find more Pymons to capture and adopt.\n")
        print("You started at ",self.current_pymon.get_location().get_name())
        Record.pymon_list.append(self.current_pymon)
        Record.pymon_list_copy.append(self.current_pymon)
        self.handle_menu()

if __name__ == '__main__':
    import os
    import sys
    directory=directory = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__))).replace("\\","/")
    ops = Operation()
    ops.setup()
    ops.start_game()

"""
- Reflection:

* I analaysed the requirements of the project and was enthusiasti of the idea that the project involved creation of a game.
* Random nuber generation function was used to allot  a random location to the Pymon initally and also when the energy is exhausted of the Pymon.
* Classes created includes: Creature, Location, Item, Record, Operation and for exceptions like InvalidDirectionException and InvalidInputFileFormat.
* First the Operation class is invoked to run the setup() function which helps to run the read function of the three csv input files and 
randomly spawn the Pymon in a random location using the spawn() function.
* The read functions reads the files that is locations, items and creatures csv files without including the header row and also making sure that the format 
of the file is correct otherwise resulting in the raising of an InvalidInputFileFormat exception.
* The Pymon class contains the attributes of the Pymon along with counting the locations moved by the Pymon using the add_move_count() function to use for reduction in the energy of the Pymon.
* The move() function within the Pymon class helps to move the Pymon across differnt locations and also reduces the energy by checlking the step count is divisible by 2 using the % operator.
* Location class contains attributes like location name, description, locations via different directions and creatures, items attached to different locaitons which is done via the methos add_creature() and
add_items() functions and this is very useful as it helps to keep track of the creatures to remove after winning a battle or remove items from locations after picking them, also the class contains methods to
remove the creatures, items through remove_creatures() and remove_item() function respectively.
* The item class contains the attributes related to items and has methods to make sure if an item is pickable or not through the get_pickable() function.
* The Record class contains the records of the locations, creatures, items, inventory, pymons acquired list and also flag for initiating the potion along with the reading of the three csv files.
* The Operation class contains the main core of the game like the battle() function which helps to have a battle with a Pymon in the same location of the current Pymon and keeping in mind of the various factors which can end the game
like the energy going to zero. Also ensuring that the core game of rock, paper and scissors is logically correct and results in the right output and also the right outcome such as capturing the Pymon resulting in it being
added to the list, and if the current Pymon loses making sure that it is released into the wild.
* The design process was a bit of an exhilariting experience since I had to think of the various logics involved in the game such as how the Pymon interacted with the items and making sure only the pickable ones were picked and also
the consumable ones were consumed alone whichn resulted in a temporary increase in energy or immunity in battle like for the potion. Also the various data structures such as class variables and static variables were used correctly to
access the required data to make the game run properly. Using lists for various purposes such as keeping records of the Pymons captured or the items in the inventory,etc.
* Writing the code required extensive back and forth testing and bug fixing to ensure that the game logic is kept in place with the requirements such as making sure that the creature is removed from the current location after being captured,
or the random spawning of the current Pymon if the battle is lost and the next Pymon in the list is taken as current Pymmon also.
* Also the scoring logic making sure that it is correct was another task which resulted in thinking of adding and subtracting from the initial score of 0 and if it is negative resulted in losing the game and if it is positive
itr resulted in winning the game and also the back and forth correction between the classes adding more if else conditinos like potion_status resulting in no energy being deducted in that encounter even if the current Pymon
loses.
* The challenges faced while coding this game was ensuring that the attributes of the current Pymon was accessed properly like the current locaiotn or its energy and making sure that it is removed from the list of Pymons while giving the current location
object to the the next Pymon in the list and then randommly respawning it.
* One more challenge faced was the generation of the battle statistics as it involved deeper understanding of the class Pymon and which all information to be given as parameter for the class method battle_stats() being called.
* Also another challenge was getting the required information to display when the binocular was used from the correct objects as different directions object was taken it resulted in a string output rather than a location output thus a temporary
variable was required to make sure that the location was captured with the right location object and then proceeded forward.
* The program was tested promptly to ensure the smooth running of the game with the right logic. 

- References:

* "Proper way to declare custom exceptions in modern Python?" stackoverflow.com. Accessed: Nov. 05, 2024. [Online]. Available: https://stackoverflow.com/questions/1319615/proper-way-to-declare-custom-exceptions-in-modern-python
* "Python Sets" w3schools.com. Accessed: Nov. 05, 2024. [Online]. Available: https://www.w3schools.com/python/python_sets.asp

These websites was used to understand the logic of using an exception class and on how to implement it and also understand on how to implement a set and its properties.
"""
