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

				<div>Quasar v{{ $q.version }}</div>
			</q-toolbar>
		</q-header>

		<q-drawer show-if-above v-model="leftDrawerOpen" side="left" bordered>
			<q-list>
				<q-item-label header>Essential Links</q-item-label>
				<q-item clickable tag="a" :to="{ name: 'setup' }">
					<q-item-section avatar>
						<q-icon name="settings_suggest" />
					</q-item-section>
					<q-item-section>
						<q-item-label>Initial Setup</q-item-label>
					</q-item-section>
				</q-item>
				<q-item
					clickable
					tag="a"
					target="_blank"
					href="https://github.com/quasarframework/"
				>
					<q-item-section avatar>
						<q-icon name="code" />
					</q-item-section>
					<q-item-section>
						<q-item-label>Github</q-item-label>
						<q-item-label caption>github.com/quasarframework</q-item-label>
					</q-item-section>
				</q-item>
				<q-item
					clickable
					tag="a"
					target="_blank"
					href="https://chat.quasar.dev"
				>
					<q-item-section avatar>
						<q-icon name="chat" />
					</q-item-section>
					<q-item-section>
						<q-item-label>Discord Chat Channel</q-item-label>
						<q-item-label caption>chat.quasar.dev</q-item-label>
					</q-item-section>
				</q-item>
				<q-item
					clickable
					tag="a"
					target="_blank"
					href="https://forum.quasar.dev"
				>
					<q-item-section avatar>
						<q-icon name="forum" />
					</q-item-section>
					<q-item-section>
						<q-item-label>Forum</q-item-label>
						<q-item-label caption>forum.quasar.dev</q-item-label>
					</q-item-section>
				</q-item>
				<q-item
					clickable
					tag="a"
					target="_blank"
					href="https://twitter.com/quasarframework"
				>
					<q-item-section avatar>
						<q-icon name="rss_feed" />
					</q-item-section>
					<q-item-section>
						<q-item-label>Twitter</q-item-label>
						<q-item-label caption>@quasarframework</q-item-label>
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