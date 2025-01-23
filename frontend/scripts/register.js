document.getElementById("registerForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const username = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    try {
        const response = await fetch("http://127.0.0.1:8000/users/signup", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({username, email, password }),
        });

        if (!response.ok) {
            throw new Error("Failed to register");
        }

        const data = await response.json();
        alert("Registration successful");
        console.log(data);
    }
    catch (error) {
        alert(error.message)
    }
    });
