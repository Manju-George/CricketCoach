import React from 'react';
import {render} from 'react-dom';
import Score from './components/scores/Score';

class App extends React.Component {
    render(){
        return (
            <div>
                <Score />
            </div>

        );
    };
}
render(<App />,window.document.getElementById('app'));


