import unittest
from blockchain import Transaction, Block, Ledger, Blockchain

class Test_Transaction(unittest.TestCase):
    '''Test cases to ensure Transaction is initilized and functions properly'''
    
    def test_init(self):
        '''tests that Transactions are initilized properly and the to, from, and amount can be 
        accessed/changed by user if needed. ie: they made a typo'''
        #makes new Transaction and edits the amt
        trans1 = Transaction('from', 'to', 100)
        self.assertEqual(trans1.from_user, 'from')
        self.assertEqual(trans1.to_user, 'to')
        self.assertEqual(trans1.amount, 100)
        trans1.amount = 25
        self.assertEqual(trans1.amount, 25)
        trans1.amount += 40275800
        self.assertEqual(trans1.amount, 40275825)

        #makes new Transaction and edits the to_user
        trans2 = Transaction('Bill', 'Jane', 100000)
        self.assertEqual(trans2.from_user, 'Bill')
        self.assertEqual(trans2.to_user, 'Jane')
        self.assertEqual(trans2.amount, 100000)
        trans2.to_user = 'Bob'
        self.assertEqual(trans2.to_user, 'Bob')
        trans2.to_user = 'Bill'
        self.assertEqual(trans2.to_user, 'Bill')

        #makes new Transaction and edits the from_user
        trans3 = Transaction('me', 'aaaaaa', 12345)
        self.assertEqual(trans3.from_user, 'me')
        self.assertEqual(trans3.to_user, 'aaaaaa')
        self.assertEqual(trans3.amount, 12345)
        trans3.from_user = 'this is quite and long string for a name. eeeeeeeeeeeeeeeeeeeeeee'
        self.assertEqual(trans3.from_user, 'this is quite and long string for a name. eeeeeeeeeeeeeeeeeeeeeee')
        trans3.from_user = 'mary'
        self.assertEqual(trans3.from_user, 'mary')

    def test_init_invalid_amount(self):
        '''makes sure that users do not input invalid amounts, like strings, to avoid paying bills. TypeError should be thrown'''
        #these should all raise errors
        with self.assertRaises(TypeError):
            Transaction('from_user', 'to_user', 'a string')
        with self.assertRaises(TypeError):
            Transaction('me', 'you', '')
        with self.assertRaises(TypeError):
            Transaction('from_user', 'to_user', None)

    def test__eq__(self):
        '''tests that __eq__ compares the to_user, from_user, and amount in each transaction to see if they are the same'''
        trans1 = Transaction('from', 'to', 100)
        trans11 = Transaction('from', 'to', 100)
        self.assertTrue(trans1 == trans11)  #these transactions should be equal

        trans2 = Transaction('bob', 'jill', 429024)
        trans22 = Transaction('bob', 'jill', 429024)
        trans23 = Transaction('jill', 'bob', 429024)
        self.assertTrue(trans2 == trans22)  #these transactions should be equal
        self.assertFalse(trans2 == trans23) #these transactions should not be equal

        self.assertTrue(Transaction('a', 'b', 1) == Transaction('a', 'b', 1))   #these transactions should be equal
        self.assertFalse(Transaction('a', 'b', 1) == Transaction('a', 'b', 2))  #these transactions should not be equal
    
