<template>
	<q-card
		flat
		bordered
		class="page-card"
		v-for="as_num in ASNList"
		:key="as_num"
	>
<<<<<<< HEAD
		<div class="wrapper">
=======
		<q-card class="col-5">
>>>>>>> main
			<q-card-section>
				<h1 class="card-title">AS{{ as_num }}</h1>
				<q-table
					title="Latest Alerts"
					:rows="data"
					:columns="columns"
					row-key="timestamp"
					dense
					flat
					:rows-per-page-options="[0]"
					:pagination="pagination"
					hide-header
					hide-bottom
				>
				</q-table>
			</q-card-section>
		</div>
	</q-card>
</template>

<script>
import axios from "axios";
export default {
	data() {
		return {
			pagination: {
				page: 1,
				rowsPerPage: 0 // 0 means all rows
			},
			ASNList: [],
			columns: [
				{
					name: "timestamp",
					required: true,
					label: "Timestamp",
					align: "left",
					field: row => row.datetime,
					format: val => this.convertDate(val),
					sortable: true
				},
				{
					name: "description",
					align: "left",
					label: "Alert Description",
					field: "description"
				}
			],
			data: []
		};
	},
	created() {
		this.get_asn();
		this.get_alerts();
	},
	methods: {
		get_asn() {
			axios({
				method: "get",
				url: "user/monitored-asns"
			}).then(response => {
				if (response.data.lenght == 0) {
					this.$router.push({ name: "setup" });
				} else {
					this.ASNList = response.data;
				}
			});
		},
		get_alerts() {
			axios({
				method: "get",
				url: "alerts/get_alerts"
			}).then(response => {
				this.data = response.data;
			});
		},
		convertDate(input) {
			let date = new Date(input * 1000);
			let year = date.getFullYear();
			let month = (date.getMonth() + 1).toString().padStart(2, "0");
			let day = date
				.getDate()
				.toString()
				.padStart(2, "0");
			let hours = date
				.getHours()
				.toString()
				.padStart(2, "0");
			let minutes = date
				.getMinutes()
				.toString()
				.padStart(2, "0");
			return `${hours}:${minutes} | ${year}-${month}-${day}`;
		}
	}
};
</script>
<style scoped>
.card-title {
	margin-left: 0.5em;
}
</style>