<template>
  <!-- <TonConnectButton /> -->
  <!-- <div class="buttonbox" v-on:click="tonConnectUI.openModal()" style="width: 200px; height: 200px; background-color: black;"></div> -->
  <div v-if="this.loading !== true">
    <div class="user">
      <!-- <div class="user-icon"> -->
          <!-- <img src="https://t.me/i/userpic/160/ASEEL_SALAH1.jpg"> -->
      <!-- </div> -->
      <div class="user-content">
          <div class="user-title">{{this.user.name}}</div>
          <div class="user-xp">{{this.user.xp}}</div>
      </div>
    </div>
    <vue-tree
      style="width: 100%; height: 100vh;"
      :dataset="tasksk"
      :config="treeConfig"
      :collapseEnabled="false"
      linkStyle="straight"
      direction="vertical"
    >
      <template v-slot:node="{ node, collapsed }">
        <div class="task task-inactive" v-on:click="clickTask(node.id, node.external_url)" v-on:touchend="clickTask(node.id, node.external_url)">
          <div :class="{'inactive-filter': !node.active}"></div>
          <div :class="{'completed-filter': user.completed_tasks.includes(node.id)}"></div>
          <div class="task-icon">
              <img :src=node.icon>
          </div>
          <div class="task-content"> 
              <div class="task-title">{{ node.title }}</div>
              <div class="task-xp">{{ node.xp }} xp</div>
          </div>
      </div>
      </template>
    </vue-tree>
  </div>
</template>

<!-- <template>
  <TonConnectButton/>
</template> -->

<script>
import VueTree from "@ssthouse/vue3-tree-chart";
import "@ssthouse/vue3-tree-chart/dist/vue3-tree-chart.css";
import {TonConnectUI} from '@tonconnect/ui'

const apiurl = 'https://cleanly-engaging-pegasus.ngrok-free.app/'
const tonConnectUI = new TonConnectUI({
      manifestUrl: 'https://gist.githubusercontent.com/siandreev/75f1a2ccf2f3b4e2771f6089aeb06d7f/raw/d4986344010ec7a2d1cc8a2a9baa57de37aaccb8/gistfile1.txt',
    });

console.log()
// import Task from "./components/Task.vue";
// const { open } = useTonConnectModal();
// open();

