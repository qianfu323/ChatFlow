import {createRouter, createWebHistory} from 'vue-router'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Home from '../views/Home.vue'
import Chat from '../views/Chat.vue'

const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home,
        meta: {requiresAuth: true}
    },
    {
        path: '/login',
        name: 'Login',
        component: Login
    },
    {
        path: '/register',
        name: 'Register',
        component: Register
    },
    {
        path: '/chat',
        name: 'Chat',
        component: Chat
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

// Navigation guard
router.beforeEach((to, from, next) => {
    const isAuthenticated = !!localStorage.getItem('user')

    if (to.meta.requiresAuth && !isAuthenticated) {
        next('/login')
    } else if ((to.name === 'Login' || to.name === 'Register') && isAuthenticated) {
        next('/')
    } else {
        next()
    }
})

export default router