class Test_Block(unittest.TestCase):
    '''Test cases to ensure that Block functions as intended'''
    
    def test_init(self):
        '''tests that Blocks are initilizes properly and each Block is essentially a list of Transactions'''
        #inits a few transactions
        trans1 = Transaction('from_user', 'to_user', 99)
        trans2 = Transaction('me', 'you', 4912792)
        trans3 = Transaction('person1', 'person2', 1000000000)

        block1 = Block([trans1])
        self.assertEqual(block1._block, [trans1])   #checks that transactions are added to the list: block._block

        block2 = Block([trans2])
        self.assertEqual(block2._block, [trans2])   #checks that transactions are added to the list: block._block

        block3 = Block([trans1, trans2])
        self.assertEqual(block3._block, [trans1, trans2])   #checks that transactions are added to the list: block._block

        block3_rev = Block([trans2, trans1])
        self.assertEqual(block3_rev._block, [trans2, trans1])   #checks that transactions are added to the list: block._block

        block4 = Block([trans1, trans2, trans3])
        self.assertEqual(block4._block, [trans1, trans2, trans3])   #checks that transactions are added to the list: block._block

        block5 = Block([])
        self.assertEqual(block5._block, []) #block._block should just be an empty list

    def test__eq__(self):
        '''tests that __eq__ accurately compares each component of each transaction in the block to tell if they are the same'''
        block1 = Block([Transaction('from_user', 'to_user', 999)])  
        block11 = Block([Transaction('from_user', 'to_user', 999)])
        self.assertTrue(block1 == block11)  #these blocks should be equal

        block2 = Block([Transaction('from_user', 'to_user', 999), Transaction('from_user', 'person2', 23), Transaction('person2', 'me', 23)])
        block22 = Block([Transaction('from_user', 'to_user', 999), Transaction('from_user', 'person2', 23), Transaction('person2', 'me', 23)])
        self.assertTrue(block2 == block22)  #these blocks should be equal

        block3 = Block([Transaction('from_user', 'to_user', 10), Transaction('from_user', 'person2', 58)])
        block33 = Block([Transaction('from_user', 'person2', 58), Transaction('from_user', 'to_user', 10)])
        self.assertFalse(block3 == block33) #these blocks should not be equal

    def test_add_transaction(self):
        '''tests that add_transaction succesfully adds a transaction to a block'''
        #inits a few transactions
        trans1 = Transaction('Mary', 'Marsha', 123)
        trans2 = Transaction('from_user', 'to_user', 99)
        trans3 = Transaction('me', 'you', 4912792)
        trans4 = Transaction('person1', 'person2', 1000000000)
        
        block = Block()
        self.assertEqual(block._block, [])  #block._block should be []
        self.assertIsNotNone(block._block)  #block._block should not be None
        
        block.add_transaction(trans1)
        self.assertEqual(block._block, [trans1])    #adds transaction: block._block should be updated
        self.assertNotEqual(block._block, [])

        block.add_transaction(trans2)
        self.assertEqual(block._block, [trans1, trans2])    #adds transaction: block._block should be updated
        self.assertNotEqual(block._block, [trans2, trans1]) #out of order is not correct 

        block.add_transaction(trans3)
        self.assertEqual(block._block, [trans1, trans2, trans3])    #adds transaction: block._block should be updated
        self.assertNotEqual(block._block, [trans2, trans1, trans3]) #out of order is not correct

        block.add_transaction(trans4)
        self.assertEqual(block._block, [trans1, trans2, trans3, trans4])    #adds transaction: block._block should be updated
        self.assertNotEqual(block._block, [trans2, trans1, trans4, trans3]) #out of order is not correct

    def test__hash__(self):
        '''tests that blocks are uniquely hashed but have the same hash if they contain the same Transactions'''
        #inits a few blocks
        block1 = Block([Transaction('me', 'you', 100)])
        block2 = Block([Transaction('me', 'you', 100)])
        block3 = Block([Transaction('me', 'you', 100), Transaction('yeet', 'tt', 2342)])
        block4 = Block([Transaction('e', 'yo', 10)]) 
        
        self.assertEqual(hash(block1), hash(block2))    #blocks hold the same values (are essentially the same): so they should have the same hash
        self.assertNotEqual(hash(block2), hash(block4)) #blocks do not hold the same vals
        self.assertNotEqual(hash(block1), hash(block3)) #blocks do not hold the same vals (block3 has 2 transactions)
        self.assertNotEqual(hash(block1), hash(block4)) #blocks do not hold the same vals
        self.assertNotEqual(hash(block2), hash(block3)) #blocks do not hold the same vals

