document.addEventListener('DOMContentLoaded', function() {
    // Handle login form submission
    const loginForm = document.getElementById('userForm');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            // Client-side validation
            const name = loginForm.elements['name'].value.trim();
            const age = loginForm.elements['age'].value.trim();
            const gender = loginForm.elements['gender'].value.trim();
            
            if (!name || !age || !gender) {
                e.preventDefault();
                alert('Please fill in all required fields');
                return false;
            }
            return true;
        });
    }

    // Handle symptoms selection (if on symptoms page)
    const symptomsForm = document.getElementById('symptomsForm');
    if (symptomsForm) {
        symptomsForm.addEventListener('submit', function(e) {
            const selected = document.querySelectorAll('#symptoms-select option:checked');
            if (selected.length === 0) {
                e.preventDefault();
                alert('Please select at least one symptom');
                return false;
            }
            return true;
        });
    }
});