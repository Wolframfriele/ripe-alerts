<template>
    <q-btn class="info-button" round>?
        <q-tooltip class="info-tooltip" anchor="center end" self="center start">{{ info }}</q-tooltip>
    </q-btn>
</template>

<script>
export default {
     props: ['info']
}
</script>

<style lang="css" scoped>
.info-button {
	float: right;
}

.info-tooltip {
	max-width: 100px;
}
</style>