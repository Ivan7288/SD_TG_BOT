let tg = window.Telegram.WebApp;
tg.expand();

// Set theme based on Telegram's theme
document.documentElement.setAttribute('data-theme', tg.colorScheme);

// Listen for theme changes
tg.onEvent('themeChanged', () => {
    document.documentElement.setAttribute('data-theme', tg.colorScheme);
});

// Elements
const promptInput = document.getElementById('prompt');
const generateButton = document.getElementById('generate');
const loadingDiv = document.getElementById('loading');
const resultDiv = document.getElementById('result');
const generatedImage = document.getElementById('generated-image');
const downloadButton = document.getElementById('download');
const historyGrid = document.getElementById('history-grid');

// Generate image
generateButton.addEventListener('click', async () => {
    const prompt = promptInput.value.trim();
    if (!prompt) return;

    loadingDiv.classList.remove('hidden');
    resultDiv.classList.add('hidden');
    generateButton.disabled = true;

    try {
        const response = await fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ prompt }),
        });

        const data = await response.json();
        if (data.success) {
            generatedImage.src = data.image_url;
            resultDiv.classList.remove('hidden');
            loadHistory();
        } else {
            alert('Error generating image: ' + data.error);
        }
    } catch (error) {
        alert('Error: ' + error.message);
    } finally {
        loadingDiv.classList.add('hidden');
        generateButton.disabled = false;
    }
});

// Download image
downloadButton.addEventListener('click', () => {
    const link = document.createElement('a');
    link.href = generatedImage.src;
    link.download = 'generated-image.png';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
});

// Load history
async function loadHistory() {
    try {
        const response = await fetch('/history');
        const data = await response.json();
        
        historyGrid.innerHTML = '';
        data.images.forEach(image => {
            const div = document.createElement('div');
            div.className = 'history-item';
            div.innerHTML = `
                <img src="${image.url}" alt="${image.prompt}">
                <div class="history-item-prompt">${image.prompt}</div>
            `;
            historyGrid.appendChild(div);
        });
    } catch (error) {
        console.error('Error loading history:', error);
    }
}

// Initial load
loadHistory(); 