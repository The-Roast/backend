import React, { useEffect, useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import "./styles/UserView.css";
import SERVER_API_URL from "../Config";

const UserView = () => {
	const [firstName, setFirstName] = useState("");
	let navigate = useNavigate();
	const [preferences, setPreferences] = useState([]);

	const access_token = localStorage.getItem("access_token");
	const refresh_token = localStorage.getItem("refresh_token");

	useEffect(() => {
		getPreferences();
	}, []);

	const Capitalize = (str) => {
		if (str == null) {
			return "";
		}
		return str.charAt(0).toUpperCase() + str.slice(1);
	};

	function getPreferences() {
		fetch(`${SERVER_API_URL}/v1/user`, {
			method: "get",
			headers: {
				Accept: "application/json",
				"Content-Type": "application/json",
				Authorization: `Bearer ${access_token}`,
			},
		})
			.then((response) => response.json())
			.then((response) => {
				console.log(response);
				fetch(`${SERVER_API_URL}/v1/user/${response.response.id}`, {
					method: "get",
					headers: {
						Accept: "application/json",
						"Content-Type": "application/json",
						Authorization: "Bearer " + access_token,
					},
				})
					.then((response) => response.json())
					.then((response) => {
						console.log(response);
						const newPreferences = [...preferences];
						response.response.digests.map(function (digest) {
							newPreferences.push(digest);
						});
						setFirstName(response.response.firstName);
						setPreferences(newPreferences);
					});
			});
	}

	const handleCardClick = (preference) => {
		let path = preference.name.toLowerCase();
		console.log(preference);
		preference.interests = preference.interests.join(", ");
		preference.sources = preference.sources.join(", ");
		navigate(path, { state: { preference: preference } });
	};

	const handleCreate = () => {
		navigate("/create-digest");
	};

	return (
		<div className="main-container">
			<div className="main">
				<div className="title-card">
					<h1>Digests</h1>
				</div>
				<div className="grid">
					{preferences.map((preference, index) => (
						<div
							key={preference.uuid}
							className={`card`}
							onClick={() => handleCardClick(preference)}
							style={{
								backgroundColor: index % 4 === 0 ? "#FCF9E1" : "#F9F9F6",
							}}
						>
							<div
								className="content"
								style={{ border: `2px solid ${preference.color.hex}` }}
							>
								<span className="content-header">
									<h1>{preference.name}</h1>
									<svg
										style={{ marginBottom: "5px" }}
										xmlns="http://www.w3.org/2000/svg"
										width="30"
										height="30"
										viewBox="0 0 30 30"
										fill="none"
									>
										<circle
											cx="15"
											cy="15"
											r="15"
											fill={preference.color.hex}
										/>
									</svg>
								</span>
								<hr />
								{/* <h1>{preference.schedule}</h1> */}
								<span>
									<p>Frequency: </p>
									<h6>Weekly</h6>
								</span>
								<hr />
								<span>
									<p>Personality: </p>
									<h6>{Capitalize(preference.personality)}</h6>
								</span>
								<hr />
								<span>
									<p>Interests: </p>
									<h6>{Capitalize(preference.interests.join(", "))}</h6>
								</span>
								<hr />
								<span>
									<p>Sources: </p>
									<h6 style={{ textTransform: "capitalize" }}>
										{preference.sources.join(", ")}
									</h6>
								</span>
								<hr />
							</div>
						</div>
					))}
					<div className="createDigest">
						<svg
							xmlns="http://www.w3.org/2000/svg"
							width="99"
							height="99"
							viewBox="0 0 99 99"
							fill="none"
							onClick={() => handleCreate()}
						>
							<line
								x1="49.5"
								y1="1.09279e-07"
								x2="49.5"
								y2="99"
								stroke="black"
								stroke-width="5"
							/>
							<line
								y1="49.5"
								x2="99"
								y2="49.5"
								stroke="black"
								stroke-width="5"
							/>
						</svg>
					</div>
				</div>
			</div>
		</div>
	);
};

export default UserView;
