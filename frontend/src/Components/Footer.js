import { NavLink } from "react-router-dom";
import "./styles/Footer.css";

function Footer() {
	return (
		<footer>
			<div className="footer">
				<div className="footer-left">
					the roast &#169;2023 All rights reserved
				</div>
				<div className="footer-right">
					<NavLink to="/">Home </NavLink>
					<NavLink to="/sign-up">Join </NavLink>
				</div>
			</div>
		</footer>
	);
}

export default Footer;
