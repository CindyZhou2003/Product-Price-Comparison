import logo from './img/logo.svg';
import './css/App.css';
import Login from './components/Login';
import SignUp from './components/Signup';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';


function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/signup" element={<SignUp />} />
      </Routes>
    </Router>
  );
}

export default App;


// {/*<header className="App-header">*/}
//       {/*  <img src={logo} className="App-logo" alt="logo" />*/}
//       {/*  <p>*/}
//       {/*    Edit <code>src/App.js</code> and save to reload.*/}
//       {/*  </p>*/}
//       {/*  <a*/}
//       {/*    className="App-link"*/}
//       {/*    href="https://reactjs.org"*/}
//       {/*    target="_blank"*/}
//       {/*    rel="noopener noreferrer"*/}
//       {/*  >*/}
//       {/*    Learn React*/}
//       {/*  </a>*/}
//       {/*</header>*/}