document.getElementById("registerForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const username = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    try {
        if (password.length < 8) {
            alert("Password must be at least 8 characters long.");
            return;
        }
        if (!email.includes("@")) {
            alert("Please enter a valid email address.");
            return;
        }
        const response = await fetch("/signup", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({username, email, password }),
        });

        if (!response.ok) {
            throw new Error("Failed to register");
            console.log(response);
            return;
        }

        const data = await response.json();
        alert("Registration successful");
        console.log(data);
        window.location.href = "/home";
    }
    catch (error) {
        alert(error.message)
    }
    });
