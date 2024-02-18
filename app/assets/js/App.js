
/*
App is the entry point for the React App
use FunctionsList and FunctionsComponent to trigger the Python functions
*/

import { FunctionsMap } from './functions.js';

class App extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div className="container">
                <img></img>
                <h1>Thanks for using Desktop Wrapper</h1>
                <p>Start Developing now!</p>
                <div className="functions-container">
                    <h1>Custom Functions</h1>
                    {
                        Object.entries(FunctionsMap).map(([funcName, func])=>{
                            return (<p className="function">{funcName}</p>)
                        })
                    }
                </div>
            </div>
        )
    }
}

export {
    App
}
