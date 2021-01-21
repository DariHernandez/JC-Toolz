const scriptURL = 'https://script.google.com/macros/s/AKfycbwJQk7QFq4gD2zc5JuLiEqJxHxlyJbHftXzVciUfGCqlDkBRhox8vGJDQ/exec'
const form = document.forms['submit-to-google-sheet']

// GSet information to google sheet when the form is submit
form.addEventListener('submit', e => {
    e.preventDefault()
    fetch(scriptURL, { method: 'POST', body: new FormData(form)})
    .then(response => console.log('Success!', response))
    .catch(error => console.error('Error!', error.message))
})

// Genarete drop list of cities

// Dictionary of cities
const cities = {
    "AK": ["Anchorage"],
    "AL": ["Birmingham", "Huntsville", "Mobile"],
    "AZ": ["Phoenix/Tucson"],
    "CA": ["Los Angeles", "San Bernardino", "San Fran./Oakland", "Stockton/Lathrop"],
    "CO": ["Denver"], 
    "DE": ["Wilmington, DE"],
    "FL": ["Jacksonville", "Miami/Ft.Lauderdale", "Panama City", "Tampa", "Titusville", "Winter Haven"],
    "GA": ["Atlanta", "Chatsworth/ARP", "Cordele", "Savannah"],
    "HI": ["Honolulu"],
    "IL": ["Chicago", "Decatur"],
    "IN": ["Indianapolis"],
    "KY": ["Georgetown", "Louisville"],
    "LA": ["New Orleans"],
    "MA": ["Boston", "Springfield", "Worcester/Ayer"],
    "MD": ["Baltimore"],
    "ME": ["Portland (Maine)"],
    "MI": ["Detroit"],
    "MN": ["Duluth", "Minne/St. Paul"],
    "MO": ["Kansas City", "St. Louis"],
    "MS": ["Gulfport", "Jackson"],
    "NC": ["Charlotte", "Greensboro", "Wilmington"],
    "ND": ["Minot"],
    "NE": ["Omaha"],
    "NM": ["Albuquerque"],
    "NV": ["Las Vegas", "Reno"],
    "NY": ["Albany", "Buffalo", "New York City/NJ", "Syracuse"],
    "OH": ["Cincinnati", "Cleveland", "Columbus", "Toledo/North Balt."],
    "OR": ["Portland"],
    "PA": ["Allentown/Beth.", "Chambrg/Greencastle", "Harrisburg/Rutherford", "Philadelphia", "Pittsburgh", "Scranton/Taylor"],
    "SC": ["Charleston", "Dillon", "Greer"],
    "TN": ["Memphis", "Nashville"],
    "TX": ["Dallas/Ft. Worth", "El Paso", "Freeport", "Houston", "Laredo", "Rio Valley/McAllen", "San Antonio"],
    "UT": ["Salt Lake City"],
    "VA": ["Front Royal", "Norfolk", "Richmond"],
    "WA": ["Quincy", "Seattle/Tacoma", "Spokane"],
    "WI": ["Chippewa Falls"],
    "WV": ["Prichard"]
}

// Variable of the current state
let current_state = "N/A"

// Get drop list (html element) of states
let state_drop_list = document.querySelector ("#state")

// Get drop list (html element) of cities
let city_drop_list = document.querySelector ("#city")

// Get Label of drop list (html element) of cities
let city_drop_list_label = document.querySelector ("#city_label")

// Update the current state when the drop list change
state_drop_list.addEventListener('change', (event) => {
    current_state = state_drop_list.value

    // Update the cities in the city_drop_list
    update_cities ()   
    

});





// Function to update city list
function update_cities () {

    // Verify the value of the state
    if (current_state == "N/A") {
        // Add class to the drop list of cities, to hide it with css
        city_drop_list.classList.add ("hide")
        city_drop_list_label.classList.add ("hide")

    } else {
        // Remove class to the drop list of cities, to show it with css
        city_drop_list.classList.remove ("hide")
        city_drop_list_label.classList.remove ("hide")
    }

    // Get all last options of the cities list
    last_options = document.querySelectorAll ("#city option")

    // Loop for each option of the city list
    for (let i=0; i<last_options.length; i++) {
        // Remove each last option
        city_drop_list.removeChild (last_options[i])
    }


    // Get a list of the cities for the current state
    current_options = cities[current_state]
    
    // Make a loop for each new option of the drop list
    for (let i=0; i<current_options.length; i++) {

        // Create option element
        option_elm = document.createElement ("option")

        // Text of the current option (the current city)
        option_text = document.createTextNode (current_options[i])

        // Add text to option element
        option_elm.appendChild (option_text)
        
        // Add option to drop list of cities
        city_drop_list.appendChild(option_elm)

    }
}
