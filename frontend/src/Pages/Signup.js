import React, { useState, useCallback } from "react";
import "./styles/Signup.css";
import { NavLink, useNavigate } from "react-router-dom";

function Signup(isSignedIn, setIsSignedIn) {
	const [firstName, setFirstName] = useState("");
	const [lastName, setLastName] = useState("");
	const [email, setEmail] = useState("");
	const [interests, setInterests] = useState("");
	const [contentSources, setContentSources] = useState("");
	const [personality, setPersonality] = useState("");
	const [digestName, setDigestName] = useState("");
	const [warningMessage, setWarningMessage] = useState("");
	const [isWarningMessage, setIsWarningMessage] = useState(false);
	const navigate = useNavigate();

	const handleFirstNameChange = (e) => {
		setFirstName(e.target.value);
	};

	const handleLastNameChange = (e) => {
		setLastName(e.target.value);
	};

	const handleEmailChange = (e) => {
		setEmail(e.target.value);
	};

	const handleInterestsChange = (e) => {
		setInterests(e.target.value);
	};

	const handleContentSourcesChange = (e) => {
		setContentSources(e.target.value);
	};

	const handlePersonalityChange = (e) => {
		setPersonality(e.target.value);
	};

	const handleDigestNameChange = (e) => {
		setDigestName(e.target.value);
	};

	// if (isSignedIn) {
	// }

	const handleSubmit = (event) => {
		event.preventDefault();

		const formData = {
			firstName,
			lastName,
			email,
			interests: interests.split(",").map((interest) => interest.trim()),
			contentSources: contentSources
				.split(",")
				.map((interest) => interest.trim()),
			personality: personality,
			digestName: digestName,
		};

		// Send the form data to the server for further processing
		console.log(formData);
		fetch("http://127.0.0.1:5000/signup", {
			method: "POST",
			headers: {
				Accept: "application/json",
				"Content-Type": "application/json",
			},
			body: JSON.stringify(formData),
		})
			.then((response) => response.json())
			.then((response) => {
				console.log(response);
				if (response.status == 404) {
					setWarningMessage("Use a different email.");
					setIsWarningMessage(true);
				} else {
					navigate("/user-view");
				}
			});
	};

	// const nameInput = useCallback((inputElement) => {
	// 	if (inputElement) {
	// 		inputElement.focus();
	// 	}
	// }, []);

	return (
		<div className="signup">
			<div className="form-container">
				<p className="already-signed-in">
					Already have an account? <NavLink to="/sign-in">Sign in</NavLink>
				</p>
				<form className="signup-form" onSubmit={handleSubmit}>
					<h1>User</h1>
					<div className="name-wrapper">
						<input
							type="text"
							placeholder="First Name"
							name="firstName"
							value={firstName}
							onChange={handleFirstNameChange}
							// ref={nameInput}
							required
						/>
						<input
							type="text"
							placeholder="Last Name"
							name="lastName"
							value={lastName}
							onChange={handleLastNameChange}
							required
						/>
					</div>
					<input
						type="text"
						placeholder="Email"
						name="email"
						value={email}
						onChange={handleEmailChange}
						required
					/>
					<h1>Personalization</h1>
					<label>Interests*</label>
					<textarea
						placeholder="Tech updates, finance news, formula one..."
						name="interests"
						value={interests}
						onChange={handleInterestsChange}
						style={{ height: "200px" }}
						required
					></textarea>

					<label>Content Sources*</label>
					<textarea
						placeholder="nytimes.com, politico.com..."
						name="contentSources"
						value={contentSources}
						onChange={handleContentSourcesChange}
						style={{ height: "200px" }}
						required
					></textarea>

					<label>Daily Digest Personality</label>
					<input
						type="text"
						placeholder="funny and humorous"
						name="personality"
						value={personality}
						onChange={handlePersonalityChange}
					/>

					<label>Digest Name</label>
					<input
						type="text"
						placeholder="Alex's Digest"
						name="digestName"
						value={digestName}
						onChange={handleDigestNameChange}
					/>
					{isWarningMessage ? (
						<div className="warning-message">
							<p>{warningMessage}</p>
						</div>
					) : (
						<div></div>
					)}
					<div className="button-wrapper">
						<input type="submit" value="Sign Up" />
					</div>
				</form>
			</div>
		</div>
	);
}

export default Signup;