class Test_Ledger(unittest.TestCase):
    '''Tests to be sure ledger is initilized and stores values properly. tests the functions in the Ledger class'''
    
    def test_init_and_set_get_item(self):
        '''Test cases to make sure Ledger get initilized properly and __getitem__ and __setitem__ are properly implemented'''
        ledge = Ledger()

        #adds user to the map and assigns a value
        ledge._ledger_hashmap['user'] = 200
        self.assertTrue('user' in ledge._ledger_hashmap)
        self.assertEqual(ledge._ledger_hashmap._len, 1)
        self.assertEqual(ledge._ledger_hashmap['user'], 200)

        ledge._ledger_hashmap['user'] = 200
        self.assertTrue('user' in ledge._ledger_hashmap)    #since entry is the same, nothing new should b added
        self.assertEqual(ledge._ledger_hashmap._len, 1)        
        self.assertEqual(ledge._ledger_hashmap['user'], 200)

        ledge._ledger_hashmap['user'] = 500                 #since key is the same, should update value and not add another
        self.assertTrue('user' in ledge._ledger_hashmap)
        self.assertEqual(ledge._ledger_hashmap._len, 1)
        self.assertEqual(ledge._ledger_hashmap['user'], 500)

        ledge._ledger_hashmap['other_user'] = 500           #val is same, but dif key, so a new entry should be added
        self.assertTrue('other_user' in ledge._ledger_hashmap)
        self.assertEqual(ledge._ledger_hashmap._len, 2)
        self.assertEqual(ledge._ledger_hashmap['user'], 500)
        self.assertEqual(ledge._ledger_hashmap['user'], ledge._ledger_hashmap['other_user'])

        ledge._ledger_hashmap['me'] = 14920342
        ledge._ledger_hashmap['you'] = 0
        me_item = ledge._ledger_hashmap['me']
        you_item = ledge._ledger_hashmap['you']
        self.assertEqual(me_item, 14920342)
        self.assertEqual(you_item, 0)

        ledge._ledger_hashmap['me'] = ledge._ledger_hashmap['you'] + 20078
        self.assertEqual(ledge._ledger_hashmap['me'], 20078)
        self.assertNotEqual(ledge._ledger_hashmap['you'], 20078)

        ledge._ledger_hashmap['you'] += 100
        self.assertEqual(ledge._ledger_hashmap['you'], 100)

        #adds and updates a bunch of key:val pairs
        for let in 'abcdefghijklmnopqrstuvwxyz':
            for i in range(10):
                with self.subTest(i=i):
                    ledge._ledger_hashmap[let] = i
                    self.assertEqual(ledge._ledger_hashmap[let], i)
        
        #we should be at 16 buckets now
        self.assertEqual(len(ledge._ledger_hashmap._L), 16)

    def test_has_funds(self):
        '''checks if has_funds works. return false if amt > user balance'''
        #inits a ledger w key val pairs
        ledge = Ledger()
        ledge._ledger_hashmap['mary'] = 12345
        ledge._ledger_hashmap['john'] = 100
        ledge._ledger_hashmap['person1'] = 10000
        ledge._ledger_hashmap['bill'] = 0

        self.assertTrue(ledge.has_funds('mary', 123))   #has enough funds for this transaction
        self.assertFalse(ledge.has_funds('mary', 23456))    #not enough funds for this transaction

        self.assertTrue(ledge.has_funds('john', 100))   #has enough funds for this transaction
        self.assertFalse(ledge.has_funds('john', 101))  #not enough funds for this transaction

        self.assertTrue(ledge.has_funds('person1', 0))  #has enough funds for this transaction
        self.assertFalse(ledge.has_funds('person1', 123141))

        self.assertFalse(ledge.has_funds('bill', 100))  #not enough funds for this transaction
        self.assertFalse(ledge.has_funds('bill', 1))    #not enough funds for this transaction

        self.assertFalse(ledge.has_funds('DNE', 1)) #not enough funds for this transaction
        self.assertFalse(ledge.has_funds('DNE', 0)) #not enough funds for this transaction

    def test_deposit(self):
        '''checks that deposit works. adds COIN to user's account'''
        ledge = Ledger()
        ledge._ledger_hashmap['john'] = 100
        self.assertEqual(ledge._ledger_hashmap['john'], 100)

        ledge.deposit('john', 23)
        self.assertEqual(ledge._ledger_hashmap['john'], 123)
        ledge.deposit('john', 200)
        self.assertEqual(ledge._ledger_hashmap['john'], 323)

        ledge._ledger_hashmap['jill'] = 0
        ledge.deposit('jill', 1000)
        self.assertEqual(ledge._ledger_hashmap['jill'], 1000)

        ledge.deposit('TOM', 200)
        self.assertEqual(ledge._ledger_hashmap['TOM'], 200)

        ledge.deposit('jose', 900000000000)
        self.assertEqual(ledge._ledger_hashmap['jose'], 900000000000)

        ledge.deposit('a', 1)
        self.assertEqual(ledge._ledger_hashmap['a'], 1)
        ledge.deposit('a', 0)
        self.assertEqual(ledge._ledger_hashmap['a'], 1)
        ledge.deposit('a', 2)
        self.assertEqual(ledge._ledger_hashmap['a'], 3)

    def test_transfer(self):
        '''checks that transfer works. subtracts COIN from user's account. in this case, end balances can 
        be <0 because the check for if the user has enought funds is in Blockchain, where these methods are used.'''
        ledge = Ledger()
        ledge._ledger_hashmap['b'] = 1000

        ledge.transfer('b', 600)
        self.assertEqual(ledge._ledger_hashmap['b'], 400)
        ledge.transfer('b', 400)
        self.assertEqual(ledge._ledger_hashmap['b'], 0)

        ledge.transfer('person1', 1)
        self.assertEqual(ledge._ledger_hashmap['person1'], -1)
        ledge.transfer('person1', 99)
        self.assertEqual(ledge._ledger_hashmap['person1'], -100)

        ledge._ledger_hashmap['carl'] = 100
        for i in range(100):
            with self.subTest(i=i):
                ledge.transfer('carl', i)
                self.assertEqual(ledge._ledger_hashmap['carl'], 100-i)

                ledge.deposit('carl', i)

