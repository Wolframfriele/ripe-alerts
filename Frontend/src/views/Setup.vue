<template>
	<q-page class="q-pa-md q-mx-auto">
		<q-stepper v-model="step" header-nav ref="stepper" color="primary" animated>
			<q-step
				:name="1"
				title="Select AS numbers"
				icon="settings"
				:done="step > 1"
				:header-nav="step > 1"
			>
				<p>
					Enter the AS numbers you want to monitor, the system checks the neigboring connections.
				</p>
				<q-input
					ref="ASNField"
					v-model="ASN"
					filled
					prefix="AS"
					min= 0
					max= 65535
					@keyup.enter="addASN()"
					error-message="Must be a number between 0 and 65535"
					:rules="[
						isValidASN
					]"
					lazy-rules
				>
					<template v-slot:append>
						<q-btn round dense flat icon="add" @click="addASN()" />
					</template>
				</q-input>
				<q-markup-table flat>
					<tbody>
						<tr v-for="item in ASNList" :key="item">
							<td class="text-left">{{ item }}</td>
							<td class="text-right"><q-btn round color="red" icon="delete" size="sm" @click="removeASN(item)"/></td>
						</tr>
					</tbody>
				</q-markup-table>

				<q-stepper-navigation>
					<q-btn
						@click="
							() => {
								step = 2;
							}
						"
						color="primary"
						label="Continue"
					/>
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
					<!-- <template v-slot:append>
						<q-btn round dense flat icon="add" @click="addEmail()" />
					</template> -->
				</q-input>

				<q-stepper-navigation>
					<q-btn
						@click="addEmail()"
						color="primary"
						label="Continue"
					/>
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
				<q-markup-table>
					<thead>
						<tr>
							<th class="text-left">Monitor the following AS Numbers</th>
						</tr>
					</thead>
					<tbody>
						<tr v-for="item in ASNList" :key="item">
							<td class="text-left">{{ item }}</td>
						</tr>
					</tbody>
				</q-markup-table>

				<q-markup-table>
					<thead>
						<tr>
							<th class="text-left">Alerts will be send to following email</th>
						</tr>
					</thead>
					<tbody>
						<tr>
							<td class="text-left">{{ emails }}</td>
						</tr>
					</tbody>
				</q-markup-table>

				<q-stepper-navigation>
					<q-btn color="primary" label="Finish" @click="submit()"/>
					<q-btn
						flat
						@click="step = 2"
						color="primary"
						label="Back"
						class="q-ml-sm"
					/>
				</q-stepper-navigation>
			</q-step>
		</q-stepper>
	</q-page>
</template>

<script>
import { ref } from "vue";
// import Api from "../components/api";
import axios from 'axios'

export default {
	setup() {
		return {
			step: ref(1),
			check1: ref(false),
			email: ref(""),
			ASN: ref(""),
		};
	},
	data() {
		return {
			ASNList: [],
			emails: ""
		};
	},
	methods: {
		addASN() {
			if (this.isValidASN(this.ASN)) {
				this.ASNList.push("AS" + this.ASN);
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
			const ASNPattern = /^[0-9]{1,5}$/;
			return ASNPattern.test(val);
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
			axios({
				method: 'post',
				url: 'http://localhost:8000/api/user/initial-setup',
				data: {
					"asns": this.ASNList,
					"email": this.emails,
				}
			}).then((response) => {
				console.log(response)
				this.$router.push({ name: 'home' })
			})
		}
	}
};
</script>
<style>
	.q-table__card{
		margin-bottom: 20px;
	}
</style>