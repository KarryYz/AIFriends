<script setup>

import {ref, watch} from "vue";

const props = defineProps(['name'])
const myName = ref(props.name)

watch(() => props.name, newValue => {
  myName.value = newValue
})

defineExpose({
  myName,
})

</script>

<template>
  <fieldset class="fieldset">
    <label class="label text-base">
      名字
    </label>
    <input type="text" v-model="myName" class="input w-108">
  </fieldset>
</template>

<style scoped>

</style>