from typing import List, Tuple, Set, Dict, Any
import urllib
import httpimport
url = "https://raw.githubusercontent.com/Dequavious6/CollectionBackend/main"
with httpimport.remote_repo(["pipUtility"], url):
    from pipUtility import *

class Type:
    def __init__():
        pass
    var1 = 100
    var2 = 200
    fix1 = 300
    fix2 = 400
    ref1 = 500
    ref2 = 600
    ref3 = 700
    
    var = 100
    fix = 300
    ref = 500
    
    fixB1 = 99999  # fixed elem 1 before var
    fixB2 = 89898  # fixed elem 2 before var
    
    fixA1 = 77777  # fixed elem 1 after var
    fixA2 = 88888  # fixed elem 2 after var
    
    nil = 3333
    none = 101010
    
## End of 'Type' class

class Structure:
    def __init__(self, choice: Type = Type.nil, rewind = False, backOnTop = False,
                 subVar = False, fixed = Type.none, reverse = False, rep = 0, quotes = False):
        self.elem = choice
        self.rewind = rewind
        self.back = backOnTop
        self.sub = subVar
        self.fix = fixed
        self.reverse = reverse
        self.nbOfRep = rep
        self.quotes = quotes
        if self.nbOfRep != 0:
            self.isRepeated = True
        else:
            self.isRepeated = False
        
        # Condition to avoid overloading the code in 'Poeme' class
        if self.sub == True:
            if self.fix == Type.fixB1:
                self.fix = Type.fixA1
            elif self.fix == Type.fixB2:
                self.fix = Type.fixA2
                
## End of 'Structure' class

