import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import axios from 'axios'

// Import Vant styles and components
import 'vant/lib/index.css';
import Vant from 'vant';

// Set base URL for axios
axios.defaults.baseURL = 'http://127.0.0.1:8000/api';
axios.defaults.withCredentials = true;

const app = createApp(App)
const pinia = createPinia()

// Register all Vant components
app.use(Vant)

app.use(pinia)
app.use(router)

app.mount('#app')