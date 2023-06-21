import React, { useState } from "react";
import { useParams, useNavigate, useLocation } from "react-router-dom";
import { SliderPicker } from "react-color";
import "./styles/NewsTemplate.css";

function NewsTemplate() {
	const navigate = useNavigate();
	const [unsavedChanges, setUnsavedChanges] = useState(false);
	const { state } = useLocation();
	const { preference } = state; // Read values passed on state
	const [title, setTitle] = useState(preference.name);
	const [color, setColor] = useState(preference.color.hex);
	const [contentSources, setContentSources] = useState(
		preference.contentSources
	);
	const [interests, setInterests] = useState(preference.interests);
	const [personality, setPersonality] = useState(preference.personality);

	const handleTitleChange = (event) => {
		setTitle(event.target.value);
		console.log(event.target.value);
		preference.name = title;
		setUnsavedChanges(true);
	};

	const handleColorChange = (color) => {
		setColor(color.hex);
		preference.color.hex = color.hex;
		setUnsavedChanges(true);
	};

	const handlePersonalityChange = (event) => {
		setPersonality(event.target.value);
		preference.personality = personality;
		setUnsavedChanges(true);
	};

	const handleInterestsChange = (event) => {
		setInterests(event.target.value.split(",").map((t) => t.trim()));
		preference.interests = interests;
	};

	const handleContentSourcesChange = (event) => {
		setContentSources(event.target.value.split(",").map((s) => s.trim()));
		preference.contentSources = contentSources;
	};

	const handleSave = () => {
		console.log(preference);
		setUnsavedChanges(false);
		// Send preferences to backend
		fetch(`http://127.0.0.1:5000/v1/digest`, {
			method: "POST",
			headers: {
				Accept: "application/json",
				"Content-Type": "application/json",
			},
			body: JSON.stringify(preference),
		})
			.then((response) => response.json())
			.then((response) => {});
	};

	const handleGenerate = () => {
		// navigate("/conversation");
		const uuid = preference.uuid;
		console.log(uuid);
		fetch(`http://127.0.0.1:5000/v1/newsletter/` + uuid, {
			method: "get",
			headers: {
				Accept: "application/json",
				"Content-Type": "application/json",
			},
		})
			.then((response) => response.json())
			.then((response) => {
				navigate("/conversation", { state: { newsletter: response } });
			});
	};

	return (
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
						value={interests.join(", ")}
						onChange={handleInterestsChange}
					/>
					<hr className="editable-line" />
				</label>
				<label>
					Content Sources:
					<input
						type="text"
						className="editable-input"
						value={contentSources.join(", ")}
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
						Save preference
					</button>
					{unsavedChanges && <span>Unsaved changes</span>}
				</div>
				<div className="button-wrapper">
					<button onClick={handleGenerate}>Generate newsletter</button>
				</div>
			</div>
		</div>
	);
}

export default NewsTemplate;
