
const filterInput = document.getElementById('filter_communities');
const resultDiv = document.getElementById('genres');

filterInput.addEventListener('input', function() {
    const query = filterInput.value.trim();

    // Перевірка на порожній запит
    if (query === '') {
        resultsDiv.innerHTML = ''; // Очищуємо результати, якщо запит порожній
        return;
};
fetch(`/social/communities/filter?query=${encodeURIComponent(query)}`)
    .then(response => response.json())
    .then(data => {
        resultDiv.innerHTML = ''; // Очищуємо попередні результати

        data.results.forEach(item => {
            const itemElement = document.createElement('p');
            itemElement.textContent = item.name;
            resultDiv.appendChild(itemElement);
        });
    })
    .catch(error => console.error('Помилка при пошуку:', error));
});