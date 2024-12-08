import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { Provider } from 'react-redux';
import './index.css';
import App from './App';
import { store, persistor } from './store';
import { PersistGate } from 'redux-persist/integration/react';
import { BrowserRouter } from 'react-router-dom';
import { init } from './init';
import './mockEnv.ts';

const root = createRoot(document.getElementById('root')!);

try {
  // Configure all application dependencies.
  init(true);

  root.render(
    <Provider store={store}>
      <PersistGate loading={null} persistor={persistor}>
        <App />
      </PersistGate>
    </Provider>,
  );
} catch (e) {
  console.error('Error initializing the application:', e);
}
