class LRUCache:

    def __init__(self, capacity: int):
        self.capacity=capacity
        self.size=0
        self.hashtable={}
        self.head=None
        self.end=None


    def get(self, key: int) -> int:
        if key in self.hashtable:
            item=self.hashtable[key]
            if not item.before is None:
                item.before.after=item.after
                if not item.after is None:
                    item.after.before=item.before
                elif self.end==item:
                    self.end=item.before
                self.head.before=item
                item.before=None
                item.after=self.head
                self.head=item
            return self.hashtable[key].value
        else:
            return -1


    def put(self, key: int, value: int) -> None:
        if key in self.hashtable:
            item=self.hashtable[key]
            item.value=value
            if not item.before is None:
                item.before.after=item.after
                if not item.after is None:
                    item.after.before=item.before
                elif self.end==item:
                    self.end=item.before
                self.head.before=item
                item.before=None
                item.after=self.head
                self.head=item
        else:
            if self.size<self.capacity:
                item=Node(key,value)
                if self.size==0:
                    self.head=item
                    self.end=item
                else:
                    self.head.before=item
                    item.after=self.head
                    self.head=item
                self.hashtable.update({key:item})
                self.size+=1
            else:
                item=Node(key,value)
                self.hashtable[key]=item
                if self.capacity==1:
                    del self.hashtable[self.head.key]
                    self.head=item
                    self.end=item
                else:
                    self.end.before.after=None
                    del self.hashtable[self.end.key]
                    self.end=self.end.before
                    self.head.before=item
                    item.after=self.head
                    self.head=item

class Node:
    def __init__(self,key,value,before=None,after=None):
        self.key=key
        self.value=value
        self.before=before
        self.after=after