<script setup>

import {useUserStore} from "@/stores/user.js";
import UserProfileIcon from "@/components/navbar/icons/UserProfileIcon.vue";
import UserSpaceIcon from "@/components/navbar/icons/UserSpaceIcon.vue";
import UserLogoutIcon from "@/components/navbar/icons/UserLogoutIcon.vue";
import {useRouter} from "vue-router";
import api from "@/js/http/api.js";

const user = useUserStore()
const router = useRouter()

function closeMenu() {
  const element = document.activeElement
  if (element && element instanceof HTMLElement) element.blur()
}

async function handleLogout() {
  try {
    const res = await api.post("/api/user/account/logout/")
    const data = res.data
    if (data.result === 'success') {
      user.logout()
      await router.push ({
        name: 'homepage-index'
      })
    }
  } catch (err) {

  }
}

</script>

<template>

  <div class="dropdown dropdown-end">
    <div tabindex="0" role="button" class="avatar btn btn-circle w-10 h-10 mr-6">
      <div class="rounded-full w-10">
        <img :src="user.photo"/>
      </div>
    </div>
    <ul tabindex="2" class="dropdown-content menu bg-base-100 rounded-box z-1 w-48 p-2 shadow-lg mt-4">
      <li>
        <RouterLink @click="closeMenu" :to="{name: 'user-space-index', params: {user_id: user.id}}">
          <div class="avatar">
            <div class="rounded-full w-12">
              <img :src="user.photo"/>
            </div>
          </div>
          <span class="text-base ml-1 font-bold line-clamp-1 break-all"> {{ user.username }} </span>
        </RouterLink>
      </li>
      <li>
        <RouterLink @click="closeMenu" :to="{name: 'user-space-index', params: {user_id: user.id}}"
                    class="text-base ml-2 font-bold py-3"
        >
          <UserSpaceIcon/>
          个人空间
        </RouterLink>
      </li>
      <li>
        <RouterLink @click="closeMenu" :to="{name: 'user-profile-index'}"
                    class="text-base ml-2 font-bold py-3"
        >
          <UserProfileIcon/>
          编辑资料
        </RouterLink>
      </li>
      <li></li>
      <li>
        <a @click="handleLogout" class="text-base ml-2 font-bold py-3">
          <user-logout-icon/>
          退出登录
        </a>
      </li>
    </ul>
  </div>
</template>

<style scoped>

</style>