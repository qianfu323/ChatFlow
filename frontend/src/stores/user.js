import {defineStore} from 'pinia'
import axios from 'axios'

export const useUserStore = defineStore('user', {
    state: () => ({
        user: null,
        isAuthenticated: false
    }),

    getters: {
        getUser: (state) => state.user,
        isLoggedIn: (state) => state.isAuthenticated
    },

    actions: {
        async login(credentials) {
            try {
                const response = await axios.post('/user/login', credentials)
                this.user = response.data.user
                this.isAuthenticated = true
                localStorage.setItem('user', JSON.stringify(this.user))
                return {success: true, data: response.data}
            } catch (error) {
                return {success: false, error: error.response?.data || 'Login failed'}
            }
        },

        async register(userData) {
            try {
                const response = await axios.post('/user/register', userData)
                return {success: true, data: response.data}
            } catch (error) {
                return {success: false, error: error.response?.data || 'Registration failed'}
            }
        },

        logout() {
            this.user = null
            this.isAuthenticated = false
            localStorage.removeItem('user')
        },

        initializeAuth() {
            const storedUser = localStorage.getItem('user')
            if (storedUser) {
                this.user = JSON.parse(storedUser)
                this.isAuthenticated = true
            }
        }
    }
})