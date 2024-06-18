import axios from 'axios';

const apiUrl = 'http://127.0.0.1:2266/api/';

// Функция для получения всех паролей
async function postPassword(data, db_name, userId) {
    try {

        const response = await axios.post(apiUrl + db_name + "/" + userId, data);
        console.log('Успешно отправлено:', response.data);

        // Обработка успешного ответа
    } catch (error) {
        console.error('Ошибка при отправке данных:', error);

        // Обработка ошибки
    }
}

async function getPassword(db_name, index, fullname = null) {
    try {
        let url = `${apiUrl}${db_name}/${index}`;
        if (fullname) {
            url += `/${fullname}`;
        }
        const response = await axios.get(url);
        return response.data;
    } catch (error) {
        console.error('Ошибка при получении данных:', error);
        throw error; // добавлено для обработки ошибок в вызывающем коде
    }
}



async function deletePassword(db_name, index){
    try {
        await console.log(index)
        const response = await axios.delete(apiUrl + db_name + "/" + index.toString());
        console.log('Пароль успешно удален:', response.data);
    } catch (error) {
        console.error('Ошибка при получении удалении:', error);
    }
}

async function putPassword(client_id, data, isStatus="False"){
    // eslint-disable-next-line no-useless-catch
    try {
        const response = await axios.put(`${apiUrl}clients/${client_id}/${isStatus}`, data);
        return response.data;
    } catch (error) {
        throw error;
    }
}

export { postPassword, getPassword, deletePassword, putPassword};
