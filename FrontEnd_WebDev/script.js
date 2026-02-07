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

function goToProfile() {
    window.location.href = "profile.html";
}






























const API_BASE = "https://api.jgao.cc";

document.addEventListener("DOMContentLoaded", () => {
  loadModules();
});

async function loadModules() {
  const root = document.getElementById("modulesRoot");
  const statusEl = document.getElementById("modulesStatus");

  root.innerHTML = "";
  statusEl.textContent = "Loading modules...";

  try {
    const res = await fetch(`${API_BASE}/GetModules`, {
      method: "GET",
      credentials: "include", // IMPORTANT if auth is cookie-based
      headers: {
        "Accept": "application/json",
      },
    });

    if (!res.ok) {
      // Useful debugging info:
      const bodyText = await res.text().catch(() => "");
      throw new Error(`GetModules failed: ${res.status} ${res.statusText} ${bodyText}`);
    }

    const modules = await res.json();

    if (!Array.isArray(modules) || modules.length === 0) {
      statusEl.textContent = "No modules returned.";
      return;
    }

    statusEl.textContent = "";
    renderModules(modules, root);

  } catch (err) {
    console.error(err);
    statusEl.textContent = `Error loading modules: ${err.message}`;
  }
}

function renderModules(modules, root) {
  // Group by parentmoduleid (optional, but matches your data structure)
  const groups = groupBy(modules, m => m.parentmoduleid ?? "unknown");

  // Sort groups by numeric parentmoduleid if possible
  const groupKeys = Object.keys(groups).sort((a, b) => Number(a) - Number(b));

  for (const key of groupKeys) {
    const group = groups[key];

    // If you don’t want group headers, remove this block.
    // const groupHeader = document.createElement("h2");
    // groupHeader.textContent = `Module Group ${key}`;
    // groupHeader.style.padding = "0 16px";
    // root.appendChild(groupHeader);

    for (const m of group) {
      root.appendChild(createModuleCard(m));
    }
  }
}

function createModuleCard(m) {
  const section = document.createElement("section");
  section.className = "content";

  const iconSection = document.createElement("div");
  iconSection.className = "icon-section";

  const p = document.createElement("p");
  const count = Number(m.lesson_count);
  p.textContent = `${Number.isFinite(count) ? count : 0} ${count === 1 ? "Lessons" : "Lessons"}`;

  const info = document.createElement("div");
  info.className = "corner-icon";
  info.title = m.description || "";

  info.innerHTML = `
    <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-info-circle" viewBox="0 0 16 16">
      <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16"/>
      <path d="m8.93 6.588-2.29.287-.082.38.45.083c.294.07.352.176.288.469l-.738 3.468c-.194.897.105 1.319.808 1.319.545 0 1.178-.252 1.465-.598l.088-.416c-.2.176-.492.246-.686.246-.275 0-.375-.193-.304-.533zM9 4.5a1 1 0 1 1-2 0 1 1 0 0 1 2 0"/>
    </svg>
  `;

  iconSection.appendChild(p);
  iconSection.appendChild(info);

  const title = document.createElement("h1");
  title.textContent = m.moduletype || "Untitled Module";
  const btn = document.createElement("button");
  btn.className = "btn";
  btn.type = "button";
  btn.setAttribute("aria-label", `Open module ${m.modulename || ""}`);
  btn.innerHTML = `
    <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-arrow-right-circle-fill" viewBox="0 0 16 16">
      <path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0M4.5 7.5a.5.5 0 0 0 0 1h5.793l-2.147 2.146a.5.5 0 0 0 .708.708l3-3a.5.5 0 0 0 0-.708l-3-3a.5.5 0 1 0-.708.708L10.293 7.5z"/>
    </svg>
  `;

  // Where the button navigates:
  // Update this to whatever your module details page is.
  btn.addEventListener("click", () => {
    // Example: module.html?parentmoduleid=1&name=Investing
    const url = new URL("module.html", window.location.href);
    url.searchParams.set("parentmoduleid", String(m.parentmoduleid ?? ""));
    url.searchParams.set("name", String(m.modulename ?? ""));
    window.location.href = url.toString();
  });

  section.appendChild(iconSection);
  section.appendChild(title);

  // If you want the description visible (not just tooltip), uncomment:
  // if (m.description) {
  //   const desc = document.createElement("p");
  //   desc.textContent = m.description;
  //   section.appendChild(desc);
  // }

  section.appendChild(btn);

  return section;
}

function groupBy(arr, keyFn) {
  return arr.reduce((acc, item) => {
    const k = String(keyFn(item));
    (acc[k] ||= []).push(item);
    return acc;
  }, {});
}

/*
  If you are using Authorization headers (NOT cookie auth), do something like:

  const token = localStorage.getItem("access_token");
  const res = await fetch(`${API_BASE}/GetModules`, {
    headers: {
      "Accept": "application/json",
      "Authorization": `Bearer ${token}`,
    }
  });

  And remove credentials: "include".
*/

async function loadFinanceLessons() {
    try {
        const response = await fetch(API_URL);
        const data = await response.json();

        const lessonContainer = document.getElementById("lessonContainer");

        // Assuming first user
        const lessons = data[0].lessons;

        lessonContainer.innerHTML = ""; // clear existing content

        lessons.forEach((lesson, index) => {
            if (lesson.moduletype === "Finance") {
                const lessonDiv = document.createElement("div");
                lessonDiv.classList.add("lesson");

                lessonDiv.innerHTML = `
                    <h2 style="text-align: center;">
                        Lesson ${index + 1}: ${lesson.modulename}
                        <div class="lesson-corner-icon">
                            <button class="btn" onclick="goToLesson(${lesson.lessonid})">
                                <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="#fff"
                                    class="bi bi-arrow-right-circle-fill" viewBox="0 0 16 16">
                                    <path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0M4.5 7.5a.5.5 0 0 0 0 1h5.793l-2.147
                                    2.146a.5.5 0 0 0 .708.708l3-3a.5.5 0 0 0 0-.708l-3-3a.5.5 0 1
                                    0-.708.708L10.293 7.5z"/>
                                </svg>
                            </button>
                        </div>
                    </h2>
                    <p style="text-align:center;">${lesson.lesson_description}</p>
                `;

                lessonContainer.appendChild(lessonDiv);
            }
        });
    } catch (error) {
        console.error("Error loading lessons:", error);
    }
}

function goToLesson(lessonId) {
    // example redirect
    window.location.href = `lesson.html?lessonId=${lessonId}`;
}

// Load lessons on page load
// loadFinanceLessons();


async function loadProfile() {
    try {
        const response = await fetch(API_URL);
        const data = await response.json();

        // Assuming first user in array
        const user = data[0];

        const profileCard = document.getElementById("profileCard");

        // Format DOB nicely
        const dob = new Date(user.dateofbirth).toLocaleDateString();

        profileCard.innerHTML = `
            <h2>${user.firstname} ${user.lastname}</h2>
            <p><strong>User ID:</strong> ${user.userid}</p>
            <p><strong>Auth User ID:</strong> ${user.auth_user_id}</p>
            <p><strong>Date of Birth:</strong> ${dob}</p>
        `;
    } catch (error) {
        console.error("Error loading profile:", error);
    }
}

// Load profile on page load
//loadProfile();
document.addEventListener("DOMContentLoaded", () => {
  if (document.getElementById("profileCard")) {
    loadProfile();
  }
});




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
