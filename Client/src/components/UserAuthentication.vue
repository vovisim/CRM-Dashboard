<template>
  <form @submit.prevent="submitForm" class="login-form">
    <h3>Войти</h3>
    <input type="text" v-model="Login.login" placeholder="Логин" required>
    <input type="password" v-model="Login.password" placeholder="Пароль" required>
    <button type="submit">Вход</button>
    <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
  </form>
</template>


<script>
import { getPassword } from "../../api/api";
import {useStore} from "vuex";


export default {
  name: "UserAuthentication",
  data() {
    return {
      Login: {
        login: "",
        password: "",
      },
      errorMessage: "",
      Fullname: ""
    }
  },
  setup(){
    const store = useStore();
    return { store };
  },
  methods: {
    async submitForm() {
      try {
        const response = await getPassword("users", 0);
        const userList = Object.values(response);
        const user = userList.find(user => user.Login === this.Login.login);
        if (user) {
          if (user.Password === this.Login.password) {
            this.errorMessage = "Успешный вход!";
            this.$emit('rerender-table');
            this.$emit("message-sent" , user.Fullname);
            await this.store.dispatch('login', user);
          } else {
            // Пароль не совпадает
            this.errorMessage = "Неправильный пароль!";
          }
        } else {
          // Логин не найден
          this.errorMessage = "Пользователь не найден!";
        }
      } catch (error) {
        console.error("Error during authentication:", error);
        this.errorMessage = "Ошибка при выполнении входа!";
      }
    },

  }
}
</script>

<!--<style scoped>-->
<!--  form{-->
<!--    display: flex;-->
<!--    align-items: center;-->
<!--    justify-content: center;-->
<!--    flex-direction: column;-->

<!--  }-->
<!--  *{-->
<!--    margin-bottom: 5px;-->
<!--  }-->
<!--</style>-->

<style scoped>
.login-form {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  background-color: #f9f9f9;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
  margin: 2rem auto;
}

.login-form h3 {
  margin-bottom: 1rem;
  color: #333;
  font-size: 1.5rem;
}

.login-form input {
  width: 100%;
  padding: 0.75rem;
  margin-bottom: 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.login-form button {
  width: 100%;
  padding: 0.75rem;
  background-color: #007bff;
  border: none;
  border-radius: 4px;
  color: #fff;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.login-form button:hover {
  background-color: #0056b3;
}

.error-message {
  color: red;
  margin-top: 1rem;
}
button{
  width: 425px !important;
}
</style>
