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

function Example1({ setIsSignedIn }) {
	const [isRecording, setIsRecording] = useState(false);
	const [showResponse, setShowResponse] = useState(false);
	const [response, setResponse] = useState("");

	// const { state } = useLocation();
	const newsletter = {
		"A Family Divided, The Changing Face of Men's Fashion, and Everton's Tale of Woe":
			"<p>In the BBC Radio 4 program 'Windrush: A Family Divided,' the 75th anniversary of the Empire Windrush docking was explored, shedding light on the impact it had on families and the challenges they faced <a href=https://www.theguardian.com/tv-and-radio/2023/jun/24/the-week-in-audio-windrush-a-family-divided-janey-godley-the-c-bomb-the-skewer-sports-strangest-crimes-review>(The Guardian)</a>. Meanwhile, the state of the nation's mood shift in men's fashion was examined through the lens of Boris Johnson's hairstyle, which has become a visual barometer for the changing trends <a href=https://www.theguardian.com/fashion/2023/jun/23/the-end-of-the-schlub-why-the-sharp-dressed-man-is-back-for-summer>(The Guardian)</a>. On a different note, Everton Football Club's ongoing struggles were highlighted, with board upheaval, financial strife, and legal challenges from former managers contributing to their tale of woe <a href=https://www.skysports.com/football/news/11095/12908668/everton-reporter-notebook-light-finally-at-the-end-of-the-tunnel-for-the-toffees>(Sky Sports)</a>.</p>",
		"Latest Updates: Retro-Style Sports Games, Toyota's GR GT3 Concept, Tronsmart's Anniversary Offers, Legged Robot SDK, Lenovo's Yoga Book 9i, Born X Raised Athleisure Line":
			"<p>Apple Arcade has added two retro-style sports management games to its roster: Retro Bowl Plus, a football game, and Retro Goal Plus, a soccer game. These new additions provide subscribers with more options for nostalgic sports gaming experiences <a href=https://www.cnet.com/tech/gaming/football-and-soccer-management-games-march-onto-apple-arcade/>(CNET)</a>. Toyota has confirmed that their GR GT3 concept, known for its stunning design, is not only being developed as a race car, but also as a road version. This news comes directly from the top of Toyota's World Endurance Championship program, exciting fans of the brand and racing enthusiasts alike <a href=https://www.autoblog.com/2023/06/23/gorgeous-toyota-gr-gt3-race-concept-will-spawn-production-sports-car/>(Autoblog)</a>. Tronsmart, in celebration of their 10th anniversary, has launched new products and offers on existing accessories. One of their latest releases, the Tronsmart Halo 200, is a portable Bluetooth speaker that boasts impressive sound quality and durability <a href=https://www.androidcentral.com/accessories/audio/tronsmart-launches-bluetooth-karaoke-speaker-with-rgb-lights>(Android Central)</a>. A legged robot with an alternate SDK version has caught the author's attention. The original SDK only came as pre-compiled binaries, limiting its functionality. The new SDK version opens up expensive features, making the robot even more versatile and appealing to developers <a href=https://hackaday.com/2023/06/24/robodog-goes-free-thanks-to-unofficial-sdk/>(Hackaday)</a>. Lenovo's Yoga Book 9i has garnered attention for its unique hinge design, which breaks up content in an awkward manner. Despite this flaw, the device offers a range of specifications, catering to different user preferences and needs <a href=https://arstechnica.com/gadgets/2023/06/a-threat-to-portable-monitors-everywhere-lenovo-yoga-book-9i-review/>(Ars Technica)</a>. Born X Raised, known for its collaborations with LA-based sports teams, has released an athleisure line in partnership with the Los Angeles Football Club. This collection combines sportswear and streetwear elements, reflecting the brand's history and aesthetics <a href=https://hypebeast.com/2023/6/born-x-raised-lafc-third-collection-2023>(HYPEBEAST)</a>.</p>",
		"Sports News Roundup":
			"<p>In this week's sports news, Chris Froome's hopes of participating in the Tour de France have been dashed as he has been left out of the Israel-Premier Tech squad for this year's race. However, the four-time winner remains determined and has expressed his intention to try again in 2024 <a href=https://www.skysports.com/transfer/news/12691/12908165/mason-mount-chelsea-reject-manchester-uniteds-third-bid-of-55m-for-england-midfielder>(Sky Sports)</a>.</p>\n<p>In the world of football, Chelsea has rejected Manchester United's third bid for midfielder Mason Mount. The bid, worth £55m, was turned down by Chelsea, who have countered with a proposal of £58m + £7m. Furthermore, Chelsea has offered to meet with United in person to negotiate a deal <a href=https://www.skysports.com/football/news/11849/12908549/rafael-benitez-set-to-be-named-new-celta-vigo-boss>(Sky Sports)</a>.</p>\n<p>Meanwhile, in Spain, Rafael Benitez is set to become the new manager of Celta Vigo. The Spanish club has announced that an 'agreement in principle' has been reached with Benitez, who has previously managed Liverpool, Newcastle, and Everton. This appointment marks a new chapter in Benitez's managerial career [3].</p>",
		"The Latest in Streaming and Television":
			"<p>YouTube TV has begun testing multiview with content outside of sports. Up to five new multiview streams, including news, sports, weather, and more, will be available. This feature allows users to watch multiple streams simultaneously, enhancing the viewing experience <a href=https://www.cnet.com/tech/services-and-software/college-world-series-2023-how-to-watch-stream-florida-vs-lsu-today-from-anywhere/>(CNET)</a>.</p>\n<p>If you are unable to view the College World Series locally, using a VPN can be a great solution. A VPN not only allows you to watch the games, but it also provides security and privacy online <a href=https://www.bbc.co.uk/sport/live/golf/65974321>(BBC News)</a>.</p>\n<p>In order to watch live TV on any channel or device, and BBC programmes on iPlayer, you need a TV license. Make sure you are aware of the requirements <a href=https://www.avclub.com/whats-on-tv-june-23-25-im-a-virgo-swagger-season-2-1850559869>(The A.V. Club)</a>.</p>\n<p>Here are the big things happening on TV from Friday, June 23, to Sunday, June 25. All times are Eastern. Stay up to date with the latest shows and events [4].</p>",
		"The Potential Cage Match Between Elon Musk and Mark Zuckerberg":
			"<p>In recent news, there has been a lot of buzz about a potential cage match between two tech giants, Elon Musk and Mark Zuckerberg. Even if you're not a fan of combat sports, this showdown is hard to ignore. The idea of these two influential figures going head-to-head in a physical battle has captured the imagination of many. But what exactly led to this bizarre proposition?</p>\n<p>It all started when professional fighters Colby Covington and Michael Chandler engaged in a heated debate on The Laura Ingraham Show. The discussion centered around who would come out on top in a fight between Musk and Zuckerberg. The intensity of the debate only fueled the curiosity surrounding this hypothetical matchup <a href=https://www.huffpost.com/entry/pro-fighters-argue-over-beta-soy-boy-mark-zuckerberg-and-sultan-of-spacex-elon-musk_n_6495c629e4b095a2925d29de>(HuffPost)</a>.</p>\n<p>While it may seem like a far-fetched idea, the clash between Musk and Zuckerberg has become even more absurd. The potential fight has garnered attention not just from fans, but also from the media. The prospect of these two tech titans physically confronting each other has become a topic of discussion across various platforms [2].</p>\n<p>Although the details of the potential cage match are still up in the air, it is clear that the idea has captured public interest. The clash between Musk and Zuckerberg, two influential figures in the tech industry, has sparked intrigue and curiosity. Whether this fight will ever come to fruition remains to be seen, but for now, it continues to be a captivating topic of conversation <a href=https://www.huffpost.com/entry/pro-fighters-argue-over-beta-soy-boy-mark-zuckerberg-and-sultan-of-spacex-elon-musk_n_6495c629e4b095a2925d29de>(HuffPost)</a> [2].</p>",
		"The Rise of Women's Football":
			"<p>The Women's World Cup has come a long way from its unofficial predecessors half a century ago. The ninth official edition of the FIFA Women's World Cup this July is on track to being the most attended yet, showcasing the growing popularity and support for women's football <a href=https://time.com/6289539/womens-world-cup-2023-history/>(Time)</a>. In line with this trend, Newcastle United Women have recently turned professional as they strive to climb from the third tier to the Women's Super League in consecutive seasons. After their recent promotion, manager Becky Langley's team is determined to make their mark in the world of women's football <a href=https://www.theguardian.com/football/2023/jun/23/newcastle-women-professional-third-tier-only-club>(The Guardian)</a>.</p>",
		conclusion:
			"That wraps up our newsletter for this week. We hope you enjoyed the latest updates in streaming and television, the exciting sports news roundup, the rise of women's football, and the intriguing potential cage match between Elon Musk and Mark Zuckerberg. Stay tuned for more exciting news and updates in the world of entertainment and sports!",
		introduction:
			"Get ready for a whirlwind tour of the latest news in streaming and television! From YouTube TV's new multiview feature to the importance of a TV license, we've got you covered. And if you're a sports fan, we've got an exciting sports news roundup, a deep dive into the rise of women's football, and updates on retro-style sports games and more. Plus, don't miss the potential cage match between Elon Musk and Mark Zuckerberg. Let's dive in!",
		title: "The Latest in Streaming and Television",
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
			{/* <div className="right-view">
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
			</div> */}
		</div>
	);
}

export default Example1;
