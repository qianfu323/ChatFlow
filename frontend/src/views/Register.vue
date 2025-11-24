<template>
    <div class="register-container">
        <div class="register-card">
            <h1 class="register-title">Register</h1>
            <van-form @submit="onSubmit">
                <van-cell-group inset>
                    <van-field
                        v-model="username"
                        name="username"
                        label="Username"
                        placeholder="Username"
                        :rules="[{ required: true, message: 'Please enter your username' }]"
                    />
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
                    <van-field
                        v-model="passwordConfirm"
                        type="password"
                        name="password_confirm"
                        label="Confirm Password"
                        placeholder="Confirm Password"
                        :rules="[{ required: true, message: 'Please confirm your password' }]"
                    />
                </van-cell-group>
                <div style="margin: 16px;">
                    <van-button round block type="primary" native-type="submit">
                        Register
                    </van-button>
                </div>
            </van-form>
            <div class="login-link">
                <span>Already have an account? </span>
                <router-link to="/login">Login</router-link>
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
    name: 'Register',
    setup() {
        const router = useRouter()
        const userStore = useUserStore()

        const username = ref('')
        const email = ref('')
        const password = ref('')
        const passwordConfirm = ref('')

        const onSubmit = async (values) => {
            if (values.password !== values.password_confirm) {
                showFailToast('Passwords do not match')
                return
            }

            const result = await userStore.register({
                username: values.username,
                email: values.email,
                password: values.password,
                password_confirm: values.password_confirm
            })

            if (result.success) {
                showSuccessToast('Registration successful')
                router.push('/login')
            } else {
                const errorMsg = Object.values(result.error).flat().join(', ') || 'Registration failed'
                showFailToast(errorMsg)
            }
        }

        return {
            username,
            email,
            password,
            passwordConfirm,
            onSubmit
        }
    }
}
</script>

<style scoped>
.register-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background-color: #e6f7ff;
}

.register-card {
    width: 90%;
    max-width: 400px;
    padding: 20px;
    background: white;
    border-radius: 10px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.register-title {
    text-align: center;
    margin-bottom: 20px;
    color: #1890ff;
}

.login-link {
    text-align: center;
    margin-top: 20px;
}
</style>