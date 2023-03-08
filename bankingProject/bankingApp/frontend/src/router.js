import { createRouter, createWebHistory } from 'vue-router'


const routes = [

    { path: '/', name: "home", component: () => import('./components/home.vue') },
    { path: '/logout', name: "logout", component: () => import('./components/logout.vue') },

    // { path: '/test', name: "item", component: () => import('./components/AddItem.vue') },
]

const router = createRouter({
    routes,
    history: createWebHistory()

})

export default router