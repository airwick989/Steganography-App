import { BrowserRouter as Router, Route, Routes} from "react-router-dom";
import Login from "./Components/Login/Login";
import Uploader from "./Components/Uploader/Uploader";
import Home from "./Components/Home/Home";
import Decoder from "./Components/Decoder/Decoder";

function App() {
  return (
    <div className="App">
      <Router>
        <Routes>
        <Route exact path="/" element={<Login />} />
        <Route exact path="upload" element={<Uploader />} />
        <Route exact path="home" element={<Home />} />
        <Route exact path="decode" element={<Decoder />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;