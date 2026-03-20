let selectedSkills = new Set();
let allSkills = [];

async function loadSkills() {
    try {
        allSkills = await api.get('/skills');
        renderSkills();
    } catch (err) {
        console.error('Failed to load skills:', err);
    }
}

function renderSkills() {
    const container = document.getElementById('skills-container');
    container.innerHTML = '';
    
    allSkills.forEach(skill => {
        const chip = document.createElement('div');
        chip.className = 'skill-chip';
        chip.innerHTML = `<span>${skill.icon}</span><span>${skill.name}</span>`;
        chip.onclick = () => toggleSkill(skill.id, chip);
        container.appendChild(chip);
    });
}

function toggleSkill(skillId, element) {
    if (selectedSkills.has(skillId)) {
        selectedSkills.delete(skillId);
        element.classList.remove('selected');
    } else {
        selectedSkills.add(skillId);
        element.classList.add('selected');
    }
    
    updateCounter();
}

function updateCounter() {
    const count = selectedSkills.size;
    const counter = document.getElementById('selection-count');
    const analyzeBtn = document.getElementById('analyze-btn');
    
    counter.textContent = `${count} skill${count !== 1 ? 's' : ''} selected`;
    analyzeBtn.disabled = count < 3;
}

document.getElementById('analyze-btn').addEventListener('click', async () => {
    const experience_level = document.getElementById('experience').value;
    const skill_ids = Array.from(selectedSkills);
    
    try {
        // Save user skills first
        await fetch('http://127.0.0.1:5000/api/user/skills', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: JSON.stringify({ skill_ids, experience_level })
        });
        
        // Redirect to domains
        window.location.href = 'domains.html';
    } catch (err) {
        alert('Failed to save profile. Please try again.');
    }
});

loadSkills();
