class T_element:
    def __init__(self,content,parent):
        self.content=content
        self.counter=0
        self.children={}
        self.parent=parent
    def has_child(self,key):
        return key in self.children.keys()
    def add_child(self,key,parent):
        return self.children.update({key:T_element(key,parent)})
    def get_child_no_protection(self,key):
        if not self.has_child(key):
            raise Trie_exp("Invalid Access")
        return self.children[key]
    def get_child(self,key):
        if not self.has_child(key):
            self.add_child(key)
        return self.children[key]
    def rm_child(self,key):
        if self.has_child(key):
            del self.children[key]
        return self
    def increase_counter(self,value=1):
        self.counter+=value
        return self
    def decrease_counter(self,value=1):
        if value>self.counter:
            raise Trie_erease_operation_ilegal_exp("Cannot decrease a value that is bigger than the counter")
        self.counter-=value
        return self
    def get_counter(self):
        return self.counter
    def get_parent(self):
        return self.parent
    def get_num_children(self):
        return len(self.children)


class Trie:
    top_level_token=" "
    top_level_parent=None
    def __init__(self):
        self.root=T_element(Trie.top_level_token,Trie.top_level_parent)
        self.len_table={} # how many prefix with length i is len_table[i]
        self._len_link={}
    def insert(self,element):
        pointer=self.root
        for index,value in enumerate(element):
            if not pointer.has_child(value): # check whether it is already added
                pointer.add_child(value,pointer)
                pointer=pointer.get_child_no_protection(value) # jump to child
                # book keeping to out len_table and _len_link
                # this point has just being added, we need to add entry to
                #   len_table and _len_link
                if not (index+1) in self.len_table:
                    self.len_table.update({index+1:1})
                else:
                    self.len_table[index+1]+=1
                if not (index+1) in self._len_link:
                    self._len_link.update({index+1:[]})
                self._len_link[index+1].append([pointer,True])
            else:
                pointer=pointer.get_child_no_protection(value)
            pointer.increase_counter() # update its number
    def erease(self,element,value=1):
        pointer=self.root
        self._erease(element,pointer,1,value)
         
    def loop_up(self,element):
        pointer=self.root
        for value in element:
            if not pointer.has_child(value):
                raise Trie_prefix_notfound_exp(str(element)+" dosen't exist in this data structure")
            pointer=pointer.get_child(value)
        return pointer.get_counter()
    
    ### private function ###
    
    def _erease(self,element,pointer,level,value=1):
        # sanity check
        if not pointer.has_child(element[0]):
            if level==0:
                raise Trie_prefix_notfound_exp("Cannot delete "+str(element)+" because it is not in this data structure")
            else:
                raise Trie_prefix_notfound_exp("")
        # get to children
        pointer=pointer.get_child_no_protection(element[0])
        # decreae the number
        #pointer.decrease_counter()
        if len(element)!=1:
            try:
                determined_value=self._erease(element[1:],pointer,(level+1),value)
            except Trie_prefix_notfound_exp as exp:
                ## friendly exception message
                if level==1:
                    raise Trie_prefix_notfound_exp(str(element)+" dosen't exist in this data structure") from exp
                else:
                    raise Trie_prefix_notfound_exp("") from exp
        
        # decreae the number
        # Here, 
        if len(element)==1: # end of recursive
            if pointer.get_num_children()!=0: # structurally, it isn't a leaf
                if value!=1:
                    raise Trie_erease_operation_ilegal_exp("Cannot delete more than 1 prefix when it isn't a leaf")
                else:
                    determined_value=value # 1
            else:# leaf
                if value==-1:
                    determined_value=pointer.get_counter()
                else:
                    determined_value=min(pointer.get_counter(),value)
        #print("determined_value is "+str(determined_value))
        pointer.decrease_counter(determined_value)
      
        # I use recursive function call, becuse i need to delete data structue if counter is down to zero
        # when function returns, we are sure that data update in children are already finished
        if pointer.get_counter()==0:
            parent=pointer.get_parent()
            parent.rm_child(element[0])
            # update len_table
            self.len_table[level]-=1
            # update _len_link
            for l in self._len_link[level]:
                if l[0]==pointer:
                    l[1]=False
                    break
        return determined_value
    # due to performance concern, when a link is deleted from link_table
    # it is in fact masked as unvalid, this function is used to clean up the space
    def link_table_clean(self):
        for key,item in self._len_link.items():
            self._len_link[key]=[ll for ll in item if ll[1]==True]
        return self
    def prefix_length_enumerator(self,length):
        if length in self._len_link:
            l=self._len_link[length]
            for item in l:
                if item[1]==True:
                    yield item[0]
        else:
            raise Trie_prefix_notfound_exp("There is no prefix in this data structure with length "+str(length))
            
        
    def prefix_length_loopup(self,length):
        if length in self.len_table:
            return self.len_table[length]
        else:
            raise Trie_prefix_notfound_exp("There is no prefix in this data structure with length "+str(length))
    
    
    @classmethod
    def assembly(cls,pointer):
        cat=[]
        while(True):
            if pointer.get_parent()!=cls.top_level_parent:
                cat.append(pointer.content)
                pointer=pointer.get_parent()
            else:
                break
        cat.reverse()
        result=""
        for item in cat:
            result+=str(item)
        return result

### Exceptions ###
class Trie_exp(Exception):
    def __init__(self,msg):
        self.message=msg
class Trie_prefix_notfound_exp(Trie_exp):
    def __init__(self,msg):
        super().__init__(msg)
class Trie_erease_operation_ilegal_exp(Trie_exp):
    def __init__(self,msg):
        super().__init__(msg)