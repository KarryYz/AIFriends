<script setup>

import {ref} from "vue";
import api from "@/js/http/api.js";
import {useUserStore} from "@/stores/user.js";
import router from "@/router/index.js";

const user = useUserStore()

const username = ref('')
const password = ref('')
const errorMessage = ref('')

async function handleLogin() {
  if (!username.value || !password.value) {
    errorMessage.value = '用户名或密码不能为空'
  }
  else {
    try {
      const res = await api.post("/api/user/account/login/", {
        username: username.value,
        password: password.value
      })
      const data = res.data
      if (data.result === 'success') {
        user.setAccessToken(data.access)
        user.setUserInfo(data)

        await router.push({
          name: 'homepage-index'
        })
      } else {
        errorMessage.value = data.result
      }
    }
    catch (error) {
    }
  }
}

</script>

<template>
  <div class="flex items-center justify-center mt-50">
    <form @submit.prevent="handleLogin"
          class="fieldset bg-base-200 border-base-300 rounded-box w-xs border p-4">
      <legend class="fieldset-legend">Login</legend>

      <label class="label">用户名</label>
      <input type="text" class="input" placeholder="用户名" v-model="username"/>

      <label class="label">密码</label>
      <input type="password" class="input" placeholder="密码" v-model="password"/>
      <button class="btn btn-neutral mt-4">
        登陆
      </button>

      <p v-if="errorMessage" class="text-base text-red-500"> {{ errorMessage }}</p>

      <div class="flex justify-end">
        <router-link :to="{name: 'user-account-register-index'}" class="btn btn-sm btn-ghost text-gray-600">
          注册
        </router-link>
      </div>
    </form>
  </div>
</template>

<style scoped>

</style>