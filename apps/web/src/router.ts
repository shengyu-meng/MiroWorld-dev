import { createRouter, createWebHistory } from 'vue-router'

import EntryView from '@/views/EntryView.vue'
import StageView from '@/views/StageView.vue'

export default createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: EntryView,
    },
    {
      path: '/world/:projectId',
      component: StageView,
      props: true,
    },
  ],
})
