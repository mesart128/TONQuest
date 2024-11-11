import { createApp } from 'vue';
import App from './App.vue';

const app = createApp(App);

// app.provide(TonConnectUIContext, tonConnectUI);
// app.provide(TonConnectUIOptionsContext, setOptions);

app.mount('#app');
// window.Telegram.WebApp.ready()