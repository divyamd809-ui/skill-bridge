let currentCourses = [];
let userProgress = [];
let domainId = new URLSearchParams(window.location.search).get('id');

async function init() {
    if (!domainId) {
        window.location.href = 'domains.html';
        return;
    }

    try {
        await loadRoadmap();
        await loadDomains();
        await checkExistingCommitment();
        
        // Timer update interval
        setInterval(updateTimers, 1000);
    } catch (err) {
        console.error('Initialization failed:', err);
    }
}

async function loadRoadmap() {
    try {
        const user = api.getUser();
        const level = user ? user.experience_level : 'student';
        const data = await api.getRoadmap(domainId);
        
        document.getElementById('domain-name').textContent = `${data.domain.icon} ${data.domain.name} Roadmap`;
        document.getElementById('domain-desc').textContent = data.domain.description;
        
        currentCourses = data.courses;
        
        // Load user progress
        userProgress = await api.getProgress();
        
        renderCourses();
    } catch (err) {
        console.error('Failed to load roadmap:', err);
    }
}

async function loadDomains() {
    try {
        const domains = await api.get('/domains/');
        const switcher = document.getElementById('domain-switcher');
        switcher.innerHTML = domains.map(d => `
            <option value="${d.id}" ${d.id == domainId ? 'selected' : ''}>${d.icon} ${d.name}</option>
        `).join('');
        
        switcher.onchange = (e) => {
            window.location.href = `roadmap.html?id=${e.target.value}`;
        };
    } catch (err) {
        console.error('Failed to load domains:', err);
    }
}

async function checkExistingCommitment() {
    try {
        const selection = await api.getSelectedRoadmap();
        const commitBar = document.getElementById('commit-bar');
        
        if (selection && selection.domain_id == domainId) {
            commitBar.innerHTML = `
                <div style="color: var(--primary); font-weight: 700; display: flex; align-items: center; gap: 0.5rem">
                    <span>✅</span> You are currently pursuing this path
                </div>
                <a href="dashboard.html" class="btn btn-outline">View Progress</a>
            `;
        }
        commitBar.classList.remove('hidden');
    } catch (err) {
        console.error('Failed to check commitment:', err);
    }
}

function renderCourses() {
    const levels = [1, 2, 3];
    const filterFree = document.getElementById('filter-free').checked;
    const filterTrial = document.getElementById('filter-trial').checked;
    const filterDuration = document.getElementById('filter-duration').value;

    levels.forEach(level => {
        const container = document.getElementById(`courses-level-1`); // Fallback if IDs differ slightly
        const levelContainer = document.getElementById(`courses-level-${level}`);
        levelContainer.innerHTML = '';

        const levelCourses = currentCourses.filter(c => c.step_level === level);
        const filtered = levelCourses.filter(c => {
            if (filterFree && !c.is_free) return false;
            if (filterTrial && !c.has_trial) return false;
            if (filterDuration === 'short' && c.duration_weeks >= 8) return false;
            if (filterDuration === 'long' && c.duration_weeks < 8) return false;
            return true;
        });

        if (filtered.length === 0) {
            levelContainer.innerHTML = '<p style="color: var(--text-muted); font-size: 0.8rem; padding: 1rem 0">No courses in this level matching filters.</p>';
            return;
        }

        filtered.forEach((c, index) => {
            const progress = userProgress.find(p => p.course_id === c.id);
            const status = progress ? progress.status : 'not_started';
            
            const card = document.createElement('div');
            card.className = 'course-card fade-in';
            card.style.animationDelay = `${index * 0.1}s`;
            
            card.innerHTML = `
                <div style="flex: 1">
                    <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 0.5rem">
                        <span class="platform-badge">${c.platform}</span>
                        ${renderStatusBadge(status, progress)}
                    </div>
                    <h3 style="margin-bottom: 0.5rem">${c.title}</h3>
                    <p style="color: var(--text-muted); font-size: 0.85rem; margin-bottom: 1rem">${c.description}</p>
                    <div style="display: flex; gap: 1.5rem; font-size: 0.8rem; color: var(--text-muted); font-weight: 500">
                        <span>⏱️ ${c.duration_weeks} Weeks</span>
                        <span>⭐ ${c.rating}</span>
                        <span>${c.is_free ? '🎁 Free' : '💸 Paid'}</span>
                    </div>
                </div>
                <div style="text-align: right; display: flex; flex-direction: column; gap: 0.8rem; align-items: flex-end; min-width: 180px;">
                    ${renderActionButtons(c, status)}
                </div>
            `;
            levelContainer.appendChild(card);
        });
    });
}

