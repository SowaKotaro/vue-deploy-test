<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const todos = ref([])
const newTodoTitle = ref('')

const apiClient = axios.create({
  baseURL: 'http://localhost:8000',
});

const fetchTodos = async () => {
  try {
    const response = await apiClient.get('/todos/')
    todos.value = response.data
  } catch (error) {
    console.error('Error fetching todos:', error)
  }
}

const addTodo = async () => {
  if (!newTodoTitle.value.trim()) {
    return
  }
  try {
    const response = await apiClient.post('/todos/', {
      title: newTodoTitle.value,
      completed: false,
    })
    todos.value.push(response.data)
    newTodoTitle.value = ''
  } catch (error) {
    console.error('Error adding todo:', error)
  }
}

const deleteTodo = async (id) => {
  try {
    await apiClient.delete(`/todos/${id}`)
    todos.value = todos.value.filter((todo) => todo.id !== id)
  } catch (error) {
    console.error('Error deleting todo:', error)
  }
}

const toggleTodo = async (todo) => {
  try {
    const updatedTodo = { ...todo, completed: !todo.completed }
    await apiClient.put(`/todos/${todo.id}`, {
      title: updatedTodo.title,
      completed: updatedTodo.completed,
    })
    // No need to refetch, just update the local state for better UX
    const index = todos.value.findIndex(t => t.id === todo.id)
    if (index !== -1) {
      todos.value[index].completed = updatedTodo.completed
    }
  } catch (error) {
    console.error('Error updating todo:', error)
  }
}

onMounted(fetchTodos)
</script>

<template>
  <main>
    <h1>My TODO App</h1>
    <form @submit.prevent="addTodo">
      <input
        type="text"
        v-model="newTodoTitle"
        placeholder="Add a new todo..."
      />
      <button type="submit">Add</button>
    </form>

    <ul>
      <li v-for="todo in todos" :key="todo.id">
        <input
          type="checkbox"
          :checked="todo.completed"
          @change="toggleTodo(todo)"
        />
        <span :class="{ completed: todo.completed }">{{ todo.title }}</span>
        <button @click="deleteTodo(todo.id)">Delete</button>
      </li>
    </ul>
  </main>
</template>

<style scoped>
main {
  max-width: 500px;
  margin: 2rem auto;
  font-family: sans-serif;
}

form {
  display: flex;
  margin-bottom: 1rem;
}

input[type="text"] {
  flex-grow: 1;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  padding: 0.5rem 1rem;
  border: none;
  background-color: #007bff;
  color: white;
  border-radius: 4px;
  margin-left: 0.5rem;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}

ul {
  list-style: none;
  padding: 0;
}

li {
  display: flex;
  align-items: center;
  padding: 0.5rem 0;
  border-bottom: 1px solid #eee;
}

li span {
  flex-grow: 1;
  margin-left: 0.5rem;
}

li .completed {
  text-decoration: line-through;
  color: #888;
}

li button {
  background-color: #dc3545;
  opacity: 0;
  transition: opacity 0.2s;
}

li:hover button {
  opacity: 1;
}
</style>