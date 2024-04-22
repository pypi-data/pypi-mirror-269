<!-- Copyright 2024 Karlsruhe Institute of Technology
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
    <div id="select-record-template" class="form-group">
      <label>{{ $t('Template') }}</label>

      <dynamic-selection container-classes="select2-single-sm"
                         :placeholder="$t('Select a template')"
                         :endpoint="endpoints.selectRecordTemplate"
                         dropdown-parent="#select-record-template"
                         @select="selectTemplate">
      </dynamic-selection>

      <div class="card bg-light mt-2 mb-3">
        <div class="card-body py-2">
          {{ $t('Template') }}:
          <a v-if="settings_.template"
             :href="settings_.template.viewEndpoint"
             target="_blank"
             rel="noopener noreferrer">
            <strong>{{ settings_.template.title }}</strong>
          </a>
        </div>
      </div>
    </div>

    <div id="select-saved-search" class="form-group">
      <label>{{ $t('Search for records') }}</label>

      <dynamic-selection container-classes="select2-single-sm"
                         :placeholder="$t('Select a saved search')"
                         :endpoint="endpoints.selectSavedSearch"
                         dropdown-parent="#select-saved-search"
                         :reset-on-select="true"
                         @select="loadSearch($event.id)">
      </dynamic-selection>
    </div>

    <div class="form-group">
      <input class="form-control" v-model="settings_.queryString" :placeholder="$t('Current search')" />
    </div>
  </div>
</template>

<script>
import dashboardSettingsMixin from 'scripts/components/mixins/dashboard-settings-mixin';

export default {
  mixins: [dashboardSettingsMixin],
  methods: {
    async selectTemplate(template) {
      try {
        const response = await axios.get(template.endpoint);
        const data = response.data;

        this.settings_.template = {
          id: data.id,
          title: data.title,
          viewEndpoint: data._links.view,
        };
      } catch (error) {
        kadi.base.flashDanger($t('Error loading template.'), {request: error.request});
      }
    },
    async loadSearch(id) {
      const errorMsg = $t('Error loading saved search.');

      try {
        const response = await axios.get(`${this.endpoints.loadSavedSearch}/${id}`);
        const data = response.data;

        if (data.object !== 'record') {
          kadi.base.flashDanger(errorMsg);
        } else {
          this.settings_.queryString = data.query_string;
        }
      } catch (error) {
        kadi.base.flashDanger(errorMsg, {request: error.request});
      }
    },
  },
};
</script>
