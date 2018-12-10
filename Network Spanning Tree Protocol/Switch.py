# This defines a Switch that can can send and receive spanning tree 
# messages to converge on a final loop free forwarding topology.  This
# class is a child class (specialization) of the StpSwitch class.
#
# self.switchID                   (the ID number of this switch object)
# self.links                      (the list of swtich IDs connected to this switch object)
# self.send_message(Message msg)  (Sends a Message object to another switch)
#
# topolink (parameter passed to initialization function)
# self.topology (link to the greater topology structure used for message passing)

			    												

from Message import *
from StpSwitch import *

class Switch(StpSwitch):

    def __init__(self, idNum, topolink, neighbors):    
        # Invoke the super class constructor, which makes available to this object the following members:
        # -self.switchID                   (the ID number of this switch object)
        # -self.links                      (the list of swtich IDs connected to this switch object)
        super(Switch, self).__init__(idNum, topolink, neighbors)
        
        #TODO: Define a data structure to keep track of which links are part of / not part of the spanning tree.
        self.rootID = self.switchID
        self.distanceToRoot = 0 
        self.parent = None 
        self.spantree = {} 
        for neighbor in self.links:
            self.spantree[neighbor] = False 

    def send_initial_messages(self):
        #TODO: This function needs to create and send the initial messages from this switch.
        #      Messages are sent via the superclass method send_message(Message msg) - see Message.py.
	    #      Use self.send_message(msg) to send this.  DO NOT use self.topology.send_message(msg)
        for neighbor in self.links:
            self.send_message(Message(self.switchID, 0, self.switchID, neighbor, False))
        
    def process_message(self, message):
        #TODO: This function needs to accept an incoming message and process it accordingly.
        #      This function is called every time the switch receives a new message.

        if (message.root == self.rootID and message.distance + 1 < self.distanceToRoot) or (message.root < self.rootID) :

            self.rootID = message.root   
            self.parent = message.origin
            self.distanceToRoot = message.distance + 1 

            for neighbor in self.links:
                if neighbor != message.origin:
                    self.spantree[neighbor] = False
                    self.send_message(Message(self.rootID, self.distanceToRoot, self.switchID, neighbor, False))
                else:
                    self.spantree[neighbor] = True
                    self.send_message(Message(self.rootID, self.distanceToRoot, self.switchID, neighbor, True))
        
        elif message.root == self.rootID and message.distance + 1 == self.distanceToRoot and \
                    self.parent and message.origin < self.parent:
            self.spantree[self.parent] = False
            self.send_message(Message(self.rootID, self.distanceToRoot, self.switchID, self.parent, False))
            # set as new parent, update to spantree list and message the origin
            self.parent = message.origin
            self.spantree[message.origin] = True
            self.send_message(Message(self.rootID, self.distanceToRoot, self.switchID, message.origin, True))

        else: 
            self.spantree[message.origin] = message.pathThrough


    def generate_logstring(self):
        #TODO: This function needs to return a logstring for this particular switch.  The
        #      string represents the active forwarding links for this switch and is invoked 
        #      only after the simulaton is complete.  Output the links included in the 
        #      spanning tree by increasing destination switch ID on a single line. 
        #      Print links as '(source switch id) - (destination switch id)', separating links 
        #      with a comma - ','.  
        #
        #      For example, given a spanning tree (1 ----- 2 ----- 3), a correct output string 
        #      for switch 2 would have the following text:
        #      2 - 1, 2 - 3
        #      A full example of a valid output file is included (sample_output.txt) with the project skeleton.
        log = []
        for neighbor in sorted(self.spantree.iterkeys()):
            if self.spantree[neighbor] == True:
                log.append('{} - {}'.format(self.switchID, neighbor))
        return ', '.join(log)
