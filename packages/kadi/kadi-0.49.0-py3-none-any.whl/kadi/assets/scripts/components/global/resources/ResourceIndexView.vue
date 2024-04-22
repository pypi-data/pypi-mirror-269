<!-- Copyright 2021 Karlsruhe Institute of Technology
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
  <card-deck :items="resources" :max-cards="2">
    <template #default="props">
      <div class="card-header py-1" v-if="props.item.pretty_type">
        <strong>{{ props.item.pretty_type }}</strong>
      </div>
      <div class="card-body py-3">
        <a class="text-default stretched-link" :href="props.item._links.view">
          <resource-type class="float-right badge-mt-plus ml-3"
                         :type="props.item.type"
                         :is-template="Boolean(props.item.data)">
          </resource-type>
          <img class="img-max-100 img-thumbnail float-right ml-3"
               loading="lazy"
               :src="props.item._links.image"
               v-if="props.item._links.image">
          <div class="d-flow-root" v-trim-ws>
            <small>
              <resource-visibility :visibility="props.item.visibility"></resource-visibility>
            </small>
            <strong class="ml-2">{{ props.item.title }}</strong>
          </div>
          <span>@{{ props.item.identifier }}</span>
          <div class="mt-2">
            <span class="text-muted" v-if="props.item.plain_description">
              {{ kadi.utils.truncate(props.item.plain_description, 150) }}
            </span>
            <em class="text-muted" v-else>{{ $t('No description.') }}</em>
          </div>
        </a>
      </div>
      <div class="card-footer py-1">
        <small class="text-muted">
          {{ $t('Last modified') }} <from-now :timestamp="props.item.last_modified"></from-now>
        </small>
      </div>
    </template>
  </card-deck>
</template>

<script>
export default {
  props: {
    resources: Array,
  },
};
</script>
