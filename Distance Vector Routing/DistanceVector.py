# Project 3 for CS 6250: Computer Networks
#
# This defines a DistanceVector (specialization of the Node class)
# that can run the Bellman-Ford algorithm. The TODOs are all related 
# to implementing BF. Students should modify this file as necessary,
# guided by the TODO comments and the assignment instructions. This 
# is the only file that needs to be modified to complete the project.
#
# Student code should NOT access the following members, otherwise they may violate
# the spirit of the project:
#
# topolink (parameter passed to initialization function)
# self.topology (link to the greater topology structure used for message passing)
#
# Copyright 2017 Michael D. Brown
# Based on prior work by Dave Lillethun, Sean Donovan, and Jeffrey Randow.
        											
from Node import *
from helpers import *

class DistanceVector(Node):
    
    def __init__(self, name, topolink, outgoing_links, incoming_links):
        ''' Constructor. This is run once when the DistanceVector object is
        created at the beginning of the simulation. Initializing data structure(s)
        specific to a DV node is done here.'''

        super(DistanceVector, self).__init__(name, topolink, outgoing_links, incoming_links)
        
        #TODO: Create any necessary data structure(s) to contain the Node's internal state / distance vector data    
        self.dv = {}
        self.dv[self.name] = 0
    
############################################above done
    def send_initial_messages(self):
        ''' This is run once at the beginning of the simulation, after all
        DistanceVector objects are created and their links to each other are
        established, but before any of the rest of the simulation begins. You
        can have nodes send out their initial DV advertisements here. 

        Remember that links points to a list of Neighbor data structure.  Access
        the elements with .name or .weight '''

        # TODO - Each node needs to build a message and send it to each of its neighbors
        # HINT: Take a look at the skeleton methods provided for you in Node.py
        msglist=[]
        msglist.append(self.name)    #0 item in list is origin node name
        msglist.append(self.dv)      #1st item in list is the actual dv message
        for dest in self.neighbor_names:
            self.send_msg(msglist, dest)  ##broadcast to all incoming links(neighbor_names)
######################################################################above done
    def process_BF(self):
        ''' This is run continuously (repeatedly) during the simulation. DV
        messages from other nodes are received here, processed, and any new DV
        messages that need to be sent to other nodes as a result are sent. '''

        # Implement the Bellman-Ford algorithm here.  It must accomplish two tasks below:
        # TODO 1. Process queued messages
        
        self.ok_to_broadcast = False  #keep track of updates     
        self.added_node = False 
        self.lowered_weight = False 
        self.not_reached_infinity = True 

        for msglist in self.messages:   

            msgorigin= msglist[0]
            msg=msglist[1]

            for msgnodes in msg:  #loop through each node info 
                if msgnodes!=self.name:  ##ignore distance info to itself
                    msgnodes_is_newnode=True   #whether msgnode is a new node to be added into dv dictionary
                    for existingnodes in self.dv:
                        if msgnodes == existingnodes:
                            msgnodes_is_newnode = False

                    if (msgnodes_is_newnode):  #test if new nodes are added to dv
                        self.dv[msgnodes] = msg[msgnodes] + int(self.get_outgoing_neighbor_weight(msgorigin))
                        self.added_node = True

                    if  (msg[msgnodes] + int(self.get_outgoing_neighbor_weight(msgorigin))) < -299:     ##test for infinity loops
                        self.dv[msgnodes] = -99
                        self.not_reached_infinity = False 

                    elif (self.dv[msgnodes]) > (msg[msgnodes] + int(self.get_outgoing_neighbor_weight(msgorigin))):    #if not infinity, reduce weight if possible
                        self.dv[msgnodes] = msg[msgnodes] + int(self.get_outgoing_neighbor_weight(msgorigin))
                        self.lowered_weight = True

               
        # Empty queue
        self.messages = []

##########################################above done

        # TODO 2. Send neighbors updated distances  

        self.ok_to_broadcast = ( (self.added_node) or (self.lowered_weight) ) and self.not_reached_infinity

        if (self.ok_to_broadcast) :
            msglist=[]
            msglist.append(self.name)    #0 item in list is origin node name
            msglist.append(self.dv)      #1st item in list is the actual dv message
            for dest in self.neighbor_names:
                self.send_msg(msglist, dest)  ##broadcast to all incoming links(neighbor_names)





########################NEED TO CONSIDER NEGATIVE LOOP HERE



             ##above done


    def log_distances(self):
        ''' This function is called immedately after process_BF each round.  It 
        prints distances to the console and the log file in the following format (no whitespace either end):
        
        A:A0,B1,C2
        
        Where:
        A is the node currently doing the logging (self),
        B and C are neighbors, with vector weights 1 and 2 respectively
        NOTE: A0 shows that the distance to self is 0 '''
        
        # TODO: Use the provided helper function add_entry() to accomplish this task (see helpers.py).
        # An example call that which prints the format example text above (hardcoded) is provided.    


         
        self.log_string = ""    
        for entry in self.dv:
            self.log_string += entry
            if self.dv[entry] < -99:
                x=-99
            else:
                x=self.dv[entry]
            self.log_string += str(x)
            self.log_string += ","
        self.log_string = self.log_string[:-1]
     
        add_entry(self.name, self.log_string)   
