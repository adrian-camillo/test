// ===== Claude Todo App =====

class TodoApp {
  constructor() {
    this.todos = JSON.parse(localStorage.getItem('claude-todos')) || [];
    this.currentFilter = 'all';
    this.editingId = null;

    this.input = document.getElementById('todoInput');
    this.addBtn = document.getElementById('addBtn');
    this.list = document.getElementById('todoList');
    this.statsText = document.getElementById('statsText');
    this.clearBtn = document.getElementById('clearCompleted');
    this.filterBtns = document.querySelectorAll('.filter-btn');

    this.bindEvents();
    this.render();
  }

  bindEvents() {
    this.addBtn.addEventListener('click', () => this.addTodo());
    this.input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') this.addTodo();
    });
    this.clearBtn.addEventListener('click', () => this.clearCompleted());
    this.filterBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        this.currentFilter = btn.dataset.filter;
        this.filterBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        this.render();
      });
    });
  }

  generateId() {
    return Date.now().toString(36) + Math.random().toString(36).slice(2, 7);
  }

  addTodo() {
    const text = this.input.value.trim();
    if (!text) {
      this.input.focus();
      return;
    }

    this.todos.unshift({
      id: this.generateId(),
      text,
      completed: false,
      createdAt: new Date().toISOString()
    });

    this.input.value = '';
    this.input.focus();
    this.save();
    this.render();
  }

  toggleTodo(id) {
    const todo = this.todos.find(t => t.id === id);
    if (todo) {
      todo.completed = !todo.completed;
      this.save();
      this.render();
    }
  }

  deleteTodo(id) {
    const item = document.querySelector(`[data-id="${id}"]`);
    if (item) {
      item.classList.add('removing');
      setTimeout(() => {
        this.todos = this.todos.filter(t => t.id !== id);
        this.save();
        this.render();
      }, 280);
    }
  }

  startEdit(id) {
    this.editingId = id;
    this.render();
    const editInput = document.querySelector('.todo-edit-input');
    if (editInput) {
      editInput.focus();
      editInput.setSelectionRange(editInput.value.length, editInput.value.length);
    }
  }

  saveEdit(id, newText) {
    const text = newText.trim();
    if (text) {
      const todo = this.todos.find(t => t.id === id);
      if (todo) todo.text = text;
    }
    this.editingId = null;
    this.save();
    this.render();
  }

  clearCompleted() {
    const completedItems = document.querySelectorAll('.todo-item.completed');
    completedItems.forEach(item => item.classList.add('removing'));
    setTimeout(() => {
      this.todos = this.todos.filter(t => !t.completed);
      this.save();
      this.render();
    }, 280);
  }

  save() {
    localStorage.setItem('claude-todos', JSON.stringify(this.todos));
  }

  getFilteredTodos() {
    switch (this.currentFilter) {
      case 'pending': return this.todos.filter(t => !t.completed);
      case 'completed': return this.todos.filter(t => t.completed);
      default: return this.todos;
    }
  }

  updateStats() {
    const total = this.todos.length;
    const completed = this.todos.filter(t => t.completed).length;
    const pending = total - completed;

    if (total === 0) {
      this.statsText.textContent = '0 tareas';
    } else {
      this.statsText.textContent = `${pending} pendiente${pending !== 1 ? 's' : ''} de ${total}`;
    }

    this.clearBtn.style.display = completed > 0 ? 'block' : 'none';
  }

  createTodoElement(todo) {
    const li = document.createElement('li');
    li.className = `todo-item${todo.completed ? ' completed' : ''}`;
    li.dataset.id = todo.id;

    if (this.editingId === todo.id) {
      li.innerHTML = `
        <input type="checkbox" class="todo-checkbox" ${todo.completed ? 'checked' : ''}>
        <input type="text" class="todo-edit-input" value="${this.escapeHtml(todo.text)}">
        <div class="todo-actions" style="opacity:1">
          <button class="btn-action btn-save" title="Guardar">
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
              <path d="M3 8L6.5 11.5L13 5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
        </div>
      `;

      const editInput = li.querySelector('.todo-edit-input');
      const saveBtn = li.querySelector('.btn-save');

      editInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') this.saveEdit(todo.id, editInput.value);
        if (e.key === 'Escape') { this.editingId = null; this.render(); }
      });
      editInput.addEventListener('blur', () => this.saveEdit(todo.id, editInput.value));
      saveBtn.addEventListener('click', () => this.saveEdit(todo.id, editInput.value));
    } else {
      li.innerHTML = `
        <input type="checkbox" class="todo-checkbox" ${todo.completed ? 'checked' : ''}>
        <span class="todo-text">${this.escapeHtml(todo.text)}</span>
        <div class="todo-actions">
          <button class="btn-action btn-edit" title="Editar">
            <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
              <path d="M8.5 2.5L11.5 5.5M1.5 12.5L2.2 9.6L10 1.8C10.4 1.4 11.1 1.4 11.5 1.8L12.2 2.5C12.6 2.9 12.6 3.6 12.2 4L4.4 11.8L1.5 12.5Z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
          <button class="btn-action btn-delete" title="Eliminar">
            <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
              <path d="M2.5 4H11.5M5 4V2.5C5 2.2 5.2 2 5.5 2H8.5C8.8 2 9 2.2 9 2.5V4M5.5 6.5V10.5M8.5 6.5V10.5M3.5 4L4 11.5C4 11.8 4.2 12 4.5 12H9.5C9.8 12 10 11.8 10 11.5L10.5 4" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
        </div>
      `;

      li.querySelector('.btn-edit').addEventListener('click', () => this.startEdit(todo.id));
      li.querySelector('.btn-delete').addEventListener('click', () => this.deleteTodo(todo.id));
    }

    li.querySelector('.todo-checkbox').addEventListener('change', () => this.toggleTodo(todo.id));

    return li;
  }

  escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  render() {
    const filtered = this.getFilteredTodos();
    this.list.innerHTML = '';

    if (filtered.length === 0) {
      const emptyMsg = this.todos.length === 0
        ? { title: 'No hay tareas todavia', sub: 'Agrega una tarea para comenzar' }
        : { title: 'Sin resultados', sub: 'No hay tareas en esta categoria' };

      this.list.innerHTML = `
        <li class="empty-state">
          <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
            <circle cx="24" cy="24" r="20" stroke="#D97757" stroke-width="2" stroke-dasharray="4 4" opacity="0.4"/>
            <path d="M18 24L22 28L30 20" stroke="#D97757" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" opacity="0.4"/>
          </svg>
          <p>${emptyMsg.title}</p>
          <span>${emptyMsg.sub}</span>
        </li>
      `;
    } else {
      filtered.forEach(todo => {
        this.list.appendChild(this.createTodoElement(todo));
      });
    }

    this.updateStats();
  }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  new TodoApp();
});
