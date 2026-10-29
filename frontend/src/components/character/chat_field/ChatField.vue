<script setup>

import {computed, nextTick, ref, useTemplateRef} from "vue";
import CharacterPhotoField from "@/components/character/chat_field/character_photo_field/CharacterPhotoField.vue";
import InputField from "@/components/character/chat_field/input_field/InputField.vue";
import ChatHistory from "@/components/character/chat_field/chat_history/ChatHistory.vue";

const props = defineProps(['friend'])
const modalRef = useTemplateRef('modal-ref')
const inputRef = useTemplateRef('input-ref')

async function showModal() {
  modalRef.value.showModal()

  await nextTick()
  inputRef.value.focus()
}

const modalStyle = computed(() => {
  if (props.friend) {
    return {
      backgroundImage: `url(${props.friend.character.background_image})`,
      backgroundSize: 'cover',
      backgroundPosition: 'center',
      backgroundRepeat: 'no-repeat',
    }
  } else {
    return {}
  }
})

defineExpose({
  showModal,
})
const chatHistoryRef = useTemplateRef('chat-history-ref')
const history = ref([])//母组件定义，然后传递给子组件input_field，chat_filed，子组件不要直接修改母组件变量，但母组件可以定义一些函数，让子组件调用来修改

//两条history操作
function handlePushBackMessage(msg){
  history.value.push(msg) //回车后增加一条消息
  chatHistoryRef.value.scrollToBottom()
}

function handleAddToLastMessage(delta){
  history.value.at(-1).content += delta//在最后一条消息上增添内容
  chatHistoryRef.value.scrollToBottom()
}

function handlePushFrontMessage(msg){
  history.value.unshift(msg)
}

</script>

<template>
  <dialog ref="modal-ref"
          class="modal"
          @cancel="modalRef.close()"
          @click="(e) => { if (e.target === modalRef) modalRef.close() }"
  >
    <div class="modal-box w-90 h-150" :style="modalStyle">
      <button @click="modalRef.close()" class="btn btn-sm btn-circle btn-ghost bg-transparent absolute right-1 top-1">✕</button>

      <ChatHistory
        v-if="friend"
        ref="chat-history-ref"
        :friendId="friend.id"
        :history="history"
        :character="friend.character"
        @pushFrontMessage="handlePushFrontMessage"
      />

      <InputField
          ref="input-ref"
          v-if="friend"
          :friendId="friend.id"
          @pushBackMessage="handlePushBackMessage"
          @addToLastMessage="handleAddToLastMessage"
      />
      <CharacterPhotoField v-if="friend" :character="friend.character" />
    </div>
  </dialog>
</template>

<style scoped>

</style>