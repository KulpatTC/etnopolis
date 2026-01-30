const questions = [
    {
        question: " 1. Россия является одним из мировых рекордсменов по этническому и языковому разнообразию. Сколько примерно народов проживает на её территории?",
        answers: ["Около 50 народов", "Более 190 народов"],
        correct: 1 // Индекс правильного ответа (0, 1, 2)
    },
    {
        question: " 2. Уникальная традиция «хороводных песен», вошедшая в список ЮНЕСКО, сохранилась в одном из регионов России. Каком?  ",
        answers: ["В Вологодской области", "В Краснодарском крае"],
        correct: 0
    },
    {
        question: "3. На севере России, в Ненецком автономном округе, до сих пор существует кочевой уклад жизни. С чем традиционно связан быт ненцев?  ",
        answers: ["С охотой на морского зверя и рыболовством", "С оленеводством и переездами по тундре   "],
        correct: 1
    },
    {
        question: "4. Закончи высказывание: На Масленицу блины пекут не просто как угощение... ",
        answers: ["включён в список нематериального культурного наследия ЮНЕСКО.", "а как символ солнца и праздник проводов зимы.", "крупнейший в мире комплекс фонтанов (около 150)"],
        correct: 1
    },
    {
        question: "5. Закончи высказывание: В России находится самый большой в мире... ",
        answers: ["но и крупнейший природный резервуар пресной воды (около 20% мировых запасов).", "крупнейший в мире комплекс фонтанов (около 150)", " лесной массив — сибирская тайга."],
        correct: 2
    },
    {
        question: "6. Закончи высказывание: Татарский праздник Сабантуй, посвящённый окончанию весенних полевых работ... ",
        answers: ["включён в список нематериального культурного наследия ЮНЕСКО.", "а как символ солнца и праздник проводов зимы.", "крупнейший в мире комплекс фонтанов (около 150)"],
        correct: 0
    },
    {
        question: "7. Закончи высказывание: В Петергофе находится ... ",
        answers: [" лесной массив — сибирская тайга.", "включён в список нематериального культурного наследия ЮНЕСКО.", "крупнейший в мире комплекс фонтанов (около 150)"],
        correct: 2
    },
    {
        question: "8. Закончи высказывание: Озеро Байкал — не только самое глубокое озеро планеты,  ... ",
        answers: ["а как символ солнца и праздник проводов зимы.", " лесной массив — сибирская тайга.", "но и крупнейший природный резервуар пресной воды (около 20% мировых запасов)."],
        correct: 2
    }

];

let currentQuestion = 0;
let score = 0;

const questionEl = document.getElementById("question");
const answersEl = document.getElementById("answers");
const nextBtn = document.getElementById("next");

function showQuestion() {
    const q = questions[currentQuestion];
    questionEl.innerText = q.question;
    answersEl.innerHTML = "";
    
    q.answers.forEach((answer, index) => {
        const button = document.createElement("button");
        button.innerText = answer;
        button.onclick = () => checkAnswer(index);
        answersEl.appendChild(button);
    });
}

function checkAnswer(index) {
    if (index === questions[currentQuestion].correct) {
        score++;
    }
    currentQuestion++;
    if (currentQuestion < questions.length) {
        showQuestion();
    } else {
        showResult();
    }
}

function showResult() {
    document.getElementById("quiz").style.display = "none";
    const resultEl = document.getElementById("result");
    resultEl.style.display = "block";
    resultEl.innerText = `Вы набрали ${score} из ${questions.length}`;
}

showQuestion(); // Запуск
