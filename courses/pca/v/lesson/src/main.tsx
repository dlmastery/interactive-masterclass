import {createRoot} from 'react-dom/client';
import {App} from './App.tsx';
import './style.css';
const root=document.getElementById('app-shell');
if(!root)throw new Error('Missing app-shell');
createRoot(root).render(<App/>);
