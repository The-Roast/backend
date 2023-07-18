import "./styles/Home.css";
import "../App.css";
import { NavLink } from "react-router-dom";
import moebius9 from "./images/moebius9.jpeg";
import Signup from "./Signup";
import logo from "../logos/the-roast-logo.png";
import NYT from "../logos/ny-times-logo.png";
import Reddit from "../logos/reddit-logo.png";
import WSJ from "../logos/wsj-logo.png";
import BleacherReport from "../logos/bleacher-report-logo.png";
import TechCrunch from "../logos/tech-crunch-logo.png";
import Politico from "../logos/politico-logo.png";
import FoxNews from "../logos/fox-news-logo.png";

function Home() {
	return (
		<div className="home">
			<div className="page-wrapper">
				<div className="home-page">
					<div className="news-navbar">
						<NavLink to="/sign-up">Subscribe </NavLink>
						<NavLink to="/sign-in">Sign in </NavLink>
					</div>
					<div className="news-header">
						<img src={logo} className="company-logo" />
						<p>Newsletters powered by AI</p>
					</div>
					<div className="news-sources">
						<p>Sourced from</p>
						<img src={NYT} />
						<img src={Reddit} />
						<img src={WSJ} />
						<img src={BleacherReport} />
						<img src={TechCrunch} />
						<img src={Politico} />
						<img src={FoxNews} />
					</div>
					<div className="news-body">
						<div className="side-column">
							<div className="news-blurb">
								<label>By GPT-4</label>
								<h1>A Tapestry of Truth</h1>
								<p>
									Sip on the essence of unwavering trust as The Roast
									meticulously sources information from credible and reliable
									outlets. With each cup served, indulge in a rich blend of
									accurate and substantiated news, expertly crafted by. A
									deliciously reliable concoction, brewed to satisfy the
									discerning reader's thirst for dependable insights.
								</p>
							</div>
							<hr />

							<div className="news-blurb">
								<label>By Pi</label>
								<h1>A Personality as Unique as You</h1>
								<p>
									Tired of generic news roundups that don’t align with your
									interests? The latest AI-driven digest tools allow you to
									craft a customized briefing as unique as your personality.
									Configure your ideal mix of topics, sources, length and
									frequency to design a personalized news playlist aligned with
									your passions. Want tech but not business? Give the AI
									guidance to tune your feed. Prefer breezy overviews instead of
									longreads?
									<br />
									<br />
									Adjust settings for quick hits. With sophisticated algorithms,
									your curated digest can learn from your feedback, adapting its
									selections over time to your taste. But will this usher in an
									era of narrowmindedness? Experts weigh merits and perils of
									ever-more-personalized news diets. The power is now yours to
									get only the news that fits - for better or worse. This month
									we explore the promise and pitfalls of bespoke AI curation
									tailored to you.
								</p>
							</div>
						</div>
						<div className="main-column">
							<h1>
								<i>Read our Free Sample!</i>
							</h1>
						</div>
						<div className="side-column">
							<div className="news-blurb">
								<label>By Claude</label>
								<h1>While You Wait: Don't Miss What Matters</h1>
								<p>
									By rapidly parsing myriad sources using A.I., this service
									curates pithy briefs about the latest happenings whenever and
									wherever you please. Get your fill of customizable updates
									instantly about any topic from breaking news to celebrity
									gossip, be it an amuse-bouche to start your day or palate
									cleanser on-the-go. The Roast pledges to distill the torrent
									of 24/7 reporting into essential elixirs on-demand.
								</p>
							</div>
							<hr />
							<div className="news-blurb">
								<label>By Bard</label>
								<h1>Your Digest Your Way</h1>
								<p>
									One marvels at the felicitous customizability of The Roast,
									enabling the harried reader to mold his news bulletin to suit
									his temperament. Like a craftsman finessing a wireless, one
									fine-tunes the thing to one's liking—fiddling with the
									figurative dials and levers to caliber the info feed just so.
									Specify which timely topics to track, stipulate the word count
									that suits your schedule, handpick the erudite outlets that
									tickle your fancy. Suddenly, you grasp the editorial reins,
									piloting your own vessel through the news-scape’s choppy seas,
									retaining only the most cogent bulletins, tossing the
									unnecessary jetsam. For the technically inclined, it culls
									solely from engineering annuals, sparing you more prosaic
									fare.
									<br />
									<br />
									For the man perpetually on-the-go, it concocts a telegraphic
									briefing perfect for absorbing en route to the next
									appointment. In this era of excessive reportage, a tool for
									parsing the signal from the babel is a godsend. By tweezing
									only the most salient briefs for one’s daily media diet, The
									Roast conquers the info torrents, keeping one’s head above
									water and sanity intact.
								</p>
								<hr />
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	);
}

export default Home;
