<template>
	<q-card flat bordered class="page-card">
		<div class="wrapper">
			<q-card-section>
				<h1>Ripe Alerter Documentation</h1>
				<p>
					This is an application aimed at monitoring neigboring networks. This
					has come from the idea that most networks are well aware of their own
					network status but checking what is going on around your network is
					much harder. This system is based around the
					<a href="https://atlas.ripe.net/"> Ripe Atlas</a>, and requires
					hosting an Anchor in your network.
				</p>
			</q-card-section>

			<q-separator inset />

			<q-card-section>
				<h2>Quickstart</h2>
				<p>
					To get started go to the 'Setup Monitor' page in the navigation. Here
					you can setup what AS Number your netwerk is, and on what email you
					want to receive alerts.
				</p>
			</q-card-section>

			<q-separator inset />

			<q-card-section>
				<h2>State of the application</h2>
				<p>
					Currently the application is in a very in-mature state, the main goal
					for now is to be able to start collecting feedback on alerts. There is
					a lack of groundtruth information, this makes it hard to verify if the
					alerts that are being generated are actualy usefull to end users.
				</p>
			</q-card-section>

			<q-separator inset />

			<q-card-section>
				<h2>Anomaly Detection Methods</h2>
				<p>
					Right now the system checks for one type of anomaly; increases in
					round trip time in the connection from neighboring networks. It is
					based on traceroute data from the
					<a
						href="https://labs.ripe.net/author/alun_davies/anchoring-measurements-bringing-back-the-balance/"
					>
						Anchoring Mesh measurements</a
					>. These are recuring measurements, where all anchors send out a
					traceroute to all other anchors every 900 seconds. We find the Anchor
					in your AS (you need to host anchor for this system to work), and look
					at the last 24 hours of data for a baseline. Timeseries are
					constructed for each of the anchors measuring toward your anchor. For
					these timeseries the system uses the round trip time of the hop at the
					first router in your network, and stores the AS number from the router
					where the signal came from. The system then analyzes these timeseries
					for anomalies, it marks all the moments with anomalies. Then it checks
					at the current time what percentage of measurements in a neigboring
					AS-number are marked as anomaly. If there are atleast 5 timeseries for
					a neigboring AS and more than 30% of these are simultaniously showing
					an anomaly, an alert is send out.
				</p>
			</q-card-section>

			<q-separator inset />

			<q-card-section>
				<h2>Frequently asked questions</h2>
				<ul>
					<li>
						<strong>
							When I look at the traceroutes to my anchor, the hop before
							entering my network is anonymous, can I still use this tool?
							<br />
						</strong>
						Unfortunatly at the moment it is not possible to monitor networks,
						that ignore traceroute requests. In the future we might develop
						anomaly detection methods that are not limited by this problem.
					</li>
					<li>
						<strong>
							I have setup the system, how do I know it is working? <br />
						</strong>
						If the correct AS number(s) are shown on the dashboard, the system
						is running. Right know it is not possible to gain more visual
						insight into status, this is planned for future releases.
					</li>
				</ul>
			</q-card-section>
		</div>
	</q-card>
</template>

<style scoped>
.page-card {
	margin: 2em;
}
</style>