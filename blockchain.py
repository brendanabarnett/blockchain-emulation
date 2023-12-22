from hashmap import HashMapping

class Transaction():
    '''A single transaction of COIN'''
    def __init__(self, from_user, to_user, amount):
        '''inits Transaction that contain: from-user, to-user, and how much'''
        self.from_user = from_user
        self.to_user = to_user
        
        #check if numerical value
        if not isinstance(amount, (int, float)): raise TypeError(f'Amount {amount} is not a numerical value!')
        self.amount = amount

    def __repr__(self):
        '''String representation of transaction'''
        return f'[Transaction: from {self.from_user} to {self.to_user}: ${self.amount}]'
    
    def __eq__(self, other):
        '''checks that each component of the transaction is the same: from, to, and amount'''
        return self.from_user == other.from_user and self.to_user == other.to_user and self.amount == other.amount
    
    def __hash__(self):
        '''returns the hash of the tuple of the from_user, to_user, and amount of this Transaction'''
        return hash((self.from_user, self.to_user, self.amount))
 
class Block():
    '''Block is a collection of Transaction objects. each block is linked with the previous one by containing the prev's hash'''
    def __init__(self, transactions=None, previous_block_hash=None):
        '''inits block w a prev hash var and _block, which is the list of Transactions'''
        self._previous_block_hash = previous_block_hash
        self._block = []
        self._len = 0
        if transactions is not None:    #adds all transactions to _block if there are any upon initilization
            for trans in transactions: self.add_transaction(trans)

    def __repr__(self):
        '''String representation of Block'''
        return f'Block: {self._block}'
    
    def __eq__(self, other):
        '''returns true if the list of Transactions in each block is the same'''
        return self._block == other._block
    
    def __hash__(self):
        '''returns the hash of the string of the list of Transactions'''
        return hash(tuple(self._block))
    
    def __iter__(self):
        '''makes Block iterable by iterating through the list: self._block'''
        return iter(self._block)
    
    def add_transaction(self, transaction):
        '''adds an input Transaction to self._block'''
        self._block.append(transaction)
        self._len += 1

class Ledger():
    '''Keeps track of all user balances using HashMapping'''
    def __init__(self):
        '''inits with an empty HashMapping'''
        self._ledger_hashmap = HashMapping()

    def __repr__(self):
        '''returns a simple print statement of the hashmap'''
        return f'Ledger: {self._ledger_hashmap}'
    
    def has_funds(self, user, amount):
        '''checks if the user has enough funds to make the transaciton'''
        if user not in self._ledger_hashmap: return False
        return self._ledger_hashmap[user] >= amount     #checks if user has enough funds

    def deposit(self, user, amount):
        '''adds COIN to user balance'''
        self._ledger_hashmap[user] += amount

    def transfer(self, user, amount):
        '''subtracts COIN from user balance'''
        #no need to check if user has enough in this method: has funds is always called before this
        self._ledger_hashmap[user] -= amount

class Blockchain():
    '''Contains the chain of blocks.''' 
    _ROOT_BC_USER = "ROOT"            # Name of root user account.  
    _BLOCK_REWARD = 1000              # Amount of COIN given as a reward for mining a block
    _TOTAL_AVAILABLE_TOKENS = 999999  # Total balance of COIN that the ROOT user receives in block0

    def __init__(self):
        '''initilizes Blockchain with a list of blocks and an instance of Ledger, along with the genesis block'''
        self._blockchain = list()     # Use list for  chain of blocks
        self._bc_ledger = Ledger()    # The ledger of COIN balances
        self._create_genesis_block()    # Create the initial block0 of the blockchain (genesis block)

    def __repr__(self):
        '''makes a simple string representation of the blockchain and its blocks (and the blocks' transactions)'''
        return f'Blockchain: {self._blockchain}'

    def _create_genesis_block(self):
        '''Creates the initial block in the chain. Process is simplified to
        facilitate the transaction of COIN easily.'''
        trans0 = Transaction(self._ROOT_BC_USER, self._ROOT_BC_USER, self._TOTAL_AVAILABLE_TOKENS)
        block0 = Block([trans0])
        self._blockchain.append(block0)
        self._bc_ledger.deposit(self._ROOT_BC_USER, self._TOTAL_AVAILABLE_TOKENS)

    def distribute_mining_reward(self, user):
        '''
        Method for distributing reward. Simplifed POC method so users need not compete
        to solve the nonce in order to mine more COIN'''
        trans = Transaction(self._ROOT_BC_USER, user, self._BLOCK_REWARD)
        block = Block([trans])
        self.add_block(block)

    def add_block(self, block):
        '''adds a block to the blockchain if it is valid; if any transaction is invalid (user doesnt have enough COIN) 
        then block is not added and returns false'''
        for trans in block:         #iterates thru curr Block
            frm, amt = trans.from_user, trans.amount
            if not self._bc_ledger.has_funds(frm, amt): return False    #returns false if any user does not have enough COIN to complete transaction

        for trans in block:         #reiterates thru the Block
            frm, to, amt = trans.from_user, trans.to_user, trans.amount
            self._bc_ledger.transfer(frm, amt)  #subtracts COIN from the from_user; updates ledger
            self._bc_ledger.deposit(to, amt)    #adds COIN to the to_user; updates ledger
        
        block._previous_block_hash = hash(self._blockchain[len(self._blockchain)-1]) #sets prev block hash using the hash of the previous block in _blockchain
        
        self._blockchain.append(block)  #appends the block to the end of the chain
        return True #returns true if the block was successfully added

    def validate_chain(self):
        '''if a block's prev hash is not the hash of the block in front of it, the block with the incorrect prev hash value is 
        returned in a list of other blocks that have been tampered with'''
        invalid_blocks = [] #inits the list of invalid blocks
        if self._blockchain[0]._previous_block_hash != None: invalid_blocks.append(self._blockchain[0])  #checks that the genesis block's prev is None

        for i in range(len(self._blockchain)-1):    #iterates thru the blockchain
            if hash(self._blockchain[i]) != self._blockchain[i+1]._previous_block_hash: #compares the hash of the block and the next block's prev_block_hash
                invalid_blocks.append(self._blockchain[i+1])    #if the prev_hash is incorrect, the block w the incorrect prev hash is appended to the list

        return invalid_blocks   #returns list of blocks that have been tampered with
