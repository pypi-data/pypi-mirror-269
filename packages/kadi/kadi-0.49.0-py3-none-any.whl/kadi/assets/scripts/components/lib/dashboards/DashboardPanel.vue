<!-- Copyright 2022 Karlsruhe Institute of Technology
   -
   - Licensed under the Apache License, Version 2.0 (the "License");
   - you may not use this file except in compliance with the License.
   - You may obtain a copy of the License at
   -
   -     http://www.apache.org/licenses/LICENSE-2.0
   -
   - Unless required by applicable law or agreed to in writing, software
   - distributed under the License is distributed on an "AS IS" BASIS,
   - WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   - See the License for the specific language governing permissions and
   - limitations under the License. -->

<template>
  <div>
    <div class="d-flex justify-content-between">
      <div class="flex-grow-1">
        <div v-if="panel">
          <div class="h5 mb-0 font-weight-bold">
            {{ panel.title }}
          </div>
          <div class="text-muted mb-1" v-if="panel.subtitle">
            {{ panel.subtitle }}
          </div>
        </div>
      </div>

      <div v-if="editMode" class="d-flex align-items-start ml-4">
        <div class="btn-group btn-group-sm">
          <button type="button"
                  class="btn btn-light btn-sm"
                  :disabled="row.countPlaceholders() === 0"
                  @click="row.growColumn(column)">
            <i class="fa-solid fa-up-right-and-down-left-from-center"></i>
          </button>

          <button type="button"
                  class="btn btn-light btn-sm"
                  :disabled="column.size <= row.minColumnSize"
                  @click="row.shrinkColumn(column)">
            <i class="fa-solid fa-down-left-and-up-right-to-center"></i>
          </button>

          <button v-if="panel"
                  type="button"
                  class="btn btn-light btn-sm"
                  @click="$emit('open-settings', panel)">
            <i class="fa-solid fa-gear"></i>
          </button>

          <select v-if="!panel" v-model="selectedType" class="btn btn-light" @change="selectPanel">
            <option v-for="(value, key) in availablePanels" :key="key" :value="key">
              {{ value.title }}
            </option>
          </select>

          <button type="button"
                  class="btn btn-light btn-sm"
                  @click="removeColumn">
            <i class="fa-solid fa-trash"></i>
          </button>

          <span class="sort-handle btn btn-small btn-light disabled">
            <i class="fa-solid fa-bars"></i>
          </span>
        </div>
      </div>
    </div>

    <div v-if="panel" class="w-100 h-100 overflow-hidden">
      <component :is="availablePanels[panel.type].component"
                 :key="panel.id"
                 :endpoints="endpoints"
                 :settings="panel.settings">
      </component>
    </div>
  </div>
</template>

<script>
import DashboardMarkdown from 'scripts/components/lib/dashboards/panels/DashboardMarkdown.vue';
import DashboardRecordView from 'scripts/components/lib/dashboards/panels/DashboardRecordView.vue';

export default {
  components: {
    DashboardMarkdown,
    DashboardRecordView,
  },
  data() {
    return {
      selectedType: null,
    };
  },
  props: {
    endpoints: Object,
    editMode: Boolean,
    column: Object,
    row: Object,
    panel: Object,
    availablePanels: Object,
  },
  methods: {
    selectPanel() {
      this.$emit('assign-panel', this.selectedType, this.column);
    },
    removeColumn() {
      this.$emit('remove-panel', this.panel, this.row, this.column);
    },
  },
};
</script>
