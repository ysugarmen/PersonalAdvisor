document.getElementById("loginForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    try {
        const response = await fetch("http://127.0.0.1:8000/users/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ email, password }),
        });

        if (!response.ok) {
            throw new Error("Failed to login");
        }

        const data = await response.json();
        alert("Login successful");
        console.log(data);
    }
    catch (error) {
        alert(error.message)
    }
    });
