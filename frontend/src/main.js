import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import { Quasar } from "quasar";
import quasarUserOptions from "./quasar-user-options";
import VueApexCharts from "vue3-apexcharts";
import axios from 'axios'

axios.defaults.baseURL = "http://localhost:8000/api/"

createApp(App)
	.use(Quasar, quasarUserOptions)
	.use(router)
	.use(VueApexCharts)
	.mount("#app");
