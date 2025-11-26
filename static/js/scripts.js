const BASE_URL = "http://127.0.0.1:8000/";
let accessToken = null;

// Show messages
function showMessage(id, message, type) {
    const box = document.getElementById(id);
    box.innerHTML = `<div class="msg ${type}">${message}</div>`;
}
console.log("Not in function")

// REGISTER USER
async function registerUser() {
    const role = document.getElementById("role").value;
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const c_password = document.getElementById("c_password").value;
    const email = document.getElementById("email").value;

    console.log("Register function")

    const res = await fetch(`${BASE_URL}/register/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ role, username, password, c_password, email })
    });

    const data = await res.json();

    if (res.ok)
        showMessage("reg_msg", "User registered!", "success");
    else
        showMessage("reg_msg", data.detail || "Error", "error");
}

// LOGIN USER
async function loginUser() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const res = await fetch(`${BASE_URL}/login/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
    });

    const data = await res.json();
    console.log("Login Response:", data);  // Debug output

    if (!res.ok) {
        showMessage("login_msg", data.error || "Login failed", "error");
        return;
    }

    // Save JWT + role
    localStorage.setItem("access", data.access);
    localStorage.setItem("role", data.role);

    showMessage("login_msg", "Login successful!", "success");

    // Now redirect based on role (this works)
    if (data.role === "admin") {
        window.location.href = "/admin_dashboard/";
    } else {
        window.location.href = "/user_dashboard/";
    }
}


// FETCH NOTES
async function fetchNotes() {
    const res = await fetch(`${BASE_URL}/u/notes/`, {
        headers: {
            "Authorization": "Bearer " + accessToken
        }
    });

    const data = await res.json();

    if (!res.ok) {
        showMessage("api_msg", "Unauthorized", "error");
        return;
    }

    // Show notes
    const list = document.getElementById("notes_list");
    list.innerHTML = "";

    data.forEach(note => {
        const li = document.createElement("li");
        li.textContent = `${note.note}`;
        list.appendChild(li);
    });

    showMessage("api_msg", "Notes fetched successfully", "success");
}

// CREATE A NOTE (Protected)
async function createNote() {
    const title = document.getElementById("note_title").value;
    const description = document.getElementById("note_desc").value;

    const res = await fetch(`${BASE_URL}/notes/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + accessToken
        },
        body: JSON.stringify({ title, description })
    });

    const data = await res.json();

    if (!res.ok) {
        showMessage("api_msg", data.detail || "Error creating note", "error");
        return;
    }

    showMessage("api_msg", "Note created!", "success");
    fetchNotes();
}

// LOGOUT
function logoutUser() {
    accessToken = null;
    document.getElementById("dashboard").style.display = "none";
}
