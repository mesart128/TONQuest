import { createRoot } from 'react-dom/client';
import { Provider } from 'react-redux';
import './index.css';
import App from './App';
import { store, persistor } from './store';
import { PersistGate } from 'redux-persist/integration/react';
createRoot(document.getElementById('root')).render(React.createElement(Provider, { store: store },
    React.createElement(PersistGate, { loading: null, persistor: persistor },
        React.createElement(App, null))));
