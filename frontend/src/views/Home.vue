<template>
	<div
		class="row wrap justify-start items-start content-start q-gutter-md q-pa-md"
	>
		<q-card class="col-5">
			<q-card-section>
				<h1 class="text-h6">Recent Alerts</h1>
			</q-card-section>
			<RecentAlerts />
		</q-card>
		<q-card class="col-grow">
			<q-card-section>
				<h1 class="text-h6">Probes Anomaly Graph</h1>
			</q-card-section>
			<AllMeasurementsGraph />
		</q-card>
	</div>
</template>

<script>
import AllMeasurementsGraph from "../components/widgets/AllMeasurementsGraph.vue";
import RecentAlerts from "../components/widgets/RecentAlerts.vue";

export default {
	components: {
		AllMeasurementsGraph,
		RecentAlerts
	}
};
</script>