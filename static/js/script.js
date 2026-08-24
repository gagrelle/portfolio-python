const header = document.querySelector('.site-header');
const progress = document.querySelector('.scroll-progress span');
const menuButton = document.querySelector('.menu-toggle');
const navLinks = document.querySelector('.nav-links');
const terminalForm = document.querySelector('#terminal-form');
const terminalInput = document.querySelector('#terminal-input');
const terminalOutput = document.querySelector('#terminal-output');

const escapeHTML = (value) => value.replace(/[&<>'"]/g, (character) => ({
  '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;'
}[character]));

const setScrollState = () => {
  const scrollable = document.documentElement.scrollHeight - window.innerHeight;
  const percentage = scrollable > 0 ? (window.scrollY / scrollable) * 100 : 0;
  progress.style.width = `${percentage}%`;
  header.classList.toggle('scrolled', window.scrollY > 18);
};

window.addEventListener('scroll', setScrollState, { passive: true });
setScrollState();

const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      revealObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.12 });

document.querySelectorAll('.reveal').forEach((element) => {
  element.style.setProperty('--delay', `${element.dataset.delay || 0}ms`);
  revealObserver.observe(element);
});

menuButton.addEventListener('click', () => {
  const isOpen = menuButton.getAttribute('aria-expanded') === 'true';
  menuButton.setAttribute('aria-expanded', String(!isOpen));
  menuButton.setAttribute('aria-label', isOpen ? 'Abrir menu' : 'Fechar menu');
  navLinks.classList.toggle('open', !isOpen);
  document.body.style.overflow = isOpen ? '' : 'hidden';
});

document.querySelectorAll('.nav-links a').forEach((link) => {
  link.addEventListener('click', () => {
    menuButton.setAttribute('aria-expanded', 'false');
    navLinks.classList.remove('open');
    document.body.style.overflow = '';
  });
});

const sections = [...document.querySelectorAll('main section[id]')];
const navigationItems = [...document.querySelectorAll('.nav-links a[href^="#"]')];
const activeSectionObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (!entry.isIntersecting) return;
    navigationItems.forEach((item) => item.classList.toggle('active', item.hash === `#${entry.target.id}`));
  });
}, { rootMargin: '-35% 0px -55%', threshold: 0 });
sections.forEach((section) => activeSectionObserver.observe(section));

const commands = {
  ajuda: () => 'Comandos: sobre · skills · projetos · experiencia · contato · curriculo · status · limpar',
  sobre: () => 'João é estudante de ADS e desenvolvedor Python em formação, com experiência em processos, dados e automação.',
  skills: () => 'Python | Java | HTML5 | CSS3 | Excel | Google Sheets | IA Generativa | Engenharia de Prompt',
  projetos: () => '3 projetos encontrados: Dashboard em Python, Controle de Devoluções e Landing Pages.',
  experiencia: () => 'Atual: Análise de Estoque na Vulp Air. Anterior: Departamento Pessoal na CW Consultores.',
  contato: () => 'E-mail: joaogilbert795@gmail.com | Telefone: +55 (81) 99677-5491',
  curriculo: () => {
    window.location.href = '/curriculo';
    return 'Preparando download de Curriculo_Joao_Gilbert_Agrelle.pdf...';
  },
  status: async () => {
    try {
      const response = await fetch('/api/status');
      const data = await response.json();
      return `${data.status.toUpperCase()} — ${data.availability} · ${data.location}`;
    } catch {
      return 'Perfil online — buscando estágio em Backend e IA Generativa.';
    }
  }
};

const appendTerminalLine = (command, response, isError = false) => {
  const commandLine = document.createElement('p');
  commandLine.className = 'terminal-command';
  commandLine.innerHTML = `<span class="prompt">$</span> ${escapeHTML(command)}`;
  const responseLine = document.createElement('div');
  responseLine.className = `terminal-response${isError ? ' error' : ''}`;
  responseLine.textContent = response;
  terminalOutput.append(commandLine, responseLine);
  terminalOutput.scrollTop = terminalOutput.scrollHeight;
};

terminalForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  const command = terminalInput.value.trim().toLowerCase();
  if (!command) return;
  terminalInput.value = '';

  if (command === 'limpar' || command === 'clear') {
    terminalOutput.innerHTML = '<p class="terminal-hint">Terminal limpo. Digite <strong>ajuda</strong> para explorar.</p>';
    return;
  }

  const handler = commands[command];
  if (!handler) {
    appendTerminalLine(command, `Comando não encontrado: ${command}. Digite “ajuda”.`, true);
    return;
  }
  appendTerminalLine(command, await handler());

  const targetMap = { sobre: '#sobre', skills: '#skills', projetos: '#projetos', experiencia: '#experiencia', contato: '#contato' };
  if (targetMap[command]) {
    setTimeout(() => document.querySelector(targetMap[command]).scrollIntoView({ behavior: 'smooth' }), 320);
  }
});

document.addEventListener('keydown', (event) => {
  if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === 'k') {
    event.preventDefault();
    document.querySelector('.terminal').scrollIntoView({ behavior: 'smooth', block: 'center' });
    setTimeout(() => terminalInput.focus(), 350);
  }
  if (event.key === 'Escape' && navLinks.classList.contains('open')) {
    menuButton.click();
  }
});

document.querySelector('.copy-email').addEventListener('click', async (event) => {
  const button = event.currentTarget;
  const originalLabel = button.textContent;
  try {
    await navigator.clipboard.writeText(button.dataset.email);
    button.textContent = 'e-mail copiado ✓';
  } catch {
    button.textContent = button.dataset.email;
  }
  setTimeout(() => { button.textContent = originalLabel; }, 2200);
});

if (window.matchMedia('(pointer: fine)').matches && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
  document.querySelectorAll('.project-card').forEach((card) => {
    card.addEventListener('mousemove', (event) => {
      const bounds = card.getBoundingClientRect();
      const rotateY = ((event.clientX - bounds.left) / bounds.width - 0.5) * 4;
      const rotateX = ((event.clientY - bounds.top) / bounds.height - 0.5) * -4;
      card.style.transform = `translateY(-7px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
    });
    card.addEventListener('mouseleave', () => { card.style.transform = ''; });
  });
}
