import { NavLink, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import "./styles/Navbar.css";

function NavBar() {
	const [isSignedIn, setIsSignedIn] = useState();
	const navigate = useNavigate();
	useEffect(() => {
		// TODO: Implement logic to check if token is expired first
		setIsSignedIn(localStorage.getItem("access_token") !== null);
	});

	const handleLogout = () => {
		localStorage.clear();
		navigate("/");
	};

	return (
		<div className="navbar">
			{/* <div id="left-div" style={{ width: "10px" }}></div> */}
			{/* <NavLink to="/">
				<img src="/logo.svg" alt="Logo" className="logo" />
			</NavLink> */}
			{/* {isSignedIn ? (
				<button className="logout-button" onClick={handleLogout}>
					<p>Log out</p>
				</button>
			) : (
				<NavLink to="/sign-in" className="sign-in-nav">
					<p>Sign in</p>
				</NavLink>
			)} */}
		</div>
	);
}

export default NavBar;
