import React, { useState, useCallback, useEffect } from "react";
import "./styles/Signup.css";
import { NavLink, useNavigate } from "react-router-dom";
import SERVER_API_URL from "../Config";

function Signup() {
	const [first_name, setFirstName] = useState("");
	const [last_name, setLastName] = useState("");
	const [email, setEmail] = useState("");
	const [interests, setInterests] = useState("");
	const [sources, setsources] = useState("");
	const [personality, setPersonality] = useState("");
	const [digest_name, setdigest_name] = useState("");
	const [password, setPassword] = useState("");
	const [confirm_password, setConfirmPassword] = useState("");
	const [warningMessage, setWarningMessage] = useState("");
	const [isWarningMessage, setIsWarningMessage] = useState(false);
	const passwordWarningMessage = "Passwords don't match!";
	const [isMismatchedPassword, setIsMismatchedPassword] = useState(false);
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

	const handlePasswordChange = (e) => {
		setIsMismatchedPassword(false);
		setPassword(e.target.value);
	};

	const handleConfirmPasswordChange = (e) => {
		setIsMismatchedPassword(false);
		setConfirmPassword(e.target.value);
	};

	const handleInterestsChange = (e) => {
		setInterests(e.target.value);
	};

	const handlesourcesChange = (e) => {
		setsources(e.target.value);
	};

	const handlePersonalityChange = (e) => {
		setPersonality(e.target.value);
	};

	const handleDigestNameChange = (e) => {
		setdigest_name(e.target.value);
	};

	const handleSubmit = (event) => {
		event.preventDefault();
		if (password !== confirm_password) {
			setIsMismatchedPassword(true);
			return;
		}
		const formData = {
			first_name,
			last_name,
			email,
			interests: interests,
			sources: sources,
			personality: personality,
			digest_name: digest_name,
			password: password,
		};

		// Send the form data to the server for further processing
		fetch(`${SERVER_API_URL}/signup`, {
			method: "POST",
			headers: {
				Accept: "application/json",
				"Content-Type": "application/json",
			},
			body: JSON.stringify(formData),
		})
			.then((response) => response.json())
			.then((response) => {
				if (response.status == 404) {
					setWarningMessage("Use a different email.");
					setIsWarningMessage(true);
				} else {
					fetch(`${SERVER_API_URL}/login`, {
						method: "POST",
						headers: {
							Accept: "application/json",
							"Content-Type": "application/json",
							Origin: "http://localhost:3000",
						},
						body: JSON.stringify({ email: email, password: password }),
					})
						.then((response) => response.json())
						.then((response) => {
							if (!response.ok) {
								setWarningMessage("Invalid email.");
								setIsWarningMessage(true);
							} else {
								localStorage.setItem(
									"access_token",
									response.response.access_token
								);
								localStorage.setItem(
									"refresh_token",
									response.response.refresh_token
								);
								navigate("/main", { state: { isSignedIn: true } });
							}
						});
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
			<form className="signup-form" onSubmit={handleSubmit}>
				<div className="back-button-wrapper">
					<button
						onClick={() => {
							navigate(-1);
						}}
					>
						Back
					</button>
				</div>
				<div className="input-container">
					<p>First name:</p>
					<input
						type="text"
						name="first_name"
						value={first_name}
						onChange={handleFirstNameChange}
						required
					/>
				</div>
				<div className="input-container">
					<p>Last name:</p>
					<input
						type="text"
						name="last_name"
						value={last_name}
						onChange={handleLastNameChange}
						required
					/>
				</div>
				<div className="input-container">
					<p>Email:</p>
					<input
						type="text"
						name="email"
						value={email}
						onChange={handleEmailChange}
						required
					/>
				</div>

				<div className="input-container">
					<p>Password:</p>
					<input
						type="text"
						name="password"
						value={password}
						onChange={handlePasswordChange}
						required
					/>
				</div>
				<div className="input-container">
					<p>Confirm password:</p>
					<input
						type="text"
						name="confirm_password"
						value={confirm_password}
						onChange={handleConfirmPasswordChange}
						required
					/>
				</div>

				{isMismatchedPassword ? (
					<div className="warning-message">
						<p>{passwordWarningMessage}</p>
					</div>
				) : null}
				{/* <div className="field-container">
				<p>What are your interests?</p>
				<input
					placeholder="Tech updates, finance news, formula one..."
					name="interests"
					value={interests}
					onChange={handleInterestsChange}
					required
				></input>
			</div>
			<div className="field-container">
				<p>Where do you get your daily content?</p>
				<input
					placeholder="NY Times, Politico..."
					name="sources"
					value={sources}
					onChange={handlesourcesChange}
				></input>
			</div>

			<p>What personality do you like?</p>
			<input
				type="text"
				placeholder="funny and humorous"
				name="personality"
				value={personality}
				onChange={handlePersonalityChange}
				required
			/>

			<p>Name your digest</p>
			<input
				type="text"
				placeholder="Alex's Digest"
				name="digest_name"
				value={digest_name}
				onChange={handleDigestNameChange}
				required
			/> */}
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
	);
}

export default Signup;
