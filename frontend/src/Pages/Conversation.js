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

function Conversation() {
	const [isRecording, setIsRecording] = useState(false);
	const [showResponse, setShowResponse] = useState(false);
	const [response, setResponse] = useState("");

	const { state } = useLocation();
	const { newsletter } = state;
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
							<div key={index}>
								{e.split(/(?<!>)\n(?!<)/).map((subValue, subIndex) => {
									const content = subValue.replace(/<\/?(?:ol|li)>/g, "<h2>"); // Remove <ol> and <li> tags
									return (
										<p
											key={subIndex}
											dangerouslySetInnerHTML={{
												__html: renderContent(content),
											}}
										/>
									);
								})}
							</div>
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

export default Conversation;
