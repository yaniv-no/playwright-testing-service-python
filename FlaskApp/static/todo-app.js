// Minimal TodoMVC logic for Playwright tests
// This is a simplified implementation to support the Playwright test suite

document.addEventListener('DOMContentLoaded', () => {
  const newTodo = document.querySelector('.new-todo');
  const todoList = document.querySelector('.todo-list');
  const mainSection = document.querySelector('.main');
  const footer = document.querySelector('.footer');
  const todoCount = document.querySelector('.todo-count');
  const toggleAll = document.getElementById('toggle-all');
  const clearCompleted = document.querySelector('.clear-completed');
  const filters = document.querySelectorAll('.filters a');

  let todos = JSON.parse(localStorage.getItem('react-todos') || '[]');
  let filter = 'all';

  function saveTodos() {
    localStorage.setItem('react-todos', JSON.stringify(todos));
  }

  // Toggle all functionality
  toggleAll.addEventListener('change', () => {
    const checked = toggleAll.checked;
    todos.forEach(t => t.completed = checked);
    saveTodos();
    render();
  });

  // Editing functionality
  function startEditing(li, idx) {
    li.classList.add('editing');
    const todo = todos[idx];
    const input = document.createElement('input');
    input.className = 'edit';
    input.value = todo.title;
    input.setAttribute('aria-label', 'Edit');
    li.querySelector('.view').style.display = 'none';
    li.appendChild(input);
    input.focus();
    input.setSelectionRange(input.value.length, input.value.length);

    function finishEdit(save) {
      let val = input.value.trim();
      if (save && val) {
        todo.title = val;
        saveTodos();
      } else if (save && !val) {
        // Remove the todo from the main todos array, not just filtered
        const todoIdx = todos.indexOf(todo);
        if (todoIdx !== -1) {
          todos.splice(todoIdx, 1);
          saveTodos();
        }
      } else if (!save) {
        // Cancel: restore original value
      }
      li.classList.remove('editing');
      input.remove();
      li.querySelector('.view').style.display = '';
      render();
    }

    let originalValue = input.value;
    input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') finishEdit(true);
      if (e.key === 'Escape') {
        input.value = originalValue;
        finishEdit(false);
      }
    });
    input.addEventListener('blur', () => finishEdit(true));
  }

  // Routing (hashchange)
  function updateFilterFromHash() {
    const hash = location.hash.replace('#/', '');
    if (['', 'active', 'completed'].includes(hash)) {
      filter = hash || 'all';
      render();
    }
  }
  window.addEventListener('hashchange', updateFilterFromHash);
  // Ensure correct filter on initial load
  updateFilterFromHash();

  // Update render to support editing and double-click
  function render() {
    // Filter todos
    let filteredTodos = todos;
    if (filter === 'active') filteredTodos = todos.filter(t => !t.completed);
    if (filter === 'completed') filteredTodos = todos.filter(t => t.completed);

    // Render todo items
    todoList.innerHTML = '';
    filteredTodos.forEach((todo, idx) => {
      const li = document.createElement('li');
      li.className = todo.completed ? 'completed' : '';
      li.setAttribute('data-testid', 'todo-item');

      const div = document.createElement('div');
      div.className = 'view';

      const checkbox = document.createElement('input');
      checkbox.type = 'checkbox';
      checkbox.className = 'toggle';
      checkbox.checked = todo.completed;
      checkbox.addEventListener('change', () => {
        todo.completed = !todo.completed;
        saveTodos();
        render();
      });
      div.appendChild(checkbox);

      const label = document.createElement('label');
      label.textContent = todo.title;
      label.setAttribute('data-testid', 'todo-title');
      label.addEventListener('dblclick', () => startEditing(li, todos.indexOf(todo)));
      div.appendChild(label);

      li.appendChild(div);
      todoList.appendChild(li);
    });

    // Show/hide main and footer
    mainSection.style.display = todos.length ? '' : 'none';
    footer.style.display = todos.length ? '' : 'none';

    // Update count
    const activeCount = todos.filter(t => !t.completed).length;
    todoCount.textContent = `${activeCount} item${activeCount !== 1 ? 's' : ''} left`;

    // Toggle all checkbox
    toggleAll.checked = todos.length && todos.every(t => t.completed);
    toggleAll.style.display = todos.length ? '' : 'none';

    // Show/hide clear completed
    const completedCount = todos.filter(t => t.completed).length;
    clearCompleted.style.display = completedCount ? '' : 'none';

    // Highlight filter
    filters.forEach(f => f.classList.remove('selected'));
    document.querySelector(`[data-testid="filter-${filter}"]`).classList.add('selected');
  }

  newTodo.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && newTodo.value.trim()) {
      todos.push({ title: newTodo.value.trim(), completed: false });
      newTodo.value = '';
      saveTodos();
      render();
    }
  });

  // Add event listeners for filter links
  filters.forEach(f => {
    f.addEventListener('click', (e) => {
      e.preventDefault();
      const href = f.getAttribute('href');
      if (href) {
        location.hash = href;
      }
    });
  });

  // Add event listener for clear completed
  clearCompleted.addEventListener('click', () => {
    todos = todos.filter(t => !t.completed);
    saveTodos();
    render();
  });

  render();
});
