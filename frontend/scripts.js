function submitLogin() {
    var loginData = new FormData(document.getElementById("loginForm"));
    // TODO: Send the login data to the server

    window.location.href = "restaurant.html";
}

function generateRestaurantHtml(restaurantInfo) {
    // Get the info div element
    var infoDiv = document.getElementById("restaurantInfo");

    // Create a paragraph element for each piece of store information and append it to the info div
    for (var key in restaurantInfo) {
        if (restaurantInfo.hasOwnProperty(key)) {
            var paragraph = document.createElement("p");
            paragraph.textContent = key + ": " + restaurantInfo[key];
            infoDiv.appendChild(paragraph);
        }
    }

}

function getResaurant() {
    // TODO: get restaurant information from server

    var restaurantInfo = {
        name: "My Restaurant",
        email: "myrestaurant@example.com",
        mobile: "+1234567890",
        address: "123 Main Street, City, Country",
        opening_time: "9:00 AM",
        closing_time: "6:00 PM"
      };

      generateRestaurantHtml(restaurantInfo);
}


function submitRestaurantForm(event) {
    event.preventDefault(); // Prevent default form submission

    // Get form data
    var formData = {
      name: document.getElementById("name").value,
      email: document.getElementById("email").value,
      mobile: document.getElementById("mobile").value,
      address: document.getElementById("address").value,
      opening_time: document.getElementById("opening_time").value,
      closing_time: document.getElementById("closing_time").value
    };
  
    // TODO: Send form data to server

    alert("the information submitted");
    window.location.href = "restaurant.html";
}


function deleteFood(itemId) {
    // TODO
    alert(itemId);
}


function generateItemstHtml(items) {
    // Get the info div element
    var itemsDiv = document.getElementById("items");

    // Create a paragraph element for each piece of store information and append it to the info div
    items.forEach(item => {
        // var itemDiv = document.createElement("div");
        var itemDivContainer = document.createElement("div");
        itemDivContainer.classList.add("col-md-4");
        var itemDiv = document.createElement("div");
        itemDiv.classList.add("item");

        for (var key in item) {
            if (item.hasOwnProperty(key)) {
                if (key === "id" || key === "image")
                    continue;
                else if (key === "name")
                    var paragraph = document.createElement("h3");
                else
                    var paragraph = document.createElement("p");
                paragraph.textContent = key + ": " + item[key];
                itemDiv.appendChild(paragraph);
            }
        }
        
        // Create the edit food button
        var editButton = document.createElement("button");
        editButton.textContent = "Edit";
        editButton.classList.add("btn");
        editButton.classList.add("btn-primary");
        editButton.addEventListener("click", () => { window.location.href = "edit_item.html"; });
        
        // Create the delete food button
        var deleteButton = document.createElement("button");
        deleteButton.textContent = "Delete";
        deleteButton.classList.add("btn");
        deleteButton.classList.add("btn-danger");
        deleteButton.addEventListener("click", () => { deleteFood(item.id); });
        
        // Append the created buttons to their respective parent div
        itemDiv.appendChild(editButton);
        itemDiv.appendChild(deleteButton);
        
        itemDivContainer.appendChild(itemDiv);

        itemsDiv.appendChild(itemDivContainer);
    });
}


function getItems() {
    // TODO: get items from server

    var items = [
        {
            id: 1,
            name: "First Food",
            description: "This food is made from this and that",
            cost: 10,
            price: 15,
            is_active: true,
            image: ""
        },
        {
            id: 2,
            name: "second Food",
            description: "This food is made from this and that",
            cost: 14,
            price: 24,
            is_active: true,
            image: ""
        },
        {
            id: 3,
            name: "third Food",
            description: "This food is made from this and that",
            cost: 20,
            price: 30,
            is_active: true,
            image: ""
        }
    ];

      generateItemstHtml(items);
}


function submitItemEdit(event) {
    event.preventDefault(); // Prevent default form submission

    // Get form data
    var formData = {
      name: document.getElementById("name").value,
      description: document.getElementById("description").value,
      cost: document.getElementById("cost").value,
      price: document.getElementById("price").value,
      is_active: document.getElementById("is_active").value,
    };
  
    // TODO: Send form data to server

    alert("the information submitted");
    window.location.href = "items.html";
}


function submitItemCreate(event) {
    event.preventDefault(); // Prevent default form submission

    // Get form data
    var formData = {
      name: document.getElementById("name").value,
      description: document.getElementById("description").value,
      cost: document.getElementById("cost").value,
      price: document.getElementById("price").value,
      is_active: document.getElementById("is_active").value,
    };
  
    // TODO: Send form data to server

    alert("the information submitted");
    window.location.href = "items.html";
}

