// Инициализация Telegram Web App API
const tg = window.Telegram.WebApp;
tg.ready();
tg.expand(); // Разворачиваем на максимум для эффекта нативности

// Локальный стейт приложения
const appState = {
    sphere: null,
    mood: "",
    backendUrl: "http://127.0.0.1:8000/api/so-na-stroyka" // Поменяйте на ваш прод URL в будущем
};

// Функция переключения экранов
function navigateTo(screenId) {
    document.querySelectorAll('.screen').forEach(screen => {
        screen.classList.remove('active');
    });
    setTimeout(() => {
        const targetScreen = document.getElementById(screenId);
        if (targetScreen) targetScreen.classList.add('active');
    }, 50); // Минимальный таймаут для чистого триггера CSS transition
}

// Экран 1 -> Экран 2
document.getElementById('btn-start').addEventListener('click', () => {
    navigateTo('screen-2');
});

// Экран 2 (Выбор сферы) -> Авто-переход на Экран 3
document.querySelectorAll('.sphere-card').forEach(card => {
    card.addEventListener('click', function() {
        // Убираем выделение у остальных
        document.querySelectorAll('.sphere-card').forEach(c => c.classList.remove('selected'));
        
        // Выделяем текущую
        this.classList.add('selected');
        appState.sphere = this.getAttribute('data-sphere');
        
        // Эстетичная пауза, чтобы пользователь увидел подсветку золотым градиентом
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
    // Активируем кнопку только если введено хотя бы 5 символов
    btnSubmit.disabled = appState.mood.length < 5;
});

// Отправка данных на бэкенд
btnSubmit.addEventListener('click', async () => {
    navigateTo('screen-4'); // Переходим на экран лоадера

    // Собираем данные. Безопасно передаем initData для валидации на бэкенде
    const payload = {
        init_data: tg.initData, 
        sphere: appState.sphere,
        mood: appState.mood
    };

    try {
        const response = await fetch(appState.backendUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) throw new Error('Ошибка сервера');

        const data = await response.json();
        
        // Наполняем блоки текстом из ответа ИИ
        document.querySelector('#block-grounding .block-content').innerText = data.grounding;
        document.querySelector('#block-focus .block-content').innerText = data.focus;
        document.querySelector('#block-visualization .block-content').innerText = data.visualization;

        // Переходим к финалу
        navigateTo('screen-5');

    } catch (error) {
        console.error(error);
        // В случае ошибки возвращаем на шаг ввода, в реальном проекте лучше показать алерт
        tg.showAlert("Не удалось связаться с Наставником. Попробуйте еще раз.");
        navigateTo('screen-3');
    }
});

// Закрытие Mini App при клике на финальную кнопку
document.getElementById('btn-close').addEventListener('click', () => {
    tg.close();
});