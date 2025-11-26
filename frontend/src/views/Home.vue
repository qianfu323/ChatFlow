<template>
    <div class="group-list-container">
        <van-nav-bar title="Chats" fixed placeholder>
            <template #right>
                <van-icon name="add" size="24" @click="showAddRoom = !showAddRoom"/>
            </template>
        </van-nav-bar>

        <van-pull-refresh
            v-model="refreshing"
            loosing-text="Refresh"
            pulling-text="Refresh"
            loading-text="Refresh"
            @refresh="onRefresh"
        >
            <van-list
                v-model:loading="loading"
                :finished="finished"
                loading-text="loading"
                finished-text="No more groups"
                @load="onLoad"
            >
                <van-swipe-cell v-for="group in groups">
                    <van-cell
                        :key="group.id"
                        :title="group.name"
                        :label="`Last message: ${formatLastMessageTime(group.last_message_at)}`"
                        @click="goToGroupChat(group.id, group.name)"
                    >
                        <template #icon>
                            <van-icon
                                :name="group.is_private ? 'user' : 'friends'"
                                size="48" color="#1890ff"
                                style="margin-right: 10px;"
                            />
                        </template>
                    </van-cell>
                    <template #right>
                        <div class="btn-area">
                            <van-button square type="primary" text="Edit" @click="editRoom(group)"/>
                            <van-button square type="danger" text="Delete" @click="deleteGroup(group.id)"/>
                        </div>
                    </template>
                </van-swipe-cell>
            </van-list>
        </van-pull-refresh>

        <van-dialog v-model:show="showAddRoom" title="Create Chat Room" @confirm="createRoom"
                    @cancel="showAddRoom = false" show-cancel-button>
            <div>
                <van-field
                    v-model="addGroupName"
                    name="groupName"
                    placeholder="Group Name"
                    :rules="[{ required: true, message: 'Please enter a group name' }]"
                />
            </div>
        </van-dialog>

        <van-dialog v-model:show="showEditRoom" title="Edit Chat Room Name" @confirm="confirmEditRoom"
                    @cancel="showAddRoom = false" show-cancel-button>
            <div>
                <van-field
                    v-model="editGroup.name"
                    name="groupName"
                    placeholder="Group Name"
                    :rules="[{ required: true, message: 'Please enter a new group name' }]"
                />
            </div>
        </van-dialog>
    </div>
</template>

<script setup>
import {ref, onMounted} from 'vue'
import {useRouter} from 'vue-router'
import {useChatStore} from '@/stores/chat'
import {showConfirmDialog, showFailToast, showSuccessToast} from "vant";

const router = useRouter()
const chatStore = useChatStore()

const groups = ref([])
const loading = ref(false)
const finished = ref(false)
const refreshing = ref(false)
const showAddRoom = ref(false)
const addGroupName = ref('')
const editGroup = ref({})
const showEditRoom = ref(false)

// navigate to group chat
const goToGroupChat = (groupId,groupName) => {
    console.log('go to group chat', groupId)
    router.push({
        name: 'Chat',
        query: {
            id: groupId,
            name: groupName
        }
    })
}

// format timestamp to date
const formatLastMessageTime = (timestamp) => {
    if (!timestamp) return 'No messages yet';
    const date = new Date(timestamp);
    return date.toLocaleString();
}

const onLoad = async () => {
    if (refreshing.value) {
        groups.value = []
        refreshing.value = false
    }

    const result = await chatStore.fetchGroups()

    // print result to console
    console.log(result)

    if (result.success) {
        groups.value = result?.data
        finished.value = true
    }

    loading.value = false
}

const onRefresh = () => {
    finished.value = false
    onLoad()
}

// create room with a name
const createRoom = () => {
    chatStore.createGroup({
        name: addGroupName.value
    }).then((result) => {
        if (result.success) {
            showSuccessToast(result.message)
            showAddRoom.value = false
            onLoad()
        } else {
            showFailToast(result.message || 'Failed to create group')
        }
    })
}

// edit room name
const editRoom = (group) => {
    showEditRoom.value = true;
    editGroup.value = group;
}

const confirmEditRoom = () => {
    chatStore.editGroup(editGroup.value).then((result) => {
        if (result.success) {
            showSuccessToast(result.message)
            showEditRoom.value = false
            onLoad()
        } else {
            showFailToast(result.message || 'Failed to edit group')
        }
    })
}

// delete room with id
const deleteGroup = (groupId) => {
    showConfirmDialog({
        title: 'Delete Group ?',
    }).then(() => {
        chatStore.deleteGroup(groupId).then((result) => {
            if (result.success) {
                showSuccessToast(result.message)
                onLoad()
            } else {
                showFailToast(result.message || 'Failed to delete group')
            }
        })
    })
}

onMounted(() => {
    onLoad()
})
</script>

<style scoped>
.group-list-container {
    height: 100vh;
    background-color: #f5f5f5;
}

.btn-area {
    background-color: white;
    display: flex;
    flex-direction: row;
    height: 100%;
    align-items: center;
}
</style>