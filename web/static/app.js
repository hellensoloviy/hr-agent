let isLoading = false;

function autoResize(el) {
  el.style.height = 'auto';
  el.style.height = Math.min(el.scrollHeight, 120) + 'px';
}

function handleKey(e) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
}

function sendSuggestion(el) {
  const text = el.dataset.message;
  if (!text) return;
  document.getElementById('input').value = text;
  sendMessage();
}

function addMessage(role, content) {
  const welcome = document.getElementById('welcome');
  if (welcome) welcome.remove();

  const msgs = document.getElementById('messages');
  const div = document.createElement('div');
  div.className = 'msg ' + role;
  div.innerHTML =
    '<div class="msg-avatar">' + (role === 'user' ? '👤' : '🤝') + '</div>' +
    '<div class="msg-content">' + (role === 'bot' ? renderMarkdown(content) : escapeHtml(content)) + '</div>';
  msgs.appendChild(div);
  msgs.scrollTop = msgs.scrollHeight;
}

function addTyping() {
  const welcome = document.getElementById('welcome');
  if (welcome) welcome.remove();
  const msgs = document.getElementById('messages');
  const div = document.createElement('div');
  div.className = 'msg bot typing';
  div.id = 'typing';
  div.innerHTML =
    '<div class="msg-avatar">🤝</div>' +
    '<div class="msg-content"><div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div></div>';
  msgs.appendChild(div);
  msgs.scrollTop = msgs.scrollHeight;
}

function removeTyping() {
  const t = document.getElementById('typing');
  if (t) t.remove();
}

function appendToolLog(tools) {
  if (!tools || tools.length === 0) return;
  const log = document.getElementById('tool-log');
  const empty = log.querySelector('.tool-log-empty');
  if (empty) empty.remove();
  tools.forEach(function(t) {
    const input = JSON.stringify(t.input);
    const result = t.result.length > 70 ? t.result.substring(0, 70) + '...' : t.result;
    log.innerHTML +=
      '<span class="tool-call">→ ' + t.name + '(' + escapeHtml(input) + ')</span>\n' +
      '<span class="tool-result">  ✓ ' + escapeHtml(result) + '</span>\n';
  });
  log.scrollTop = log.scrollHeight;
}

function escapeHtml(text) {
  return String(text)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
}

function renderMarkdown(text) {
  // Escape HTML first
  let t = escapeHtml(text);

  // Bold
  t = t.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');

  // Tables — collect rows then wrap
  t = t.replace(/(\|.+\|\n?)+/g, function(block) {
    const rows = block.trim().split('\n').filter(function(r) {
      return r.trim() && !r.match(/^\|[\s\-|]+\|$/);
    });
    if (rows.length === 0) return block;
    const header = rows[0];
    const body = rows.slice(1);
    const thCells = header.split('|').filter(function(c) { return c.trim(); });
    const thead = '<tr>' + thCells.map(function(c) { return '<th>' + c.trim() + '</th>'; }).join('') + '</tr>';
    const tbody = body.map(function(row) {
      const cells = row.split('|').filter(function(c) { return c.trim(); });
      return '<tr>' + cells.map(function(c) { return '<td>' + c.trim() + '</td>'; }).join('') + '</tr>';
    }).join('');
    return '<table><thead>' + thead + '</thead><tbody>' + tbody + '</tbody></table>';
  });

  // Bullet lists
  t = t.replace(/(^|\n)(- .+)+/g, function(block) {
    const items = block.trim().split('\n').filter(function(l) { return l.startsWith('- '); });
    return '<ul>' + items.map(function(i) { return '<li>' + i.slice(2) + '</li>'; }).join('') + '</ul>';
  });

  // Line breaks
  t = t.replace(/\n/g, '<br>');

  return t;
}

async function sendMessage() {
  if (isLoading) return;
  const input = document.getElementById('input');
  const message = input.value.trim();
  if (!message) return;

  input.value = '';
  input.style.height = 'auto';
  isLoading = true;
  document.getElementById('send-btn').disabled = true;

  addMessage('user', message);
  addTyping();

  try {
    const res = await fetch('/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: message })
    });

    const data = await res.json();
    removeTyping();

    if (data.error) {
      addMessage('bot', 'Sorry, something went wrong. Please try again.');
    } else {
      addMessage('bot', data.response);
      appendToolLog(data.tools_used);
    }
  } catch (e) {
    removeTyping();
    addMessage('bot', 'Connection error. Is the server running?');
    console.error(e);
  }

  isLoading = false;
  document.getElementById('send-btn').disabled = false;
  document.getElementById('input').focus();
}

async function resetChat() {
  await fetch('/reset', { method: 'POST' });
  document.getElementById('messages').innerHTML =
    '<div class="welcome" id="welcome">' +
    '<div class="big-avatar">🤝</div>' +
    '<h2>Hi, I\'m Alex</h2>' +
    '<p>Your HR assistant at TechCorp.<br>I can help you manage candidates and schedule interviews.</p>' +
    '</div>';
  document.getElementById('tool-log').innerHTML = '<span class="tool-log-empty">Tool calls will appear here...</span>';
}

document.getElementById('input').focus();