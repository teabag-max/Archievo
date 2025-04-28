<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Archievo</title>

  <style>
    /* --- Same CSS as before --- */
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: 'Poppins', sans-serif;
      background-color: #f5f5f5;
      color: #333;
      transition: background-color 0.3s, color 0.3s;
    }
    .navbar {
      background-color: #6200ea;
      color: white;
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 1rem;
    }
    #theme-toggle {
      background: none;
      border: none;
      color: white;
      font-size: 1.5rem;
      cursor: pointer;
    }
    .container { padding: 2rem; }
    .goal-card {
      background: white;
      padding: 1rem;
      margin: 1rem 0;
      border-radius: 10px;
      box-shadow: 0 2px 6px rgba(0,0,0,0.1);
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
    }
    .goal-text { flex: 1; }
    .goal-actions button {
      margin-left: 10px;
      padding: 6px 10px;
      border: none;
      border-radius: 5px;
      cursor: pointer;
    }
    .goal-actions .edit-btn { background-color: #4caf50; color: white; }
    .goal-actions .delete-btn { background-color: #f44336; color: white; }
    .add-goal-form {
      margin-top: 1rem;
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
    }
    .add-goal-form input[type="text"],
    .add-goal-form input[type="date"] {
      padding: 0.5rem;
      flex: 1 1 200px;
      border: 1px solid #ccc;
      border-radius: 5px;
    }
    .add-goal-form button {
      padding: 0.5rem 1rem;
      background-color: #6200ea;
      color: white;
      border: none;
      border-radius: 5px;
      cursor: pointer;
    }
    /* Dark theme */
    body.dark { background-color: #121212; color: #e0e0e0; }
    body.dark .goal-card { background: #1e1e1e; }
    body.dark .navbar { background-color: #333; }
    body.dark .add-goal-form input { background-color: #222; color: #eee; border: 1px solid #555; }
    body.dark .add-goal-form button { background-color: #bb86fc; }
    body.dark .goal-actions .edit-btn { background-color: #03dac6; }
    body.dark .goal-actions .delete-btn { background-color: #cf6679; }
  </style>

</head>
<body>

  <nav class="navbar">
    <div class="logo">🎯 Archievo</div>
    <button id="theme-toggle">🌗</button>
  </nav>

  <main class="container">

    <div class="quote-box" id="quote-box">Loading motivation...</div>

    <section class="daily-challenge">
      <h2>✅ Daily Challenge</h2>
      <p id="challenge-text">
        Walk 5,000 steps today!
        <button id="accept-challenge-btn">Accept Challenge</button>
      </p>
    </section>

    <section class="goals-section">
      <h2>Your Goals</h2>

      <form class="add-goal-form" id="add-goal-form">
        <input type="text" id="goal-input" placeholder="Enter your goal..." required>
        <input type="date" id="goal-date" required>
        <button type="submit">Add Goal</button>
      </form>

      <div id="goals-list"></div>
    </section>

    <section class="achievements">
      <h2>🏅 Achievements</h2>
      <ul>
        <li>First Goal Completed Badge</li>
        <li>3-Day Streak Badge</li>
      </ul>
    </section>

    <button class="summary-btn">View Weekly Summary 📊</button>

  </main>

  <script>
    // --- JavaScript ---

    // Theme Toggle
    const themeToggle = document.getElementById('theme-toggle');
    themeToggle.addEventListener('click', () => {
      document.body.classList.toggle('dark');
      themeToggle.textContent = document.body.classList.contains('dark') ? '🌞' : '🌗';
    });

    // Motivational Quotes
    const quotes = [
      "Push yourself because no one else is going to do it for you.",
      "Dream big. Work hard. Stay focused.",
      "Success doesn’t come to you — you go to it.",
      "Little by little, day by day, what is meant for you will find its way.",
      "You don’t have to be great to start, but you have to start to be great.",
      "Believe you can and you're halfway there.",
      "The harder you work for something, the greater you’ll feel when you achieve it.",
      "Don’t stop until you’re proud.",
      "Focus on your goal. Don’t look in any direction but ahead.",
      "Discipline is doing what needs to be done, even when you don’t feel like doing it."
    ];
    const quoteBox = document.getElementById('quote-box');
    quoteBox.textContent = `"${quotes[Math.floor(Math.random() * quotes.length)]}"`;

    // Daily Challenge Button
    const acceptBtn = document.getElementById('accept-challenge-btn');
    acceptBtn.addEventListener('click', () => {
      acceptBtn.disabled = true;
      acceptBtn.textContent = 'Challenge Accepted! 🎉';
      acceptBtn.style.backgroundColor = '#4caf50';
      acceptBtn.style.color = 'white';
    });

    // Goals
    const addGoalForm = document.getElementById('add-goal-form');
    const goalInput = document.getElementById('goal-input');
    const goalDate = document.getElementById('goal-date');
    const goalsList = document.getElementById('goals-list');

    addGoalForm.addEventListener('submit', function(e) {
      e.preventDefault();
      const goalText = goalInput.value.trim();
      const targetDate = goalDate.value;

      if (goalText && targetDate) {
        const goalCard = document.createElement('div');
        goalCard.className = 'goal-card';

        const daysLeft = calculateDaysLeft(targetDate);

        goalCard.innerHTML = `
          <div class="goal-text">
            <h3 contenteditable="false">${goalText}</h3>
            <p><strong>Days Left:</strong> ${daysLeft} days</p>
          </div>
          <div class="goal-actions">
            <button class="edit-btn">✏️ Edit</button>
            <button class="delete-btn">🗑️ Delete</button>
          </div>
        `;

        // Edit and Delete buttons
        goalCard.querySelector('.edit-btn').addEventListener('click', function() {
          const title = goalCard.querySelector('h3');
          title.contentEditable = true;
          title.focus();
        });

        goalCard.querySelector('.delete-btn').addEventListener('click', function() {
          goalCard.remove();
        });

        goalsList.appendChild(goalCard);
        goalInput.value = "";
        goalDate.value = "";
      }
    });

    // Function to calculate days left
    function calculateDaysLeft(targetDate) {
      const today = new Date();
      const goalDay = new Date(targetDate);
      const diffTime = goalDay - today;
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
      return diffDays > 0 ? diffDays : 0;
    }

  </script>

</body>
</html>
