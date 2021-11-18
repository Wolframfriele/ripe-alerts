<template>
  <q-page class="q-pa-md q-mx-auto">

    <q-stepper
      v-model="step"
      header-nav
      ref="stepper"
      color="primary"
      animated
    >
      <q-step
        :name="1"
        title="Select targets and anchors"
        icon="settings"
        :done="step > 1"
        :header-nav="step > 1"
      >
        Select targets and anchors here.

        <q-stepper-navigation>
          <q-btn @click="() => { done1 = true; step = 2 }" color="primary" label="Continue" />
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
          <q-btn @click="() => { done2 = true; step = 3 }" color="primary" label="Continue" />
          <q-btn flat @click="step = 1" color="primary" label="Back" class="q-ml-sm" />
        </q-stepper-navigation>
      </q-step>

      <q-step
        :name="3"
        title="Alerting method"
        icon="notifications"
        :header-nav="step > 3"
      >
        Alerting method here.

        <q-stepper-navigation>
          <q-btn @click="() => { done3 = true; step = 4 }" color="primary" label="Continue" />
          <q-btn flat @click="step = 2" color="primary" label="Back" class="q-ml-sm" />
        </q-stepper-navigation>
      </q-step>
      <q-step
        :name="4"
        title="Summary"
        icon="add_comment"
        :header-nav="step > 4"
      >
        Summary here.

        <q-stepper-navigation>
          <q-btn color="primary" @click="done4 = true" label="Finish" />
          <q-btn flat @click="step = 3" color="primary" label="Back" class="q-ml-sm" />
        </q-stepper-navigation>
      </q-step>
    </q-stepper>
  </q-page>
</template>

<script>
import { ref } from 'vue'

export default {
  setup () {
    return {
      step: ref(1)
    }
  }
}
</script>

<style>
.q-page {
  max-width: 1024px;
}
</style>