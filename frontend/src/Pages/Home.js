import "./styles/Home.css";
import "../App.css";
import { NavLink } from "react-router-dom";
import moebius9 from "./images/moebius9.jpeg";

function Home() {
	const backgroundImageStyle = {
		backgroundImage: `linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), url(${moebius9})`,
		backgroundSize: "100%", // Adjust the percentage value to scale the image down
		borderRadius: "25px",
		opacity: "1",
	};

	return (
		<div className="home">
			<div className="hero-section" style={backgroundImageStyle}>
				<h1>Your Daily Digest, Brewed Just How You Like It</h1>
				<p className="subscribe-text-home">
					<NavLink
						to="/sign-up"
						className="subscribe-button-home"
						style={{ color: "#fefbf0;" }}
					>
						Subscribe
					</NavLink>
				</p>
			</div>
		</div>
	);
}

export default Home;
