import { createRouter, createWebHashHistory } from "vue-router";
import Home from "../views/home.vue";
import Setup from "../views/setup.vue";

const routes = [
	{ path: "/", name: "home", component: Home },
	{ path: "/setup", name: "setup", component: Setup },
	{ path: "/manage-alerts", name: "managealerts", component: () => import(/* webpackChunkName: "manage-alerts" */ '../views/manage_alerts.vue') },
];

const router = createRouter({
	history: createWebHashHistory(),
	routes,
});

export default router;
