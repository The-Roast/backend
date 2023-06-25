import logo from "./logo.svg";
import "./App.css";
import Home from "./Pages/Home";
import Signup from "./Pages/Signup";
import Signin from "./Pages/Signin";
import UserView from "./Pages/UserView";
import NewsTemplate from "./Pages/NewsTemplate";
import Conversation from "./Pages/Conversation";
import CreateNewsTemplate from "./Pages/CreateNewsTemplate";
import Navbar from "./Components/Navbar";
import Footer from "./Components/Footer";
import {
	BrowserRouter as Router,
	Routes,
	Route,
	Navigate,
} from "react-router-dom";
import { useState } from "react";

function App() {
	const [isSignedIn, setIsSignedIn] = useState(false);
	// console.log(isSignedIn);
	return (
		<Router>
			<Navbar isSignedIn={isSignedIn} />
			<Routes>
				<Route path="/" element={<Home />} />
				<Route
					path="/sign-up"
					element={
						<Signup isSignedIn={isSignedIn} setIsSignedIn={setIsSignedIn} />
					}
				/>
				<Route
					path="/sign-in"
					element={<Signin setIsSignedIn={setIsSignedIn} />}
				/>
				<Route
					exact
					path="/user-view"
					element={<UserView isSignedIn={isSignedIn} />}
				/>
				<Route path="/user-view/:flavor" element={<NewsTemplate />} />
				<Route path="/create-digest" element={<CreateNewsTemplate />} />
				<Route
					path="/conversation"
					element={<Conversation setIsSignedIn={setIsSignedIn} />}
				/>
				<Route
					path=""
					element={
						isSignedIn ? (
							<Route element={<Navigate to="/user-view" />} />
						) : (
							<Route element={<Navigate to="/sign-up" />} />
						)
					}
				/>
			</Routes>
			{/* <Footer /> */}
		</Router>
	);
}

export default App;
