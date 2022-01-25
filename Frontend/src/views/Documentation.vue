<template>
	<div id="q-app">
		<q-card flat bordered class="as-status-card">
			<q-card-section>
				<div class="text-h4">Ripe Alerter Documentation</div>
			</q-card-section>

			<q-card-section class="q-pt-none">
				This is an application aimed at monitoring neigboring networks. This has
				comes from the idea that most networks are well aware of their own network status
				but checking what is going on around your network is much harder.
				This system is based around the Ripe Atlas, and requires hosting an Anchor in your
				network.
			</q-card-section>

			<q-separator inset />

			<q-card-section>
				<div class="text-h5">Quickstart</div>
			</q-card-section>

			<q-card-section class="q-pt-none">
				To get started go to the 'Setup Monitor' page in the navigation. 
				Here you can setup what AS Number your netwerk is, and on what 
				email you want to receive alerts.
			</q-card-section>

			<q-separator inset />

			<q-card-section>
				<div class="text-h5">Anomaly Detection Methods</div>
			</q-card-section>

			<q-card-section class="q-pt-none">
				Right now the system checks for one type of anomaly; increases in round trip time in 
				the connection from neighboring networks.
			</q-card-section>
		</q-card>
	</div>
</template>

<style scoped>
	.as-status-card {
		margin: 2em;
	}
</style>