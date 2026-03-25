const form = document.getElementById('form');

form.addEventListener('submit', function(event){
    event.preventDefault();
    const user = document.getElementById('user').value;
    const password = document.getElementById('password').value;
    login(user, password)
    .then(response => {
        window.location.href = '/dashboard/';
    })
    .catch(async(response)=>{
        const data = await response.json();
        const message = data?.message ?? "Error desconocido "  + response.status;
        document.getElementById('error').textContent = message;
        // alert("Credenciales incorrrecta");
    })

})

const login = async (user, password) => {
    const response = await fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: JSON.stringify({ user, password })
    });
    
    if (response.ok) {
        
        return response.json();
        
    } else {
        throw response;
    }
}