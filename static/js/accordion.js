var acc = document.getElementsByClassName('accordion');
var i;

for (i=0; i < acc.length; i++) {
    acc[i].addEventListener('click', function() {
        this.classList.toggle('accordion-active');

        var panel = this.nextElementSibling;
        if (panel.style.display === "block") {
            panel.style.display = "none";
        } else {
            panel.style.display = "block";
        }
    });
}

// according (modal) game
const player1 = document.querySelector("#player1");
const player2 = document.querySelector("#player2");

const win = document.querySelector("#winner");
const play = document.querySelector("#play");

let player1Counter = 0;
let player2Counter = 0;

play.onclick = function() {
    player1Counter = 0
    player2Counter = 0

    player1.value = 0
    player2.value = 0

    let gameInterval = setInterval(function() {
        player1Counter += Math.random() * 10;
        player2Counter += Math.random() * 10;
        win.innerHTML = ""

        player1.value = player1Counter;
        player2.value = player2Counter;

        if (player1Counter >= 100) {
            clearInterval(gameInterval)
            win.innerHTML = "Player 1";
        } else if (player2Counter >= 100) {
            clearInterval(gameInterval)
            win.innerHTML = "Player 2";
        }
    }, 200)
}