import React, { useState } from "react";
import { useParams, useNavigate, useLocation } from "react-router-dom";
import HuePicker from "react-color";
import Loading from "../Components/Loading";
import Grid from "../Components/SettingsGrid";
import "./styles/NewsTemplate.css";
import SERVER_API_URL from "../Config";

function NewsTemplate() {
	const navigate = useNavigate();
	const [unsavedChanges, setUnsavedChanges] = useState(false);
	const { state } = useLocation();
	const { preference } = state;
	const [title, setTitle] = useState(preference.name);
	const [color, setColor] = useState(preference.color.hex);
	const [sources, setSources] = useState(preference.sources);
	const [interests, setInterests] = useState(preference.interests);
	const [personality, setPersonality] = useState(preference.personality);
	const [isLoading, setIsLoading] = useState(false);

	const uuid = preference.uuid;
	const access_token = localStorage.getItem("access_token");
	const refresh_token = localStorage.getItem("refresh_token");

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

	function updatePreferences() {
		preference.name = title;
		preference.color.hex = color;
		preference.sources = sources;
		preference.interests = interests;
		preference.personality = personality;
	}

	const handleSave = () => {
		setUnsavedChanges(false);
		updatePreferences();
		const access_token = localStorage.getItem("access_token");
		const refresh_token = localStorage.getItem("refresh_token");
		fetch(`${SERVER_API_URL}/v1/digest`, {
			method: "PUT",
			headers: {
				Accept: "application/json",
				"Content-Type": "application/json",
				Authorization: `Bearer ${access_token}`,
			},
			body: JSON.stringify(preference),
		});
	};

	const handleGenerate = () => {
		updatePreferences();
		setIsLoading(true);
		fetch(`${SERVER_API_URL}/v1/newsletter/${uuid}`, {
			method: "get",
			headers: {
				Accept: "application/json",
				"Content-Type": "application/json",
				Authorization: `Bearer ${access_token}`,
			},
		})
			.then((response) => response.json())
			.then((response) => {
				navigate("/newsletter/" + response.response["title"], {
					state: { newsletter: response.response },
				});
				setIsLoading(false);
			});
	};

	const handleDelete = () => {
		fetch(`${SERVER_API_URL}/v1/digest`, {
			method: "delete",
			headers: {
				Accept: "application/json",
				"Content-Type": "application/json",
				Authorization: `Bearer ${access_token}`,
			},
			body: JSON.stringify({ uuid: uuid }),
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

	return isLoading ? (
		<Loading />
	) : (
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
					<button onClick={handleGenerate}>Generate digest</button>
				</div>
				<div className="button-wrapper">
					<button onClick={handleDelete}>Delete digest</button>
				</div>
			</div>
		</div>
	);
}

export default NewsTemplate;
