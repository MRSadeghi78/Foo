const serverURL = "https://foo-backend.cognix.tech/"

/**
 * Function to handle login form submission.
 *
 * This function gathers the login data from the form, constructs a POST request with the email and password,
 * and sends it to the server. If the login is successful, the token is stored in local storage and the user
 * is redirected to the restaurant page. If the login fails, an alert is shown with the error message.
 */
function submitLogin() {
    var loginData = new FormData(document.getElementById("loginForm"));
    var username = document.getElementById("email").value;
    var password = document.getElementById("password").value;
    
    var request = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            "email": username,
            "password": password
          })
    };

    fetch(serverURL + 'auth/login/', request)
    .then(response => {
        if (response.ok) {
            return response.json();
        }
        return Promise.reject(response); 
    })
    .then(data=>{
        localStorage.setItem("token", "Token " + data.token);
        window.location.href = "restaurant.html";
    }).catch((response) => {
        response.json().then(data=>{
            alert("Error " + response.status + ": " + data.detail);
        })
    });

}

/**
 * Function to generate HTML content for restaurant information.
 *
 * This function takes restaurant information and updates the DOM to display the restaurant's details,
 * including its logo, name, email, mobile number, address, opening and closing times, creation, and update timestamps.
 *
 * @param {Object} restaurantInfo - The information of the restaurant.
 */
function generateRestaurantHtml(restaurantInfo) {
    // Get the info div element
    var infoDiv = document.getElementById("restaurantInfo");

    infoDiv.innerHTML = `
    <img style="max-height: 300px; width: auto;" src="${serverURL+restaurantInfo.logo}" class="card-img-top" alt="${restaurantInfo.name}">
    <div class="card-body">
        <h5 class="card-title">${restaurantInfo.name}</h5>
        <p class="card-text">Email: ${restaurantInfo.email}</p>
        <p class="card-text">Mobile: ${restaurantInfo.mobile}</p>
        <p class="card-text">Address: ${restaurantInfo.address}</p>
        <p class="card-text">Opeining Time: ${restaurantInfo.opening_time}</p>
        <p class="card-text">Closing Time: ${restaurantInfo.closing_time}</p>
        <p class="card-text">Create at: ${restaurantInfo.created_at}</p>
        <p class="card-text">Updated at: ${restaurantInfo.updated_at}</p>
    </div>
    `;

    localStorage.setItem("restaurantId", restaurantInfo.id);
}

/**
 * Function to fetch restaurant information from the server.
 *
 * This function sends a GET request to the server to retrieve the restaurant's information using the stored token
 * for authorization. If the request is successful, it stores the restaurant ID and generates the HTML to display
 * the restaurant information. If the request fails, it shows an alert with the error message.
 */

function getResaurant() {
    // TODO: get restaurant information from server

    var request = {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': localStorage.getItem("token") 
        }
    };

    fetch(serverURL + 'restaurant/', request)
    .then(response => {
        if (response.ok) {
            return response.json();
        }
        return Promise.reject(response); 
    })
    .then(data=>{
        localStorage.setItem("temp_res_id", data.id);
        generateRestaurantHtml(data);
    }).catch((response) => {
        response.json().then(data=>{
            alert("Error " + response.status + ": " + data.detail);
        })
    });

      
}

/**
 * Function to handle restaurant form submission.
 *
 * This function gathers the restaurant form data, constructs a PUT request with the form data, and sends it to the server.
 * If the request is successful, it alerts the user and redirects them to the restaurant page. If the request fails,
 * an alert is shown with the error message.
 *
 * @param {Event} event - The form submission event.
 */

function submitRestaurantForm(event) {
    event.preventDefault(); // Prevent default form submission

    var formData = new FormData();

formData.append("name", document.getElementById("name").value);
formData.append("email", document.getElementById("email").value);
formData.append("mobile", document.getElementById("mobile").value);
formData.append("address", document.getElementById("address").value);
formData.append("opening_time", document.getElementById("opening_time").value);
formData.append("closing_time", document.getElementById("closing_time").value);
formData.append("logo", document.getElementById("logo").files[0], document.getElementById("logo").files[0].name);

  
    // TODO: Send form data to server
    var request = {
        method: 'PUT',
        headers: { 
            'Accept': 'application/json',
            'Authorization': localStorage.getItem("token")
        },
        body: formData
    };

    fetch(serverURL + 'restaurant/', request)
    .then(response => {
        if (response.ok) {
            return response.json();
        }
        return Promise.reject(response); 
    })
    .then(data=>{
        alert("the information submitted");
        window.location.href = "restaurant.html";
    }).catch((response) => {
        response.json().then(data=>{
            alert("Error " + response.status + ": " + data.detail);
        })
    });

}

