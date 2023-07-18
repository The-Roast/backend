import React, { useState } from "react";
import { useParams, useNavigate, useLocation } from "react-router-dom";
import { SliderPicker } from "react-color";
import Grid from "../Components/SettingsGrid";
import "./styles/NewsTemplate.css";
import SERVER_API_URL from "../Config";

function CreateNewsTemplate() {
	const navigate = useNavigate();
	const [unsavedChanges, setUnsavedChanges] = useState(false);
	const [title, setTitle] = useState("");
	const [color, setColor] = useState("");
	const [sources, setSources] = useState("");
	const [interests, setInterests] = useState("");
	const [personality, setPersonality] = useState("");

	const handleTitleChange = (event) => {
		setTitle(event.target.value);
		setUnsavedChanges(true);
	};

	const handleColorChange = (color) => {
		setColor(color.hex);
		setUnsavedChanges(true);
	};

	const handlePersonalityChange = (event) => {
		setPersonality(event.target.value);
		setUnsavedChanges(true);
	};

	const handleInterestsChange = (event) => {
		setInterests(event.target.value);
		setUnsavedChanges(true);
	};

	const handleSourcesChange = (event) => {
		setSources(event.target.value);
		setUnsavedChanges(true);
	};

	const handleSave = () => {
		setUnsavedChanges(false);
	};

	const handleCreate = () => {
		let preference = {
			name: "",
			color: { hex: "" },
			sources: "",
			interests: "",
			personality: "",
			uuid: "",
		};
		preference.name = title;
		preference.color.hex = color;
		preference.sources = sources;
		preference.interests = interests;
		preference.personality = personality;
		console.log(preference);

		const access_token = localStorage.getItem("access_token");
		const refresh_token = localStorage.getItem("refresh_token");
		fetch(`${SERVER_API_URL}/v1/digest`, {
			method: "POST",
			headers: {
				Accept: "application/json",
				"Content-Type": "application/json",
				Authorization: "Bearer " + access_token,
			},
			body: JSON.stringify(preference),
		})
			.then((response) => response.json())
			.then((response) => {
				navigate("/main");
			});
	};

	const data = [
		{ preference: "Title", value: title, onChange: handleTitleChange },
		{
			preference: "Personality",
			value: personality,
			onChange: handlePersonalityChange,
		},
		{
			preference: "Interests",
			value: interests,
			onChange: handleInterestsChange,
		},
		{ preference: "Sources", value: sources, onChange: handleSourcesChange },
		{ preference: "Color", value: color, onChange: handleColorChange },
	];

	return (
		<div className="news-template">
			<div className="title-card">
				<h1>Settings</h1>
			</div>
			<div className="preference-wrapper">
				<Grid data={data} />
			</div>
			<div className="button-row-wrapper">
				<div className="button-wrapper">
					<button
						onClick={() => {
							navigate(-1);
						}}
					>
						Back
					</button>
				</div>
				<div className="button-wrapper">
					<button onClick={handleSave} disabled={!unsavedChanges}>
						Save preferences
					</button>
					{unsavedChanges && <span>Unsaved changes</span>}
				</div>
				<div className="button-wrapper">
					<button onClick={handleCreate}>Create Digest</button>
				</div>
			</div>
		</div>
	);
}

export default CreateNewsTemplate;
