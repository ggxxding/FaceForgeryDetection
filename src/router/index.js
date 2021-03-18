import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import Hello from '@/components/Hello'
import elform from '@/components/elform'
import Ping from '@/components/Ping'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'HelloWorld',
      component: HelloWorld,
      redirect:'/Hello',
      meta:{
        title:'title'
      }
    },
    {
      path: '/Hello',
      name: 'Hello',
      component: Hello,
      meta:{
        title:'BERT Cloze Test'
      }
    },
    {
      path: '/ele',
      name: 'ele',
      component: elform
    },
    {
      path: '/ping',
      name: 'ping',
      component: Ping
    }
  ],
  mode: 'history'
})