/**
 * Function to delete an item/food from the restaurant.
 *
 * This function sends a DELETE request to the server to remove an item/food from the restaurant using the stored token
 * for authorization. If the request is successful, it alerts the user and reloads the page. If the request fails,
 * an alert is shown with the error message.
 *
 * @param {number} itemId - The ID of the item to be deleted.
 */

function deleteFood(itemId) {
    var request = {
        method: 'Delete',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': localStorage.getItem("token") 
        }
    };

    fetch(serverURL + "items/" + itemId + "/", request)
    .then(response => {
        if (response.ok) {
            return response.json();
        }
        return Promise.reject(response); 
    })
    .then(data=>{
        alert("Item deleted successfully");
        window.location.reload();
    }).catch((response) => {
        response.json().then(data=>{
            alert("Error " + response.status + ": " + data.detail);
        })
    });
}

/**
 * Function to generate HTML content for a list of items.
 *
 * This function takes an array of item objects and updates the DOM to display each item's details,
 * including its image, name, description, cost, price, and active status. It also includes buttons
 * for editing and deleting each item.
 *
 * @param {Array<Object>} items - The array of item objects to be displayed.
 */

function generateItemstHtml(items) {
    // Get the info div element
    var itemsDiv = document.getElementById("items");
    items.forEach(item => {
        console.log("ID: " + item.id);
        const itemCard = `
          <div class="col-md-4">
            <div class="card">
              <img src="${serverURL+item.image}" class="card-img-top" alt="${item.name}">
              <div class="card-body">
                <h5 class="card-title">${item.name}</h5>
                <p class="card-text">${item.description}</p>
                <p class="card-text">Cost: ${item.cost}</p>
                <p class="card-text">Price: ${item.price}</p>
                <p class="card-text">Active: ${item.is_active}</p>
                <div class="row" >
                <button class="btn btn-primary edit-btn" data-item-id="${item.id}">Edit</button>
                <button class="btn btn-danger delete-btn" data-item-id="${item.id}">Delete</button>
                </div>
              </div>
            </div>
          </div>
        `;
        itemsDiv.innerHTML += itemCard;

    });

    // Add event listeners to the edit and delete buttons
    var editButtons = document.querySelectorAll('.edit-btn');
    editButtons.forEach(button => {
        button.addEventListener('click', function() {
            var itemId = button.dataset.itemId;

            // Execute command for editing item with itemId
            window.location.href = "edit_item.html";
            localStorage.setItem("currentId", itemId);
        });
    });

    var deleteButtons = document.querySelectorAll('.delete-btn');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function() {
            var itemId = button.dataset.itemId;

            // Execute command for deleting item with itemId
            deleteFood(itemId);
        });
    });
    
}

/**
 * Function to fetch items associated with a specific restaurant from the server.
 *
 * This function sends a GET request to the server to retrieve the items for the restaurant identified by the
 * `temp_res_id` stored in local storage. If the request is successful, it generates the HTML to display the items.
 * If the request fails, it shows an alert with the error message.
 */

function getItems() {
    var request = {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': localStorage.getItem("token") 
        }
    };

    fetch(serverURL + 'items/'+localStorage.getItem('temp_res_id')+'/', request)
    .then(response => {
        if (response.ok) {
            return response.json();
        }
        return Promise.reject(response); 
    })
    .then(data=>{
        generateItemstHtml(data);
    }).catch((response) => {
        response.json().then(data=>{
            alert("Error " + response.status + ": " + data.detail);
        })
    });

}

/**
 * Function to handle the submission of an item edit form.
 *
 * This function gathers the item edit form data, constructs a PUT request with the form data, and sends it to the server.
 * If the request is successful, it alerts the user and redirects them to the items page. If the request fails,
 * an alert is shown with the error message.
 *
 * @param {Event} event - The form submission event.
 */

