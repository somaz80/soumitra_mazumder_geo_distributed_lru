from time import time

'''
    This is a cache node class it knows start next and time to live
'''


class CacheNode:
    def __init__(self, next=None, prev=None, key=None, data=None, ttl=20):
        self.next = next  # reference to next node in DLL
        self.prev = prev  # reference to previous node in DLL
        self.key = key
        self.data = data
        self.expires_at = time() + ttl
        self._expired = False

    '''
     This function returns true if the node has expired 
    '''

    def expired(self):
        if self._expired is False:
            return self.expires_at < time()
        else:
            return self._expired


class LRUCache:
    def __init__(self):
        self.start_node = None

    '''
        Inserts an item to an empty list does not do anything when it is not empty
    '''

    def insert_in_empty_list(self, cache_node_key=None, cache_node_data=None, time_to_live_seconds=None):
        if self.start_node is None:
            cache_node = CacheNode(key=cache_node_key, data=cache_node_data, ttl=time_to_live_seconds)
            self.start_node = cache_node

    '''
        inserts an cache node at the start of list
    '''

    def insert_at_start(self, cache_node_key=None, cache_node_data=None, time_to_live_seconds=None):
        if self.start_node is None:
            self.insert_in_empty_list(cache_node_key=cache_node_key, cache_node_data=cache_node_data,
                                      time_to_live_seconds=time_to_live_seconds)
            return
        cache_node = CacheNode(key=cache_node_key, data=cache_node_data, ttl=time_to_live_seconds)
        cache_node.next = self.start_node
        self.start_node.prev = cache_node
        self.start_node = cache_node

    '''
        inserts an cache node item at the end of the list
    '''

    def insert_at_end(self, cache_node_key=None, cache_node_data=None, time_to_live_seconds=None):
        if self.start_node is None:
            cache_node = CacheNode(key=cache_node_key, data=cache_node_data, ttl=time_to_live_seconds)
            self.start_node = cache_node
            return
        single_node = self.start_node
        while single_node.next is not None:
            single_node = single_node.nref
        cache_node = CacheNode(key=cache_node_key, data=cache_node_data, ttl=time_to_live_seconds)
        single_node.next = cache_node
        cache_node.prev = single_node


    '''
        Takes a key as input and deletes the node if found after traversing
    '''
    def remove_element_by_key(self, key):
        if self.start_node is None:
            print("The list has no element to delete")
            return
        if self.start_node.next is None:
            if self.start_node.key == key:
                self.start_node = None
            else:
                print("Cache Node not found")
            return

        if self.start_node.key == key:
            self.start_node = self.start_node.next
            self.start_node.prev = None
            return

        a_node = self.start_node
        while a_node.next is not None:
            if a_node.key == key:
                break
            a_node = a_node.next
        if a_node.next is not None:
            a_node.prev.next = a_node.next
            a_node.next.prev = a_node.prev
        else:
            if a_node.key == key:
                a_node.pref.next = None
            else:
                print("Cache Node not found")

    def list_length(self):
        "returns the number of list items"

        count = 0
        current_node = self.start_node

        while current_node is not None:
            # increase counter by one
            count = count + 1

            # jump to the linked node
            current_node = current_node.next

        return count

    def traverse_list(self):
        if self.start_node is None:
            print("CacheList has no element")
            return
        else:
            a_node = self.start_node
            while a_node is not None:
                print(" Node data found : ", a_node.key , a_node.data)
                a_node = a_node.next

    def get_value_by_key(self, key=None):
        return_value = None
        if self.start_node is None:
            print("CacheList has no element")
            return
        if self.start_node.key == key:
            return self.start_node

        else:
            a_node = self.start_node
            while a_node is not None:
                print(" Node data found : ", a_node.key, a_node.data)
                if a_node.key == key:
                    self.move_node_to_start_return_node_value(a_node)
                    return a_node.data
                a_node = a_node.next

    def move_node_to_start_return_node_value(self, cache_node=None):

        if cache_node.prev is not None:
            cache_node.prev.next = cache_node.next
            self.start_node = cache_node
            cache_node.prev = None
        print(self.traverse_list())



if __name__ == '__main__':
    new_linked_list = LRUCache()
    new_linked_list.insert_at_start('k1', 'v1', 20)
    new_linked_list.insert_at_start('k2', 'v2', 20)
    new_linked_list.insert_at_start('k3', 'v3', 20)
    new_linked_list.insert_at_start('k4', 'v4', 20)
    new_linked_list.insert_at_start('k5', 'v5', 20)
    new_linked_list.traverse_list()
    print('after deletion the value')
    print('Node Found ', new_linked_list.get_value_by_key('k4'))
    print('after deletion the value')
    new_linked_list.traverse_list()
    print(new_linked_list.list_length())
    new_linked_list.remove_element_by_key('k3')
    print('after deletion the value')
    new_linked_list.traverse_list()
    print(new_linked_list.list_length())