let authMode = 'login';

function switchAuth(mode) {
    authMode = mode;
    const title = document.getElementById('auth-title');
    const submitBtn = document.getElementById('auth-submit');
    const usernameGroup = document.getElementById('username-group');
    const expGroup = document.getElementById('experience-group');
    const loginTab = document.getElementById('tab-login');
    const regTab = document.getElementById('tab-register');
    const message = document.getElementById('auth-message');
    
    message.textContent = '';

    if (mode === 'login') {
        title.textContent = 'Welcome Back';
        submitBtn.textContent = 'Login';
        usernameGroup.classList.add('hidden');
        expGroup.classList.add('hidden');
        loginTab.classList.add('active');
        regTab.classList.remove('active');
    } else {
        title.textContent = 'Create Account';
        submitBtn.textContent = 'Register';
        usernameGroup.classList.remove('hidden');
        expGroup.classList.remove('hidden');
        loginTab.classList.remove('active');
        regTab.classList.add('active');
    }
}

document.getElementById('auth-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const message = document.getElementById('auth-message');
    
    message.style.color = 'var(--text-muted)';
    message.textContent = 'Processing...';

    try {
        let response;
        if (authMode === 'login') {
            response = await fetch('http://127.0.0.1:5000/api/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });
        } else {
            const username = document.getElementById('username').value;
            const experience_level = document.getElementById('experience').value;
            response = await fetch('http://127.0.0.1:5000/api/auth/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, email, password, experience_level })
            });
        }

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.message || 'Authentication failed');
        }

        api.setToken(data.access_token);
        api.setUser(data.user);
        
        // If registering, go to skills directly
        if (authMode === 'register') {
            window.location.href = 'skills.html';
        } else {
            window.location.href = 'dashboard.html';
        }
    } catch (err) {
        message.style.color = 'var(--error)';
        message.textContent = err.message;
    }
});
