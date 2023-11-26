//
// Dark or light mode
//

const LTCSS   = document.querySelectorAll('link[class=css-lt]');
const DKCSS   = document.querySelectorAll('link[class=css-dk]');
const MODEBTN = document.querySelectorAll('.switcher-btn');
const MODEICO = document.querySelectorAll('.switcher-icon');

function getSystemScheme() {
    return matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
}

function getSavedScheme() {
    return localStorage.getItem('color-scheme');
}

function getCurrentScheme() {
    return getSavedScheme() ? getSavedScheme() : getSystemScheme();
}

function saveScheme(scheme) {
    localStorage.setItem('color-scheme', scheme)
}

function setScheme(scheme) {
    [...LTCSS].forEach((link) => {
        link.media = (scheme === 'light') ? 'all' : 'not all';
    });

    [...DKCSS].forEach((link) => {
        link.media = (scheme === 'dark') ? 'all' : 'not all';
    });
}

function setupSwitcher(scheme) {
    [...MODEICO].forEach((icon) => {
        let attribute = icon.getAttribute('data-theme-mode');

        if (attribute === scheme) {
            icon.classList.toggle('d-none')
        }
    });
}

let scheme = getCurrentScheme();

[...MODEBTN].forEach((btn) => {
    btn.addEventListener('click', (event) => {

        [...MODEICO].forEach((icon) => {
            if (icon.classList.contains('d-none')) {
                scheme = icon.getAttribute('data-theme-mode');
            }
            icon.classList.toggle('d-none')
        });

        if (scheme) {
            saveScheme(scheme);
            setScheme(scheme);
        }
    });
});

setupSwitcher(scheme);