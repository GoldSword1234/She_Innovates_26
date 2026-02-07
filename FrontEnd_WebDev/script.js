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





let overallProgressLoaded = false;
let welcomeMessageLoaded = false;

async function updateOverAllProgress() {
  if (overallProgressLoaded) return;
  overallProgressLoaded = true;

  try {
    const response = await fetch('https://api.jgao.cc/GetOverAllStatus', {
      method: 'GET',
      credentials: 'include'
    });

    if (!response.ok) throw new Error('Network response was not ok');

    const data = await response.json();
    if (!Array.isArray(data) || data.length === 0)
      throw new Error('No status data found');

    const percentage = data[0].percentage ?? 0;
    document.getElementById('overall-percentage').textContent = `${percentage}%`;

  } catch (error) {
    console.error('Error fetching overall status:', error);
  }
}

async function updateWelcomeMessage() {
  if (welcomeMessageLoaded) return;
  welcomeMessageLoaded = true;

  try {
    const response = await fetch('https://api.jgao.cc/GetUser', {
      method: 'GET',
      credentials: 'include'
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

document.addEventListener('DOMContentLoaded', () => {
  updateOverAllProgress();
  updateWelcomeMessage();
});
