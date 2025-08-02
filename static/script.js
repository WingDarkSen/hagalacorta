window.onload = () => {
  const checkbox = document.getElementById('modeToggle');
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  const storedMode = localStorage.getItem('darkMode');
  const isDark = storedMode === null ? prefersDark : storedMode === 'true';

  setMode(isDark);
  checkbox.checked = isDark;

  checkbox.addEventListener('change', () => {
    const active = checkbox.checked;
    setMode(active);
    localStorage.setItem('darkMode', active);
  });
};

function setMode(active) {
  document.body.classList.toggle('light-mode', !active);
}

function limpiarCampo() {
  const input = document.getElementById("urlInput");
  if (input) input.value = "";
}

function copiarEnlace() {
  const enlace = document.querySelector(".resultado a");
  if (enlace) {
    navigator.clipboard.writeText(enlace.href).then(() => {
      const btn = document.querySelector("button[onclick='copiarEnlace()']");
      if (btn) {
        const original = btn.textContent;
        btn.textContent = "Copiado ✅";
        setTimeout(() => btn.textContent = original, 1500);
      }
    });
  }
}
