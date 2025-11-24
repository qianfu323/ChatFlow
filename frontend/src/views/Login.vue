<template>
    <div class="login-container">
        <div class="login-card">
            <h1 class="login-title">Login</h1>
            <van-form @submit="onSubmit">
                <van-cell-group inset>
                    <van-field
                        v-model="email"
                        name="email"
                        label="Email"
                        placeholder="Email"
                        :rules="[{ required: true, message: 'Please enter your email' }]"
                    />
                    <van-field
                        v-model="password"
                        type="password"
                        name="password"
                        label="Password"
                        placeholder="Password"
                        :rules="[{ required: true, message: 'Please enter your password' }]"
                    />
                </van-cell-group>
                <div style="margin: 16px;">
                    <van-button round block type="primary" native-type="submit">
                        Login
                    </van-button>
                </div>
            </van-form>
            <div class="register-link">
                <span>Don't have an account? </span>
                <router-link to="/register">Register</router-link>
            </div>
        </div>
    </div>
</template>

<script>
import {ref} from 'vue'
import {useRouter} from 'vue-router'
import {useUserStore} from '@/stores/user'
import {showFailToast, showSuccessToast} from 'vant'

export default {
    name: 'Login',
    setup() {
        const router = useRouter()
        const userStore = useUserStore()

        const email = ref('')
        const password = ref('')

        const onSubmit = async (values) => {
            const result = await userStore.login({
                email: values.email,
                password: values.password
            })

            if (result.success) {
                showSuccessToast('Login successful')
                router.push('/')
            } else {
                showFailToast(result.error.error || 'Login failed')
            }
        }

        return {
            email,
            password,
            onSubmit
        }
    }
}
</script>

<style scoped>
.login-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background-color: #e6f7ff;
}

.login-card {
    width: 90%;
    max-width: 400px;
    padding: 20px;
    background: white;
    border-radius: 10px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.login-title {
    text-align: center;
    margin-bottom: 20px;
    color: #1890ff;
}

.register-link {
    text-align: center;
    margin-top: 20px;
}
</style>