function renderStatusBadge(status, progress) {
    if (status === 'completed') {
        return `<div class="status-indicator"><span class="status-dot completed"></span> Completed</div>`;
    }
    if (status === 'tried') {
        const timeLeft = calculateTimeLeft(progress.trial_started_at, 7); // 7 days trial
        return `
            <div class="status-indicator">
                <span class="status-dot tried"></span> 
                Trial Active 
                <span class="countdown-badge" data-start="${progress.trial_started_at}">${timeLeft}</span>
            </div>
        `;
    }
    return '';
}

function renderActionButtons(course, status) {
    let btns = '';
    
    if (status === 'not_started') {
        btns += `<button class="btn btn-primary" style="width: 100%; font-size: 0.85rem" onclick="handleTry(${course.id})">Try Now</button>`;
    } else if (status === 'tried') {
        btns += `<button class="btn btn-primary" style="width: 100%; font-size: 0.85rem" onclick="handleComplete(${course.id})">Mark Complete</button>`;
    } else if (status === 'completed') {
        btns += `<button class="btn btn-outline" style="width: 100%; font-size: 0.85rem" disabled>Course Finished</button>`;
    }

    btns += `<a href="${course.url}" target="_blank" class="btn btn-outline" style="width: 100%; font-size: 0.85rem; padding: 0.5rem">Go to Platform</a>`;
    if (course.coupon_code) {
        btns += `<p style="font-size: 0.65rem; color: var(--primary); font-weight: 800; border: 1px dashed var(--primary); padding: 2px 6px; border-radius: 4px;">COUPON: ${course.coupon_code}</p>`;
    }
    
    return btns;
}

async function handleTry(courseId) {
    try {
        await api.tryCourse(courseId);
        await loadRoadmap(); // Refresh to show timer
    } catch (err) {
        alert(err.message);
    }
}

async function handleComplete(courseId) {
    try {
        await api.completeCourse(courseId);
        await loadRoadmap();
    } catch (err) {
        alert(err.message);
    }
}

document.getElementById('commit-btn').onclick = async () => {
    try {
        const user = api.getUser();
        await api.selectRoadmap(domainId, user.experience_level);
        window.location.href = 'dashboard.html';
    } catch (err) {
        alert('Failed to commit: ' + err.message);
    }
};

function calculateTimeLeft(startDateStr, durationDays) {
    const start = new Date(startDateStr);
    const end = new Date(start.getTime() + durationDays * 24 * 60 * 60 * 1000);
    const now = new Date();
    
    const diff = end - now;
    if (diff <= 0) return "Expired";
    
    const d = Math.floor(diff / (1000 * 60 * 60 * 24));
    const h = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const m = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
    const s = Math.floor((diff % (1000 * 60)) / 1000);
    
    return `${d}d ${h}h ${m}m ${s}s`;
}

function updateTimers() {
    document.querySelectorAll('.countdown-badge').forEach(badge => {
        const start = badge.getAttribute('data-start');
        badge.textContent = calculateTimeLeft(start, 7);
    });
}

// Event listeners
document.getElementById('filter-free').onchange = renderCourses;
document.getElementById('filter-trial').onchange = renderCourses;
document.getElementById('filter-duration').onchange = renderCourses;

init();

