
import { createStore } from 'vuex';

const store = createStore({
    state: {
        isAuthenticated: false,
        user: null
    },
    mutations: {
        setAuthenticated(state, payload) {
            state.isAuthenticated = payload.isAuthenticated;
            state.user = payload.user;
        }
    },
    actions: {
        login({ commit }, user) {
            commit('setAuthenticated', { isAuthenticated: true, user });
        },
        logout({ commit }) {
            commit('setAuthenticated', { isAuthenticated: false, user: null });
        }
    },
    getters: {
        isAuthenticated: state => state.isAuthenticated,
        user: state => state.user
    }
});

export default store;
