<script setup>
import {useRoute} from "vue-router";
import UserInfoField from "@/views/user/space/components/UserInfoField.vue";
import {nextTick, onBeforeUnmount, onMounted, ref, useTemplateRef} from "vue";
import Character from "@/components/character/Character.vue";
import api from "@/js/http/api.js";

const characters = ref([])
const userProfile = ref(null)
const isLoading = ref(false)
const hasCharacter = ref(true)
const sentinelRef = useTemplateRef('sentinel-ref')
const route = useRoute()

function checkSentinelVisible() {  // 判断哨兵是否能被看到
  if (!sentinelRef.value) return false

  const rect = sentinelRef.value.getBoundingClientRect()
  return rect.top < window.innerHeight && rect.bottom > 0
}

async function loadMore() {
  if (isLoading.value || !hasCharacter.value) return
  isLoading.value = true

  let newCharacter = []
  try {
    const res = await api.get('api/create/character/get_list/', {
      params: {
        items_count: characters.value.length,
        user_id: route.params.user_id,
      }
    })
    const data = res.data
    if (data.result === 'success') {
      userProfile.value = data.user_profile
      newCharacter = data.characters
    }
  } catch (e) {
  } finally {
    isLoading.value = false
    if (newCharacter.length === 0) {
      hasCharacter.value = false
    } else {
      characters.value.push (...newCharacter)
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

function removeCharacter(characterId) {
  characters.value = characters.value.filter(c => c.id !== characterId)
}


onBeforeUnmount(() => {
  observer?.disconnect()  // 解绑监听器
})

</script>

<template>
  <div class="flex flex-col items-center mb-12">
    <UserInfoField :userProfile="userProfile" />
    <div class="grid grid-cols-[repeat(auto-fill,minmax(240px,1fr))] gap-9 mt-12 justify-items-center w-full px-9">
      <Character
        v-for="character in characters"
        :key="character.id"
        :character="character"
        :canEdit="true"
        @remove="removeCharacter"
      />
    </div>
    <div ref="sentinel-ref" class="h-2 mt-8 " ></div>
    <div v-if="isLoading" class="text-gray-500 mt-4">加载中...</div>
    <div v-else-if="! hasCharacter" class="text-gray-500 mt-4">没有更多角色了</div>
  </div>
</template>

<style scoped>

</style>