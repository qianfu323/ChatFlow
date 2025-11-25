import {defineStore} from 'pinia'
import axios from 'axios'

export const useChatStore = defineStore('chat', {
    state: () => ({
        ws: null
    }),

    actions: {
        // Fetch groups from the server api
        async fetchGroups() {
            try {
                const response = await axios.get('/room')
                return response.data
            } catch (error) {
                return {success: false, error: error.response?.data || 'Failed to fetch groups'}
            }
        },

        // Create a new group
        async createGroup(groupData) {
            try {
                const response = await axios.post('/room', groupData)
                return response.data
            } catch (error) {
                return {success: false, error: error.response?.message || 'Failed to create group'}
            }
        },

        // Send edit request to the server
        async editGroup(groupData) {
            try {
                const response = await axios.put(`/room`, groupData)
                return response.data
            } catch (error) {
                return {success: false, error: error.response?.message || 'Failed to edit group'}
            }
        },

        // Delete a group
        async deleteGroup(groupId) {
            try {
                const response = await axios.delete(`/room?id=${groupId}`)
                return response.data
            } catch (error) {
                return {success: false, error: error.response?.message || 'Failed to delete group'}
            }
        },
    }
})