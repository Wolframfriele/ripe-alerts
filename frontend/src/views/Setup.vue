<template>
	<q-card flat bordered class="page-card">
		<div class="wrapper">
			<q-card-section>
				<h1>Adjust Monitoring settings</h1>
				<InfoButton
					info="The AS number (Autonomous System number),
					is the starting point for anomaly detection.
					This is used to find Anchors that are located in your AS.
					For each Anchor the system finds the relevant measurements
					and sends those to the anomaly detection."
				/>
				<h2>AS Numbers</h2>
				<p>Set the AS number that you want to monitor.</p>
				<q-input
					ref="ASNField"
					v-model="asNumber"
					filled
					prefix="AS"
					min="0"
					max="4294967295"
					error-message="Must be a number between 0 and 4294967295"
					:rules="[isValidASN]"
					lazy-rules
				>
				</q-input>
				
				<q-banner v-if="isMonitorable" class="bg-green-3">
					<p v-if="hostname">
						The monitoring process is running. AS belongs to: <strong> {{ hostname }} </strong>.
					</p>
					<p v-else>
						The monitoring process is running.
					</p>
					
				</q-banner>

				<q-banner v-if="errorMessage" class="bg-red">
					{{ errorMessage }}
				</q-banner>

				<q-btn color="primary" label="Save" @click="submit()">
					<q-popup-proxy v-if="alert">
						<q-banner>
							All fields need to be filled before submitting.
						</q-banner>
					</q-popup-proxy>
				</q-btn>
			</q-card-section>

			<!-- <q-separator inset />

			<q-card-section>
				<InfoButton
					info="Email will be used as the place where alerts will be sent."
				/>
				<h2>Email</h2>
				<p>Change the email where you want to receive alerts.</p>
				<q-input
					ref="emailField"
					v-model="email"
					filled
					type="email"
					label="Email"
					@keyup.enter="addEmail()"
					:rules="[
						val => !!val || 'Email is missing',
						isValidEmail || 'Email is not valid'
					]"
					lazy-rules
				>
				</q-input>
				<q-btn color="primary" label="Save" @click="submit()">
					<q-popup-proxy v-if="alert">
						<q-banner>
							All fields need to be filled before submitting.
						</q-banner>
					</q-popup-proxy>
				</q-btn>
			</q-card-section> -->
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
			asHasBeenSetup: false,
			asNumber: "",
			alert: true,
			message: "",
			errorMessage: "",
			hostname: "",
			isMonitorable: false
		};
	},
	created() {
		this.get_asn();
	},
	methods: {
		get_asn() {
			axios({
				method: "get",
				url: "settings"
			}).catch((error) => {
				if (error) {
					console.log(error);
          this.asNumber = ""
          this.isMonitorable = false
          this.hostname = ""
          this.asHasBeenSetup = false
				}
			}).then(response => {
        console.log(response)
				if (response.data.monitoring_possible) {
					this.asHasBeenSetup = true;
					this.asNumber = response.data.autonomous_system.slice(3);
					this.isMonitorable  = response.data.monitoring_possible
					this.hostname = response.data.host
				}
			});
		},
		isValidASN(val) {
			const ASNPattern = /^[0-9]{1,6}$/;
			return ASNPattern.test(val);
		},
		submit() {
			if (this.isValidASN(this.asNumber)) {
				this.alert = false;
				axios({
					method: "put",
					url: `settings/${this.asNumber}`,
				}).catch((error) => {
					if (error.response.data.monitoring_possible == false) {
						console.log("Monitoring not possible")
						this.hostname = ""
						this.isMonitorable  = false
						this.errorMessage = error.response.data.message
					}
				}).then(response => {
					if (response.data.monitoring_possible) {
						this.errorMessage = ""
						this.get_asn()
					}
				})
			}
		},
		// addEmail() {
		// 	if (this.isValidEmail(this.email)) {
		// 		this.emails = this.email;
		// 		this.step = 3;
		// 	}
		// },
		// removeEmail(item) {
		// 	const idx = this.emails.indexOf(item);
		// 	if (idx > -1) {
		// 		this.emails.splice(idx, 1);
		// 	}
		// },
		// isValidEmail(val) {
		// 	const emailPattern = /^(?=[a-zA-Z0-9@._%+-]{6,254}$)[a-zA-Z0-9._%+-]{1,64}@(?:[a-zA-Z0-9-]{1,63}\.){1,8}[a-zA-Z]{2,63}$/;
		// 	return emailPattern.test(val);
		// },
	}
};
</script>
<style>
.page-card {
	margin: 2em;
}
.q-table__card {
	margin-bottom: 20px;
}
.center {
	margin: 0 auto;
}

.q-banner{
	margin-bottom: 20px
}
</style>