pragma solidity ^0.4.18;

contract Store {
    
    mapping(uint => uint) users;
    
    uint owner_funds = 0;
    
    function register(uint user_id) public {
        users[user_id] = 500; // Default 500 balance
    }
    
    function getUserFunds(uint user_id) view public returns (uint) {
        return users[user_id];
    }
    
    function getOwnerFunds() view public returns (uint) {
        return owner_funds;
    }
    
    function unregister(uint user_id) public{
        // Remove user_id from users map
        owner_funds  = owner_funds + users[user_id];    // Take that users money
        delete users[user_id];
    }
    
    function deposit(uint user_id, uint fundsToAdd) public{
        // Update funds for specified user in users map
        users[user_id] = users[user_id] + fundsToAdd;
    }
    
    function pay(uint buyer, uint seller, uint amount) public{
        // Remove funds from buyers account
        deposit(buyer, -amount);
        // Deposit funds into sellers account
        deposit(seller, amount);
    }
    
    function buy(uint listing_id, uint buyer, uint seller, uint amount) public{
        pay(buyer, seller, amount);
        Buy(listing_id, buyer, seller, amount); // Trigger event to be recorded on the blockchain
    }
    
    event Buy(
        uint listing_id,
        uint buyer,
        uint seller,
        uint amount
    );
}