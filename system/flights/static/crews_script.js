var flights_el;
window.onload = function () {
	flights_el = document.getElementById("flights");
};
var flights;
var crews = new Map();
var api_root = "/api/";

var getCookie = function (name) {
	let value = "; " + document.cookie;
	let parts = value.split("; " + name + "=");
	if (parts.length == 2) 
		return parts.pop().split(";").shift();
};

function formatDate(date) {
	let options = {  
		year: "numeric", month: "short",  
		day: "numeric", hour: "2-digit", minute: "2-digit"  
	};
	date = new Date(date);
	toLocale = date.toLocaleDateString("en-US", options);
	return toLocale;
}

// function responsible for creating select column for a given row
function createSelect(flightId) {
	let div = document.createElement("div");
	let select = document.createElement("select");
	select.name = "Change crew";
	select.value = "";
	for (let [key, val] of crews) {
		let option = document.createElement("option");
		option.value = key;
		option.innerText = val;
		select.appendChild(option);
	}
	div.appendChild(select);
	let button = document.createElement("button");
	div.appendChild(button);
	button.innerText = "Submit";
	select.setAttribute("id", "select" + flightId);
	button.setAttribute("onClick", "patchCrew(" + flightId + ")");
	return div;
}

// function responsible for creating one row in flights table
function createRow(data) {
	let actRow = document.createElement("tr");
	children = [];
	children.push(data.start_airport.city + "(" + data.start_airport.country +
		") -> " + data.final_airport.city + "(" + data.final_airport.country);
	children.push(data.airplane.official_number);
	children.push(formatDate(data.departure_time));
	children.push(formatDate(data.arrival_time));
	for (let child of children) {
		let elem = document.createElement("td");
		elem.innerText = child;
		actRow.appendChild(elem);
	}
	let crew = document.createElement("td");
	if (data.crew === null)
		crew.innerText = "";
	else 
		crew.innerText = crews.get(data.crew);
	crew.setAttribute("id", "crew" + data.id);
	actRow.appendChild(crew);
	actRow.appendChild(createSelect(data.id));
	flights_el.appendChild(actRow);
}

// function resposnbiel for getting crews from API
function fetchCrews() {
	fetch(api_root + "crew/")
	.then((response) => response.json())
	.then((data) => {
		for (let crew of data)
			crews.set(crew.id, crew.captainsName + " " + crew.captainsSurname);
		fetchFlights();
	});
}

// function responsible for getting flights from API
function fetchFlights() {
	fetch(api_root + "flights/")
	.then((response) => response.json())
	.then((data) => {
		flights = data;
		for (let flight of data)
			createRow(flight);
	});
}

// function responsible for changing crew for a give flight
function patchCrew(flightId) {
	let csrftoken = getCookie("csrftoken");
	let url = this.api_root + "flights/" + flightId + "/";
	let crew = document.getElementById("select" + flightId).value;
	let fetchData = {
		method: "PATCH",
		body: JSON.stringify({
			"crew": crew
		}),
		credentials: "same-origin",
		headers: {
			"content-type": "application/json",
			"X-CSRFToken": csrftoken
		},
	};
	fetch(url, fetchData)
	.then((response) => {
		if (response.status === 400)
			alert("This crew is busy!");
		if (response.status === 401)
			alert("You need to bo logged in to set crew. Head to localhost:8000/auth/login.");
		if (response.ok === false)
			return "";
		return response.json();

	})
	.then((data) => {
		if (data != "")
			crewElement = document.getElementById("crew" + flightId).innerText = crews.get(data.crew);
	})
	.catch((error) => console.log(error));
}

// function responsible for adding new crew
function postCrew() {
	let captainsName = document.getElementById("captainsName").value;
	let captainsSurname = document.getElementById("captainsSurname").value;
	if (captainsName === "" || captainsSurname === "") {
		alert("Make sure to write both name and surname!");
		document.getElementById("captainsName").value = "";
		document.getElementById("captainsSurname").value = "";
	} else {
		let csrftoken = getCookie("csrftoken");
		let url = api_root + "crew/";
		let fetchData = {
			method: "POST",
			body: JSON.stringify({
				"captainsName": captainsName,
				"captainsSurname": captainsSurname,
			}),
			credentials: "same-origin",
			headers: {
				"content-type": "application/json",
				"X-CSRFToken": csrftoken
			},
		};

		fetch(url, fetchData)
		.then((response) => {
			if (response.status === 400)
				alert("This name and surname are already in use!");
			if (response.status === 401)
				alert("You need to bo logged in to create new crew. Head to localhost:8000/auth/login.");
			if (response.ok === false)
				return "";
			return response.json();
		})
		.then((data) => {
			if (data != "") {
				crewId = data.crew;
				crewName = captainsName + " " + captainsSurname;
				crews.set(crewId + crewName);
				for (let flight of flights) {
					let newOption = document.createElement("option");
					newOption.value = crewId;
					newOption.innerText = crewName;
					let select = document.getElementById("select" + flight.id);
					select.appendChild(newOption);
				}
				alert("New crew added!");
			}
			document.getElementById("captainsName").value = "";
			document.getElementById("captainsSurname").value = "";
		})
		.catch((error) => console.log(error));
	}
}

fetchCrews();