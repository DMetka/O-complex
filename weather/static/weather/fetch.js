const supportInput = () => {
    const input = document.getElementById('city-input');
    const suggestions = document.getElementById('suggestions');

    suggestions.style.display = 'none';

    input.addEventListener('input', async () => {
        const query = input.value.trim();
        if (query.length < 2) {
            suggestions.innerHTML = '';
            suggestions.style.display = 'none';
            return;
        }

        const url = new URL('api/v1/weather/helper', window.location.origin);
        url.searchParams.set('key_words', query);

        try {
            const response = await fetch(url);
            if (!response.ok) new Error('Network error');

            const data = await response.json();
            suggestions.innerHTML = '';

            data.results.forEach(city => {
                const name = city.name + (city.country ? ', ' + city.country : '');
                const h4 = document.createElement('h4');
                h4.textContent = name;
                h4.dataset.name = city.name;
                suggestions.appendChild(h4);
            });

            if (suggestions.children.length > 0) {
                suggestions.style.display = 'flex';
            } else {
                suggestions.style.display = 'none';
            }
        } catch (err) {
            console.error(err);
            suggestions.innerHTML = '';
        }
    });

    suggestions.addEventListener('click', e => {
        if (e.target && e.target.dataset.name) {
            input.value = e.target.dataset.name;
            suggestions.innerHTML = '';
            suggestions.style.display = 'none';
        }
    });

    document.addEventListener('click', e => {
        if (!e.target.closest('#city-input') && !e.target.closest('#suggestions')) {
            suggestions.innerHTML = '';
            suggestions.style.display = 'none';
        }
    });
}

document.addEventListener('DOMContentLoaded', () => {
  supportInput()
})