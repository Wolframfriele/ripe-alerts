import { createRouter, createWebHashHistory } from "vue-router";
import Home from "../views/Home.vue";
import Setup from "../views/Setup.vue";
import ManageAlerts from "../views/ManageAlerts.vue";
import Documentation from "../views/Documentation.vue";



const routes = [
	{ path: "/", name: "home", component: Home },
	{ path: "/setup", name: "setup", component: Setup },
	{ path: "/manage-alerts", name: "managealerts", component: ManageAlerts },
	{ path: "/documentation", name: "documentation", component: Documentation  },
];

const router = createRouter({
	history: createWebHashHistory(),
	routes,
});

export default router;
