import React, { useState, useEffect, useRef } from "react";
import { useWhisper } from "@chengsokdara/use-whisper";
import "./styles/Newsletter.css";
import { useLocation } from "react-router-dom";
import moebius1 from "./images/moebius1.png";
import moebius2 from "./images/moebius2.jpeg";
import moebius3 from "./images/moebius3.jpeg";
import moebius4 from "./images/moebius4.jpeg";
import moebius5 from "./images/moebius5.jpeg";
import moebius6 from "./images/moebius6.jpeg";
import moebius7 from "./images/moebius7.jpeg";
import moebius8 from "./images/moebius8.jpeg";

function Example3() {
	const [isRecording, setIsRecording] = useState(false);
	const [showResponse, setShowResponse] = useState(false);
	const [response, setResponse] = useState("");

	// const { state } = useLocation();
	const newsletter = {
		"NBA Draft Highlights":
			"<p>The NBA draft is always an exciting time for basketball fans, and this year's draft did not disappoint. Let's take a look at some of the standout picks and potential steals from the 2023 NBA draft.</p>\n<p>First up, we have Amen Thompson, a talented playmaker from Overtime Elite. Thompson was selected with the No. 4 overall pick by the Houston Rockets <a href=https://bleacherreport.com/articles/10075466-amen-thompsons-draft-scouting-report-pro-comparison-updated-rockets-roster>(Bleacher Report)</a>. With his exceptional skills on the court, Thompson is expected to make an immediate impact in the NBA.</p>\n<p>Next, we have Emoni Bates, a forward from Eastern Michigan. Despite being selected 49th overall by the Cleveland Cavaliers <a href=https://bleacherreport.com/articles/10080378-emoni-bates-pick-welcomed-by-cavaliers-fans-during-2nd-round-of-2023-nba-draft>(Bleacher Report)</a>, Bates has the potential to be the steal of the draft. Once considered the No. 1 prospect, Bates brings a versatile skill set and a strong basketball IQ to the table, making him a valuable addition to any team.</p>\n<p>Lastly, we have Dariq Whitehead, a sharpshooter from Duke University. The Brooklyn Nets selected Whitehead with the No. 22 overall pick <a href=https://bleacherreport.com/articles/10075506-dariq-whiteheads-draft-scouting-report-pro-comparison-updated-nets-roster>(Bleacher Report)</a>. Known for his exceptional shooting ability, Whitehead will provide the Nets with a much-needed outside threat, further strengthening their offensive arsenal.</p>\n<p>Overall, the 2023 NBA draft showcased a wealth of talent and potential, with Thompson, Bates, and Whitehead being just a few of the standout players. It will be exciting to see how these young stars develop and contribute to their respective teams in the coming seasons.</p>",
		"NBA Draft Surprises and Trades":
			"<p>In the world of professional basketball, the NBA draft is always an exciting time filled with surprises and trades. This year was no exception, as several unexpected moves and acquisitions took place. Let's dive into some of the highlights.</p>\n<p>First up, we have Kevin Murphy of the 3 Headed Monsters. Murphy, a Tennessee Tech product and former NBA second-round pick, has been making waves in the international basketball scene <a href=https://bleacherreport.com/articles/10080256-big3-basketball-league-2023-season-schedule-and-full-team-rosters>(Bleacher Report)</a>. His skill and talent have caught the attention of many, and it will be interesting to see how his career progresses.</p>\n<p>Next, we turn our attention to Brandin Podziemski, who was selected by the Golden State Warriors with the 19th overall pick in the 2023 NBA draft <a href=https://bleacherreport.com/articles/10080520-warriors-brandin-podziemski-im-a-triple-double-guy-in-the-nba-in-a-few-seasons>(Bleacher Report)</a>. While this pick raised some eyebrows, Podziemski's confidence and potential have eased any doubts. The Warriors clearly see something special in him, and we can't wait to see him in action.</p>\n<p>Speaking of the Golden State Warriors, they made another surprising move by trading Jordan Poole to the Washington Wizards for veteran Chris Paul <a href=https://bleacherreport.com/articles/10080497-warriors-steve-kerr-on-chris-paul-jordan-poole-trade-we-sensed-we-needed-a-shift>(Bleacher Report)</a>. Head coach Steve Kerr believes that Paul's experience and leadership will greatly benefit the team. This trade has certainly sparked Newsletters among fans and analysts alike.</p>\n<p>Lastly, the Oklahoma City Thunder made a solid move by acquiring Cason Wallace, a talented guard from Kentucky <a href=https://bleacherreport.com/articles/10075751-cason-wallaces-draft-scouting-report-pro-comparison-updated-thunder-roster>(Bleacher Report)</a>. Initially selected by the Dallas Mavericks with the No. 10 overall pick, Wallace brings a versatile skill set to the Thunder. He is expected to make an impact on the court and contribute to the team's success.</p>\n<p>Overall, the NBA draft was full of surprises and trades, showcasing the ever-changing landscape of the league. These moves have generated excitement and anticipation among fans, as they eagerly await the upcoming season.</p>",
		"NBA Draft Updates":
			"<p>The NBA draft is always an exciting time for basketball fans, and this year's draft did not disappoint. Let's take a look at some of the key highlights and moves that took place.</p>\n<p>First up, the Portland Trail Blazers made a splash in the draft by selecting Scoot Henderson with the 3rd overall pick. Henderson is a promising young talent who is expected to make an immediate impact on the team <a href=https://bleacherreport.com/articles/10080452-blazers-gm-on-scoot-henderson-rather-have-the-shorter-guy-whos-the-better-player>(Bleacher Report)</a>.</p>\n<p>Meanwhile, the Minnesota Timberwolves added some firepower to their roster by selecting Leonard Miller with the No. 33 overall pick. Miller, who previously played for the NBA G League Ignite, is known for his scoring ability and versatility <a href=https://bleacherreport.com/articles/10075890-leonard-millers-draft-scouting-report-pro-comparison-updated-timberwolves-roster>(Bleacher Report)</a>.</p>\n<p>In other news, the Minnesota Timberwolves have a rising star in their midst. Rudy Gobert, the talented center known for his defensive prowess, has been making waves in the league. Gobert's future with the Timberwolves is looking bright, as he continues to excel on the court <a href=https://bleacherreport.com/articles/10080273-non-us-countries-that-have-produced-the-most-nba-draft-picks-in-the-last-10-years>(Bleacher Report)</a>.</p>\n<p>Shifting our focus back to the Portland Trail Blazers, there have been rumors surrounding the future of star point guard Damian Lillard. However, recent reports suggest that trade discussions involving Lillard have been discontinued, indicating that he may be staying with the team for the foreseeable future <a href=https://bleacherreport.com/articles/10080381-haynes-damian-lillard-hasnt-had-any-recent-talks-with-blazers-amid-trade-rumors>(Bleacher Report)</a>.</p>\n<p>Lastly, the Blazers have been actively searching for another star player to complement Lillard. However, one veteran forward, whose name has not been disclosed, is reportedly not on their radar. It remains to be seen who the Blazers will ultimately acquire to strengthen their roster <a href=https://bleacherreport.com/articles/10080533-paul-george-trade-rumors-blazers-were-not-eager-to-pair-star-with-damian-lillard>(Bleacher Report)</a>.</p>\n<p>Overall, the NBA draft has brought about some exciting changes and developments for various teams. Fans can look forward to seeing how these new additions and potential trades will shape the upcoming season.</p>",
		"NBA Draft and International Basketball Updates":
			"<p>In the world of basketball, there are exciting developments on both the international and NBA draft fronts. Philadelphia 76ers star Joel Embiid, who holds dual citizenship in two countries, is still contemplating whether he will compete in the 2024 Paris Olympics <a href=https://bleacherreport.com/articles/10080551-report-joel-embiid-quietly-being-recruited-by-team-usa-france-for-2024-olympics>(Bleacher Report)</a>. Meanwhile, NBA scouting departments are gearing up to evaluate prospects for the 2024 draft after the conclusion of the summer league in July <a href=https://bleacherreport.com/articles/10080322-way-too-soon-2024-nba-mock-draft-lottery-edition>(Bleacher Report)</a>. One player who will be making an appearance on the international stage is the reigning NBA Rookie of the Year, who is set to join Team USA for the 2023 FIBA World Cup this summer <a href=https://bleacherreport.com/articles/10080507-magics-paolo-banchero-reportedly-to-play-for-team-usa-at-2023-fiba-world-cup>(Bleacher Report)</a>. Looking ahead to next year's NBA draft, although it may not have the same star power as the 2023 class, there are still some notable names on the prospective list, including potential G League Ignite stars <a href=https://bleacherreport.com/articles/10080021-bronny-james-top-potential-landing-spots-in-2024-after-2023-nba-draft>(Bleacher Report)</a>. Lastly, it's important to remember that players selected in the teens of the NBA draft first round have the potential to blossom into superstars, as we've seen with the likes of Shai Gilgeous-Alexander and Giannis Antetokounmpo <a href=https://bleacherreport.com/articles/10080352-gradey-dick-hyped-as-a-steal-by-fans-after-raptors-take-sg-in-2023-nba-draft>(Bleacher Report)</a>.</p>",
		"NBA Draft: Spurs Secure Promising Prospect, Popovich Downplays Comparisons":
			"<p>The San Antonio Spurs made a strategic move by selecting Victor Wembanyama as their top pick in the NBA draft <a href=https://bleacherreport.com/articles/10080250-2023-nba-draft-live-grades-for-every-pick>(Bleacher Report)</a>. Standing tall with immense potential, Wembanyama has already caught the attention of basketball enthusiasts. Following his arrival in San Antonio, the young prospect had the privilege of dining with Spurs legends, setting the stage for his promising future <a href=https://bleacherreport.com/articles/10080531-spurs-victor-wembanyama-had-dinner-with-duncan-ginobili-robinson-after-nba-draft>(Bleacher Report)</a>. However, head coach Gregg Popovich remains grounded, refusing to indulge in comparisons between Wembanyama and other notable players who entered the league <a href=https://bleacherreport.com/articles/10080549-spurs-popovich-victor-wembanyama-shouldnt-be-compared-to-lebron-kobe-duncan>(Bleacher Report)</a>. Meanwhile, the Utah Jazz secured Baylor shooting guard Keyonte George with the 16th overall pick, adding depth and skill to their roster <a href=https://bleacherreport.com/articles/10075645-keyonte-georges-draft-scouting-report-pro-comparison-updated-jazz-roster>(Bleacher Report)</a>. On the other hand, the Portland Trail Blazers may have missed out on Wembanyama, but they made a solid choice by selecting a talented player from the NBA G League Ignite <a href=https://bleacherreport.com/articles/10075762-scoot-hendersons-draft-scouting-report-pro-comparison-updated-trail-blazers-roster>(Bleacher Report)</a>. The NBA draft has certainly set the stage for exciting developments in the league, with teams making strategic moves to secure promising prospects and strengthen their rosters.</p>",
		"NBA News Roundup":
			"<p>In the world of professional basketball, there is always excitement and anticipation surrounding the NBA draft and potential player moves. Let's dive into some recent developments that have caught the attention of fans and analysts alike.</p>\n<p>First up, we have Rayan Rupert, a promising talent who gained valuable experience in the National Basketball League last season. After making an impact there, Rupert is now ready to take on the NBA. He was recently selected in the draft, and fans are eager to see how he will perform at the highest level of the sport <a href=https://bleacherreport.com/articles/10075732-rayan-ruperts-draft-scouting-report-pro-comparison-updated-trail-blazers-roster>(Bleacher Report)</a>.</p>\n<p>Next, we turn our attention to the Charlotte Hornets, who made a significant move during the draft. They chose Nick Smith Jr., a talented guard from Arkansas, with the 27th pick. This selection has generated a lot of buzz, as many believe the Hornets have found a hidden gem. Fans are excited to see how Smith Jr. will contribute to the team's success <a href=https://bleacherreport.com/articles/10075597-nick-smith-jrs-draft-scouting-report-pro-comparison-updated-hornets-roster>(Bleacher Report)</a>.</p>\n<p>Lastly, we have two defensive stalwarts, Dillon Brooks and Patrick Beverley, who are expected to be on the move this summer. Both players have earned reputations as irritants on the court, and their tenacious defense has made them hot commodities in the NBA. As they become available in the market, teams will be vying for their services, hoping to bolster their defensive prowess. It will be interesting to see where these two players end up and how their new teams will benefit from their skills <a href=https://bleacherreport.com/articles/10079482-dillon-brooks-patrick-beverleys-top-free-agent-landing-spots-after-2023-nba-draft>(Bleacher Report)</a>.</p>\n<p>Stay tuned for more updates as the NBA offseason continues to unfold!</p>",
		"NBA Offseason Trades: Knicks' Pursuit of Donovan Mitchell and Celtics' Trade of Marcus Smart":
			"<p>In a surprising turn of events, the New York Knicks are reportedly determined to acquire Donovan Mitchell, the star shooting guard for the Utah Jazz. After failing to secure Mitchell last offseason, the Knicks are motivated to make a strong push for him this time around. This comes after a disappointing playoff run where the team struggled to shoot from beyond the arc, shooting under 30 percent from three-point range <a href=https://bleacherreport.com/articles/10080346-buy-or-sell-post-nba-draft-trade-rumors-and-buzz>(Bleacher Report)</a>. Meanwhile, the Boston Celtics made a shocking decision recently by trading away Marcus Smart in a three-team deal that also involved Kristaps Porzingis. Although it was a difficult choice for the Celtics, they are seemingly willing to part ways with Smart in order to make significant changes to their roster <a href=https://bleacherreport.com/articles/10080484-celtics-brad-stevens-talks-marcus-smart-trade-something-we-felt-like-we-had-to-do>(Bleacher Report)</a>.</p>",
		"NBA Trade Rumors and Breakout Players":
			"<p>In the world of professional basketball, there is always a buzz surrounding potential trades and breakout players. Let's dive into some recent news and rumors circulating in the NBA.</p>\n<p>First up, we have the Atlanta Hawks making a move to bolster their roster. Michigan's Kobe Bufkin, who had an impressive season as one of the most improved players and top breakout guards in college basketball, has joined the Hawks after being selected 15th overall in the draft <a href=https://bleacherreport.com/articles/10075646-kobe-bufkins-draft-scouting-report-pro-comparison-updated-hawks-roster>(Bleacher Report)</a>. This acquisition could add some fresh talent and energy to the team.</p>\n<p>Next, there's speculation about a potential trade involving Philadelphia 76ers' Ben Simmons. The Athletic's Jon Krawczynski suggests that a trade involving Karl-Anthony Towns cannot be ruled out completely, and the Brooklyn Nets could be a potential destination <a href=https://bleacherreport.com/articles/10079641-every-teams-top-target-entering-chaotic-nba-trade-free-agency-season>(Bleacher Report)</a>. It's always exciting to see how trade rumors unfold and impact the league.</p>\n<p>Meanwhile, the Atlanta Hawks are actively seeking a trade partner for forward John Collins. According to NBA insider Marc Stein, finding a suitable trade is a top priority for the Hawks this offseason <a href=https://bleacherreport.com/articles/10080538-hawks-rumors-john-collins-trade-is-atlantas-ongoing-top-priority-in-nba-offseason>(Bleacher Report)</a>. This development could lead to significant changes in the team's dynamics.</p>\n<p>Lastly, the Atlanta Hawks are exploring ways to improve their roster with the addition of Toronto Raptors' Pascal Siakam. Siakam has emerged as a key player for the Raptors, and his potential move to the Hawks could shake up the Eastern Conference <a href=https://bleacherreport.com/articles/10080537-pascal-siakam-trade-rumors-hawks-have-tried-to-deal-for-raptors-pf-without-success>(Bleacher Report)</a>. It will be intriguing to see how this situation develops and if Siakam becomes a new force for the Hawks.</p>\n<p>With these trade rumors and breakout players making headlines, the NBA offseason is full of excitement and anticipation. Stay tuned for more updates as teams continue to make moves and shape their rosters.</p>",
		"Sports News Roundup":
			"<p>In the world of sports, there have been some exciting developments that fans won't want to miss. Let's dive right in!</p>\n<p>First up, in Major League Baseball, the Houston Astros have made a strategic move by acquiring infielder Ramón Urías <a href=https://bleacherreport.com/articles/10080309-re-drafting-harper-machado-and-2010-mlb-draft-including-international-prospects>(Bleacher Report)</a>. This addition is sure to strengthen their lineup and provide a boost to their infield defense.</p>\n<p>Meanwhile, the Toronto Blue Jays have made a notable acquisition as well, bringing on outfielder Eddie Rosario <a href=https://bleacherreport.com/articles/10075640-jett-howards-draft-scouting-report-pro-comparison-updated-magic-roster>(Bleacher Report)</a>. Known for his impressive hitting abilities, Rosario is expected to make a significant impact on the team's offensive performance.</p>\n<p>Over in the NBA, the Orlando Magic has made a promising pick in the 2023 NBA draft. They selected Jett Howard, a sharpshooter from Michigan, with the 11th overall pick <a href=https://bleacherreport.com/articles/10080434-dwyane-wade-udonis-haslem-has-had-greatest-career-in-miami-heat-history>(Bleacher Report)</a>. With his shooting skills, Howard is poised to become a valuable asset to the team.</p>\n<p>Speaking of the NBA, Dwyane Wade, a legendary player for the Miami Heat, recently shared his thoughts on who he believes had the best career in the franchise's history. Surprisingly, Wade bestowed this honor on one of his former teammates, not himself <a href=https://bleacherreport.com/articles/10075895-kris-murrays-draft-scouting-report-pro-comparison-updated-trail-blazers-roster>(Bleacher Report)</a>. This revelation has sparked much debate among basketball enthusiasts.</p>\n<p>Lastly, the Portland Trail Blazers made a smart move by selecting Kris Murray, a talented finisher from Iowa, with the 23rd overall pick in the 2023 NBA draft [4]. Murray's ability to score in crucial moments is expected to elevate the Blazers' offensive game.</p>\n<p>These developments in baseball and basketball are sure to captivate sports fans around the world. Stay tuned for more exciting updates!</p>",
		conclusion:
			"Overall, the NBA draft was full of surprises and trades, showcasing the ever-changing landscape of the league. These moves have generated excitement and anticipation among fans, as they eagerly await the upcoming season.",
		introduction:
			"In the world of professional basketball, the NBA draft is always an exciting time filled with surprises and trades. This year was no exception, as several unexpected moves and acquisitions took place. Let's dive into some of the highlights.",
		title: "NBA Draft Surprises and Trades",
	};

	useEffect(() => {
		console.log(newsletter);
	}, []);

	const [newsIndex, setNewsIndex] = useState(0);
	const [audioUrl, setAudioUrl] = useState("");
	const audioRef = useRef(null);

	const sections = Object.entries(newsletter).filter(
		([key]) => key !== "introduction" && key !== "conclusion" && key !== "title"
	);

	const [messages, setMessages] = useState([]);

	const handleUserMessage = (e) => {
		if (e.key === "Enter") {
			e.preventDefault();
			const userInput = e.target.value.trim();
			if (userInput !== "") {
				setMessages((prevMessages) => [
					...prevMessages,
					{ content: userInput, sender: "user" },
				]);
				e.target.value = "";
				setTimeout(() => {
					const botResponse = getBotResponse(userInput);
					setMessages((prevMessages) => [
						...prevMessages,
						{ content: botResponse, sender: "bot" },
					]);
				}, 800); // Add a slight delay to the bot response
			}
		}
	};

	const handleGenerateTTS = () => {
		const { title, introduction, conclusion, ...sections } = newsletter;

		// const text = `${introduction}\n${Object.values(sections)
		// 	.map((section) => section.replace(/<\/?a>/g, ""))
		// 	.join("\n")}\n${conclusion}`;
		fetchAudio(introduction);
	};

	const getBotResponse = (userInput) => {
		// Hardcoded array of bot responses
		const botResponses = [
			"Hello! How can I assist you today? If you have any questions or need help with our products, feel free to ask.",
			"I apologize for the inconvenience. Can you please provide more details? Our team is committed to resolving any issues you may be facing.",
			"Thank you for your inquiry. Our team will get back to you shortly. In the meantime, please let me know if there is anything else I can assist you with.",
			"I understand your concern, but I'm sorry, I cannot provide that information at the moment. We are continuously working to improve our services and expand our knowledge base.",
			"Please try again later. Our systems are currently undergoing maintenance, and we expect to be back up shortly. We appreciate your patience and understanding.",
			// Add more bot responses here
		];
		const randomIndex = Math.floor(Math.random() * botResponses.length);
		return botResponses[randomIndex];
	};

	const fetchAudio = async (text) => {
		console.log("Fetching audio!");
		const response = await fetch(
			"https://api.elevenlabs.io/v1/text-to-speech/cjlys0iHziXap7q8d4rh?optimize_streaming_latency=0",
			{
				method: "POST",
				headers: {
					"Content-Type": "application/json",
					"xi-api-key": "8b9914b4a9e536a1f236e02385f55df9",
					accept: "audio/mpeg",
				},
				body: JSON.stringify({
					text: text,
					model_id: "eleven_monolingual_v1",
					voice_settings: {
						stability: 0.75,
						similarity_boost: 0,
					},
				}),
				responseType: "blob",
			}
		);
		if (response.status === 200) {
			console.log(response);
			const blob = await response.blob();
			console.log(blob);
			const audioUrl = URL.createObjectURL(blob);
			console.log(audioUrl);
			const ttsAudio = document.getElementById("existing-audio");
			ttsAudio.src = audioUrl;
		} else {
			console.log("Error: Unable to stream audio.");
		}
	};
	const [randomImage, setRandomImage] = useState(null);

	useEffect(() => {
		const imageList = [
			moebius1,
			moebius2,
			moebius3,
			moebius4,
			moebius5,
			moebius6,
			moebius7,
			moebius8,
		];

		const randomIndex = Math.floor(Math.random() * imageList.length);
		const randomImage = imageList[randomIndex];

		setRandomImage(randomImage);
	}, []);

	const renderContent = (content) => {
		const pattern = /<a>(.*?)<\/a>/g;
		const matches = content.match(pattern);
		if (matches) {
			matches.forEach((match) => {
				const htmlTag = match.replace(/<\/?a>/g, "");
				content = content.replace(match, htmlTag);
			});
		}
		return content;
	};

	return (
		<div className="Newsletter-wrapper">
			<div className="left-view">
				<div className="tts-wrapper">
					<button
						className="generate-button"
						onClick={() => handleGenerateTTS()}
					>
						Generate TTS
					</button>
					<audio id="existing-audio" controls></audio>
				</div>
				<img
					src={randomImage}
					width="70%"
					style={{ borderRadius: "20px", marginTop: "50px", opacity: "80%" }}
				/>
				<h1>{newsletter["title"]}</h1>
				<p>{newsletter["introduction"]}</p>
				{sections.map(([key, value], index) => (
					<div key={key}>
						<h2>{key}</h2>
						{value.split("\n\n").map((e, index) => (
							<p
								key={index}
								dangerouslySetInnerHTML={{ __html: renderContent(e) }}
							/>
						))}
					</div>
				))}

				<h1>Conclusion</h1>
				<p>{newsletter["conclusion"]}</p>
			</div>
			<div className="right-view">
				<div className="notepad">
					<div className="chat-messages">
						{messages.map((message, index) => (
							<div
								key={index}
								className={`message ${
									message.sender === "user" ? "user" : "bot"
								}`}
							>
								{message.content}
							</div>
						))}
					</div>
					<input
						type="text"
						className="message-input"
						placeholder="Type your message..."
						onKeyDown={handleUserMessage}
					/>
				</div>
			</div>
		</div>
	);
}

export default Example3;
