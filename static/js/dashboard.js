const modal = document.getElementById('taskModal');
const openBtn = document.getElementById('openModalBtn');
const closeBtn = document.getElementById('closeModalBtn');
const taskForm = document.getElementById('taskForm');
const modalTitle = document.getElementById('taskModalTitle');
const submitBtn = document.getElementById('taskSubmitBtn');

function resetTaskForm() {
    taskForm.reset();
    taskForm.action = taskForm.dataset.createUrl;
    modalTitle.textContent = 'Add New Task';
    submitBtn.textContent = 'Create Task';
}

openBtn.addEventListener('click', () => {
    resetTaskForm();
    modal.classList.add('active');
});

closeBtn.addEventListener('click', () => {
    modal.classList.remove('active');
    resetTaskForm();
});

document.querySelectorAll('.btn-action.edit').forEach((link) => {
    link.addEventListener('click', (event) => {
        event.preventDefault();
        taskForm.action = link.href;
        taskForm.elements.title.value = link.dataset.title;
        taskForm.elements.description.value = link.dataset.description;
        taskForm.elements.due_date.value = link.dataset.dueDate;
        taskForm.elements.priority.value = link.dataset.priority;
        modalTitle.textContent = 'Edit Task';
        submitBtn.textContent = 'Save Changes';
        modal.classList.add('active');
    });
});

window.addEventListener('click', (e) => {
    if (e.target === modal) {
        modal.classList.remove('active');
        resetTaskForm();
    }
});