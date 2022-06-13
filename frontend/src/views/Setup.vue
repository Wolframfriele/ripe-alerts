<template>
	<q-card v-if="init_setup" flat bordered class="page-card">
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
				<p>Remove or add AS numbers that you want to monitor.</p>
				<q-input
					ref="ASNField"
					v-model="ASN"
					filled
					prefix="AS"
					min="0"
					max="4294967295"
					@keyup.enter="addASN()"
					error-message="Must be a number between 0 and 4294967295"
					:rules="[isValidASN]"
					lazy-rules
				>
					<template v-slot:append>
						<q-btn round dense flat icon="add" @click="addASN()" />
					</template>
				</q-input>
				<q-markup-table flat>
					<tbody>
						<tr v-for="item in ASNList" :key="item">
							<td class="text-left">AS{{ item }}</td>
							<td class="text-right">
								<q-btn
									round
									color="red"
									icon="delete"
									size="sm"
									@click="removeASN(item)"
								/>
							</td>
						</tr>
					</tbody>
				</q-markup-table>
			</q-card-section>
<<<<<<< HEAD

			<q-separator inset />

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
			</q-card-section>
		</div>
	</q-card>
	<div v-if="init_setup" class="wrapper">
		<q-btn label="Bypass" @click="init_setup = false" />
		This button exist purely for demo purpuses, to go to initial setup.
	</div>
	<q-card v-else flat bordered class="page-card">
		<div class="wrapper">
			<q-card-section>
				<h1>Initial Setup</h1>
				<q-stepper
					v-model="step"
					flat
					bordered
					header-nav
					ref="stepper"
					color="primary"
					animated
				>
					<q-step
						:name="1"
						title="Select AS numbers"
						icon="settings"
						:done="step > 1"
						:header-nav="step > 1"
					>
						<p>
							Enter the AS numbers you want to monitor.
						</p>
						<q-input
							ref="ASNField"
							v-model="ASN"
							filled
							prefix="AS"
							min="0"
							max="4294967295"
							@keyup.enter="addASN()"
							error-message="Must be a number between 0 and 4294967295"
							:rules="[isValidASN]"
							lazy-rules
						>
							<template v-slot:append>
								<q-btn round dense flat icon="add" @click="addASN()" />
							</template>
						</q-input>
						<q-markup-table flat>
							<tbody>
								<tr v-for="item in ASNList" :key="item">
									<td class="text-left">AS{{ item }}</td>
									<td class="text-right">
										<q-btn
											round
											color="red"
											icon="delete"
											size="sm"
											@click="removeASN(item)"
										/>
									</td>
								</tr>
							</tbody>
						</q-markup-table>

						<q-stepper-navigation>
							<q-btn @click="step2()" color="primary" label="Continue">
								<q-popup-proxy v-if="alert">
									<q-banner>
										There needs to be atleast 1 AS number before continuing.
									</q-banner>
								</q-popup-proxy>
							</q-btn>
						</q-stepper-navigation>
					</q-step>

					<q-step
						:name="2"
						title="Alerting method"
						icon="notifications"
						:done="step > 2"
						:header-nav="step > 2"
					>
						<p>
							Enter the email that you want to receive alerts on.
						</p>
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

						<q-stepper-navigation>
							<q-btn @click="addEmail()" color="primary" label="Continue">
								<q-popup-proxy v-if="alert">
									<q-banner>
										Email needs to be entered before continuing.
									</q-banner>
								</q-popup-proxy>
							</q-btn>
							<q-btn
								flat
								@click="step = 1"
								color="primary"
								label="Back"
								class="q-ml-sm"
							/>
						</q-stepper-navigation>
					</q-step>
					<q-step
						:name="3"
						title="Summary"
						icon="fact_check"
						:header-nav="step > 3"
					>
						<strong>Monitoring the following AS numbes:</strong>
						<q-list>
							<q-item v-for="item in ASNList" :key="item" v-ripple>
								<q-item-section>AS{{ item }}</q-item-section>
							</q-item>
						</q-list>
						<strong>Alerts will be send to:</strong>
						<q-list>
							<q-item v-ripple>
								<q-item-section>{{ emails }}</q-item-section>
							</q-item>
						</q-list>

						<q-stepper-navigation>
							<q-btn color="primary" label="Finish" @click="submit()" />
							<q-btn
								flat
								@click="step = 2"
								color="primary"
								label="Back"
								class="q-ml-sm"
							>
								<q-popup-proxy v-if="alert">
									<q-banner>
										All fields need to be filled before submitting.
									</q-banner>
								</q-popup-proxy>
							</q-btn>
						</q-stepper-navigation>
					</q-step>
				</q-stepper>
			</q-card-section>
