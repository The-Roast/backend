import React, { useState } from "react";
import { useParams, useNavigate, useLocation } from "react-router-dom";
import { SliderPicker } from "react-color";
import Loading from "../Components/Loading";
import "./styles/NewsTemplate.css";

function NewsTemplate() {
	const navigate = useNavigate();
	const [unsavedChanges, setUnsavedChanges] = useState(false);
	const { state } = useLocation();
	const { preference } = state; // Read values passed on state
	const [title, setTitle] = useState(preference.name);
	const [color, setColor] = useState(preference.color.hex);
	const [contentSources, setContentSources] = useState(
		preference.contentSources.join(", ")
	);
	const [interests, setInterests] = useState(preference.interests.join(", "));
	const [personality, setPersonality] = useState(preference.personality);
	const [isLoading, setIsLoading] = useState(false);

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

	const handleContentSourcesChange = (event) => {
		setContentSources(event.target.value);
		setUnsavedChanges(true);
	};

	const handleSave = () => {
		setUnsavedChanges(false);
		preference.name = title;
		preference.color.hex = color;
		preference.contentSources = contentSources.split(",").map((t) => t.trim());
		preference.interests = interests.split(",").map((t) => t.trim());
		preference.personality = personality;
		fetch(`http://127.0.0.1:5000/v1/digest`, {
			method: "POST",
			headers: {
				Accept: "application/json",
				"Content-Type": "application/json",
			},
			body: JSON.stringify(preference),
		})
			.then((response) => response.json())
			.then((response) => {
				// navigate("/conversation", { state: { newsletter: response } });
			});
	};

	const handleGenerate = () => {
		preference.name = title;
		preference.color.hex = color;
		preference.contentSources = contentSources.split(",").map((t) => t.trim());
		preference.interests = interests.split(",").map((t) => t.trim());
		preference.personality = personality;

		const uuid = preference.uuid;
		setIsLoading(true);
		fetch(`http://127.0.0.1:5000/v1/newsletter/` + uuid, {
			method: "get",
			headers: {
				Accept: "application/json",
				"Content-Type": "application/json",
			},
		})
			.then((response) => response.json())
			.then((response) => {
				navigate("/conversation", { state: { newsletter: response.response } });
			});
	};

	return isLoading ? (
		<Loading />
	) : (
		<div className="news-template">
			<div className="button-wrapper">
				<button
					onClick={() => {
						navigate(-1);
					}}
				>
					Back
				</button>
			</div>
			<h1 className="title">Settings:</h1>
			<div className="preference-wrapper">
				<h2>
					<input
						type="text"
						className="editable-input title"
						value={title}
						onChange={handleTitleChange}
						style={{ color: color }}
					/>
					<hr className="editable-line" />
				</h2>
				<label>
					Personality:
					<input
						type="text"
						className="editable-input"
						value={personality}
						onChange={handlePersonalityChange}
					/>
					<hr className="editable-line" />
				</label>
				<label>
					Interests:
					<input
						type="text"
						className="editable-input"
						value={interests}
						onChange={handleInterestsChange}
					/>
					<hr className="editable-line" />
				</label>
				<label>
					Content Sources:
					<input
						type="text"
						className="editable-input"
						value={contentSources}
						onChange={handleContentSourcesChange}
					/>
					<hr className="editable-line" />
				</label>
				<div className="color-picker">
					<div className="color-values-wrapper">
						<label className="color-label">Color:</label>
						<div className="color-values">
							<div className="color-hex">{color}</div>
						</div>
					</div>
					<div className="color-picker-container">
						<SliderPicker color={color} onChange={handleColorChange} />
					</div>
				</div>
			</div>
			<div style={{ display: "flex", justifyContent: "center", gap: "40px" }}>
				<div className="button-wrapper">
					<button onClick={handleSave} disabled={!unsavedChanges}>
						Save preferences
					</button>
					{unsavedChanges && <span>Unsaved changes</span>}
				</div>
				<div className="button-wrapper">
					<button onClick={handleGenerate}>Generate Digest</button>
				</div>
			</div>
		</div>
	);
}

export default NewsTemplate;
