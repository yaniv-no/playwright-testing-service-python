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
      if (href === '#/') filter = 'all';
      if (href === '#/active') filter = 'active';
      if (href === '#/completed') filter = 'completed';
      render();
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
