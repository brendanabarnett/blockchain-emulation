# Blockchain Emulation
A simplified emulation of a blockchain system: a decentralized ledger of transactions across a P2P network

### Features:
- **Transaction Handling:** Tracks COIN transactions between users
- **Block Structure:** Organizes transactions into blocks linked via previous block hash
- **Ledger Management:** Maintains user balances through a hash mapping system

### Classes:
- **Transaction:** Represents a single COIN transaction
- **Block:** Contains a collection of transactions linked via hash
- **Ledger:** Manages user balances using HashMapping
- **Blockchain:** Manages the chain of blocks and ledger interactions

### How It Works:
- Users can conduct transactions with COIN
- Blocks are added to the blockchain if transactions are valid
- The ledger ensures users have sufficient funds for transactions

### Next Steps:
- Utilize the Elliptic Curve Digital Signature Algorithm (ECDSA) to generate COIN keys
- Implement consensus algorithms like Proof of Work (PoW) or Proof of Stake (PoS) to secure the network and validate transactions
- Create a network architecture to simulate peer-to-peer communication between nodes
