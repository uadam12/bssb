const themeSwitcher = document.getElementById('dark-mode');
const getTheme = () => localStorage.getItem('theme');
const setTheme = theme => localStorage.setItem('theme', theme);

function switchTheme() {
    let theme = getTheme();

    if(theme !== 'dark' && theme !== 'light') theme = window.matchMedia(
        '(prefers-color-scheme: dark)'
    ).matches ? 'dark' : 'light';

    themeSwitcher.checked = (theme == 'dark');
    document.documentElement.setAttribute('data-bs-theme', theme);
}

themeSwitcher.addEventListener('change', () => {
    const darkModeEnabled = themeSwitcher.checked;
    const theme = darkModeEnabled? 'dark': 'light';
    setTheme(theme);
    switchTheme();
});

switchTheme();