class Test_Blockchain(unittest.TestCase):
    '''Test cases to ensure blockchain get initilized properly and its methods work properly'''

    def setUp(self):
        '''a bunch of transactions and blocks to be used'''
        self.trans1 = Transaction('bill', 'jane', 100)
        self.trans2 = Transaction('bob', 'jane', 99)
        self.trans3 = Transaction('person1', 'kyle', 123)
        self.trans4 = Transaction('jimmy', 'jimmie', 9999999999)
        self.trans5 = Transaction('spongebob', 'sandy', 0)
        self.trans6 = Transaction('a', 'sandy', 3)

        self.block1 = Block([self.trans1])
        self.block11 = Block([self.trans2])
        self.block12 = Block([self.trans3])
        self.block2 = Block([self.trans1, self.trans1, self.trans1])
        self.block3 = Block([self.trans1, self.trans2, self.trans3])
        self.block4 = Block([self.trans2, self.trans3, self.trans5, self.trans6])
        self.block5 = Block([self.trans1, self.trans2, self.trans3, self.trans4, self.trans5, self.trans6])
    
    def test_init(self):
        '''tests that a Blockchain is init w the correct genesis block and updated Ledger'''
        chain = Blockchain()
        self.assertEqual(len(chain._bc_ledger._ledger_hashmap), 1)      #init genesis block - 1 block
        self.assertEqual(chain._bc_ledger._ledger_hashmap['ROOT'], 999999)  #init root transaction - genesis block
        self.assertEqual(len(chain._blockchain), 1)     #only has genesis block in chain
        self.assertIsNone(chain._blockchain[0]._previous_block_hash)    #genesis block prev hash is None

        other_chain = Blockchain()
        self.assertEqual(len(other_chain._bc_ledger._ledger_hashmap), 1)      #init genesis block - 1 block
        self.assertEqual(other_chain._bc_ledger._ledger_hashmap['ROOT'], 999999)  #init root transaction - genesis block
        self.assertEqual(len(other_chain._blockchain), 1)     #only has genesis block in chain
        self.assertIsNone(other_chain._blockchain[0]._previous_block_hash)    #genesis block prev hash is None

    def test_add_block(self):
        '''tests that add_block works when the user calls it and in the distribute mining reward method'''
        chain = Blockchain()
        self.assertEqual(len(chain._blockchain), 1) #ROOT deposit - block(trans)

        chain.distribute_mining_reward('bill')
        self.assertEqual(len(chain._blockchain), 2)     #ROOT deposit and ROOT to bill block(transaction)

        self.assertTrue(chain.add_block(self.block1))   #bill has enough COIN for this transation so it should return true and add the block
        self.assertEqual(len(chain._blockchain), 3)     #all blocks to this point
        self.assertEqual(chain._blockchain[2], self.block1)

        self.assertTrue(chain.add_block(self.block2))   #bill has enough COIN for these transations so it should return true and add the block
        self.assertEqual(len(chain._blockchain), 4)     #all blocks to this point
        self.assertEqual(chain._blockchain[3], self.block2)

        self.assertFalse(chain.add_block(self.block3))   #bob jimmy and person1 have no COIN, so block was not added
        self.assertEqual(len(chain._blockchain), 4)      #len still same

        #dist COIN for all. this calls add_block every time it is called
        chain.distribute_mining_reward('bill')
        chain.distribute_mining_reward('bob')
        chain.distribute_mining_reward('person1')
        chain.distribute_mining_reward('jimmy')
        chain.distribute_mining_reward('spongebob')
        chain.distribute_mining_reward('a')

        self.assertEqual(len(chain._blockchain), 10)    #should have added 6 more blocks

        self.assertFalse(chain.add_block(self.block5)) #jimmy does not have enough COIN
        self.assertEqual(len(chain._blockchain), 10)

        self.assertTrue(chain.add_block(self.block4)) #everyone has enough COIN
        self.assertEqual(len(chain._blockchain), 11)

    def test_prev_block_hash(self):
        '''makes sure that the 'prev hash' of a block is the previous block's hash value'''
        chain = Blockchain()
        chain.distribute_mining_reward('bill')
        chain.distribute_mining_reward('bob')
        chain.distribute_mining_reward('person1')
        self.assertEqual(len(chain._blockchain), 4) #we should have 4 blocks

        self.assertIsNone(self.block1._previous_block_hash) #should be none as the block has not been added into the chain yet
        self.assertIsNone(self.block11._previous_block_hash)    #should be none as the block has not been added into the chain yet

        self.assertTrue(chain.add_block(self.block1))   #enough COIN available
        self.assertTrue(chain.add_block(self.block11))  #enough COIN available
        self.assertEqual(hash(chain._blockchain[4]), chain._blockchain[5]._previous_block_hash) #these hash vals should be the same
        self.assertEqual(hash(self.block1), self.block11._previous_block_hash)  #these hash vals should be the same

        self.assertTrue(chain.add_block(self.block2))   #enough COIN available
        self.assertEqual(hash(self.block11), self.block2._previous_block_hash)  #these hash vals should be the same

        self.assertTrue(chain.add_block(self.block3))   #enough COIN available
        self.assertEqual(hash(self.block2), self.block3._previous_block_hash)   #these hash vals should be the same

        self.assertFalse(chain.add_block(self.block4))  #a does not have any COIN yet
        self.assertEqual(None, self.block4._previous_block_hash)    #the block is not added so it does not have the prev block hash

        self.assertFalse(chain.add_block(self.block5))  #a does not have any COIN yet
        self.assertEqual(self.block5._previous_block_hash, None)    #the block is not added so it does not have the prev block hash

        self.assertTrue(chain.add_block(self.block12))  #enough COIN available
        self.assertEqual(hash(self.block3), self.block12._previous_block_hash)  #these hash vals should be the same

        for i in range(len(chain._blockchain)-1):#iterates thru each block...
            self.assertEqual(hash(chain._blockchain[i]), chain._blockchain[i+1]._previous_block_hash)   #these hash vals should be the same

    def test_validate_chain(self):
        '''tests that validate chain works: if a blocks prev hash is not the hash of the block in front of it, 
        the block with the incorrect prev hash value is returned in a list of other blocks that have been tampered with'''
        chain = Blockchain()
        chain.distribute_mining_reward('bill')
        chain.distribute_mining_reward('bob')
        chain.distribute_mining_reward('person1')
        self.assertEqual(len(chain._blockchain), 4) #should be 4 blocks

        self.assertEqual(chain.validate_chain(), [])    #no blocks should be invalid yet: i have not begun tampering

        self.assertTrue(chain.add_block(self.block1))
        self.assertTrue(chain.add_block(self.block11))

        self.assertEqual(chain.validate_chain(), [])    #no blocks should be invalid yet: i have not begun tampering
        self.assertEqual(hash(chain._blockchain[3]), chain._blockchain[4]._previous_block_hash)
        self.assertEqual(hash(chain._blockchain[4]), chain._blockchain[5]._previous_block_hash)
        
        self.block1._previous_block_hash = 12345    #changes prevblockhash of block1
        self.assertNotEqual(hash(chain._blockchain[3]), chain._blockchain[4]._previous_block_hash)
        self.assertEqual(chain.validate_chain(), [self.block1]) #block1 returned in invalid blocks list

        self.assertEqual(hash(chain._blockchain[1]), chain._blockchain[2]._previous_block_hash)
        self.assertEqual(hash(chain._blockchain[2]), chain._blockchain[3]._previous_block_hash)
        
        chain._blockchain[2]._previous_block_hash = 0   #changes prevblockhash of 3rd block in chain
        self.assertEqual(chain.validate_chain(), [Block([Transaction('ROOT','bob',1000)]), self.block1]) #both block1 and 3rd block are returned

        self.assertFalse(chain.add_block(self.block4))  #a does not have any COIN yet, block should not be added
        self.assertEqual(chain.validate_chain(), [Block([Transaction('ROOT','bob',1000)]), self.block1])

        self.assertTrue(chain.add_block(self.block12))
        self.assertTrue(chain.add_block(self.block3))
        self.assertEqual(chain.validate_chain(), [Block([Transaction('ROOT','bob',1000)]), self.block1])    #returned lsit should be same
        
        self.block3._previous_block_hash = 9999999
        self.assertEqual(chain.validate_chain(), [Block([Transaction('ROOT','bob',1000)]), self.block1, self.block3])   #returned list added block3

        self.block12._previous_block_hash = 'heeheehee'
        self.assertEqual(chain.validate_chain(), [Block([Transaction('ROOT','bob',1000)]), self.block1, self.block12, self.block3])#returned list added block12

unittest.main()
