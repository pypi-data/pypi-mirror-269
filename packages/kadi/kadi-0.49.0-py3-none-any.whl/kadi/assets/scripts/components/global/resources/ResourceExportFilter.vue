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
  <div class="card">
    <div class="card-body filter-container">
      <div class="form-check my-2" v-if="showRecordsFilter">
        <input type="checkbox" class="form-check-input" :id="`records-${suffix}`" v-model="filter.records">
        <label class="form-check-label" :for="`records-${suffix}`">{{ $t('Exclude records') }}</label>
      </div>
      <div class="my-2" v-if="showExportFilter">
        <div class="mb-2">{{ $t('Include export data') }}</div>
        <div class="card bg-light">
          <div class="card-body">
            <div class="form-check"
                 v-for="exportMeta in [['json', 'JSON'], ['rdf', 'RDF (Turtle)'], ['pdf', 'PDF']]"
                 :key="exportMeta[0]">
              <input type="checkbox"
                     class="form-check-input"
                     :id="`export-type-${exportMeta[0]}-${suffix}`"
                     v-model="filter.crateExportData[exportMeta[0]]">
              <label class="form-check-label" :for="`export-type-${exportMeta[0]}-${suffix}`">
                {{ exportMeta[1] }}
              </label>
            </div>
          </div>
        </div>
      </div>
      <div class="form-check my-2" v-if="showUserFilter">
        <input type="checkbox" class="form-check-input" :id="`user-${suffix}`" v-model="filter.user">
        <label class="form-check-label" :for="`user-${suffix}`">{{ $t('Exclude user information') }}</label>
      </div>
      <div class="my-2" v-if="showLinksFilter">
        <label class="form-control-label" :for="`links-${suffix}`">{{ $t('Exclude record links') }}</label>
        <select class="custom-select custom-select-sm" :id="`links-${suffix}`" v-model="filter.links">
          <option value=""></option>
          <option value="out">{{ $t('Outgoing') }}</option>
          <option value="in">{{ $t('Incoming') }}</option>
          <option value="both">{{ $t('Both') }}</option>
        </select>
      </div>
      <div class="my-2" v-if="showExtrasFormatFilter">
        <label class="form-control-label" :for="`format-${suffix}`">{{ $t('Extra metadata format') }}</label>
        <select class="custom-select custom-select-sm" :id="`format-${suffix}`" v-model="filter.extrasFormat">
          <option value="standard">{{ $t('Standard') }}</option>
          <option value="plain">{{ $t('Plain') }}</option>
        </select>
      </div>
      <div class="my-2" v-if="showExtrasFilter">
        <div class="row mb-2">
          <div class="col-md-6 mb-2 mb-md-0">{{ $t('Exclude extra metadata') }}</div>
          <div class="col-md-6 d-md-flex justify-content-end" v-if="showExtrasPropagationFilter">
            <div class="form-check">
              <input type="checkbox" class="form-check-input" :id="`propagate-${suffix}`" v-model="filter.propagate">
              <label class="form-check-label" :for="`propagate-${suffix}`">{{ $t('Apply to linked records') }}</label>
            </div>
          </div>
        </div>
        <div class="card bg-light">
          <div class="card-body">
            <extras-selector :extras="extras" @select="filter.extras = $event"></extras-selector>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.filter-container {
  padding-bottom: 0.75rem;
  padding-top: 0.75rem;
}
</style>

<script>
export default {
  data() {
    return {
      suffix: kadi.utils.randomAlnum(),
      filter: {
        user: this.defaultUserFilter,
        records: false,
        links: '',
        extrasFormat: 'standard',
        extras: {},
        propagate: false,
        crateExportData: {
          json: true,
          rdf: true,
          pdf: false,
        },
      },
    };
  },
  props: {
    resourceType: String,
    exportType: {
      type: String,
      default: null,
    },
    extras: {
      type: Array,
      default: () => [],
    },
    allowExtrasPropagation: {
      type: Boolean,
      default: true,
    },
    defaultUserFilter: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    showRecordsFilter() {
      return this.resourceType === 'collection';
    },
    showExportFilter() {
      return this.exportType === 'ro-crate' && !this.filter.records;
    },
    showUserFilter() {
      return ['record', 'collection', 'template'].includes(this.resourceType) && this.exportType !== 'json-schema';
    },
    showLinksFilter() {
      return ['record', 'collection'].includes(this.resourceType) && !this.filter.records;
    },
    showExtrasFormatFilter() {
      return this.resourceType === 'extras' && this.exportType === 'json';
    },
    showExtrasFilter() {
      return ['record', 'extras', 'template'].includes(this.resourceType) && this.extras.length > 0;
    },
    showExtrasPropagationFilter() {
      return this.resourceType === 'record' && this.allowExtrasPropagation && this.filter.links !== 'both';
    },
  },
  watch: {
    filter: {
      handler() {
        this.updateFilter();
      },
      deep: true,
    },
  },
  methods: {
    updateFilter() {
      const filter = {};

      if (this.filter.user !== false) {
        filter.user = this.filter.user;
      }
      if (this.filter.records !== false) {
        filter.records = this.filter.records;
      }
      if (this.filter.links !== '') {
        filter.links = this.filter.links === 'both' ? true : this.filter.links;
      }
      if (this.filter.extrasFormat !== 'standard') {
        filter.format = this.filter.extrasFormat;
      }
      if (Object.keys(this.filter.extras).length > 0) {
        filter.extras = this.filter.extras;
      }
      if (this.filter.propagate) {
        filter.propagate_extras = true;
      }

      if (this.exportType === 'ro-crate') {
        const exportData = [];

        for (const [key, value] of Object.entries(this.filter.crateExportData)) {
          if (value) {
            exportData.push(key);
          }
        }

        filter.export_data = exportData;
      }

      this.$emit('filter', filter);
    },
  },
  mounted() {
    this.updateFilter();
  },
};
</script>