class Poeme:
    def __init__(self, variables, fixedElements, chorus, structure: [Structure]):
        self.varList = variables
        self.fixedList = fixedElements
        self.refList = chorus
        self.structure = structure
    
    def getPoeme(self) -> List[str]:
        li = CList()
        i = 0
        while i < len(self.varList):
        #for i in range(len(self.varList)):
            tmp = self.getElem(index = i)
            li.extend(tmp[0])
            #li.append(' ')
            if i == tmp[1]:
                i+=1
            else:
                i = tmp[1]
        return li
    
    def getElem(self, index) -> List[str]:
        li = CList()
        increment = False
        ##
        for i in range(len(self.structure)):
            ## rewind condition to get the last elem
            if self.structure[i].rewind == True and index>0:
                    index -= 1
            # var/var1
            # Check if stonza starts with a variable
            if self.structure[i].elem == Type.var1 and index<len(self.varList) and self.structure[i].reverse == False:
                # Check if the verse starts with a fixed elem (1)
                if self.structure[i].fix == Type.fixB1:
                    if self.structure[i].isRepeated == True:
                        li.appendS(self.fixedList[0] + self.varList[index], self.structure[i].nbOfRep)
                    elif self.structure[i].isRepeated == False:
                        li.append(self.fixedList[0] + self.varList[index])
                        
                # Check if the verse starts with a fixed elem (2)
                elif self.structure[i].fix == Type.fixB2:
                    if self.structure[i].isRepeated == True:
                        li.appendS(self.fixedList[0] + self.varList[index], self.structure[i].nbOfRep)
                    elif self.structure[i].isRepeated == False:
                        li.append(self.fixedList[0] + self.varList[index])
                        
                # Check if we add a fixed elem (1) After the var
                elif self.structure[i].fix == Type.fixA1:
                    if self.structure[i].isRepeated == True:  # Check if we repeat the verse several times
                        li.appendS(self.varList[index] + self.fixedList[0], self.structure[i].nbOfRep)
                    else:
                        li.append(self.varList[index] + self.fixedList[0])
                
                # Check if we add a fixed elem (2) After the var
                elif self.structure[i].fix == Type.fixA2:
                    if self.structure[i].isRepeated == True:
                        li.appendS(self.varList[index] + self.fixedList[0], self.structure[i].nbOfRep)
                    else:
                        li.append(self.varList[index] + self.fixedList[0])
                    
                # Without a fixed elem
                elif self.structure[i].fix == Type.none:
                    # Check if we repeat the verse several times (without a fixed elem)
                    if self.structure[i].isRepeated == True:
                        li.appendS(self.varList[index], self.structure[i+1].nbOfRep)
                    elif self.structure[i].isRepeated == False:
                        li.append(self.varList[index])
                           
            elif self.structure[i].elem == Type.var1 and index >= len(self.varList)-1 and self.structure[i].reverse == False:
                return li, index
            ## end of var1
            
            ##
            # var2
            ##
            if self.structure[i].elem == Type.var2 and index<len(self.varList)-1:
                
                # Check if we add a fixed elem (1) Before var2
                if self.structure[i].fix == Type.fixB1:
                    if self.structure[i].isRepeated == True:
                        li.appendS(self.fixedList[0] + self.varList[index+1], self.structure[i].nbOfRep)
                    elif self.structure[i].isRepeated == False:
                        li.append(self.fixedList[0] + self.varList[index+1])
                        
                # Check if we add a fixed elem (2) Before var2
                elif self.structure[i].fix == Type.fixB2:
                    if self.structure[i].isRepeated == True:
                        li.appendS(self.fixedList[1] + self.varList[index+1].lower(), self.structure[i].nbOfRep)
                    elif self.structure[i].isRepeated == False:
                        if self.structure[i].quotes == True:
                            li.append('\"' + self.fixedList[1] + self.varList[index+1].lower() +'\"')
                        else:
                            li.append(self.fixedList[1] + self.varList[index+1].lower())
                
                # Check if we add a fixed elem (1) After var2
                if self.structure[i].fix == Type.fixA1:
                    # Check if we use a subVar (only a part of the var)
                    if self.structure[i].sub == True:
                        if self.structure[i].isRepeated == True:
                            li.appendS(self.getSubVerse(index+1) + self.fixedList[0], self.structure[i].nbOfRep)
                            increment = True
                        elif self.structure[i].isRepeated == False:
                            li.append(self.getSubVerse(index+1) + self.fixedList[0])
                            increment = True
                    elif self.structure[i].sub == False:
                        if self.structure[i].isRepeated == True:
                            li.appendS(self.varList[index+1] + self.fixedList[0], self.structure[i].nbOfRep)
                            increment = True
                        elif self.structure[i].isRepeated == False:
                            li.append(self.varList[index+1] + self.fixedList[0])
                            increment = True
                
                # Check if we add a fixed elem (2) After var2
                elif self.structure[i].fix == Type.fixA2:
                    # Check if we use a subVar (only a part of the var)
                    if self.structure[i].sub == True:
                        if self.structure[i].isRepeated == True:
                            li.appendS(self.getSubVerse(index+1) + self.fixedList[1], self.structure[i].nbOfRep)
                            increment = True
                        elif self.structure[i].isRepeated == False:
                            li.append(self.getSubVerse(index+1) + self.fixedList[1])
                            increment = True
                    elif self.structure[i].sub == False:
                        if self.structure[i].isRepeated == True:
                            li.appendS(self.varList[index+1] + self.fixedList[1], self.structure[i].nbOfRep)
                            increment = True
                        elif self.structure[i].isRepeated == False:
                            li.append(self.varList[index+1] + self.fixedList[1])
                            increment = True
                
                # var2 without a fixed element (before or after)
                elif self.structure[i].fix == Type.none:
                    # Check if we repeat the verse several times (without a fixed elem)
                    if self.structure[i].isRepeated == True:
                        li.appendS(self.varList[index+1], self.structure[i].nbOfRep)
                        increment = True
                    elif self.structure[i].isRepeated == False:
                        li.append(self.varList[index+1])
                        increment = True  # (for loraine)
            ## End of var2
            
            ## Get the first var for the last stonza of the poeme (Limited implementation to avoid overloading the code)
            if self.structure[i].elem == Type.var2 and index>=len(self.varList)-1 and self.structure[i].back == True:
                # Check if we add a fixed elem (1) Before var
                if self.structure[i].fix == Type.fixB1:
                    if self.structure[i].isRepeated == True:
                        li.appendS(self.fixedList[0] + self.varList[0], self.structure[i].nbOfRep)
                    elif self.structure[i].isRepeated == False:
                        li.append(self.fixedList[0] + self.varList[0])
                        
                # Check if we add a fixed elem (2) Before var
                elif self.structure[i].fix == Type.fixB2:
                    if self.structure[i].isRepeated == True:
                        li.appendS(self.fixedList[1] + self.varList[0].lower(), self.structure[i].nbOfRep)
                    elif self.structure[i].isRepeated == False:
                        if self.structure[i].quotes == True:
                            li.append('\"' + self.fixedList[1] + self.varList[0].lower() + '\"')
                        else:
                            li.append(self.fixedList[1] + self.varList[0].lower())
            ## End of Back on Top
                    
            # var with a repeat loop
            if self.structure[i].elem == Type.var1 and self.structure[i].reverse == True:
                li.extend(list(self.varList[j] for j in reversed(range(index+1))))
                        
                
            # ref/ref1
            if self.structure[i].elem == Type.ref1:
                if self.structure[i].isRepeated == True:
                    li.appendS(self.refList[0], self.structure[i].nbOfRep)
                elif self.structure[i].isRepeated == False:
                    li.append(self.refList[0])
            ## End of ref1
                
            # ref2
            if self.structure[i].elem == Type.ref2:
                if self.structure[i].isRepeated == True:
                    li.appendS(self.refList[1], self.structure[i].nbOfRep)
                elif self.structure[i].isRepeated == False:
                    li.append(self.refList[1])
            ## End of ref2
            
            # ref3
            if self.structure[i].elem == Type.ref3:
                if self.structure[i].isRepeated == True:
                    li.appendS(self.refList[2], self.structure[i].nbOfRep)
                elif self.structure[i].isRepeated == False:
                    li.append(self.refList[2])
            ## End of ref3
              
        if increment == True:
            index += 2
        li.append(' ')
        return li, index
    ## end of getElem() func
    
    def getSubVerse(self, index) -> str:
        #var = self.varList[index]
        indexes = [i for i, item in enumerate(self.varList[index]) if item == ' ']
        return self.varList[index][0 : indexes[1]]
###
## END OF 'POEME' CLASS ##
###
    ## class indications for user:
    # Add a fixed parameter to a structure element (var1 or var2) to have a fixed elem
    # at the begining or at the end of the verse, following these definitions:
    # fixB1 = fixed elem (1) before the var
    # fixB2 = fixed elem (2) before the var
    # fixA1 = fixed elem (1) after the var
    # fixA2 = fixed elem (2) after the var
    #
    # All element names used in "Poeme" class are parameters of class "Type" (Type class serves as an enum)
    #
    # To simplify the code and not overload the 'Poeme' class structure, we assume that a subVerse implies
    # a fixed element after it.
    
    # Cannot append a fixed elem by itself (a fixed elem cannot solely compose a verse)
    # Quotes at the end of a verse are only available for a specific use case (fixB2 + var2)
    # To enable quotes add the "quotes = True" key to the structure element declaration
    
    ####
    ## !!! The order of the structure list matter !!!
    ##  --> It gives the order of the verses in a stonza which is then repeated through the whole poeme
    ####
    
