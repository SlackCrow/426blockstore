pragma solidity ^0.4.18;

contract Store {
    
    struct Listing {
        uint user_id;
        string title;
        string description;
        uint price;
        string status;
        string date_listed;
        string date_sold;
    }
    
    struct User {
        string username;
        string password;
        uint funds;
    }
    
    
    mapping(uint => Listing) public listings;
    mapping(uint => User) public users;
    
    uint[] public user_ids;
    uint[] public listing_ids;
    
    function addUser(uint user_id, string memory username, string memory password, uint funds) public {
        // Create User struct
        User memory user = users[user_id];
        user.username = username;
        user.password = password;
        user.funds = funds;
        // Add user to users mapping
        user_ids.push(user_id) -1;
    }
    
    function getUser(uint user_id) view public returns (string memory, string memory, uint) {
        return (users[user_id].username, users[user_id].password, users[user_id].funds);
    }
    
    function getUsers() view public returns(uint[] memory){
        return user_ids;
    }
    
    function addListing(uint listing_id, string memory title, string memory description, uint price, string memory status, string memory date_listed, string memory date_sold) public {
        // Create Listing struct
        Listing memory listing = listings[listing_id];
        listing.title = title;
        listing.description = description;
        listing.price = price;
        listing.status = status;
        listing.date_listed = date_listed;
        listing.date_sold = date_sold;
        // Add listing to listings mapping
        listing_ids.push(listing_id) -1;
    }
    
    function getListing(uint listing_id) view public returns (uint, string memory, string memory, uint, string memory, string memory, string memory) {
        return (listings[listing_id].user_id, listings[listing_id].title, listings[listing_id].description, 
        listings[listing_id].price, listings[listing_id].status, listings[listing_id].date_listed, listings[listing_id].date_sold);
    }
    
    function getListings() view public returns(uint[] memory){
        return listing_ids;
    }
    
    function removeListing(uint listing_id) public{
        // Remove listing_id from listings map
        delete listings[listing_id];
        for(uint i=0;i<listing_ids.length; i++){
            if(listings_ids[i] == listing_id)
            {
                delete listings_ids[i];
                break;
            }
        }
    }
    
    function removeUser(uint user_id) public{
        // Remove user_id from users map
        delete users[user_id];
        for(uint i=0;i<user_ids.length; i++){
            if(listings_ids[i] == user_id)
            {
                delete user_ids[i];
                break;
            }
        }
    }
    
    function addFunds(uint user_id, uint fundsToAdd) public{
        // Update funds for specified user in users map
    }
    
    function removeFunds(uint user_id, uint fundsToRemove) public{
        // Update funds for specified user in users map
    }
    
    function settlePayment(uint listing_id, uint buyer, uint seller) public{
        // Obtain price of listing through listings map
        // Call removeListing method and pass in listing_id
        // Call addFunds on seller with price
        // Call removeFunds on buyer with price
    }
}
