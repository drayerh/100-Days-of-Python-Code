let timeout;
let timer;
let countdown;
let timeLeft;
let originalDuration;
let isWriting = false;

function updateTimerDisplay(seconds) {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    document.getElementById('timer').textContent =
        `${String(minutes).padStart(2, '0')}:${String(remainingSeconds).padStart(2, '0')}`;
}

function startTimer(duration) {
    timeLeft = duration;
    updateTimerDisplay(timeLeft);

    countdown = setInterval(() => {
        timeLeft--;
        updateTimerDisplay(timeLeft);

        if (timeLeft <= 0) {
            clearInterval(countdown);
            document.getElementById('text-area').value = '';
            alert('Time\'s up! Your text has been deleted.');
        }
    }, 1000);
}

function setTimer(seconds) {
    clearTimeout(timeout);
    clearInterval(countdown);
    originalDuration = seconds;
    startTimer(seconds);

    const textArea = document.getElementById('text-area');
    textArea.value = '';
    textArea.focus();
}

document.getElementById('text-area').addEventListener('keyup', () => {
    clearTimeout(timeout);
    clearInterval(countdown);
    startTimer(originalDuration);
    timeout = setTimeout(() => {
        document.getElementById('text-area').value = '';
        alert('You stopped writing! Your text has been deleted.');
    }, originalDuration * 1000);
});

// Initialize with 5 seconds
setTimer(5);