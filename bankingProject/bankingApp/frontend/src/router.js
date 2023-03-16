import { createRouter, createWebHistory } from 'vue-router'


const routes = [

    { path: '/', name: "home", component: () => import('./components/home.vue') },
    { path: '/logout', name: "logout", component: () => import('./components/logout.vue') },
    { path: '/savings', name: "savings", component: () => import('./components/saving.vue') },
    { path: '/transaction-history', name: "history", component: () => import('./components/history.vue') },
    // { path: '/test', name: "item", component: () => import('./components/AddItem.vue') },
]

const router = createRouter({
    routes,
    history: createWebHistory()

})

export default router