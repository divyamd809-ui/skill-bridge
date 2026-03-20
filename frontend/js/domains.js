async function loadDomainMatches() {
    try {
        // Load matches
        const matches = await api.matchDomains();
        renderDomains(matches);

        // Load trending
        const trending = await api.getTrendingDomains();
        renderTrending(trending);
    } catch (err) {
        console.error('Failed to load domains data:', err);
    }
}

function renderTrending(trending) {
    const container = document.getElementById('trending-strip');
    if (!container) return;
    
    container.innerHTML = trending.map(d => `
        <div class="trending-pill" onclick="window.location.href='roadmap.html?id=${d.id}'">
            <span>${d.icon}</span> ${d.name}
            <span style="font-size: 0.7rem; opacity: 0.6; margin-left: 4px;">📈 ${d.trending_score}</span>
        </div>
    `).join('');
}

function renderDomains(matches) {
    const container = document.getElementById('domains-grid');
    container.innerHTML = '';
    
    if (matches.length === 0) {
        container.innerHTML = '<p>No matches found. Try selecting more skills.</p>';
        return;
    }

    matches.forEach((match, index) => {
        const d = match.domain;
        const card = document.createElement('div');
        card.className = 'domain-card fade-in';
        card.style.position = 'relative'; // For absolute badge placement
        
        const isTopPick = index === 0 && match.match_score > 40;
        const topPickBadge = isTopPick ? `
            <div class="top-pick-badge">
                <span>⭐</span> Top Pick
            </div>
        ` : '';

        card.innerHTML = `
            ${topPickBadge}
            <div class="match-badge">${match.match_score}% Match</div>
            <div class="score-circle">${d.icon}</div>
            <h3>${d.name}</h3>
            <p style="color: var(--text-muted); font-size: 0.8rem; line-height: 1.5; margin-bottom: 1.5rem">${d.description}</p>
            
            <div style="margin-bottom: 1.5rem">
                <h4 style="font-size: 0.8rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.5rem">Career Roles</h4>
                <div class="career-list">
                    ${d.career_opportunities.slice(0, 3).map(job => `<span class="tag">${job}</span>`).join('')}
                </div>
            </div>

            <div style="margin-top: auto; padding-top: 1rem">
                <a href="roadmap.html?id=${d.id}" class="btn btn-primary" style="width: 100%">Explore Roadmap</a>
            </div>
        `;
        container.appendChild(card);
    });
}

loadDomainMatches();

