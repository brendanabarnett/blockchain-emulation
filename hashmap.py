class Entry:
    '''each Entry holds a key:value pair. hashmapping holds a collection of Entry objects'''
    def __init__(self, key, value):
        '''inits the key:value pair that makes up each entry'''
        self.key = key
        self.value = value

    def __repr__(self):
        '''simple print statement to see the key:val when testing/debugging'''
        return f"Entry(key={self.key}, value={self.value})"

class HashMapping:
    '''each Hashmapping hold a collection of Entry objects. rehashes when len of self if 2x the size of the num of buckets'''
    def __init__(self):
        '''inits bass num of buckets as 8, inits a len and 8 empty buckets in _L'''
        self._num_buckets = 8                            #init number of buckets
        self._len = 0                                    #init len
        self._L = [[] for i in range(self._num_buckets)] # list of buckets

    def __repr__(self):
        '''simple print statement to print each value pair and their bucket, along w the empty buckets'''
        return f'{self._L}'

    def __len__(self):
        '''returns how many Entries there are'''
        return self._len

    def __contains__(self, key):
        '''Returns True (False) if key is (is not) in HashMapping'''
        idx = self._get_bucket(key) # find bucket

        for entry in self._L[idx]: # scan bucket, return if key is found
            if entry.key == key: return True

        return False    # not found- return false

    def __setitem__(self, key, value):
        '''Adds key:value pair to HashMapping, or updates hashmap[key] if it already exists'''
        idx = self._get_bucket(key) #finds index (which bucket the key should be in)

        for entry in self._L[idx]:  #scans thru bucket
            if entry.key == key:    #if entry is in bucket, val is updated
                entry.value = value
                return  #returns to skip the rest of the function if val is updated
            
        #if key not found...
        self._L[idx].append(Entry(key, value))
        self._len += 1

        if len(self) > 2*self._num_buckets: self._rehash(2*self._num_buckets)   #rehash if needed!

    def __getitem__(self, key):
        '''Returns value associated with key. Raises KeyError if key not in HashMapping'''
        idx = self._get_bucket(key) #finds index (which bucket the key should be in)

        for entry in self._L[idx]:  #scans thru bucket
            if entry.key == key: return entry.value #if key is found, return associated val
        
        return False #return false if key not found
    
    def _get_bucket(self, key):
        '''Returns index of bucket key should be in'''
        return hash(key) % self._num_buckets
    
    def _rehash(self, new_buckets):
        '''Rehashes to amount of new_buckets'''
        new_L = [[] for i in range(new_buckets)]    # make a new list of buckets
        self._num_buckets = new_buckets     #update new num of buckets

        for bucket in self._L:  #look thru every bucket
            for entry in bucket:    #look thru every entry
                idx = self._get_bucket(entry.key)   #rehash that entry
                new_L[idx].append(entry)    #add it to new_L

        self._L = new_L # update self._L to new list