=======
>>>>>>> main
		</div>
	</q-card>
</template>

<script>
import { ref } from "vue";
import axios from "axios";
import InfoButton from "../components/InfoButton.vue";

export default {
	components: {
		InfoButton
	},
	setup() {
		return {
			step: ref(1),
			check1: ref(false),
			email: ref(""),
			ASN: ref("")
		};
	},
	data() {
		return {
			init_setup: false,
			ASNList: [],
			emails: "",
			alert: true
		};
	},
	created() {
		this.get_asn();
	},
	methods: {
		get_asn() {
			axios({
				method: "get",
<<<<<<< HEAD
				url: "user/monitored-asns"
=======
				url: "settings"
>>>>>>> main
			}).then(response => {
				if (response.data.length > 0) {
					this.init_setup = true;
					this.ASNList = response.data;
				}
			}).catch((error) => {
				if (error) {
					this.asNumber = ""
					this.hostname = ""
					this.isMonitorable = false
					this.asHasBeenSetup = false
				}
			});
		},
		addASN() {
			if (this.isValidASN(this.ASN)) {
				this.ASNList.push(this.ASN);
				this.ASN = "";
			}
		},
		removeASN(item) {
			const idx = this.ASNList.indexOf(item);
			if (idx > -1) {
				this.ASNList.splice(idx, 1);
			}
		},
		isValidASN(val) {
			const ASNPattern = /^[0-9]{1,6}$/;
			return ASNPattern.test(val);
		},
		step2() {
			if (this.ASN.length > 0) {
				this.addASN();
			}
			if (this.ASNList > 0) {
				this.step = 2;
			}
		},
		addEmail() {
			if (this.isValidEmail(this.email)) {
				this.emails = this.email;
				this.step = 3;
			}
		},
		removeEmail(item) {
			const idx = this.emails.indexOf(item);
			if (idx > -1) {
				this.emails.splice(idx, 1);
			}
		},
		isValidEmail(val) {
			const emailPattern = /^(?=[a-zA-Z0-9@._%+-]{6,254}$)[a-zA-Z0-9._%+-]{1,64}@(?:[a-zA-Z0-9-]{1,63}\.){1,8}[a-zA-Z]{2,63}$/;
			return emailPattern.test(val);
		},
		submit() {
			if (this.ASNList.length > 0 && this.email.length > 0) {
				this.alert = false;
				axios({
<<<<<<< HEAD
					method: "post",
					url: "user/initial-setup",
					data: {
						asns: this.ASNList,
						email: this.email
					}
				}).then(this.$router.push({ name: "home" }));
			}
		}
=======
					method: "put",
					url: `settings/${this.asNumber}`,
				}).then(response => {
					if (response.data.monitoring_possible) {
						this.errorMessage = ""
						this.get_asn()
					}
				}).catch((error) => {
					if (error.response.data.monitoring_possible == false) {
						console.log("Monitoring not possible")
						this.hostname = ""
						this.isMonitorable  = false
						this.errorMessage = error.response.data.message
					}
				})
			}
		},
>>>>>>> main
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
</style>