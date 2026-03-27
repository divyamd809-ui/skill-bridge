document.addEventListener('DOMContentLoaded', () => {
    const user = api.getUser();
    if (!user) {
        window.location.href = 'auth.html';
        return;
    }

    const container = document.getElementById('questions-container');
    
    // Generate simple questions based on user's profile
    const questions = generateQuestions(user);
    
    if (questions.length === 0) {
        // If no questions, just skip to dashboard
        window.location.href = 'dashboard.html';
        return;
    }

    questions.forEach((q, index) => {
        const qCard = document.createElement('div');
        qCard.className = 'question-card';
        
        const qTitle = document.createElement('div');
        qTitle.className = 'question-title';
        qTitle.textContent = `${index + 1}. ${q.text}`;
        
        const optionsGroup = document.createElement('div');
        optionsGroup.className = 'options-group';
        
        q.options.forEach((opt, optIdx) => {
            const label = document.createElement('label');
            label.className = 'option-label';
            
            const radio = document.createElement('input');
            radio.type = 'radio';
            radio.name = `question_${index}`;
            radio.value = opt;
            radio.required = true;
            
            label.appendChild(radio);
            label.appendChild(document.createTextNode(opt));
            optionsGroup.appendChild(label);
        });
        
        qCard.appendChild(qTitle);
        qCard.appendChild(optionsGroup);
        container.appendChild(qCard);
    });

    document.getElementById('onboarding-form').addEventListener('submit', (e) => {
        e.preventDefault();
        // In a real app we might save these answers. For now we just ask and proceed.
        // The prompt says "ask them basic questions ... no need to add these feature in the login pagfe"
        // After asking, we send them to dashboard.
        window.location.href = 'dashboard.html';
    });
});

function generateQuestions(user) {
    return [
        {
            text: 'Logic: If all BLOOPS are Razzies and all Razzies are Lazzies, are all BLOOPS definitely Lazzies?',
            options: ['Yes', 'No', 'Cannot be determined', 'None of the above']
        },
        {
            text: 'Aptitude: A train 120 meters long is running with a speed of 60 km/hr. In what time will it pass a boy who is running at 6 km/hr in the direction opposite to that in which the train is going?',
            options: ['6.54 seconds', '4.44 seconds', '6.82 seconds', '7.32 seconds']
        },
        {
            text: 'Computer Science: What is the average time complexity of a Binary Search algorithm?',
            options: ['O(1)', 'O(log n)', 'O(n)', 'O(n^2)']
        },
        {
            text: 'Material Science/Physics: Which of the following materials is mathematically the best conductor of electricity at room temperature?',
            options: ['Silver', 'Copper', 'Gold', 'Aluminum']
        },
        {
            text: 'Software Engineering: What does the acronym "API" stand for?',
            options: ['Applied Programming Interface', 'Application Programming Interface', 'Automated Program Integration', 'Advanced Processing Interface']
        },
        {
            text: 'Systems Engineering: If a cloud provider guarantees "99.9% uptime" per year, approximately how much downtime is mutually permitted annually?',
            options: ['8.7 hours', '1 day', '8.7 days', '1 hour']
        },
        {
            text: 'Physics/Mechanics: Which fundamental force strictly opposes the relative sliding motion between two solid surfaces in contact?',
            options: ['Gravity', 'Friction', 'Inertia', 'Tension']
        },
        {
            text: 'Aptitude: If 5 machines take 5 minutes to make 5 widgets, how long would it take 100 machines to make 100 widgets?',
            options: ['100 minutes', '5 minutes', '1 minute', '500 minutes']
        },
        {
            text: 'Logic / Mathematics: Which number should logically come next in the sequence: 2, 6, 12, 20, 30, ... ?',
            options: ['40', '42', '44', '46']
        },
        {
            text: 'Project Management: In modern software and product engineering, what does the "Agile" methodology primarily emphasize?',
            options: ['Rigid, unyielding planning', 'Iterative and incremental development', 'Strict hierarchical team structure', 'Comprehensive upfront design']
        }
    ];
}
