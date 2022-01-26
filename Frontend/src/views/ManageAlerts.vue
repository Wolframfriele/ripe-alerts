<template>
	<div id="q-app">
		<div class="q-pa-md">
			<div class="row q-col-gutter-sm">
				<div class="col">
					<q-table
						title="Alerts Overview and Feedback"
						:rows="data"
						:columns="columns"
						row-key="timestamp"
						dense
					>
                        <template v-slot:body-cell="props">
                            <q-td
                            :props="props"
                            :class="(props.row.label==1)?'bg-green text-white':'bg-white text-black'"
                            >
                            {{props.value}}
                            </q-td>
                        </template>
						<template v-slot:body-cell-actions="props">
							<q-td :props="props">
								<q-btn
									dense
									round
									flat
									color="green"
									@click="positiveFeedback(props.row)"
									icon="thumb_up"
								></q-btn>
								<q-btn
									dense
									round
									flat
									color="red"
									@click="negativeFeedback(props.row)"
									icon="thumb_down"
								></q-btn>
							</q-td>
						</template>
					</q-table>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import axios from "axios";
export default {
	data() {
		return {
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
				},
				{ name: "actions", label: "Feedback", field: "", align: "center" }
			],
			data: [],
			noti: () => {},
			editedIndex: -1,
			pagination: {
				page: 1
			},
			page: 1,
			totalRecord: 0,
			pageCount: 1
		};
	},
	created() {
		this.get_alerts();
	},
	methods: {
		positiveFeedback(row) {
            axios({
                method: "post",
                url: "alerts/label_alert",
                data: {
                    anomaly_id: row.anomaly_id,
                    label: true
                }
            }).then(row.label = true)
		},
		negativeFeedback(row) {
            axios({
                method: "post",
                url: "alerts/label_alert",
                data: {
                    anomaly_id: row.anomaly_id,
                    label: false
                }
            }).then(row.label = false)
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
			return `${year}-${month}-${day}  |  ${hours}:${minutes}`;
		}
	}
};
</script>

<style scoped>
.q-pa-md {
	margin: 1em;
}
</style>