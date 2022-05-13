<template>
	<q-card flat bordered class="page-card">
		<div class="alert-wrapper">
			<q-card-section>
				<InfoButton
					info="If you are happy with the alerts you can give positive feedback,
					if you thought an anomaly was not alert worthy you can give negative feedback.
					The system will use this feedback to predict if future anomalies are alert worthy.
					To give the feedback you can use the thumbs."
				/>
				<h1>Anomaly Overview and Feedback</h1>
				<q-table :rows="data" :columns="columns" row-key="timestamp" dense flat>
					<template v-slot:body-cell="props">
						<q-td
							:props="props"
							:class="
								props.row.feedback == null
									? 'bg-grey-3 text-black'
									: 'bg-white text-black'
							"
						>
							{{ props.value }}
						</q-td>
					</template>
					<template v-slot:body-cell-actions="props">
						<q-td :props="props">
							<q-btn
								dense
								round
								flat
								:color="getUpThumbColor(props.row)"
								@click="positiveFeedback(props.row)"
								icon="thumb_up"
							></q-btn>
							<q-btn
								dense
								round
								flat
								:color="getDownThumbColor(props.row)"
								@click="negativeFeedback(props.row)"
								icon="thumb_down"
							></q-btn>
						</q-td>
					</template>
				</q-table>
			</q-card-section>
		</div>
	</q-card>
</template>

<script>
import axios from "axios";
import InfoButton from "../components/InfoButton.vue";

export default {
	components: {
		InfoButton
	},
	data() {
		return {
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
					name: "detection_method",
					align: "left",
					label: "Detection Method",
					field: "detection_method",
					format: val => this.getDetectionType(val)
				},
				{
					name: "ip_adresses",
					align: "left",
					label: "IP Adresses",
					field: "ip_addresses",
					format: val => this.firstInList(val)
				},
				{
					name: "as_number",
					align: "left",
					label: "AS Number",
					field: "asn",
				},
				{
					name: "anomalie_score",
					align: "left",
					label: "Anomaly Score",
					field: "anomaly_score",
				},
				{
					name: "mean_value_increase",
					align: "left",
					label: "Value Increase",
					field: "mean_increase"
				},
				{
					name: "description",
					align: "left",
					label: "Alert Description",
					field: "description"
				},
				{
					name: "predicted",
					align: "left",
					label: "Predicion",
					format: val => this.format_prediction(val),
					field: "prediction_value"
				},
				{
					name: "actions",
					label: "Feedback",
					field: "",
					align: "center"
				}
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
				method: "put",
				url: `feedback/feedback?anomaly_id=${row.id}&user_feedback=true`,
			}).then(this.get_alerts());
		},
		negativeFeedback(row) {
			axios({
				method: "put",
				url: `feedback/feedback?anomaly_id=${row.id}&user_feedback=false`,
			}).then(this.get_alerts());
		},
		get_alerts() {
			axios({
				method: "get",
				url: "asn/anomaly"
			}).then(response => {
				this.data = response.data.items;
				// console.log(this.data)
			});
		},
		convertDate(input) {
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
		firstInList(list) {
			return list[0]
		},
		getDetectionType(detectionObject) {
			return detectionObject.type
		},
		format_prediction(input) {
			let format = "No Alert";
			if (input == true) {
				format = "Alert";
			}
			return format
		},
		getUpThumbColor(row) {
			if (row.feedback == 1) {
				return 'green'
			}
			else{
				return 'grey'
			}
		},
		getDownThumbColor(row) {
			if (row.feedback == 0) {
				return 'red'
			}
			else{
				return 'grey'
			}
		}
	}
};
</script>

<style scoped>
/* .alert-wrapper {
	max-width: 1024px;
	margin: 0 auto;
} */
</style>