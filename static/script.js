// This small UI script was created with AI assistance and reviewed by the author.
document.addEventListener("DOMContentLoaded", () => {
  const search = document.getElementById("searchProblems");
  const difficulty = document.getElementById("filterDifficulty");
  const topic = document.getElementById("filterTopic");
  const rows = document.querySelectorAll("#problemsTable tr");
  const noMatches = document.getElementById("noMatches");

  function filterProblems() {
    if (!search || !difficulty || !topic) return;
    let visible = 0;
    rows.forEach((row) => {
      const matchesName = row.dataset.name.includes(search.value.trim().toLowerCase());
      const matchesDifficulty = !difficulty.value || row.dataset.difficulty === difficulty.value;
      const matchesTopic = !topic.value || row.dataset.topic === topic.value.toLowerCase();
      const show = matchesName && matchesDifficulty && matchesTopic;
      row.classList.toggle("d-none", !show);
      if (show) visible += 1;
    });
    if (noMatches) noMatches.classList.toggle("d-none", visible !== 0);
  }

  [search, difficulty, topic].forEach((element) => element?.addEventListener("input", filterProblems));
  difficulty?.addEventListener("change", filterProblems);
  topic?.addEventListener("change", filterProblems);

  document.querySelectorAll("[data-delete-form]").forEach((form) => {
    form.addEventListener("submit", (event) => {
      if (!window.confirm("Delete this problem permanently?")) event.preventDefault();
    });
  });
});
