<template>
	<div id="q-app">
		<q-card flat bordered class="as-status-card">
			<q-card-section>
				<div class="text-h6">AS13245</div>
			</q-card-section>

			<q-card-section class="q-pt-none">
				Current status: Oke
			</q-card-section>

			<q-separator inset />

			<q-card-section>
				Latest results

				Hallo
			</q-card-section>
		</q-card>
	</div>
</template>

<script>

import axios from 'axios'
export default {
	setup() {
		
	},
	created () {
		this.get_asn()
	},
	methods: {
		get_asn() {
			axios ({
				method: 'get',
				url: 'http://localhost:8000/api/user/monitored-asns',
			}).then((response) => {
				if (response.data.lenght == 0) {

				}
			})
		}
	}
}
</script>
<style scoped>
	.as-status-card {
		width: 50%;
		margin: 2em;
	}
</style>