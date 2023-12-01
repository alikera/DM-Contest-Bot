function startCountdown(duration, display) {
    var timer = duration, hours, minutes, seconds;

    var countdown = setInterval(function() {
      hours = parseInt(timer / 3600, 10);
      minutes = parseInt((timer % 3600) / 60, 10);
      seconds = parseInt((timer % 3600) % 60, 10);

      hours = hours < 10 ? "0" + hours : hours;
      minutes = minutes < 10 ? "0" + minutes : minutes;
      seconds = seconds < 10 ? "0" + seconds : seconds;

      display.textContent = hours + ":" + minutes + ":" + seconds;

      if (--timer < 0) {
        clearInterval(countdown);
        display.textContent = "Time's up!";
      }
    }, 1000);
  }

  var countdownDisplay = document.getElementById("countdown");
  var countdownDuration = 3600;
  startCountdown(countdownDuration, countdownDisplay);