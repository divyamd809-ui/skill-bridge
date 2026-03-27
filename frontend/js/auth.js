let authMode = 'login';

function switchAuth(mode) {
    authMode = mode;
    const title = document.getElementById('auth-title');
    const submitBtn = document.getElementById('auth-submit');
    const loginTab = document.getElementById('tab-login');
    const regTab = document.getElementById('tab-register');
    const message = document.getElementById('auth-message');
    const btnNext = document.getElementById('btn-next');
    const step1 = document.getElementById('step-1');
    const step2 = document.getElementById('step-2');
    
    message.textContent = '';
    
    // Reset to step 1
    step1.classList.remove('hidden');
    step2.classList.add('hidden');

    if (mode === 'login') {
        title.textContent = 'Welcome Back';
        submitBtn.classList.remove('hidden');
        btnNext.classList.add('hidden');
        loginTab.classList.add('active');
        regTab.classList.remove('active');
    } else {
        title.textContent = 'Create Account (1/2)';
        submitBtn.classList.add('hidden');
        btnNext.classList.remove('hidden');
        loginTab.classList.remove('active');
        regTab.classList.add('active');
    }
}

document.getElementById('btn-next')?.addEventListener('click', () => {
    // Basic validation before next
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const message = document.getElementById('auth-message');
    
    if (!username || !password) {
        message.style.color = 'var(--error)';
        message.textContent = 'Please fill all fields first.';
        return;
    }
    
    message.textContent = '';
    document.getElementById('step-1').classList.add('hidden');
    document.getElementById('step-2').classList.remove('hidden');
    document.getElementById('auth-title').textContent = 'Create Account (2/2)';
});

document.getElementById('btn-prev')?.addEventListener('click', () => {
    document.getElementById('step-1').classList.remove('hidden');
    document.getElementById('step-2').classList.add('hidden');
    document.getElementById('auth-title').textContent = 'Create Account (1/2)';
});

document.getElementById('auth-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const message = document.getElementById('auth-message');
    
    message.style.color = 'var(--text-muted)';
    message.textContent = 'Processing...';

    try {
        let response;
        if (authMode === 'login') {
            response = await fetch(`${API_BASE_URL}/auth/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email: username, password: password }) // Backend accepts username via email field
            });
        } else {
            const semester = parseInt(document.getElementById('semester').value);
            let branch = document.getElementById('branch').value;
            if (branch === 'OTHER') {
                const otherBranchInput = document.getElementById('other-branch');
                if (otherBranchInput && otherBranchInput.value.trim() !== '') {
                    branch = otherBranchInput.value.trim();
                }
            }
            
            // Get selected interests
            const interests = [];
            document.querySelectorAll('input[name="interest"]:checked').forEach(cb => {
                interests.push(cb.value);
            });

            response = await fetch(`${API_BASE_URL}/auth/register`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    username, 
                    email: `${username}@skillbridge.local`, 
                    password, 
                    semester,
                    branch,
                    interests
                })
            });
        }

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.message || 'Authentication failed');
        }

        api.setToken(data.access_token);
        api.setUser(data.user);
        
        // If registering, go to onboarding directly
        if (authMode === 'register') {
            window.location.href = 'onboarding.html';
        } else {
            window.location.href = 'dashboard.html';
        }
    } catch (err) {
        message.style.color = 'var(--error)';
        message.textContent = err.message;
    }
});
