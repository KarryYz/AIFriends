import {defineStore} from "pinia";
import {ref} from "vue";

export const useUserStore = defineStore('userStore', (initialState) => {
    const id = ref(0)
    const username = ref('')
    const photo = ref('')
    const profile = ref('')
    const accessToken = ref('')
    const hasPulledUserInfo = ref(false)

    function isLogin() {
        return !!accessToken.value
    }

    function setAccessToken(token) {
        accessToken.value = token
    }

    function setUserInfo(userInfo) {
        id.value = userInfo.user_id
        username.value = userInfo.username
        photo.value = userInfo.photo
        profile.value = userInfo.profile
    }

    function logout () {
        id.value = 0
        username.value = ''
        photo.value = ''
        profile.value = ''
        accessToken.value = ''
    }

    function setHasPulledUserInfo(newStatus) {
        hasPulledUserInfo.value = newStatus
    }

    return {
        id,
        username,
        photo,
        profile,
        accessToken,
        isLogin,
        setAccessToken,
        setUserInfo,
        logout,
        hasPulledUserInfo,
        setHasPulledUserInfo
    }
})