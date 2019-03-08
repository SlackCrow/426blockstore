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


    mapping(uint => Listing) listings;
    mapping(uint => User) users;

    uint[] public user_ids;
    uint[] public listing_ids;

    function addUser(uint user_id, string username, string password, uint funds) public {
        // Create User struct
        User user = users[user_id];
        user.username = username;
        user.password = password;
        user.funds = funds;
        // Add user to users mapping
        user_ids.push(user_id) -1;
    }

    function getUser(uint user_id) view public returns (string, string, uint) {
        return (users[user_id].username, users[user_id].password, users[user_id].funds);
    }

    function getUsers() view public returns(uint[]){
        return user_ids;
    }

    function addListing(uint listing_id, uint user_id, string title, string description, uint price, string status, string date_listed, string date_sold) public {
        // Create Listing struct
        Listing listing = listings[listing_id];
        listing.user_id = user_id;
        listing.title = title;
        listing.description = description;
        listing.price = price;
        listing.status = status;
        listing.date_listed = date_listed;
        listing.date_sold = date_sold;
        // Add listing to listings mapping
        listing_ids.push(listing_id) -1;
    }

    function getListing(uint listing_id) view public returns (uint, string, string, uint, string, string, string) {
        return (listings[listing_id].user_id, listings[listing_id].title, listings[listing_id].description,
        listings[listing_id].price, listings[listing_id].status, listings[listing_id].date_listed, listings[listing_id].date_sold);
    }

    function getListings() view public returns(uint[]){
        return listing_ids;
    }

    function removeListing(uint listing_id) public{
        // Remove listing_id from listings map
        delete listings[listing_id];
    }

    function removeUser(uint user_id) public{
        // Remove user_id from users map
        delete users[user_id];
    }

    function addFunds(uint user_id, uint fundsToAdd) public{
        // Update funds for specified user in users map
        User user = users[user_id];
        user.funds = user.funds + fundsToAdd;
        AddFunds(user_id, fundsToAdd);
    }

    function removeFunds(uint user_id, uint fundsToRemove) public{
        // Update funds for specified user in users map
        User user = users[user_id];
        user.funds = user.funds - fundsToRemove;
        RemoveFunds(user_id, fundsToRemove);
    }

    function settlePayment(uint listing_id, uint buyer, uint seller, uint amount) public{
        // Obtain price of listing through listings map
        Listing listing = listings[listing_id];
        uint listingPrice = listing.price;
        removeListing(listing_id);
        addFunds(seller, amount);
        removeFunds(buyer, amount);
        SettlePayment(listing_id, buyer, seller, amount);
        // Call removeListing method and pass in listing_id
        // Call addFunds on seller with price
        // Call removeFunds on buyer with price
    }

    event SettlePayment(
        uint listing_id,
        uint buyer,
        uint seller,
        uint amount
    );

    event AddFunds(
        uint seller,
        uint amount
    );

    event RemoveFunds(
        uint buyer,
        uint amount
    );
}