<template>
  <div class="">
    <UserAuthentication @message-sent="handleMessageSent"/>
    <UserTable :message="message"/>


  </div>
</template>

<script>
import UserAuthentication from './components/UserAuthentication.vue';
import UserTable from './components/UserTable.vue';



export default {
  name: 'App',
  components: {
    UserAuthentication,
    UserTable,

  },
  data() {
    return {
      userDataObject: {},
      message: ''
    }
  },

  methods: {
    handleMessageSent(newMessage) {
      this.message = newMessage
      console.log("app")
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}



</style>
