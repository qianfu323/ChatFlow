<template>
    <div class="group-chat-container">
        <van-nav-bar
            :title="groupInfo.name"
            left-arrow
            @click-left="goBack"
            fixed
            placeholder
        />

        <!-- Messages area -->
        <div class="messages-container" ref="messagesContainer">
            <div
                v-for="message in messages"
                :key="message.id"
                :class="['message-wrapper', message.sender_id === currentUser.id ? 'sent' : 'received']"
            >
                <!-- Avatar -->
                <div class="avatar" :style="{ backgroundColor: getAvatarColor(message.username) }">
                    {{ getAvatarText(message.username) }}
                </div>

                <!-- Message bubble -->
                <div class="message-bubble">
                    <div class="sender-name" v-if="message.sender_id !== currentUser.id">
                        {{ message.username }}
                    </div>
                    <div class="message-text">{{ message.message }}</div>
                    <div class="message-time">{{ formatTime(message.timestamp) }}</div>
                </div>
            </div>
        </div>

        <!-- Input area -->
        <div class="input-container">
            <van-field
                v-model="messageText"
                placeholder="Type a message"
                @keyup.enter="sendMessage"
            >
                <template #button>
                    <van-button type="primary" @click="sendMessage">Send</van-button>
                </template>
            </van-field>
        </div>
    </div>
</template>

<script setup>
import {ref, onMounted, onUnmounted, nextTick} from 'vue'
import {useRoute, useRouter} from 'vue-router'
import {useChatStore} from '@/stores/chat'
import {useUserStore} from '@/stores/user'
import {showFailToast} from 'vant'

const route = useRoute()
const router = useRouter()
const chatStore = useChatStore()
const userStore = useUserStore()

const messages = ref([])
const messageText = ref('')
const messagesContainer = ref(null)
const groupInfo = ref({
    name: route.query.name || 'Group Chat',
})
const currentUser = ref({})
const ws = ref(null)

const goBack = () => {
    router.push({
        name: 'Home'
    })
}

// Format time
const formatTime = (timestamp) => {
    const date = new Date(timestamp)
    return date.toLocaleTimeString([], {hour: '2-digit', minute: '2-digit'})
}

// Get avatar text - first letter of username (uppercase)
const getAvatarText = (username) => {
    if (!username) return '?'
    // Get first character and convert to uppercase
    return username.charAt(0).toUpperCase()
}

// Generate consistent color for username
const getAvatarColor = (username) => {
    if (!username) return '#999'

    // Predefined color palette
    const colors = [
        '#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A',
        '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E2',
        '#F8B739', '#52B788', '#E76F51', '#2A9D8F'
    ]

    // Generate index based on username
    let hash = 0
    for (let i = 0; i < username.length; i++) {
        hash = username.charCodeAt(i) + ((hash << 5) - hash)
    }

    return colors[Math.abs(hash) % colors.length]
}

// send message and scroll to bottom auto
const scrollToBottom = () => {
    nextTick(() => {
        if (messagesContainer.value) {
            messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
        }
    })
}

// load messages from server
const loadMessages = async () => {
    const result = await chatStore.fetchMessages('group', route.query.id)
    if (result.success) {
        messages.value = result.data
        scrollToBottom()
    }
}

// WebSocket connection
const connectWebSocket = () => {
    console.log('Connecting to WebSocket...', route.query.id)

    ws.value = new WebSocket(`ws://127.0.0.1:8000/ws/chat/${route.query.id}/`)

    ws.value.onopen = () => {
        console.log('WebSocket connected')
    }

    ws.value.onmessage = (event) => {
        const data = JSON.parse(event.data)
        console.log('Received message:', data)

        // Extract message from the received data structure
        const message = {
            id: Date.now(),
            sender_id: data.sender_id || data.message?.sender_id,
            username: data.username || data.message?.username || 'Unknown',
            message: data.message?.message || data.message || '',
            timestamp: data.timestamp || data.message?.timestamp || Date.now()
        }

        messages.value.push(message)
        scrollToBottom()
    }

    ws.value.onclose = () => {
        console.log('WebSocket disconnected')
    }

    ws.value.onerror = (error) => {
        console.error('WebSocket error:', error)
        showFailToast('Connection error')
    }
}

// send message
const sendMessage = () => {
    if (!messageText.value.trim()) return

    // Create message data
    const messageData = {
        type: 'group',
        room_id: route.query.id,
        sender_id: currentUser.value.id,
        username: currentUser.value.username,
        message: messageText.value,
        timestamp: Date.now(),
    }

    // send message via WebSocket
    if (ws.value && ws.value.readyState === WebSocket.OPEN) {
        ws.value.send(JSON.stringify(messageData))
        messageText.value = ''
        scrollToBottom()
    } else {
        showFailToast('Failed to send message')
    }
}

// load messages and connect websocket
onMounted(async () => {
    currentUser.value = userStore.getUser
    // await loadMessages()
    connectWebSocket()
})

// unmount and close websocket
onUnmounted(() => {
    if (ws.value) {
        ws.value.close()
    }
})
</script>

<style scoped>
.group-chat-container {
    height: 100vh;
    display: flex;
    flex-direction: column;
    background-color: #f5f5f5;
}

.messages-container {
    flex: 1;
    overflow-y: auto;
    padding: 15px;
    padding-bottom: 20px;
}

.message-wrapper {
    display: flex;
    align-items: flex-start;
    margin-bottom: 20px;
    gap: 10px;
}

.message-wrapper.sent {
    flex-direction: row-reverse;
}

.message-wrapper.received {
    flex-direction: row;
}

.avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 16px;
    font-weight: bold;
    flex-shrink: 0;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.message-bubble {
    max-width: 65%;
    padding: 12px 15px;
    border-radius: 12px;
    position: relative;
}

.message-wrapper.sent .message-bubble {
    background-color: #1890ff;
    color: white;
    border-bottom-right-radius: 4px;
}

.message-wrapper.received .message-bubble {
    background-color: white;
    color: #333;
    border: 1px solid #e8e8e8;
    border-bottom-left-radius: 4px;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.sender-name {
    font-size: 12px;
    color: #1890ff;
    margin-bottom: 5px;
    font-weight: 500;
}

.message-wrapper.sent .sender-name {
    color: rgba(255, 255, 255, 0.9);
}

.message-text {
    word-wrap: break-word;
    line-height: 1.5;
    font-size: 14px;
}

.message-time {
    font-size: 10px;
    margin-top: 6px;
    text-align: right;
    opacity: 0.6;
}

.message-wrapper.sent .message-time {
    color: rgba(255, 255, 255, 0.8);
}

.message-wrapper.received .message-time {
    color: #999;
}

.input-container {
    padding: 10px;
    background-color: white;
    border-top: 1px solid #eee;
    box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.05);
}

.messages-container::-webkit-scrollbar {
    width: 6px;
}

.messages-container::-webkit-scrollbar-track {
    background: transparent;
}

.messages-container::-webkit-scrollbar-thumb {
    background: #d0d0d0;
    border-radius: 3px;
}

.messages-container::-webkit-scrollbar-thumb:hover {
    background: #b0b0b0;
}
</style>