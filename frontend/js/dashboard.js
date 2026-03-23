async function loadDashboard() {
    try {
        const user = api.getUser();
        if (user) {
            // Stats & Skills
            const skills = await api.getUserSkills();
            document.getElementById('stat-skills').textContent = skills.length;
            renderSkills(skills);

            // Progress & Activity
            const progress = await api.getProgress();
            document.getElementById('stat-trials').textContent = progress.filter(p => p.status === 'tried').length;
            document.getElementById('stat-completed').textContent = progress.filter(p => p.status === 'completed').length;

            // Commitment
            const selection = await api.getSelectedRoadmap();
            renderActivePath(selection);

            // Bookmarks
            const bookmarks = await api.getBookmarks();
            document.getElementById('stat-bookmarks').textContent = bookmarks.length;
            renderBookmarks(bookmarks);
        }
    } catch (err) {
        console.error('Failed to load dashboard:', err);
    }
}

function renderActivePath(selection) {
    const container = document.getElementById('active-path-container');
    if (!selection) {
        container.innerHTML = `
            <div class="card" style="padding: 3rem; margin-bottom: 3rem; border: 2px dashed var(--accent); text-align: center; background: var(--secondary)">
                <p style="color: var(--text-muted); margin-bottom: 1.5rem; font-size: 1.1rem">You haven't committed to a career path yet.</p>
                <a href="domains.html" class="btn btn-primary">Discover Your Career Matches</a>
            </div>
        `;
        return;
    }

    container.innerHTML = `
        <div class="active-path-card fade-in" style="margin-bottom: 3rem; padding: 3rem; background: linear-gradient(135deg, var(--primary-dark), var(--primary)); border: none;">
            <div>
                <h4 style="text-transform: uppercase; font-size: 0.8rem; letter-spacing: 2px; opacity: 0.8; margin-bottom: 0.75rem">Current Career Path</h4>
                <h2 style="font-size: 2.5rem; margin-bottom: 0.5rem; color: white;">${selection.domain_name}</h2>
                <p style="font-size: 1.1rem; opacity: 0.9">Level: <strong>${selection.level.toUpperCase()}</strong> Specialization</p>
            </div>
            <div style="text-align: right">
                <a href="roadmap.html?id=${selection.domain_id}" class="btn" style="background: white; color: var(--primary-dark); font-weight: 700; padding: 1rem 2rem; border-radius: var(--radius-xl)">Continue Roadmap</a>
            </div>
        </div>
    `;
}

function renderSkills(skills) {
    const container = document.getElementById('dashboard-skills');
    container.innerHTML = skills.map(s => `
        <span class="skill-tag">
            ${s.icon} ${s.name}
        </span>
    `).join('');
}

function renderBookmarks(bookmarks) {
    const container = document.getElementById('dashboard-bookmarks');
    if (bookmarks.length === 0) {
        container.innerHTML = '<p style="color: var(--text-muted)">No activity yet. Explore roadmaps to start your journey!</p>';
        return;
    }

    container.innerHTML = bookmarks.map(b => `
        <div class="card" style="margin-bottom: 1.5rem; display: flex; justify-content: space-between; align-items: center; padding: 2rem; border: 1px solid var(--secondary);">
            <div>
                <span class="platform-badge" style="background: var(--secondary); color: var(--primary-dark); font-size: 0.75rem">${b.course.platform}</span>
                <h4 style="margin-top: 0.75rem; font-size: 1.1rem">${b.course.title}</h4>
            </div>
            <div style="display: flex; gap: 1.5rem; align-items: center">
                <a href="${b.course.url}" target="_blank" class="btn btn-outline" style="font-size: 0.85rem; padding: 0.5rem 1rem">Go to Course</a>
                <button class="btn" style="color: var(--error); background: none; font-size: 0.85rem; padding: 0" onclick="removeBookmark(${b.course.id})">Remove</button>
            </div>
        </div>
    `).join('');
}

async function removeBookmark(courseId) {
    if (confirm('Remove this bookmark?')) {
        try {
            await api.removeBookmark(courseId);
            loadDashboard();
        } catch (err) {
            console.error('Failed to remove bookmark:', err);
        }
    }
}

loadDashboard();

