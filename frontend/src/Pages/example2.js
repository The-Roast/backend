import React, { useState, useEffect, useRef } from "react";
import { useWhisper } from "@chengsokdara/use-whisper";
import "./styles/Conversation.css";
import XI_API_KEY from "../Config";
import { useLocation } from "react-router-dom";
import moebius1 from "./images/moebius1.png";
import moebius2 from "./images/moebius2.jpeg";
import moebius3 from "./images/moebius3.jpeg";
import moebius4 from "./images/moebius4.jpeg";
import moebius5 from "./images/moebius5.jpeg";
import moebius6 from "./images/moebius6.jpeg";
import moebius7 from "./images/moebius7.jpeg";
import moebius8 from "./images/moebius8.jpeg";

function Example2({ setIsSignedIn }) {
	const [isRecording, setIsRecording] = useState(false);
	const [showResponse, setShowResponse] = useState(false);
	const [response, setResponse] = useState("");

	// const { state } = useLocation();
	const newsletter = {
		"In the News: Tsitsipas Clarifies Comments, Aussies Discover 'Bazball'":
			"<p>In a recent Netflix documentary, Break Point, comments made by Stefanos Tsitsipas about Nick Kyrgios at last year's Wimbledon were featured and perceived as controversial. However, Tsitsipas has now clarified that his remarks were misinterpreted <a href=https://www.bbc.co.uk/sport/av/basketball/65997138>(BBC News)</a>. Meanwhile, Australians have recently learned about a 19-year-old basketball sensation named Baz, whose skills have garnered attention <a href=https://www.independent.co.uk/news/espn-ap-nba-san-antonio-spurs-abc-b2363390.html>(Independent)</a>.</p>",
		"NBA Draft Highlights: SEC Players, Tennessee's Success, and Historic Night for Penn State":
			"<p>The 2023 NBA draft took place on Thursday night, and it was a night full of excitement and historic moments. Ten former SEC players were celebrated as draft picks, with six of them going in the first round <a href=https://volswire.usatoday.com/lists/every-tennessee-vols-basketball-player-selected-in-nba-draft-since-2000/>(USA Today)</a>. Tennessee, under the leadership of head coach Rick Barnes, has been a consistent producer of NBA draft selections, with 12 players drafted since 2000 <a href=https://nittanylionswire.usatoday.com/2023/06/24/andrew-funk-lands-nba-summer-league-deal-with-nba-champs/>(USA Today)</a>. Another highlight of the night was the historic moment for Penn State basketball, as Jalen Pickett and Seth Lundy became the first duo from Penn State to be drafted in the same year <a href=https://rolltidewire.usatoday.com/2023/06/23/alabama-basketball-nate-oats-alabama-are-quickly-becoming-an-nba-pipeline/>(USA Today)</a>. Additionally, the Alabama men's basketball program experienced a significant turnaround in terms of NBA draft picks after the hiring of coach Nate Oats in 2019 [7]. The Portland Trail Blazers made a notable selection in Scoot Henderson with the 3rd overall pick <a href=https://deadspin.com/nba-draft-grades-warriors-heat-celtics-mavs-lakers-jazz-1850571706>(Deadspin)</a>. Overall, the draft showcased the talent and potential of these players and the impact they could have in the NBA.</p>",
		"NBA News: Rising Star Rayan Rupert Ready for NBA Debut; Defensive Duo Dillon Brooks and Patrick Beverley on the Move":
			"<p>In the world of professional basketball, exciting developments are taking place as new talents emerge and seasoned players prepare for potential moves. Rayan Rupert, who gained valuable experience in the National Basketball League last season, is now poised to make his mark in the NBA. After being selected <a href=https://bleacherreport.com/articles/10079482-dillon-brooks-patrick-beverleys-top-free-agent-landing-spots-after-2023-nba-draft>(Bleacher Report)</a>, Rupert is eager to showcase his skills and contribute to the league. Meanwhile, two of the NBA's most notorious defensive irritants, Dillon Brooks and Patrick Beverley, are expected to switch teams this summer, generating considerable interest among potential suitors. Brooks and Beverley have established themselves as formidable forces on the defensive end, and their availability in the market is sure to attract attention [2]. Stay tuned for more updates on these intriguing developments in the world of professional basketball!</p>",
		"NBA Trade Updates and Player Moves":
			"<p>In recent NBA news, the Boston Celtics made a three-team trade that brought in Kristaps Porzingis but saw Marcus Smart head to the Memphis Grizzlies <a href=https://www.espn.com/nba/story/_/id/37903852/brad-stevens-porzingis-best-level-sad-see-marcus-smart-go>(ESPN)</a>. Meanwhile, Michigan's Kobe Bufkin, a top breakout guard in college basketball last season, is now a member of the Atlanta Hawks after being drafted 15th overall <a href=https://bleacherreport.com/articles/10075646-kobe-bufkins-draft-scouting-report-pro-comparison-updated-hawks-roster>(Bleacher Report)</a>. Additionally, there are rumors surrounding Ben Simmons' future with the Philadelphia 76ers, with a potential Karl-Anthony Towns trade not being ruled out completely <a href=https://bleacherreport.com/articles/10079641-every-teams-top-target-entering-chaotic-nba-trade-free-agency-season>(Bleacher Report)</a>. On a different note, Bryan Hoeing, a right-hander for the Miami Marlins, was once recruited by Brad Stevens, the current president of basketball operations for the Boston Celtics <a href=https://deadspin.com/marlins-turn-to-bryan-hoeing-in-bid-to-top-pirates-1850573301>(Deadspin)</a>. In disciplinary news, the NBA has suspended Ja Morant of the Memphis Grizzlies for at least 25 games, a decision that has the support of the team's general manager, Zach Kleiman <a href=https://bleacherreport.com/articles/10080415-ja-morants-25-game-suspension-was-appropriate-grizzlies-gm-zach-kleiman-says>(Bleacher Report)</a>. Lastly, following the resignation of West Virginia men's basketball coach Bob Huggins, Kerr Kriisa is re-entering the transfer portal, potentially seeking a new team <a href=https://bleacherreport.com/articles/10080451-3-west-virginia-basketball-players-enter-transfer-portal-after-bob-huggins-exit>(Bleacher Report)</a>. Kentucky star Oscar Tshiebwe, who was not selected in the 2023 NBA draft, will sign a two-way deal with the Indiana Pacers <a href=https://bleacherreport.com/articles/10080459-nba-rumors-oscar-tshiebwe-pacers-agree-to-2-way-contract-after-2023-nba-draft>(Bleacher Report)</a>.</p>",
		"Sports News Roundup":
			"<p>Qatar's Sovereign Wealth Fund Invests in Washington Sports Teams</p>\n<p>Qatar's sovereign wealth fund has recently acquired a 5% stake in the parent company of the NBA's Washington Wizards, NHL's Washington Capitals, and WNBA's Washington Mystics. This deal, worth $4.05 billion, solidifies Qatar's growing presence in the world of sports ownership. <a href=https://time.com/6289525/qatar-washington-wizards-capitals-mystics-sports-ownership/>(Time)</a></p>\n<p>Exciting Developments in the 2023 NBA Draft</p>\n<p>The 2023 NBA draft has already made waves with its first round. The top pick went to a remarkable 7-foot-5 talent, signaling the arrival of a generational player. The draft also saw several trades involving top-10 picks and a surprising slide for one player. The excitement and unpredictability of the draft continue to captivate basketball fans. <a href=https://www.espn.com/nba/story/_/id/37893062/nba-draft-2023-surprises-winners-losers-first-round>(ESPN)</a></p>\n<p>Fashion and Basketball Collide at the NBA Draft</p>\n<p>The NBA draft is not just about the players; it's also a showcase for fashion. This year, the intersection of basketball and menswear delivered some delightful gifts. Fans witnessed stylish outfits and unique fashion choices, making the draft a Christmas morning for fashion enthusiasts. <a href=https://www.gq.com/gallery/2023-nba-draft-biggest-fits>(GQ Magazine)</a></p>\n<p>Rediscovering the New Balance 550</p>\n<p>The New Balance 550 has been making waves in the world of sneakers, thanks to its collaboration with Aimé Leon Dore. However, many are surprised to learn that this basketball sneaker actually first hit the shelves in 1989. The enduring popularity of the New Balance 550 proves that classic designs can stand the test of time. <a href=https://www.highsnobiety.com/p/new-balance-550-thisisneverthat/>(Highsnobiety)</a></p>",
		"Surprising Picks and Versatile Players in the 2023 NBA Draft":
			"<p>The 2023 NBA draft saw some unexpected selections and the acquisition of versatile players who are poised to make an impact in the league. The Golden State Warriors raised eyebrows when they chose Brandin Podziemski with the 19th overall pick. Despite the skepticism, Podziemski's confidence and skill set suggest that he has the potential to be a valuable asset for the team <a href=https://bleacherreport.com/articles/10080520-warriors-brandin-podziemski-im-a-triple-double-guy-in-the-nba-in-a-few-seasons>(Bleacher Report)</a>. The New Orleans Pelicans made a smart move by selecting Jordan Hawkins from Connecticut with the No. 14 overall pick. Hawkins is known for his versatility and ability to make shots, making him a valuable addition to the Pelicans' roster <a href=https://bleacherreport.com/articles/10075642-jordan-hawkins-draft-scouting-report-pro-comparison-updated-pelicans-roster>(Bleacher Report)</a>. Another notable pick was Keyonte George, a shooting guard from Baylor, who was chosen by the Utah Jazz with the No. 16 overall pick. George's skills and potential have been recognized by Bleacher Report Draft Expert Jonathan Wasserman, making him an exciting prospect for the Jazz <a href=https://bleacherreport.com/articles/10075645-keyonte-georges-draft-scouting-report-pro-comparison-updated-jazz-roster>(Bleacher Report)</a>.</p>",
		"Victor Wembanyama: The Phenomenal French Rookie":
			"<p>In a highly anticipated move, the San Antonio Spurs selected Victor Wembanyama as the first overall pick in the 2023 NBA Draft <a href=https://www.theguardian.com/sport/2023/jun/22/future-arrives-as-spurs-pick-wembanyama-with-first-pick-of-nba-draft>(The Guardian)</a>. The 19-year-old French phenom is considered the most coveted draft prospect since LeBron James and Kareem Abdul-Jabbar <a href=https://bleacherreport.com/articles/10080221-biggest-winners-and-losers-from-2023-nba-draft-night>(Bleacher Report)</a>. Wembanyama's arrival in the United States was met with excitement as he experienced his first subway ride in New York City and threw out the first pitch at a baseball game <a href=https://deadspin.com/spurs-select-victor-wembanyama-first-overall-in-nba-dra-1850568337>(Deadspin)</a>. The 7ft 4in rookie has already captured the attention of fans and experts alike, with comparisons being drawn to some of the game's greatest players <a href=https://bleacherreport.com/articles/10080221-biggest-winners-and-losers-from-2023-nba-draft-night>(Bleacher Report)</a>. The Dallas Mavericks also made waves on draft night by trading Dvis Bertns' contract to the Oklahoma City Thunder <a href=https://bleacherreport.com/articles/10080549-spurs-popovich-victor-wembanyama-shouldnt-be-compared-to-lebron-kobe-duncan>(Bleacher Report)</a>. Meanwhile, San Antonio Spurs head coach Gregg Popovich remains unfazed by the comparisons and is focused on nurturing Wembanyama's unique talent [8]. With Wembanyama officially joining the Spurs, the era of this exceptional French rookie has begun <a href=https://www.espn.com/fantasy/basketball/story/_/id/37904164/nba-draft-picks-fantasy-basketball-rookies-biggest-impact-2023-24>(ESPN)</a>.</p>",
		conclusion:
			"As we wrap up this edition of our sports newsletter, we've covered a range of topics, from the NBA draft highlights to intriguing player moves and even fashion at the draft. The basketball world is buzzing with excitement, and we can't wait to see how these stories unfold. Stay tuned for more updates and enjoy the thrilling action on the court!",
		introduction:
			"Welcome to our latest sports newsletter, where we dive into the exciting world of professional basketball. From surprising picks in the NBA draft to thrilling developments in the league, there's plenty to discuss. Let's jump right in!",
		title: "NBA Draft Highlights and Exciting Developments",
	};

	useEffect(() => {
		setIsSignedIn(true);
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
		<div className="conversation-wrapper">
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

export default Example2;
