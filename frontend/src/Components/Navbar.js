import { NavLink } from "react-router-dom";
import "./styles/Navbar.css";

function NavBar({ isSignedIn }) {
	return (
		<div className="navbar">
			{isSignedIn ? (
				<div></div>
			) : (
				<div id="left-div" style={{ width: "10px" }}></div>
			)}
			<NavLink to="/">
				<img src="/logo.svg" alt="Logo" className="logo" />
			</NavLink>
			{isSignedIn ? (
				<div></div>
			) : (
				<NavLink to="/sign-in" className="sign-in-nav">
					<p>Sign in</p>
				</NavLink>
			)}
		</div>
	);
}

export default NavBar;
