import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE || '', // if empty, dev proxy handles /api
  timeout: 15000,
})

export default api
