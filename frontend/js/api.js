const API_BASE_URL = 'http://127.0.0.1:5000/api';

const api = {
    async request(endpoint, options = {}) {
        const token = localStorage.getItem('token');
        const headers = {
            'Content-Type': 'application/json',
            ...options.headers,
        };

        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            ...options,
            headers,
        });

        const data = await response.json();

        if (!response.ok) {
            if (response.status === 401 && !endpoint.includes('/auth')) {
                // Token expired or invalid, logout
                localStorage.removeItem('token');
                localStorage.removeItem('user');
                window.location.href = 'auth.html';
            }
            throw new Error(data.message || 'Something went wrong');
        }

        return data;
    },

    get(endpoint) {
        return this.request(endpoint, { method: 'GET' });
    },

    post(endpoint, body) {
        return this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(body),
        });
    },

    delete(endpoint) {
        return this.request(endpoint, { method: 'DELETE' });
    },

    // Auth helpers
    setToken(token) {
        localStorage.setItem('token', token);
    },

    setUser(user) {
        localStorage.setItem('user', JSON.stringify(user));
    },

    getUser() {
        const user = localStorage.getItem('user');
        return user ? JSON.parse(user) : null;
    },

    logout() {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        window.location.href = 'index.html';
    },

    // ── Helper Methods ──────────────────────────────────────────────────
    async fetch(endpoint, method = 'GET', body = null) {
        return this.request(endpoint, {
            method,
            body: body ? JSON.stringify(body) : null
        });
    },

    async getSkills() { return this.fetch('/skills'); },
    async saveSkills(skillIds) { return this.fetch('/user/skills', 'POST', { skill_ids: skillIds }); },
    async getUserSkills() { return this.fetch('/user/skills'); },
    
    async matchDomains(skillIds) { return this.fetch('/domains/match', 'POST', { skill_ids: skillIds }); },
    async getTrendingDomains() { return this.fetch('/domains/trending'); },

    async getRoadmap(domainId) { return this.fetch(`/roadmaps/${domainId}`); },
    
    async tryCourse(courseId) { return this.fetch('/progress/try', 'POST', { course_id: courseId }); },
    async completeCourse(courseId) { return this.fetch('/progress/complete', 'POST', { course_id: courseId }); },
    async getProgress() { return this.fetch('/progress/'); },
    
    async selectRoadmap(domainId, level) { return this.fetch('/progress/select-roadmap', 'POST', { domain_id: domainId, level }); },
    async getSelectedRoadmap() { return this.fetch('/progress/selected-roadmap'); },

    async getBookmarks() { return this.fetch('/bookmarks/'); },
    async addBookmark(courseId) { return this.fetch('/bookmarks/', 'POST', { course_id: course_id }); },
    async removeBookmark(courseId) { return this.fetch(`/bookmarks/${courseId}`, 'DELETE'); }
};


// Global auth check for protected pages
function checkAuth() {
    if (!localStorage.getItem('token')) {
        window.location.href = 'auth.html';
    }
}
