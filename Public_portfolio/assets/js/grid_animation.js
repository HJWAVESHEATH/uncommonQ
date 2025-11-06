const canvas = document.getElementById("resonantGrid");
const ctx = canvas.getContext("2d");
let w, h, lines;

function init() {
  w = canvas.width = window.innerWidth;
  h = canvas.height = window.innerHeight;
  lines = [];
  for (let i = 0; i < 60; i++) {
    lines.push({
      x: Math.random() * w,
      y: Math.random() * h,
      speed: 0.3 + Math.random() * 0.5,
      length: 60 + Math.random() * 120,
      phase: Math.random() * Math.PI * 2
    });
  }
}
function draw() {
  ctx.clearRect(0, 0, w, h);
  ctx.strokeStyle = "rgba(76,209,243,0.2)";
  ctx.lineWidth = 1;
  lines.forEach(l => {
    ctx.beginPath();
    const dx = Math.cos(l.phase) * l.length;
    const dy = Math.sin(l.phase) * l.length;
    ctx.moveTo(l.x, l.y);
    ctx.lineTo(l.x + dx, l.y + dy);
    ctx.stroke();
    l.phase += 0.002;
    l.y -= l.speed;
    if (l.y < -l.length) l.y = h + l.length;
  });
  requestAnimationFrame(draw);
}
window.addEventListener("resize", init);
init(); draw();
