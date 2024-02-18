
import { App } from "./App";

const e = React.createElement;

function createApp() {
    let root = document.getElementById('root');
    const reactRoot = ReactDOM.createRoot(root);
    reactRoot.render(e(App));
}

createApp();
