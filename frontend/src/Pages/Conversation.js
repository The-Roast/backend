import React, { useState, useEffect, useRef } from "react";
import { useWhisper } from "@chengsokdara/use-whisper";
import "./styles/Conversation.css";
import XI_API_KEY from "../Config";
import { useLocation } from "react-router-dom";

function Conversation({ setIsSignedIn }) {
	const [isRecording, setIsRecording] = useState(false);
	const [showResponse, setShowResponse] = useState(false);
	const [response, setResponse] = useState("");

	const { state } = useLocation();
	const { newsletter } = state;
	useEffect(() => {
		setIsSignedIn(true);
		console.log(newsletter);
	}, []);

	const [newsIndex, setNewsIndex] = useState(0);
	const [audioUrl, setAudioUrl] = useState("");

	const sections = Object.entries(newsletter).filter(
		([key]) => key !== "introduction" && key !== "conclusion" && key !== "title"
	);

	const [messages, setMessages] = useState([]);

	const audioRef = useRef(null);

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
		try {
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
				}
			);
			const data = await response.blob();
			console.log(data);
			const audioUrl = URL.createObjectURL(data);
			console.log(audioUrl);
			setAudioUrl(audioUrl);
		} catch (error) {
			console.error("Error fetching audio:", error);
		}
	};

	const playNextSection = () => {
		if (newsIndex < sections.length) {
			const sectionText = sections[newsIndex][1];
			fetchAudio(sectionText);
			setNewsIndex((prevIndex) => prevIndex + 1);
		}
	};

	const playAudio = () => {
		if (audioUrl) {
			audioRef.current.src = audioUrl;
			console.log("playing audio!");
			audioRef.current.play();
		} else {
			playNextSection();
		}
	};

	useEffect(() => {
		if (newsIndex > 0) {
			playAudio();
		}
	}, [newsIndex]);

	return (
		<div className="conversation-wrapper">
			<div className="left-view">
				<button onClick={playAudio}>Listen to Newsletter</button>
				<audio ref={audioRef} controls />
				<h1>Today's News Digest</h1>
				<p>{newsletter["introduction"]}</p>
				{sections.map(([key, value], index) => (
					<div key={key}>
						<h2>{key}</h2>
						<p>{value}</p>
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

export default Conversation;
