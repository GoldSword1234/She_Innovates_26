//api.jgao.cc/GetUsers
// /GetLessons
// /GetOverAllStatus

function goToHome() {
  window.location.href = "home.html"; // Replace with your target URL
}

function goToModules() {
  window.location.href = "modules.html"; // Replace with your target URL
}

function goToFinance() {
  window.location.href = "finance_module.html"; // Replace with your target URL
}

function goToSavingInvesting() {
  window.location.href = "saving_investing_101.html"; // Replace with your target URL
}

function goToBadges() {
  window.location.href = "badges.html"; // Replace with your target URL
}








async function updateWelcomeMessage() {
  try {
    const response = await fetch('https://api.jgao.cc/GetUser', {
      method: 'GET',
      credentials: 'include'   // REQUIRED
    });

    if (!response.ok) throw new Error('Network response was not ok');

    const data = await response.json();

    if (!Array.isArray(data) || data.length === 0)
      throw new Error('No user data found');

    const firstName = data[0].firstname || 'User';

    document.getElementById('welcome-message').textContent =
      `Welcome back, ${firstName}!`;

  } catch (error) {
    console.error('Error fetching user data:', error);
  }
}



// Run after page loads
window.addEventListener('DOMContentLoaded', updateWelcomeMessage);
