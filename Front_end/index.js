//var token = "d5ed6735def24bd682b378749fab5eb1"
var index = 0;
var add_type = "new"

function get_employees() {
	//document.getElementById("register-btn").style.display = "none"
	//document.getElementById("login-btn").style.display = "none"
	document.getElementById("alert").style.display = "none"
	var token = localStorage.getItem('token')
	var user_id = localStorage.getItem('user_id')
	console.log(token)
	console.log(user_id)
	document.getElementById("form-info").style.display = "none"
	//document.getElementById("table-info").style.display = "block"
	//document.getElementById("footer-info").style.display = "block"
	data = ""
	add_type = "new"
	console.log(token)
	fetch("http://0.0.0.0/employees",
		{
			headers: {
				'Accept': 'application/json',
				'Content-Type': 'application/json',
				'role': 'admin',
				'Authorization': 'bearer ' + token,
				"user" : user_id
			},
			method: "GET",
			mode: "cors"
		})
		.then(function (res) {
			console.log("data arrived")
			if(res.ok) {
				return res.json();
			}
			return res.json().then(text => {throw new Error(text["description"])})
		}).then(function (data) {
			console.log(data)
			ele = document.getElementById("table-body")
			data = data["employees"]
			for (i in data) {
				let emp = data[i]
				let x = emp.emp_id
				let row = ele.insertRow()
				row.insertCell(0).innerText = emp.emp_id
				row.insertCell(1).innerText = emp.emp_name
				row.insertCell(2).innerText = emp.emp_salary
				row.insertCell(3).innerText = emp.emp_address
				row.insertCell(4).innerText = emp.emp_designation
				let edit_btn = document.createElement("button");
				edit_btn.addEventListener("click", function () {
					let y = emp.emp_id
					edit_employee(y)
				}
				)
				//edit_btn.onclick = edit_employee.bind(emp.emp_id)
				edit_btn.innerHTML = "Edit"
				let delete_btn = document.createElement("button")
				delete_btn.addEventListener("click", function () {
					let y = x;
					delete_employee(y);
				})

				delete_btn.innerHTML = "Delete"
				edit = row.insertCell(5)
				edit.append(edit_btn)
				edit.append(delete_btn)
			}
		})
		.catch(function (res) { 
			document.getElementById("alert").style.display = "block"
			document.getElementById("error-msg").innerHTML= res
			console.log(res) })
}

function edit_employee(x) {
	console.log(x)
	document.getElementById("form-info").style.display = "block"
	document.getElementById("table-info").style.display = "none"
	document.getElementById("footer-info").style.display = "none"
	var token = localStorage.getItem('token')
	var user_id = localStorage.getItem('user_id')
	fetch("http://0.0.0.0/employee/" + x.toString(),
		{
			headers: {
				'Accept': 'application/json',
				'Content-Type': 'application/json',
				'role': 'admin',
				'Authorization': 'bearer ' + token,
				"user" : user_id
			},
			method: "GET",
			mode: "cors"
		})
		.then(function (res) {
			console.log("data arrived")
			if(res.ok) {
				return res.json();
			}
			return res.json().then(text => {throw new Error(text["description"])})
		}).then(function (data) {
			console.log(data)
			console.log("employee")
			emp = data["employee"]
			document.getElementById("emp-name").value = emp.emp_name
			document.getElementById("emp-salary").value = emp.emp_salary
			document.getElementById("emp-address").value = emp.emp_address
			document.getElementById("emp-designation").value = emp.emp_designation
			ele = document.getElementById("submit-btn")
			ele.addEventListener("click", function () {
				let y = emp.emp_id
				update_employee(y)
			})
		})
		.catch(function (res) { 
			document.getElementById("alert").style.display = "block"
			document.getElementById("error-msg").innerHTML= res
			console.log(res) })
}

function delete_employee(x) {
	console.log("delete called with emp id ", x)
	var token = localStorage.getItem('token')
	let user_id = localStorage.getItem('user_id')
	fetch("http://0.0.0.0/employee/" + x.toString(),
		{
			headers: {
				'Accept': 'application/json',
				'Content-Type': 'application/json',
				'role': 'admin',
				'Authorization': 'bearer ' + token,
				"user" : user_id
			},
			method: "DELETE",
			mode: "cors"
		})
		.then(function (res) {
			console.log("data arrived")
			if(res.ok) {
				return res.json();
			}
			return res.json().then(text => {throw new Error(text["description"])})
		}).then(function (data) {
			console.log(data)
			window.location.href = "home.html";
		})
		.catch(function (res) { 
			document.getElementById("alert").style.display = "block"
			document.getElementById("error-msg").innerHTML= res
			console.log(res) })
}

