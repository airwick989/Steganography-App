import { BrowserRouter as Router, Route ,Link, Routes} from "react-router-dom";
import Login from "./Components/Login/Login";
import Uploader from "./Components/Uploader/Uploader";

function App() {
  return (
    <div className="App">
      <Router>
        <Routes>
        <Route exact path="/" element={<Login />} />
        <Route exact path="upload" element={<Uploader />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;