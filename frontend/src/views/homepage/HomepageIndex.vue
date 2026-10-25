<script setup>

import UserInfoField from "@/views/user/space/components/UserInfoField.vue";
import Character from "@/components/character/Character.vue";
import {useRoute} from "vue-router";
import {nextTick, onBeforeUnmount, onMounted, ref, useTemplateRef, watch} from "vue";
import api from "@/js/http/api.js";

const route = useRoute()
const characters = ref([])
const sentinelRef = useTemplateRef('sentinel-ref')
const userProfile = ref(null)
const isLoading = ref(false)
const hasCharacters = ref(true)

function checkSentinelVisible() {  // 判断哨兵是否能被看到
  if (!sentinelRef.value) return false

  const rect = sentinelRef.value.getBoundingClientRect()
  return rect.top < window.innerHeight && rect.bottom > 0
}

async function loadMore () {
  if (isLoading.value || !hasCharacters.value) return
  isLoading.value = true

  let newCharacter = []

  try {
    const res = await api.get ('api/homepage/index/', {
      params: {
        'items_count': characters.value.length,
        'search_query': route.query.q || '',
      }
    })
    const data = res.data
    if (data.result === 'success') {
      newCharacter = data.characters
    }
  } catch(e) {
  } finally {
    isLoading.value = false

    if (newCharacter.length === 0) {
      hasCharacters.value = false
    } else {
      characters.value.push (... newCharacter)
      await nextTick()

      if (checkSentinelVisible()) {
        await loadMore()
      }
    }
  }
}

let observer = null
onMounted(async () => {
  await loadMore()  // 加载新元素

  observer = new IntersectionObserver(
    entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          loadMore()
        }
      })
    },
    {root: null, rootMargin: '2px', threshold: 0}
  )

  //监听哨兵元素， 每次哨兵被看到时，都会触发一次
  observer.observe(sentinelRef.value)
})

onBeforeUnmount(() => {
  observer?.disconnect()  // 解绑监听器
})

function reset() {
  characters.value = []
  isLoading.value = false
  hasCharacters.value = true
  loadMore()
}

watch(() => route.query.q, newQ => {
  reset()
})


</script>

<template>
  <div class="flex flex-col items-center mb-12">
    <div class="grid grid-cols-[repeat(auto-fill,minmax(240px,1fr))] gap-9 mt-12 justify-items-center w-full px-9">
      <Character
        v-for="character in characters"
        :key="character.id"
        :character="character"
      />
    </div>
    <div ref="sentinel-ref" class="h-2 mt-8 " ></div>
    <div v-if="isLoading" class="text-gray-500 mt-4">加载中...</div>
    <div v-else-if="! hasCharacters" class="text-gray-500 mt-4">没有更多角色了</div>
  </div>
</template>

<style scoped>

</style>