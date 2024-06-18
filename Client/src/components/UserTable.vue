<template>
  <div class="table-container">
    <table class="user-table"  v-if="userDataArray.length > 1">
      <thead>
      <tr>
        <th>Индекс</th>
        <th>AccountNumber</th>
        <th>Surname</th>
        <th>Name</th>
        <th>Patronymic</th>
        <th>Birthday</th>
        <th>TIN</th>
        <th>FullNameResponsible</th>
        <th>Status</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="(userData, index) in userDataArray" :key="index">
        <td>{{ index }}</td>
        <td>{{ userData.AccountNumber }}</td>
        <td>{{ userData.Surname }}</td>
        <td>{{ userData.Name }}</td>
        <td>{{ userData.Patronymic }}</td>
        <td>{{ userData.Birthday }}</td>
        <td>{{ userData.TIN }}</td>
        <td>{{ userData.FullNameResponsible }}</td>
        <td class="status">
          <select v-model="userData.Status" @change="updateStatus(userData)">
            <option value="В работе">В работе</option>
            <option value="Отказ">Отказ</option>
            <option value="Сделка закрыта">Сделка закрыта</option>
          </select>
        </td>
      </tr>
      </tbody>
    </table>
  </div>
</template>


<script>
import { getPassword, putPassword } from "../../api/api"; // Добавьте функцию обновления статуса в ваш API

export default {
  name: 'UserTable',
  data() {
    return {
      userDataArray: []
    }
  },
  unmounted() {
    this.$root.$off('rerender-table', this.fetchClients);
  },
  props: {
    message: String,
  },
  watch: {
    message(newMessage) {
      console.log("watch")
      if (newMessage) {
        console.log("newmessage")
        this.fetchClients(this.message);
      }
    }
  },
  mounted() {
    this.$root.$on('rerender-table', this.fetchClients);
    if (this.message) {
      this.fetchClients(this.message);
    }
  },
  methods: {
    async fetchClients(fullname) {
      try {
        const response = await getPassword('clients', 0, fullname);

        if (response) {
          this.userDataArray = Object.values(response);
        }
      } catch (error) {
        console.error('Error fetching clients:', error);
      }
    },
    async updateStatus(userData) {

      try {
        await putPassword(userData.id, {Status: userData.Status}, "True");
      } catch (error) {
        console.error('Error updating status:', error);
      }
    }
  }
};
</script>

<style scoped>
.table-container {
  display: flex;
  justify-content: center;
  padding: 2rem;
}

.user-table {
  width: 100%;
  max-width: 1200px;
  border-collapse: collapse;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

th, td {
  padding: 1rem;
  border: 1px solid #ddd;
  text-align: left;
}

th {
  background-color: #f2f2f2;
  font-weight: bold;
}

tr:nth-child(even) {
  background-color: #f9f9f9;
}

tr:hover {
  background-color: #f5f5f5;
}

.status select {
  padding: 0.5rem;
  border-radius: 4px;
  border: 1px solid #ddd;
  background-color: #fff;
  width: 100%;
}

.status {
  position: relative;
  width: 150px;
}

select {
  width: calc(100% - 1rem);
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: #fff;
  appearance: none; /* Убирает стрелку по умолчанию */
}

select:focus {
  outline: none;
  border-color: #007bff;
}

.table-container {
  width: 100%;
  overflow-x: auto;
}

.table-container::-webkit-scrollbar {
  height: 8px;
}

.table-container::-webkit-scrollbar-thumb {
  background-color: #ccc;
  border-radius: 4px;
}

.table-container::-webkit-scrollbar-track {
  background-color: #f9f9f9;
}
</style>

