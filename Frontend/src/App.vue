<template>
	<q-layout view="lHh LpR lFr">
		<q-header reveal elevated class="bg-primary text-white">
			<q-toolbar>
				<q-btn
					flat
					dense
					round
					@click="toggleLeftDrawer"
					aria-label="Menu"
					icon="menu"
				/>
				<q-toolbar-title>
					Ripe Alerter
				</q-toolbar-title>

				<div>v 0.1</div>
			</q-toolbar>
		</q-header>

		<q-drawer show-if-above v-model="leftDrawerOpen" side="left" bordered>
			<q-list>
				<q-item-label header>Navigation</q-item-label>
				<q-item clickable tag="a" :to="{ name: 'home' }">
					<q-item-section avatar>
						<q-icon name="space_dashboard" />
					</q-item-section>
					<q-item-section>
						<q-item-label>Dashboard</q-item-label>
					</q-item-section>
				</q-item>
				
				<q-item clickable tag="a" :to="{ name: 'managealerts' }">
					<q-item-section avatar>
						<q-icon name="format_list_bulleted" />
					</q-item-section>
					<q-item-section>
						<q-item-label>Alerts Feedback</q-item-label>
					</q-item-section>
				</q-item>
				<q-item clickable tag="a" :to="{ name: 'setup' }">
					<q-item-section avatar>
						<q-icon name="settings_suggest" />
					</q-item-section>
					<q-item-section>
						<q-item-label>Setup Monitoring</q-item-label>
					</q-item-section>
				</q-item>
				<q-separator />
				<q-item clickable tag="a" :to="{ name: 'documentation' }">
					<q-item-section avatar>
						<q-icon name="article" />
					</q-item-section>
					<q-item-section>
						<q-item-label>Documentation</q-item-label>
					</q-item-section>
				</q-item>
			</q-list>
		</q-drawer>

		<q-page-container>
			<router-view />
		</q-page-container>
	</q-layout>
</template>

<script>
import { ref } from "vue";

export default {
	setup() {
		const leftDrawerOpen = ref(false);

		return {
			leftDrawerOpen,
			toggleLeftDrawer() {
				leftDrawerOpen.value = !leftDrawerOpen.value;
			}
		};
	}
};
</script>