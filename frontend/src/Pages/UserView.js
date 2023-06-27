import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./styles/UserView.css";

const UserView = (isSignedIn) => {
	const [firstName, setFirstName] = useState("");
	const [hoveredSquare, setHoveredSquare] = useState(null);
	let navigate = useNavigate();
	const [preferences, setPreferences] = useState([]);

	useEffect(() => {
		getPreferences();
	}, []);

	function getPreferences() {
		fetch("http://127.0.0.1:5000/v1/user", {
			method: "get",
			headers: {
				Accept: "application/json",
				"Content-Type": "application/json",
			},
		})
			.then((response) => response.json())
			.then((response) => {
				fetch(`http://127.0.0.1:5000/v1/user/${response.email}`, {
					method: "get",
					headers: {
						Accept: "application/json",
						"Content-Type": "application/json",
					},
				})
					.then((response) => response.json())
					.then((response) => {
						const newPreferences = [...preferences];
						response.digests.map(function (digest) {
							newPreferences.push(digest);
						});
						setPreferences(newPreferences);
					});
			});
	}

	const handleSquareClick = (preference) => {
		let path = preference.name.toLowerCase();
		if (path === "pumpkin spice") {
			path = "pumpkin-spice";
		}
		navigate(path, { state: { preference: preference } });
	};

	const handleSquareHover = (uuid) => {
		setHoveredSquare(uuid);
	};

	const handleSquareLeave = () => {
		setHoveredSquare(null);
	};

	const handleCreate = () => {
		navigate("/create-digest");
	};

	return (
		<div className="main-container">
			<div className="main">
				{/* Left-aligned greeting */}
				<h1 className="greeting">Hello, {firstName}!</h1>
				<h1 className="welcome">Welcome to your Profile</h1>

				{/* 2x3 grid of squares */}
				<div className="grid">
					{preferences.map((preference) => (
						<div
							key={preference.uuid}
							className={`square ${
								hoveredSquare === preference.uuid ? "hovered" : ""
							}`}
							style={{
								backgroundColor:
									hoveredSquare === preference.uuid
										? "transparent"
										: preference.color.hex,
								color:
									hoveredSquare === preference.uuid
										? preference.color.hex
										: "#fefbf0",
								border:
									hoveredSquare === preference.uuid
										? "5px solid " + preference.color.hex
										: "5px solid transparent",
								// outlineOffset: hoveredSquare === flavor.id ? "-10px" : "0",
							}}
							onClick={() => handleSquareClick(preference)}
							onMouseEnter={() => handleSquareHover(preference.uuid)}
							onMouseLeave={handleSquareLeave}
						>
							<div className="content">
								<div className="flavor">{preference.name}</div>
							</div>
						</div>
					))}
					<div className="create-digest" onClick={() => handleCreate()}>
						<div className="flavor">Create Digest</div>
					</div>
				</div>
			</div>
		</div>
	);
};

export default UserView;
