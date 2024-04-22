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
    <confirm-dialog ref="dialog"></confirm-dialog>

    <dashboard-panel-settings ref="panelSettings"
                              :component="settingsComponent"
                              :panel="editedPanel"
                              :endpoints="endpoints"
                              @panel-updated="onPanelUpdated">
    </dashboard-panel-settings>

    <div v-if="!inEditMode" class="row">
      <div class="col-lg-8 mb-2 mb-lg-0">
        <button type="button" class="btn btn-sm btn-primary" :disabled="!isEditable" @click="newDashboard">
          <i class="fa-solid fa-plus"></i> {{ $t('New') }}
        </button>
        <button type="button"
                class="btn btn-sm btn-light"
                :disabled="!isEditable"
                v-if="dashboard"
                @click="enterEditMode">
          <i class="fa-solid fa-pencil"></i> {{ $t('Edit') }}
        </button>
        <button type="button"
                class="btn btn-sm btn-danger"
                :disabled="!isEditable"
                v-if="dashboard"
                @click="deleteDashboard">
          <i class="fa-solid fa-trash"></i> {{ $t('Delete') }}
        </button>
      </div>

      <div class="col-lg-4 d-flex align-items-center">
        <dynamic-selection container-classes="select2-single-sm"
                           :placeholder="$t('Select a dashboard')"
                           :endpoint="selectEndpoint"
                           :reset-on-select="false"
                           @select="selectDashboard"
                           @unselect="resetDashboard">
        </dynamic-selection>
      </div>
    </div>

    <div class="row" v-if="inEditMode && dashboard">
      <div class="col-md-10 mb-2 mb-md-0">
        <button type="button" class="btn btn-sm btn-primary" @click="saveDashboard" :disabled="!unsavedChanges_">
          <i class="fa-solid fa-floppy-disk"></i> {{ $t('Save') }}
        </button>
        <button type="button" class="btn btn-sm btn-primary" @click="dashboard.layout.addRow()">
          <i class="fa-solid fa-plus"></i> {{ $t('Add Row') }}
        </button>
        <button type="button" class="btn btn-sm btn-light" @click="cancelEditMode">
          <i class="fa-solid fa-ban"></i> {{ $t('Cancel') }}
        </button>
        <div class="input-group input-group-sm d-sm-inline-flex w-auto mt-2 mt-sm-0">
          <div class="input-group-prepend">
            <span class="input-group-text">{{ $t('Name') }}</span>
          </div>
          <input class="form-control" v-model="dashboard.name">
        </div>
      </div>
    </div>

    <hr v-if="dashboard && dashboard.layout.rows.length > 0">

    <grid v-if="dashboard"
          :id="dashboard.layout.id"
          :rows="dashboard.layout.rows"
          :disabled="!inEditMode">

      <grid-row v-for="(row, index) in dashboard.layout.rows"
                :key="row.id"
                :id="row.id"
                :disabled="!inEditMode"
                :columns="row.columns"
                :class="{'mb-4': index < dashboard.layout.rows.length - 1}"
                @remove-row="removeRow(row)">

        <grid-column v-for="(column, columnIndex) in row.columns"
                     :key="column.id"
                     :id="column.id"
                     :size="column.size"
                     :same-height="false">

          <dashboard-panel v-if="!column.isPlaceholder"
                           class="column column-panel h-100"
                           :endpoints="endpoints"
                           :edit-mode="inEditMode"
                           :row="row"
                           :column="column"
                           :available-panels="availablePanels"
                           :panel="dashboard.getPanelByColumnId(column.id)"
                           @assign-panel="assignPanel"
                           @remove-panel="removePanel"
                           @open-settings="openSettings" />

          <div v-else
               class="column h-100 d-flex justify-content-center align-items-center"
               :class="{'column-placeholder': inEditMode}">
            <div v-if="inEditMode && row.canInsertColumn()">
              <button type="button"
                      class="btn btn-light btn-sm"
                      @click="row.insertColumnAt(columnIndex)">
                <i class="fa-solid fa-plus"></i>
              </button>
            </div>
          </div>
        </grid-column>
      </grid-row>
    </grid>
  </div>
