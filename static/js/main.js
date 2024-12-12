// Get Elements from DOM
const themeSwitcher = document.getElementById('dark-mode');
const loader = document.getElementById('loader');

// Switch theme
const getTheme = () => localStorage.getItem('theme');
const setTheme = theme => localStorage.setItem('theme', theme);

function switchTheme() {
    let theme = getTheme();

    if (theme !== 'dark' && theme !== 'light') theme = window.matchMedia(
        '(prefers-color-scheme: dark)'
    ).matches ? 'dark' : 'light';

    themeSwitcher.checked = (theme == 'dark');
    document.documentElement.setAttribute('data-bs-theme', theme);
}

themeSwitcher.addEventListener('change', () => {
    const darkModeEnabled = themeSwitcher.checked;
    const theme = darkModeEnabled ? 'dark' : 'light';
    setTheme(theme);
    switchTheme();
});

switchTheme();


// Hide Page Loader
window.onload = function () {
    loader.classList.remove('show');
}

document.getElementById('notificationBell').addEventListener('click', function () {
    const dropdown = document.getElementById('notificationsDropdown');
    dropdown.classList.toggle('show');
});

document.addEventListener('click', function (event) {
    const dropdown = document.getElementById('notificationsDropdown');
    if (!event.target.closest('#notificationBell') && !event.target.closest('#notificationsDropdown')) {
        dropdown.classList.remove('show');
    }
});