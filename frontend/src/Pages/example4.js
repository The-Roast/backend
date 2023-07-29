import React, { useEffect, useState } from "react";
import jsonData from "./data.json";

const TextColumns = () => {
	const [pages, setPages] = useState([]);

	useEffect(() => {
		splitContent();
		window.addEventListener("resize", splitContent);
		return () => {
			window.removeEventListener("resize", splitContent);
		};
	}, []);

	const splitContent = () => {
		const newspaperWidth = 600; // Adjust the newspaper width as needed
		const columnGap = 20; // Adjust the column gap as needed
		const columnWidth = (newspaperWidth - columnGap) / 2;
		const lineHeight = 18; // Adjust the line height as needed
		const newspaperHeight = 800; // Adjust the newspaper height as needed
		const numLinesPerPage = Math.floor(newspaperHeight / lineHeight);

		let content = jsonData.reduce((acc, { title, body }) => {
			return acc + (title ? `<h1>${title}</h1>` : "") + body;
		}, "");

		const pages = [];
		let currentPage = "";
		let currentLine = 0;
		let currentColumn = 0;

		while (content.length > 0) {
			const text = extractText(content, columnWidth);
			const numLines = Math.floor(text.length / (columnWidth / 8)); // Approximating characters to fit in a line

			if (currentLine + numLines > numLinesPerPage) {
				if (currentColumn === 1) {
					pages.push(currentPage);
					currentPage = "";
					currentColumn = 0;
				} else {
					currentColumn = 1;
				}
				currentLine = 0;
			}

			currentPage += text;
			currentLine += numLines;
		}

		if (currentPage !== "") {
			pages.push(currentPage);
		}

		setPages(pages);
	};

	const extractText = (text, maxWidth) => {
		let charCount = 0;
		for (let i = 0; i < text.length; i++) {
			const char = text[i];
			charCount += 1;
			if (char === "<" && text.slice(i, i + 4) === "<br>") {
				i += 3; // Skip '<br>'
				charCount = 0;
			}
			if (charCount >= maxWidth) {
				return text.slice(0, i + 1);
			}
		}
		return text;
	};

	return (
		<div style={{ padding: "20px", boxSizing: "border-box" }}>
			{pages.map((pageContent, index) => (
				<div
					key={index}
					style={{
						backgroundColor: "lightgray",
						width: "600px",
						height: "800px",
						padding: "20px",
						marginBottom: "20px",
						boxShadow: "5px 5px 10px #888888",
						fontSize: "12px",
						textAlign: "justify",
						boxSizing: "border-box",
						columnCount: 2,
						columnGap: "20px",
						overflow: "hidden",
					}}
				>
					<div dangerouslySetInnerHTML={{ __html: pageContent }} />
				</div>
			))}
		</div>
	);
};

export default TextColumns;
