<script setup>

import {ref, watch} from "vue";

const props = defineProps(['profile'])
const myProfile = ref(props.profile)

defineExpose({
  myProfile
})

watch( () => props.profile, newValue => {
  myProfile.value = newValue
})

</script>

<template>
  <div class="fieldset">
    <div class="label text-base">个人简介</div>
    <input v-model="myProfile" type="text" class="input w-108" />
  </div>

</template>

<style scoped>

</style>