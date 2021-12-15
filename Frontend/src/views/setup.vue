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
				<q-input
					ref="ASNField"
					v-model="ASN"
					filled
					type="number"
					prefix="AS"
					min= 0
					max= 65535
					@keyup.enter="addASN()"
					error-message="Must be a number between 0 and 65535"
					:rules="[
						isValidASN
					]"
				>
					<template v-slot:append>
						<q-btn round dense flat icon="add" @click="addASN()" />
					</template>
				</q-input>

				<q-list v-for="ASN in ASNList" :key="ASN">
					<q-item tag="label">
						<q-item-section>
							<q-item-section>{{ ASN }}</q-item-section>
						</q-item-section>
					</q-item>
				</q-list>

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
				>
					<template v-slot:append>
						<q-btn round dense flat icon="add" @click="addEmail()" />
					</template>
				</q-input>
				<q-list v-for="email in emails" :key="email">
					<q-item tag="label">
						<q-item-section>
							<q-item-section>{{ email }}</q-item-section>
						</q-item-section>
					</q-item>
				</q-list>

				<q-stepper-navigation>
					<q-btn
						@click="
							() => {
								step = 3;
							}
						"
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
				Summary here.

				<q-stepper-navigation>
					<q-btn color="primary" label="Finish" />
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
			ASNList: ["AS1102","AS1103","AS1146"],
			emails: []
		};
	},
	methods: {
		addEmail() {
			if (this.isValidEmail(this.email)) {
				this.emails.push(this.email);
				this.email = "";
			}
		},
		isValidEmail(val) {
			const emailPattern = /^(?=[a-zA-Z0-9@._%+-]{6,254}$)[a-zA-Z0-9._%+-]{1,64}@(?:[a-zA-Z0-9-]{1,63}\.){1,8}[a-zA-Z]{2,63}$/;
			return emailPattern.test(val);
		},
		addASN() {
			if (this.isValidASN(this.ASN)) {
				this.ASNList.push("AS" + this.ASN);
				this.ASN = "";
			}
		},
		isValidASN(val) {
			const ASNPattern = /^[0-9]{1,5}$/;
			return ASNPattern.test(val);
		},
	}
};
</script>

<style>
.q-page {
	max-width: 1024px;
}
</style>
