<template>
	<div id="q-app">
		<q-card flat bordered class="as-status-card">
			<q-card-section>
				<div class="text-h4">Ripe Alerter Documentation</div>
			</q-card-section>

			<q-card-section class="q-pt-none">
				This is an application aimed at monitoring neigboring networks. This has
				come from the idea that most networks are well aware of their own
				network status but checking what is going on around your network is much
				harder. This system is based around the
				<a href="https://atlas.ripe.net/"> Ripe Atlas</a>, and requires hosting
				an Anchor in your network.
			</q-card-section>

			<q-separator inset />

			<q-card-section>
				<div class="text-h5">Quickstart</div>
			</q-card-section>

			<q-card-section class="q-pt-none">
				To get started go to the 'Setup Monitor' page in the navigation. Here
				you can setup what AS Number your netwerk is, and on what email you want
				to receive alerts.
			</q-card-section>

			<q-separator inset />

			<q-card-section>
				<div class="text-h5">State of the application</div>
			</q-card-section>

			<q-card-section class="q-pt-none">
				Currently the application is in a very in-mature state, the main goal 
				for now is to be able to start collecting feedback on alerts. There is
				a lack of groundtruth information, this makes it hard to verify if the
				alerts that are being generated are actualy usefull to end users.
			</q-card-section>

			<q-separator inset />

			<q-separator inset />

			<q-card-section>
				<div class="text-h5">Anomaly Detection Methods</div>
			</q-card-section>

			<q-card-section class="q-pt-none">
				Right now the system checks for one type of anomaly; increases in round
				trip time in the connection from neighboring networks. It is based on
				traceroute data from the
				<a
					href="https://labs.ripe.net/author/alun_davies/anchoring-measurements-bringing-back-the-balance/"
				>
					Anchoring Mesh measurements</a
				>. These are recuring measurements, where all anchors send out a
				traceroute to all other anchors every 900 seconds. We find the Anchor in
				your AS (you need to host anchor for this system to work), and look at
				the last 24 hours of data for a baseline. Timeseries are constructed for
				each of the anchors measuring toward your anchor. For these timeseries
				the system uses the round trip time of the hop at the first router in
				your network, and stores the AS number from the router where the signal
				came from. The system then analyzes these timeseries for anomalies, it
				marks all the moments with anomalies. Then it checks at the current time
				what percentage of measurements in a neigboring AS-number are marked as
				anomaly. If there are atleast 5 timeseries for a neigboring AS and more
				than 30% of these are simultaniously showing an anomaly, an alert is
				send out.
			</q-card-section>
			<q-separator inset />

			<q-card-section>
				<div class="text-h5">Frequently asked questions</div>
			</q-card-section>

			<q-card-section class="q-pt-none">
				<ul>
					<li>
						<strong>
							When I look at the traceroutes to my anchor, the hop before entering
							my network is anonymous, can I still use this tool? <br />
						</strong>
						Unfortunatly at the moment it is not possible to monitor networks,
						that ignore traceroute requests. In the future we might develop
						anomaly detection methods that are not limited by this problem.
					</li>
					<li>
						<strong>
							I have set up my AS and email but I would like to change this, how
							can I do this? <br />
						</strong>
						Right now it is impossible to change the setup after the initial
						setup, the workaround is to simply delete the docker container and
						set up from scratch. We understand this is very inconvienent, this
						will be one of the first functions we will add.
					</li>
					<li>
						<strong>
							I setup the system, how do I know it is working? <br>
						</strong>
						If the correct AS number(s) are shown on the dashboard, the system is running.
						Right know it is not possible to gain more visual insight into status, 
						this is planned for future releases.
					</li>
				</ul>
			</q-card-section>
		</q-card>
	</div>
</template>

<style scoped>
.as-status-card {
	margin: 2em;
}
.q-pt-none {
	max-width: 900px;
}
</style>