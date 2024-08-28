import { BrowserRouter, Route } from "react-router-dom";
import "./App.css";
import Footer from "./components/Footer/Footer";
import Header from "./components/Header/Header";
import LandingPage from "./screens/LandingPage/LandingPage";
import MyNotes from "./screens/MyNotes/MyNotes";
import LoginScreen from "./screens/LoginScreen/LoginScreen";
import RegisterScreen from "./screens/RegisterScreen/RegisterScreen";

function App() {
  return (
    <BrowserRouter>
      <Header />
      <main>
        <Route path="/" compponent={LandingPage} exact />
        <Route path="/login" compponent={LoginScreen} exact />
        <Route path="/register" compponent={RegisterScreen} exact />
        <Route path="/mynotes" compponent={() => <MyNotes />} />
      </main>
      <Footer></Footer>
    </BrowserRouter>
  );
}

export default App;
