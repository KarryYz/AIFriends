<script setup>

import {useUserStore} from "@/stores/user.js";
import Photo from "@/views/user/profile/components/Photo.vue";
import Username from "@/views/user/profile/components/Username.vue";
import Profile from "@/views/user/profile/components/Profile.vue";

const user = useUserStore()

</script>

<template>
  <div class="flex justify-center">
    <div class="card bg-base-200 w-120 shadow-sm mt-16">
      <div class="card-body">
        <h2 class="card-title">编辑资料</h2>

        <Photo :photo="user.photo" />
        <Username :username="user.username"/>
        <Profile :profile="user.profile"/>

        <div class="flex justify-center">
          <button class="btn btn-neutral w-60 mt-2">更新</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>