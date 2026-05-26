// Инициализация Telegram Web App API
const tg = window.Telegram.WebApp;
tg.ready();
tg.expand(); // Разворачиваем на максимум для эффекта нативности

// Локальный стейт приложения
const appState = {
    sphere: null,
    mood: ""
};

// Словарь для красивого перевода ключей сфер
const SPHERES_RU = {
    "career": "💼 Карьера / Финансы",
    "relations": "❤️ Отношения",
    "health": "🍏 Здоровье / Энергия",
    "balance": "🧘‍♂️ Внутренний баланс"
};

// Функция переключения экранов
function navigateTo(screenId) {
    document.querySelectorAll('.screen').forEach(screen => {
        screen.classList.remove('active');
    });
    setTimeout(() => {
        const targetScreen = document.getElementById(screenId);
        if (targetScreen) targetScreen.classList.add('active');
    }, 50);
}

// Экран 1 -> Экран 2
document.getElementById('btn-start').addEventListener('click', () => {
    navigateTo('screen-2');
});

// Экран 2 (Выбор сферы) -> Авто-переход на Экран 3
document.querySelectorAll('.sphere-card').forEach(card => {
    card.addEventListener('click', function() {
        document.querySelectorAll('.sphere-card').forEach(c => c.classList.remove('selected'));
        
        this.classList.add('selected');
        
        // Получаем технический ключ сферы (career, relations, etc.)
        const sphereKey = this.getAttribute('data-sphere');
        // Переводим в красивое название
        appState.sphere = SPHERES_RU[sphereKey] || "Внутренний баланс";
        
        setTimeout(() => {
            navigateTo('screen-3');
        }, 400);
    });
});

// Экран 3 (Ввод текста и валидация)
const moodTextarea = document.getElementById('mood-text');
const btnSubmit = document.getElementById('btn-submit');

moodTextarea.addEventListener('input', function() {
    appState.mood = this.value.trim();
    // Кнопка активна, если введено от 5 символов
    btnSubmit.disabled = appState.mood.length < 5;
});

// НАШ НАТИВНЫЙ МОСТИК: Отправка данных прямо в чат Telegram
btnSubmit.addEventListener('click', () => {
    navigateTo('screen-4'); // Включаем красивый лоадер ("Наставник настраивается...")

    // Собираем пакет данных для бота
    const payload = {
        sphere: appState.sphere,
        mood: appState.mood
    };

    // Отправляем данные в чат и закрываем мини-приложение
    setTimeout(() => {
        tg.sendData(JSON.stringify(payload));
        tg.close();
    }, 1000); // Небольшая задержка, чтобы пользователь успел прочувствовать экран лоадера
});

// Закрытие Mini App при клике на финальную кнопку (если экран 5 используется внутри)
document.getElementById('btn-close').addEventListener('click', () => {
    tg.close();
});