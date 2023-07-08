import logo from "./logo.svg";
import "./App.css";
import Home from "./Pages/Home";
import Signup from "./Pages/Signup";
import Signin from "./Pages/Signin";
import UserView from "./Pages/UserView";
import NewsTemplate from "./Pages/NewsTemplate";
import Conversation from "./Pages/Conversation";
import CreateNewsTemplate from "./Pages/CreateNewsTemplate";
import Example1 from "./Pages/example1";
import Example2 from "./Pages/example2";
import Example3 from "./Pages/example3";
import Example4 from "./Pages/example4";
import Navbar from "./Components/Navbar";
import {
	BrowserRouter as Router,
	Routes,
	Route,
	Navigate,
} from "react-router-dom";
import { useState } from "react";

function App() {
	return (
		<Router>
			<Navbar isSignedIn={false} />
			<Routes>
				<Route path="/" element={<Home />} />
				<Route path="/sign-up" element={<Signup />} />
				<Route path="/sign-in" element={<Signin />} />
				<Route exact path="/user-view" element={<UserView />} />
				<Route path="/user-view/:flavor" element={<NewsTemplate />} />
				<Route path="/create-digest" element={<CreateNewsTemplate />} />
				<Route path="/example1" element={<Example1 />} />
				<Route path="/example2" element={<Example2 />} />
				<Route path="/example3" element={<Example3 />} />
				<Route path="/example4" element={<Example4 />} />
				<Route path="/conversation" element={<Conversation />} />
			</Routes>
		</Router>
	);
}

export default App;
