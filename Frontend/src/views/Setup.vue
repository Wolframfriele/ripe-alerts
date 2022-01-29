<template>
	<q-card v-if="init_setup" flat bordered class="page-card">
		<div class="wrapper">
			<q-card-section>
				<h1>Adjust Monitoring settings</h1>
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

			<q-separator inset />

			<q-card-section>
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
		</div>
	</q-card>
</template>

<script>
import { ref } from "vue";
import axios from "axios";

export default {
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
				url: "user/monitored-asns"
			}).then(response => {
				if (response.data.length > 0) {
					this.init_setup = true;
					this.ASNList = response.data;
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
				this.addASN()
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
					method: "post",
					url: "user/initial-setup",
					data: {
						asns: this.ASNList,
						email: this.email
					}
				}).then(this.$router.push({ name: "home" }));
			}
		}
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