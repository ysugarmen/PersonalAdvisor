document.getElementById("loginForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    try {

        const response = await fetch("/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ email, password }),
        });

        if (!response.ok) {
            throw new Error("Failed to login");
            console.log(response);
            return;
        }

        const data = await response.json();
        alert("Login successful");
        console.log(data);
        window.location.href = "/home";
    }
    catch (error) {
        alert(error.message)
    }
    });
