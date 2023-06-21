import React, { useState, useEffect } from "react";
import { useWhisper } from "@chengsokdara/use-whisper";
import "./styles/Conversation.css";
import XI_API_KEY from "../Config";
import { useLocation } from "react-router-dom";

function Conversation({ setIsSignedIn }) {
	const [isRecording, setIsRecording] = useState(false);
	const [showResponse, setShowResponse] = useState(false);
	const [response, setResponse] = useState("");

	const [index, setIndex] = useState(0);
	const { state } = useLocation();
	const { newsletter } = state;
	useEffect(() => {
		setIsSignedIn(true);
		// fetch("http://127.0.0.1:5000/v1/newsletter/", {
		// 	method: "get",
		// 	headers: {
		// 		Accept: "application/json",
		// 		"Content-Type": "application/json",
		// 	},
		// })
		// 	.then((response) => response.json())
		// 	.then((response) => {

		// 	});
	}, []);

	const [newsIndex, setNewsIndex] = useState(false);
	return (
		<div className="conversation-wrapper">
			<div className="left-view">
				<h1>Today's News Digest</h1>

				<p>
					Welcome, readers, to today's edition of the News Digest. We've
					compiled stories from reputable sources to bring you an informed
					perspective on current events.{" "}
				</p>

				<h2>News Briefs </h2>

				<p>
					According to <a href="https://www.reuters.com/">Reuters</a>, former
					Treasury Secretary Lawrence Summers expressed confusion over the
					Federal Reserve's recent decision to raise interest rates, arguing
					such hikes could lead to a harsher recession. In a win for democracy,
					the Supreme Court (
					<a href="https://www.supremecourt.gov/">SupremeCourt.gov</a>) ruled
					that North Carolina's gerrymandered voting districts were
					unconstitutional.{" "}
				</p>

				<p>
					The administration nominated a former North Carolina health secretary
					to lead the CDC (<a href="https://www.cdc.gov/">CDC.gov</a>), a
					reassuring choice. An inquiry found British Prime Minister Boris
					Johnson (
					<a href="https://www.gov.uk/government/people/boris-johnson">
						Gov.UK
					</a>
					) misled Parliament on lockdown violations, confirming concerns over
					integrity in leadership. On a more hopeful note, the Supreme Court
					upheld protections for Native American children in foster care (
					<a href="https://www.usnews.com/">US News</a>), recognizing the
					government's duty to vulnerable groups.{" "}
				</p>

				<h2>The Day's Scoop </h2>

				<p>
					According to the <a href="https://www.nytimes.com/">New York Times</a>
					, Pentagon Papers whistleblower Daniel Ellsberg died at 92. Ellsberg
					risked his freedom to expose government deception on Vietnam, leaving
					behind a courageous legacy of dissent for the greater good. Haitians
					continue suffering under the control of violent gangs, as reported by
					eyewitnesses.{" "}
				</p>

				<p>
					Former President Trump's legal troubles persist, with a judge
					demanding attorneys acquire top security clearance to review
					classified records in forthcoming trials (
					<a href="https://www.nytimes.com/">The New York Times</a>). Prime
					Minister Johnson and staff denounced an official report on lockdown
					violations as "vindictive," an ironic charge from leaders accused of
					callousness toward citizens' sacrifice (
					<a href="https://www.bbc.com/news">BBC News</a>).{" "}
				</p>

				<p>
					A report found Trump-era tariffs on China significantly damaged the
					U.S. economy (
					<a href="https://carnegieendowment.org/">Carnegie Endowment</a>) while
					failing to achieve policy aims, confirming expert warnings. Finally,
					two-time Academy Award winner Glenda Jackson died at 87. Jackson
					brought subtlety and intelligence to her craft, often portraying
					fiercely independent women. Though her ctlhe magnetic performances
					will endure, the world has lost a seminal talent (
					<a href="https://www.theguardian.com/film/2022/jun/01/glenda-jackson-fierce-sensual-and-always-cerebral-a-british-film-acting-great">
						The Guardian
					</a>
					).
				</p>

				<h2>The Day's Headlines</h2>

				<p>
					The U.S. and China agreed artificial intelligence poses risks, a
					warning for lawmakers to enact safeguards protecting citizens (
					<a href="https://www.nytimes.com/">The New York Times</a>). After 57
					years reporting for{" "}
					<a href="https://www.theguardian.com/uk">The Guardian</a>, celebrated
					journalist Jeremy Alexander retired, though his principled work will
					serve as an enduring model.{" "}
				</p>

				<p>
					With former Prime Minister Silvio Berlusconi's death, questions arise
					over how he acquired and spent his fortune, much of it while in office
					(<a href="https://www.bbc.com/news/world-europe-49008743">BBC News</a>
					). Women's sports are gaining mainstream popularity but struggling to
					balance commercial interests with athlete wellbeing, as discussed in{" "}
					<a href="https://www.nytimes.com/2021/03/30/opinion/womens-sports-commercialization.html">
						The New York Times
					</a>
					.{" "}
				</p>

				<p>
					Filmmaker Michelangelo Antonioni, who explored ennui and isolation in
					postwar Italy, died at 94. His films captured modern anxieties with a
					singular artistic vision (
					<a href="https://www.theguardian.com/world/2007/jul/31/italy.filmnews">
						The Guardian)
					</a>
					. According to <a href="https://www.politico.com/">Politico</a>, Vice
					President Kamala Harris polled well in a hypothetical Republican
					primary, indicating some conservatives find her pragmatic, charismatic
					leadership appealing. Finally, experts debated how to regulate
					cryptocurrency to prevent fraud and abuse while encouraging innovation
					(
					<a href="https://hbr.org/2021/05/who-should-regulate-crypto">
						Harvard Business Review
					</a>
					).{" "}
				</p>

				<p>
					We hope you found today's Digest informative. Our duty is to report
					the news accurately and objectively, with a touch of wry humor and a
					nod to the indomitability of human progress. Until next time, dear
					readers!{" "}
				</p>
			</div>
		</div>
	);
}

export default Conversation;
