<script setup>

import {ref} from "vue";
import {useUserStore} from "@/stores/user.js";
import api from "@/js/http/api.js";
import router from "@/router/index.js";
const username = ref('')
const password = ref('')
const confirm_password = ref('')
const errorMessage = ref('')

const user = useUserStore()

async function handleRegister() {
  if (!username.value || !password.value || !confirm_password.value) {
    errorMessage.value = '用户名或密码不能为空'
  } else {
    try {
      const res = await api.post('/api/user/account/register/', {
        username: username.value,
        password: password.value,
        confirm_password: confirm_password.value
      })
      const data = res.data

      if (data.result === 'success') {
        user.setAccessToken(data.access)
        user.setUserInfo(data)

        await router.push ({
          name: 'homepage-index'
        })
      } else {
        errorMessage.value = data.result
      }

    } catch(error) {

    }
  }
}


</script>

<template>
  <div class="flex items-center justify-center mt-50">
    <form @submit.prevent="handleRegister"
          class="fieldset bg-base-200 border-base-300 rounded-box w-xs border p-4">
      <legend class="fieldset-legend">Register</legend>

      <label class="label">用户名</label>
      <input v-model="username" type="text" class="input" placeholder="用户名" />

      <label class="label">密码</label>
      <input v-model="password" type="password" class="input" placeholder="密码" />

      <label class="label">确认密码</label>
      <input v-model="confirm_password" type="password" class="input" placeholder="确认密码" />

      <p v-if="errorMessage" class="text-base text-red-500"> {{ errorMessage }}</p>

      <button class="btn btn-neutral mt-4">注册</button>
      <div class="flex justify-end">
        <router-link :to="{name: 'user-account-login-index'}" class="btn btn-sm btn-ghost text-gray-600">
          登陆
        </router-link>
      </div>
    </form>
  </div>
</template>

<style scoped>

</style>