</template>

<style lang="scss" scoped>
.column {
  min-height: 10em;
  padding: 0.75em;
}

.column-panel {
  border-radius: 0.5em;
  border: 1px solid lightgray;
}

.column-placeholder {
  border-radius: 0.5em;
  border: 1px dashed lightgray;
  max-height: 10em;
}
</style>

<script>
import {Upload, UploadProvider} from 'scripts/lib/uploads.js';
import Dashboard from 'scripts/lib/dashboard.js';

import DashboardPanelSettings from 'scripts/components/lib/dashboards/DashboardPanelSettings.vue';
import DashboardPanel from 'scripts/components/lib/dashboards/DashboardPanel.vue';

import Grid from 'scripts/components/lib/grid/Grid.vue';
import GridRow from 'scripts/components/lib/grid/GridRow.vue';
import GridColumn from 'scripts/components/lib/grid/GridColumn.vue';

export default {
  components: {
    DashboardPanel,
    DashboardPanelSettings,
    Grid,
    GridColumn,
    GridRow,
  },
  data() {
    return {
      dashboard: null,
      editableDashboard: null,
      editedPanel: null,
      inEditMode: false,
      uploadProvider: null,
      dashboardFile: null,
      unsavedChanges_: false,
      availablePanels: {
        markdown: {
          title: 'Markdown',
          settings: {
            text: '',
          },
          component: 'DashboardMarkdown',
          settingsComponent: 'DashboardMarkdownSettings',
        },
        recordView: {
          title: 'Record View',
          settings: {
            template: null,
            queryString: '',
          },
          component: 'DashboardRecordView',
          settingsComponent: 'DashboardRecordViewSettings',
        },
      },
    };
  },
  props: {
    selectEndpoint: String,
    uploadEndpoint: String,
    linkEndpoint: String,
    imageEndpoint: String,
    selectRecordTemplateEndpoint: String,
    newRecordEndpoint: String,
    recordsEndpoint: String,
    selectSavedSearchEndpoint: String,
    loadSavedSearchEndpoint: String,
    unsavedChanges: {
      type: Boolean,
      default: false,
    },
  },
  watch: {
    uploadEndpoint() {
      this.initUploadProvider();
    },
    unsavedChanges() {
      this.unsavedChanges_ = this.unsavedChanges;
    },
    unsavedChanges_() {
      this.$emit('unsaved-changes', this.unsavedChanges_);
    },
    dashboard: {
      handler() {
        this.unsavedChanges_ = this.inEditMode;
      },
      deep: true,
    },
  },
  computed: {
    isEditable() {
      return this.uploadProvider !== null;
    },
    endpoints() {
      return {
        image: this.imageEndpoint,
        link: this.linkEndpoint,
        selectRecordTemplate: this.selectRecordTemplateEndpoint,
        newRecord: this.newRecordEndpoint,
        records: this.recordsEndpoint,
        selectSavedSearch: this.selectSavedSearchEndpoint,
        loadSavedSearch: this.loadSavedSearchEndpoint,
      };
    },
    settingsComponent() {
      return this.editedPanel ? this.availablePanels[this.editedPanel.type].settingsComponent : null;
    },
  },
  methods: {
    initUploadProvider() {
      if (!this.uploadEndpoint) {
        return;
      }

      this.uploadProvider = new UploadProvider(this.uploadEndpoint, this.onUploadReplace, this.onUploadSuccess);
    },
    async enterEditMode() {
      this.inEditMode = true;

      this.editableDashboard = Dashboard.from(this.dashboard);

      // Switch references so that we see the copy of the original dashboard.
      [this.dashboard, this.editableDashboard] = [this.editableDashboard, this.dashboard];

      await this.$nextTick();

      this.unsavedChanges_ = false;
    },
    cancelEditMode() {
      // Switch back to the original (unchanged) dashboard.
      [this.dashboard, this.editableDashboard] = [this.editableDashboard, this.dashboard];

      this.leaveEditMode();
    },
    leaveEditMode() {
      this.inEditMode = false;
      this.editedPanel = null;
    },
    newDashboard() {
      this.dashboardFile = null;
      this.dashboard = new Dashboard(`dashboard_${kadi.utils.randomAlnum(10)}`);
      this.enterEditMode();
    },
    resetDashboard() {
      this.leaveEditMode();

      this.dashboard = null;
      this.editableDashboard = null;
      this.dashboardFile = null;
    },
    saveDashboard() {
      if (!this.isEditable || !this.dashboard.name) {
        kadi.base.flashDanger($t('Error saving dashboard.'));
        return;
      }

      const file = new File([JSON.stringify(this.dashboard.toJSON())], `${this.dashboard.name}.json`);
      const upload = new Upload(file.name, file.size, file);

      this.uploadProvider.upload(upload);
    },
    async loadDashboard(endpoint) {
      const errorMsg = $t('Error loading dashboard.');

      try {
        const response = await axios.get(endpoint);

        this.editableDashboard = null;
        this.dashboard = Dashboard.from(response.data);

        if (this.dashboard) {
          this.dashboard.layout.restore();
        } else {
          kadi.base.flashDanger(errorMsg);
        }
      } catch (error) {
        kadi.base.flashDanger(errorMsg, {request: error.request});
      }
    },
    async deleteDashboard() {
      if (!this.dashboardFile) {
        return;
      }

      const input = await this.$refs.dialog.open($t('Are you sure you want to delete this dashboard?'));

      if (!input.status) {
        return;
      }

      try {
        await axios.delete(this.dashboardFile.deleteEndpoint);

        kadi.base.flashSuccess($t('Dashboard deleted successfully.'), {scrollTo: false});

        this.resetDashboard();
        this.selectDashboard(null);
      } catch (error) {
        kadi.base.flashDanger($t('Error deleting dashboard.'), {request: error.request});
      }
    },
    selectDashboard(file) {
      if (file) {
        this.dashboardFile = {
          downloadEndpoint: file.download_endpoint,
          deleteEndpoint: file.delete_endpoint,
        };
        this.loadDashboard(this.dashboardFile.downloadEndpoint);
      } else {
        this.dashboardFile = null;
      }
    },
    async removeRow(row) {
      const input = await this.$refs.dialog.open(`${$t('Delete')}?`);

      if (input.status) {
        this.dashboard.layout.removeRow(row);
      }
    },
    assignPanel(panelType, column) {
      const panelTemplate = this.availablePanels[panelType];

      const panel = this.dashboard.createPanel(panelType);
      panel.settings = panelTemplate.settings;

      this.$set(this.dashboard.panels, panel.id, panel);
      this.$set(this.dashboard.layoutAssignments, column.id, panel.id);
    },
    async removePanel(panel, row, column) {
      const input = await this.$refs.dialog.open(`${$t('Delete')}?`);

      if (input.status) {
        if (panel) {
          this.dashboard.removePanel(panel, column.id);
        }

        row.removeColumn(column);
      }
    },
    openSettings(panel) {
      this.editedPanel = panel;
      this.$refs.panelSettings.show();
    },
    onPanelUpdated(editedPanel) {
      this.dashboard.panels[editedPanel.id] = kadi.utils.deepClone(editedPanel);
    },
    async onUploadReplace(upload) {
      const msg = $t(
        'A file with the name "{{filename}}" already exists in the current record. Do you want to replace it?',
        {filename: upload.name},
      );

      const input = await this.$refs.dialog.open(msg);
      return input.status;
    },
    onUploadSuccess(upload, file) {
      this.dashboardFile = {
        downloadEndpoint: file._links.download,
        deleteEndpoint: file._actions.delete,
      };

      this.unsavedChanges_ = false;
      this.leaveEditMode();

      kadi.base.flashSuccess($t('Dashboard saved successfully.'), {scrollTo: false});
    },
    beforeUnload(e) {
      if (this.unsavedChanges_) {
        e.preventDefault();
        return '';
      }
      return null;
    },
  },
  mounted() {
    this.initUploadProvider();
    window.addEventListener('beforeunload', this.beforeUnload);
  },
  beforeDestroy() {
    window.removeEventListener('beforeunload', this.beforeUnload);
  },
};
</script>
