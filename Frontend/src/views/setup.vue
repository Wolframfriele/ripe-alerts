<template>
	<q-page class="q-pa-md q-mx-auto">
		<q-stepper v-model="step" header-nav ref="stepper" color="primary" animated>
			<q-step
				:name="1"
				title="Select targets and anchors"
				icon="settings"
				:done="step > 1"
				:header-nav="step > 1"
			>
				Select targets and anchors here.
				<q-list bordered separator v-for="target in targets" :key="target">
					<q-item tag="label" clickable v-ripple>
						<q-item-section side top>
							<q-checkbox v-model="check1" />
						</q-item-section>
						<q-item-section>
							<q-item-label>{{ target.target }}</q-item-label>
							<q-item-label caption>Caption</q-item-label>
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
				title="Select measurements"
				icon="auto_graph"
				:done="step > 2"
				:header-nav="step > 2"
			>
				Select measurements here.

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
				title="Alerting method"
				icon="notifications"
				:done="step > 3"
				:header-nav="step > 3"
			>
				Alerting method here.
				<q-list v-for="email in emails" :key="email">
					<q-item tag="label">
						<q-item-section>
							<q-item-label>{{ email }}</q-item-label>
						</q-item-section>
					</q-item>
				</q-list>

				<q-stepper-navigation>
					<q-btn
						@click="
							() => {
								step = 4;
							}
						"
						color="primary"
						label="Continue"
					/>
					<q-btn
						flat
						@click="step = 2"
						color="primary"
						label="Back"
						class="q-ml-sm"
					/>
				</q-stepper-navigation>
			</q-step>
			<q-step :name="4" title="Summary" icon="fact_check" :header-nav="step > 4">
				Summary here.

				<q-stepper-navigation>
					<q-btn color="primary" label="Finish" />
					<q-btn
						flat
						@click="step = 3"
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
		};
	},
	data() {
		return {
			targets: [
				{ target: "192.168.0.1" },
				{ target: "netflix.com" },
				{ target: "8.8.8.8" },
			],
			emails: ["webmaster@website.com", "example@example.com", "me@mysite.net"],
		};
	},
};
</script>

<style>
.q-page {
	max-width: 1024px;
}
</style>
