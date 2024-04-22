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
    <span class="dropdown">
      <button type="button" class="btn btn-sm btn-light dropdown-toggle mr-1" data-toggle="dropdown">
        {{ $t('Import from file') }}
      </button>
      <div class="dropdown-menu dropdown-menu-right">
        <a class="dropdown-item" href="#" @click="openInput('json')">JSON</a>
      </div>
    </span>
    <popover-toggle toggle-class="btn btn-sm btn-light text-muted" :title="$t('Supported formats')">
      <template #toggle>
        <i class="fa-regular fa-circle-question"></i> {{ $t('Help') }}
      </template>
      <template #content>
        <div class="row">
          <div class="col-2">
            <strong>JSON</strong>
          </div>
          <div class="col-10">
            <!-- eslint-disable-next-line max-len -->
            {{ $t('Only the JSON format used by Kadi4Mat is currently supported. Valid contents include the exported data of records, record templates and extras templates, of which the basic and generic record metadata will be used.') }}
          </div>
        </div>
      </template>
    </popover-toggle>
    <submission-form enctype="multipart/form-data" :check-dirty="false" ref="form">
      <input class="input" :name="importTypeName" :value="importType">
      <input type="file" class="input" :name="importDataName" :accept="accept" @change="changeFile" ref="input">
      <slot></slot>
    </submission-form>
  </div>
</template>

<style scoped>
.input {
  position: absolute;
  visibility: hidden;
}
</style>

<script>
export default {
  data() {
    return {
      importTypes: {
        json: ['application/json'],
      },
      importType: '',
      accept: '',
    };
  },
  props: {
    maxSize: Number,
    importTypeName: {
      type: String,
      default: 'import_type',
    },
    importDataName: {
      type: String,
      default: 'import_data',
    },
  },
  methods: {
    async openInput(type) {
      this.importType = type;
      this.accept = this.importTypes[type].join(',');

      await this.$nextTick();

      this.$refs.input.click();
    },
    changeFile(e) {
      const file = e.target.files[0];

      if (file.size > this.maxSize) {
        kadi.base.flashWarning($t('File exceeds the maximum size.'));
        this.$refs.input.value = '';
      } else {
        this.$refs.form.submit();
      }
    },
  },
};
</script>