function login() {
	username = document.getElementById("username").value
	password = document.getElementById("password").value
	data = {
		username: username,
		password: password
	}
	fetch("http://0.0.0.0/login",
		{
			headers: {
				'Accept': 'application/json',
				'Content-Type': 'application/json',
				'role': 'admin'
			},
			method: "POST",
			mode: "cors",
			body: JSON.stringify(data)
		})
		.then(function (res) {
			console.log("data arrived")
			if(res.ok) {
				return res.json();
			}
			return res.json().then(text => {throw new Error(text["description"])})
		}).then(function (data) {
			console.log(data)
			token = data["token"];
			localStorage.setItem('token', token)
			user_id = data["user_id"]
			localStorage.setItem('user_id', user_id)
			console.log(user_id)
			console.log(token)
			window.location.href = "home.html";
		})
		.catch(function (res) {
			console.log("error in login")
			document.getElementById("alert").style.display = "block"
			document.getElementById("error-msg").innerHTML= res
			console.log(res)
		})
}

function register() {

	username = document.getElementById("username").value
	password = document.getElementById("password").value
	data = {
		username: username,
		password: password
	}
	fetch("http://0.0.0.0/register",
		{
			headers: {
				'Accept': 'application/json',
				'Content-Type': 'application/json',
				'token': "9a39b55fc9454b50bbf80ce66c629fc7",
				'role': 'admin'
			},
			method: "POST",
			mode: "cors",
			body: JSON.stringify(data)
		})
		.then(function (res) {
			console.log("data arrived")
			if(res.ok) {
				return res.json();
			}
			return res.json().then(text => {throw new Error(text["description"])})
		}).then(function (data) {
			console.log(data)
			window.location.href = "login.html";
		})
		.catch(function (res) {
			console.log("registration error")
			document.getElementById("alert").style.display = "block"
			document.getElementById("error-msg").innerHTML= res
			console.log(res)
		})
}


function add_employee() {
	var token = localStorage.getItem('token')
	let user_id = localStorage.getItem('user_id')
	emp_name = document.getElementById("emp-name").value
	emp_salary = document.getElementById("emp-salary").value
	emp_address = document.getElementById("emp-address").value
	emp_designation = document.getElementById("emp-designation").value
	var data = {
		name: emp_name,
		salary: emp_salary,
		address: emp_address,
		designation: emp_designation
	}
	fetch("http://0.0.0.0/employees",
		{
			headers: {
				'Accept': 'application/json',
				'Content-Type': 'application/json',
				'role': 'admin',
				'Authorization': 'bearer ' + token,
				"user" : user_id
			},
			method: "POST",
			mode: "cors",
			body: JSON.stringify(data)
		})
		.then(function (res) {
			console.log("data arrived")
			if(res.ok) {
				return res.json();
			}
			return res.json().then(text => {throw new Error(text["description"])})
		}).then(function (data) {
			console.log(data)
			window.location.href = "home.html";
		})
		.catch(function (res) { 
			document.getElementById("alert").style.display = "block"
			document.getElementById("error-msg").innerHTML= res
			console.log(res) })
}

function logout() {
	var token = localStorage.getItem('token')
	let user_id = localStorage.getItem('user_id')
	fetch("http://0.0.0.0/logout",
		{
			headers: {
				'Accept': 'application/json',
				'Content-Type': 'application/json',
				'role': 'admin',
				'Authorization': 'bearer ' + token,
				"user" : user_id
			},
			method: "GET",
			mode: "cors"
		})
		.then(function (res) {
			console.log("data arrived")
			if(res.ok) {
				return res.json();
			}
			return res.json().then(text => {throw new Error(text["description"])})
		}).then(function (data) {
			console.log(data)
			window.location.href = "index.html";
		})
		.catch(function (res) { 
			document.getElementById("alert").style.display = "block"
			document.getElementById("error-msg").innerHTML= res
			console.log(res) })
}

function update_employee(x) {
	var token = localStorage.getItem('token')
	let user_id = localStorage.getItem('user_id')
	emp_name = document.getElementById("emp-name").value
	emp_salary = document.getElementById("emp-salary").value
	emp_address = document.getElementById("emp-address").value
	emp_designation = document.getElementById("emp-designation").value
	var data = {
		name: emp_name,
		salary: emp_salary,
		address: emp_address,
		designation: emp_designation
	}
	fetch("http://0.0.0.0/employee/" + x.toString(),
		{
			headers: {
				'Accept': 'application/json',
				'Content-Type': 'application/json',
				'role': 'admin',
				'Authorization': 'bearer ' + token,
				"user" : user_id
			},
			method: "PuT",
			mode: "cors",
			body: JSON.stringify(data)
		})
		.then(function (res) {
			console.log("data arrived")
			if(res.ok) {
				return res.json();
			}
			return res.json().then(text => {throw new Error(text["description"])})
		}).then(function (data) {
			console.log(data)
			window.location.href = "home.html";
		})
		.catch(function (res) { 
			document.getElementById("alert").style.display = "block"
			document.getElementById("error-msg").innerHTML= res
			console.log(res) })
}

function login_load() {
	document.getElementById("alert").style.display = "none"
}