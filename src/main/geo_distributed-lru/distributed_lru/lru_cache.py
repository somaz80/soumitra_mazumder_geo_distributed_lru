from distributed_lru.cache_entry import DoublyLinkedList


class LRUCache:
    def __init__(self, capacity, expiration_time):
        self.capacity = capacity
        self.cache = DoublyLinkedList(capacity, expiration_time)

    '''
        returns value of the element from cache
    '''

    def get_element_from_cache(self, key):
        try:
            key, value, expires_at = self.cache.get_value_by_key(key)
            return key, value, expires_at
        except KeyError:
            return -1

    '''
       checks if the cache element exists, if so updates the value, else creates a new element at the end
    '''

    def set_element_in_cache(self, key, value, time_to_live_seconds):
        if self.cache.is_existing_key(key):
            # exiting key just update the value
            self.cache.update_existing_key(key=key, data=value)
        else:

            # if we have reached capacity of the cache then only call remove
            if self.cache.list_length() == self.capacity:
                self.cache.remove_last_element_from_list()
            # new key insert the key at the end
            self.cache.insert_at_start(cache_node_key=key, cache_node_data=value,
                                       time_to_live_seconds=time_to_live_seconds)

    def delete_item_from_cache(self, key):
        flag_value = self.cache.remove_element_by_key(key)

        if not flag_value:
            raise KeyError('Key Not Found')