export default {
  name: "treemap",
  components: { VueTree},
  data() {
    return {
      loading: true,
      user: {id: 110, completed_tasks: [1]},
      tasksk: {
        id: -1,
        title: "Connect Wallet",
        icon: "https://cryptologos.cc/logos/toncoin-ton-logo.png",
        xp: 100,
        active: true,
        children: [
          
        ],
        links: [
          { parent: 1, child: 2 },
          { parent: 3, child: 2 },
          { parent: 4, child: 2 },
        ],
        identifier: "customID",
      },
      treeConfig: { nodeWidth: 150, nodeHeight: 80, levelHeight: 120 },
    };
  },
  methods: {
    touchHandler(event) {
        var touches = event.changedTouches,
          first = touches[0],
          type = "";
      switch(event.type)
      {
          case "touchstart": type = "mousedown"; break;
          case "touchmove":  type = "mousemove"; break;        
          case "touchend":   type = "mouseup";   break;
          default:           return;
      }

      // initMouseEvent(type, canBubble, cancelable, view, clickCount, 
      //                screenX, screenY, clientX, clientY, ctrlKey, 
      //                altKey, shiftKey, metaKey, button, relatedTarget);

      var simulatedEvent = document.createEvent("MouseEvent");
      simulatedEvent.initMouseEvent(type, true, true, window, 1, 
                                    first.screenX, first.screenY, 
                                    first.clientX, first.clientY, false, 
                                    false, false, false, 0/*left*/, null);

      first.target.dispatchEvent(simulatedEvent);
      event.preventDefault();
    },
    getTasks() {
      let tasks = fetch("http://localhost:3000/tasks")
        .then((response) => response.json())
        .then((data) => {
          this.tasks = data;
        });
    },
    async clickTask(task_id, external_url) {
      console.log(task_id);
      if (task_id === -1) {
        await tonConnectUI.openModal();
      }
      else {
        window.Telegram.WebApp.openLink(external_url);
      }
    },
    async getUser(user_id) {
      let data =  await fetch(apiurl + "users/" + user_id, {
        headers: {
          "ngrok-skip-browser-warning": "true",
        },
      })
      return await data.json();
    },
    async createUser(user_data) {
      let data =  await fetch(apiurl + "users/", {
        method: "POST",
        headers: {
          "ngrok-skip-browser-warning": "true",
          "Content-Type": "application/json",
        },
        body: JSON.stringify(user_data),
      })
      return await data.json();
    }
  },
  async mounted() {
    document.getElementById('app').addEventListener("touchstart", this.touchHandler, true);
    document.getElementById('app').addEventListener("touchmove", this.touchHandler, true);
    document.getElementById('app').addEventListener("touchend", this.touchHandler, true);
    document.getElementById('app').addEventListener("touchcancel", this.touchHandler, true);  
    // fetch(apiurl + "users/" + window.Telegram.WebApp.initDataUnsafe.user.id, {
    //   headers: {
    //         "ngrok-skip-browser-warning": "true",
    //       },
    // })
    //   .then((response) => this.user = response.json().then((data) => {
    //     if (data.error) {
    //       fetch(apiurl + "users/", {
    //         method: "POST",
    //         headers: {
    //           "ngrok-skip-browser-warning": "true",
    //           "Content-Type": "application/json",
    //         },
    //         body: JSON.stringify({id: window.Telegram.WebApp.initDataUnsafe.user.id, name: window.Telegram.WebApp.initDataUnsafe.user.first_name, profile_photo: ''}),
    //       }).then((response) => this.user = response.json().then((data) => this.user = data))
    //     }
    //     else {
    //       this.user = data;
    //     }
    //     if (this.user.address !== "") {
    //       this.user.completed_tasks.push(-1);
    //     }
    //   }))
    let user = await this.getUser(window.Telegram.WebApp.initDataUnsafe.user.id);
    console.log(user);
    if (user.error) {
        await this.createUser({id: window.Telegram.WebApp.initDataUnsafe.user.id, name: window.Telegram.WebApp.initDataUnsafe.user.first_name, profile_photo: ''});
        this.user = await this.getUser(window.Telegram.WebApp.initDataUnsafe.user.id);
    }
    else {
      this.user = user;
    }
    
    if (this.user.address !== "") {
      this.user.completed_tasks.push(-1);
    }


    fetch(apiurl + "tasks", {
      headers: {
            "ngrok-skip-browser-warning": "true",
          },
    })
      .then((response) => this.tasks = response.json().then((data) => this.tasksk.children = data))
    
    setTimeout(() => {
      this.loading = false;
    }, 4000);
    console.log(this.user);
    // this.getTasks();
    tonConnectUI.onStatusChange((wallet) => {
      if (wallet.account.address) {
        console.log('Wallet connected:mhznvcbdamnbBND MSNAMDNAMSNBDMANSBDMNABSMDNBMASBCDVsgajdhagcsdvasgnndg', wallet);
        fetch(apiurl + "users/address/" + window.Telegram.WebApp.initDataUnsafe.user.id + "/" + wallet.account.address, {
          method: "GET",
          headers: {
            "ngrok-skip-browser-warning": "true",
          },
        }).then((response) => {
        this.user.completed_tasks.push(-1);
        this.user.xp += 300;
        this.getUser(window.Telegram.WebApp.initDataUnsafe.user.id).then((data) => this.user = data);
        })
      } else {
        console.log('Wallet disconnected');
      }
    });

    

    
  },
    
};
</script>

<style>
body {
  font-family: 'Roboto', sans-serif;
  margin: 0;
  padding: 0;
}

.task {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: #2D2D2D;
  padding: 10px;
  border-radius: 7px;
  width: fit-content;
  user-select: none;
  position: relative;
}

.task-icon {
  padding: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 7px;  
  background-color: #484848;
}

.task-icon img {
  width: 35px;
  height: 35px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.task-content {
  display: flex;
  flex-direction: column;
  margin-left: 10px;
}

.task-title {
  font-size: 16px;
  font-weight: medium;
  color: #fff;
  /* height: 20px; */
  width: 125px;
  overflow: hidden;
}

.task-xp {
  font-size: 14px;
  color: #868686;
}

.container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.rich-media-node {
  width: auto;
  padding: 8px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: center;
  color: white;
  background-color: #f7c616;
  border-radius: 4px;
}

.inactive-filter {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  border-radius: inherit;
  cursor: default;
}

.completed-filter {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(36, 200, 0, 0.3);
  border-radius: inherit;
}

.user {
  display: flex;
  width: 100%;
  height: 100px;
  background-color: #1A1A1A;
  padding: 20px;
  box-sizing: border-box;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 15;
}

.user-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 120px;
  /* height: 100px; */
  border-radius: 50%;
}

.user-icon img {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  border-radius: 50%;
}

.user-content {
  display: flex;
  justify-content: space-between;
  margin-left: 10px;
  width: 100%;
  padding: 20px;
  align-items: center;
  font-size: 24px;
  font-family: 'Roboto', sans-serif;
  
  color: white;
}

.loading {
  display: none;
}

</style>
