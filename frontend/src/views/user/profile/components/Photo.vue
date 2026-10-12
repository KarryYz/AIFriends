<script setup>
import {ref, watch} from "vue";

const props = defineProps(['photo'])
const myPhoto = ref(props.photo)

defineExpose({
  myPhoto
})

watch (() => props.photo, newValue => {
  myPhoto.value = newValue
})

</script>

<template>

</template>

<style scoped>

</style>