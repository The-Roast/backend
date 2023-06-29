import React, { useState } from "react";
import { useParams, useNavigate, useLocation } from "react-router-dom";
import { SliderPicker } from "react-color";
import "./styles/NewsTemplate.css";

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
		fetch(`http://127.0.0.1:5000/v1/digest`, {
			method: "POST",
			headers: {
				Accept: "application/json",
				"Content-Type": "application/json",
				Authorization: "Bearer " + access_token,
			},
			body: JSON.stringify(preference),
		});
		navigate("/user-view");
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
						value={sources}
						onChange={handleSourcesChange}
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
					<button onClick={handleCreate}>Create Digest</button>
				</div>
			</div>
		</div>
	);
}

export default CreateNewsTemplate;
