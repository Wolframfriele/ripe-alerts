<template>
  <div id="q-app">
    <div class="q-pa-md">
      <div class="row q-col-gutter-sm">
        <div class="col">
          <q-table
            title="Alerts Overview and Feedback"
            :rows="data"
            :columns="columns"
            row-key="timestamp"
            dense
          >
            <template v-slot:body-cell-actions="props">
              <q-td :props="props">
                <q-btn dense round flat color="green" @click="editRow(props)" icon="thumb_up"></q-btn>
                <q-btn dense round flat color="red" @click="deleteRow(props)" icon="thumb_down"></q-btn>
              </q-td>          
            </template>
          </q-table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  setup() {
    
  },
  data () {
    return {
      columns: [
        {
          name: 'timestamp',
          required: true,
          label: 'Timestamp',
          align: 'left',
          field: row => row.timestamp,
          // format: val => `${val}`,
          sortable: true
        },
        { name: 'description', align: 'left', label: 'Alert Description', field: 'description'},
        { name: 'actions', label: 'Feedback', field: '', align:'center' },
      ],
      data: [
        {
          timestamp: '2021-1-10 18:22',
          description: 'Neigbor AS26677: Increase in RTT to 260 (140 normal)',
        },
        {
          timestamp: '2021-1-11 17:30',
          description: 'Neigbor AS26677: Increase in RTT to 260 (140 normal)',
        },
      ],
      noti: () => {},
      editedIndex: -1,
      pagination: {
        page: 1,
      },
      page: 1,
      totalRecord: 0,
      pageCount: 1,
    }
  },
  methods: {
    editRow(props) {
      console.log(props)
    },
    deleteRow(props){
      console.log(props)
    },
  },
}
</script>

<style scoped>
  .q-pa-md {
    margin: 1em;
  }
</style>