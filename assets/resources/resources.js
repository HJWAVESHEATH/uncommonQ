document.getElementById("year").textContent = new Date().getFullYear();

async function loadResources() {
  const container = document.getElementById("resourcesGrid");
  const res = await fetch("../data/resources.json?_=" + Date.now());
  const items = await res.json();

  container.innerHTML = items.map(item => `
    <div class="resource-card" data-domain="${item.domain || ''}">
      <h2>${item.title}</h2>
      <p>${item.description}</p>
      <div class="links">
        ${item.pdf ? `<a href="${item.pdf}" class="btn gold" download>Download PDF</a>` : ""}
        ${item.repo ? `<a href="${item.repo}" target="_blank" class="btn cyan">GitHub Repo</a>` : ""}
      </div>
    </div>
  `).join("");
}
loadResources();

document.getElementById("filterBar").addEventListener("click", e => {
  if (e.target.tagName !== "BUTTON") return;
  document.querySelectorAll(".filter-bar button").forEach(b=>b.classList.remove("active"));
  e.target.classList.add("active");
  const filter = e.target.getAttribute("data-filter");
  document.querySelectorAll(".resource-card").forEach(card=>{
    const match = filter==="all" || card.dataset.domain===filter;
    card.style.display = match ? "flex" : "none";
  });
});
