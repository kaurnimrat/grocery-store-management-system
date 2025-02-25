document.addEventListener("DOMContentLoaded", function() {
    const loginForm = document.querySelector("#login")

    loginForm.addEventListener("submit", function(event) {
        event.preventDefault()  
        data = {
            login_username: document.getElementById('#login_email').value,
            login_password: document.getElementById('#login_password').value,
        }

        fetch("http://127.0.0.1:8000/api/login", {
            method: 'POST',
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(data => {
            if(data.sucesss){
                alert('login successful!')
                window.location.replace('/dashboard')
            } else {
                alert(data.message)
            }
        })
        .catch(error => {
            console.log(error)
        })
    })
})