function submitItemEdit(event) {
    event.preventDefault(); // Prevent default form submission

    // Get form data
    var formData = new FormData();
    formData.append("name", document.getElementById("name").value);
    formData.append("description", document.getElementById("description").value);
    formData.append("cost", document.getElementById("cost").value);
    formData.append("price", document.getElementById("price").value);
    formData.append("is_active", document.getElementById("is_active").value);
    formData.append("image", document.getElementById("image").files[0], document.getElementById("image").files[0].name);


    // Send form data to server
    var itemId = localStorage.getItem("currentId");
    var request = {
        method: 'PUT',
        headers: { 
            'Accept': 'application/json',
            'Authorization': localStorage.getItem("token")
        },
        body: formData
    };

    fetch(serverURL + 'items/' + itemId + '/', request)
    .then(response => {
        if (response.ok) {
            return response.json();
        }
        return Promise.reject(response); 
    })
    .then(data=>{
        alert("the information submitted");
        window.location.href = "items.html";
    }).catch((response) => {
        response.json().then(data=>{
            alert("Error " + response.status + ": " + data.detail);
        })
    });

}

/**
 * Function to handle the submission of a new item creation form.
 *
 * This function gathers the item creation form data, constructs a POST request with the form data, and sends it to the server.
 * If the request is successful, it alerts the user and redirects them to the items page. If the request fails,
 * an alert is shown with the error message.
 *
 * @param {Event} event - The form submission event.
 */

function submitItemCreate(event) {
    event.preventDefault(); // Prevent default form submission

    // Get form data
    var formData = new FormData();
    formData.append("restaurant_id", localStorage.getItem("restaurantId"));
    formData.append("name", document.getElementById("name").value);
    formData.append("description", document.getElementById("description").value);
    formData.append("cost", document.getElementById("cost").value);
    formData.append("price", document.getElementById("price").value);
    formData.append("is_active", document.getElementById("is_active").value);
    formData.append("image", document.getElementById("image").files[0], document.getElementById("image").files[0].name);
  
    // TODO: Send form data to server
    var itemId = localStorage.getItem("currentId");
    var request = {
        method: 'POST',
        headers: { 
            'Accept': 'application/json',
            'Authorization': localStorage.getItem("token")
        },
        body: formData
    };

    fetch(serverURL + 'items/', request)
    .then(response => {
        if (response.ok) {
            return response.json();
        }
        return Promise.reject(response); 
    })
    .then(data=>{
        alert("the information submitted");
        window.location.href = "items.html";
    }).catch((response) => {
        response.json().then(data=>{
            alert("Error " + response.status + ": " + data.detail);
        })
    });

}

/**
 * Function to delete all items from the server.
 *
 * This function sends a DELETE request to the server to remove all items using the stored token for authorization.
 * If the request is successful, it alerts the user and reloads the page. If the request fails, it shows an alert
 * with the error message.
 */

function deleteAllItems() {
    var request = {
        method: 'Delete',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': localStorage.getItem("token") 
        }
    };

    fetch(serverURL + "items/all/", request)
    .then(response => {
        if (response.ok) {
            return response.json();
        }
        return Promise.reject(response); 
    })
    .then(data=>{
        alert("All items deleted successfully");
        window.location.reload();
    }).catch((response) => {
        response.json().then(data=>{
            alert("Error " + response.status + ": " + data.detail);
        })
    });
}


/**
 * Function to fetch and display the user's location based on their IP address.
 *
 * This function sends a GET request to the server to retrieve the user's location information.
 * If the request is successful, it displays the user's IP address and location in the DOM.
 * If the request fails, it shows an alert with the error message.
 */

function getLocation() {

    var locationDiv = document.getElementById("location");

    var request = {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    };

    fetch(serverURL + 'location/', request)
    .then(response => {
        if (response.ok) {
            return response.json();
        }
        return Promise.reject(response); 
    })
    .then(data=>{
        console.log(data);
        locationDiv.innerHTML = `
            <p>Your IP is: ${data.query} and your location is: ${data.city}, ${data.country} </p>
        `;
    }).catch((response) => {
        response.json().then(data=>{
            alert("Error " + response.status + ": " + data.detail);
        })
    });

}