// Show password 
function showpass(){
    var x = document.getElementById("password");
    if (x.type === "password"){
        x.type = "text";
    } else {
        x.type = "password";
    }
}


document.getElementById('loginForm').addEventListener('submit', function(e) {
    e.preventDefault(); // Prevent form submission
    
    // Get form values
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    
    // Reset error messages
    document.getElementById('emailError').style.display = 'none';
    document.getElementById('passwordError').style.display = 'none';
    
    let isValid = true;
    
    // Email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        document.getElementById('emailError').style.display = 'block';
        isValid = false;
    }
    
    // Password validation
    if (password.length < 6) {
        document.getElementById('passwordError').style.display = 'block';
        isValid = false;
    }
    
    // If valid, proceed with login
    if (isValid) {
        // Disable button and show loading state
        const signInBtn = document.getElementById('signInBtn');
        signInBtn.disabled = true;
        signInBtn.textContent = 'Signing In...';
        
        // Simulate API call (replace with actual authentication)
        setTimeout(() => {
            alert('Login successful!');
            // Here you would typically redirect or make an API call
            // window.location.href = '/dashboard';
            
            // Reset button
            signInBtn.disabled = false;
            signInBtn.textContent = 'Sign In';
        }, 1500);
    }
});

// Real-time validation as user types
document.getElementById('email').addEventListener('input', function() {
    const email = this.value;
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    
    if (email && !emailRegex.test(email)) {
        document.getElementById('emailError').style.display = 'block';
    } else {
        document.getElementById('emailError').style.display = 'none';
    }
});

document.getElementById('password').addEventListener('input', function() {
    const password = this.value;
    
    if (password && password.length < 6) {
        document.getElementById('passwordError').style.display = 'block';
    } else {
        document.getElementById('passwordError').style.display = 'none';
    }
});