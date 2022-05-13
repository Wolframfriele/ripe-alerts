<template>
	<q-card-section>
		<q-table
			:rows="data"
			:columns="columns"
			row-key="timestamp"
			dense
			flat
			:rows-per-page-options="[5]"
			:pagination="pagination"
			hide-footer
			hide-page
		>
		</q-table>
	</q-card-section>
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
					field: row => row.timestamp,
					format: val => this.convertDate(val),
					sortable: true
				},
				{
					name: "description",
					align: "left",
					label: "Alert Description",
					field: "description"
				},
			],
			data: []
		};
	},
	created() {
		this.get_alerts();
	},
	methods: {
		get_alerts() {
			axios({
				method: "get",
				url: "asn/anomaly"
			}).then(response => {
				this.data = response.data.items;
				console.log(this.data)
			});
		},
		convertDate(input) {
			console.log(input)
			let date = new Date(input);
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
			return `${year}-${month}-${day}  |  ${hours}:${minutes}`;
		},
	}
};
</script>
<style scoped>
.card-title {
	margin-left: 0.5em;
}
</style>