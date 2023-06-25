import "./styles/Home.css";
import "../App.css";
import { NavLink } from "react-router-dom";

function Home() {
	return (
		<div className="home">
			<div className="hero-section">
				<h1>Your Daily Digest, Brewed Just How You Like It</h1>
				<p className="subscribe-text">
					<NavLink to="/sign-up" className="subscribe-button">
						Subscribe
					</NavLink>
				</p>
			</div>
		</div>
	);
}

export default Home;
