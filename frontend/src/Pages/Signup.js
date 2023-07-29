import React, { useState, useCallback, useEffect } from "react";
import "./styles/Signup.css";
import { NavLink, useNavigate } from "react-router-dom";

function Signup() {
	const [first_name, setfirst_name] = useState("");
	const [last_name, setlast_name] = useState("");
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

	const handlefirst_nameChange = (e) => {
		setfirst_name(e.target.value);
	};

	const handlelast_nameChange = (e) => {
		setlast_name(e.target.value);
	};

	const handleEmailChange = (e) => {
		setEmail(e.target.value);
	};

	const handlePasswordChange = (e) => {
		setPassword(e.target.value);
	};

	const handleConfirmPasswordChange = (e) => {
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
				if (response.status == 404) {
					setWarningMessage("Use a different email.");
					setIsWarningMessage(true);
				} else {
					fetch("http://127.0.0.1:5000/login", {
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
								navigate("/user-view", { state: { isSignedIn: true } });
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
							name="first_name"
							value={first_name}
							onChange={handlefirst_nameChange}
							// ref={nameInput}
							required
						/>
						<input
							type="text"
							placeholder="Last Name"
							name="last_name"
							value={last_name}
							onChange={handlelast_nameChange}
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
					{isMismatchedPassword ? (
						<div className="warning-message">
							<p>{passwordWarningMessage}</p>
						</div>
					) : (
						<div></div>
					)}
					<input
						type="password"
						name="password"
						value={password}
						onChange={handlePasswordChange}
						required
					/>
					<input
						type="password"
						name="confirm_password"
						value={confirm_password}
						onChange={handleConfirmPasswordChange}
						required
					/>
					<h1>Personalization</h1>
					<label>Interests</label>
					<textarea
						placeholder="Tech updates, finance news, formula one..."
						name="interests"
						value={interests}
						onChange={handleInterestsChange}
						style={{ height: "200px" }}
						required
					></textarea>

					<label>Content Sources</label>
					<textarea
						placeholder="NY Times, Politico..."
						name="sources"
						value={sources}
						onChange={handlesourcesChange}
						style={{ height: "200px" }}
					></textarea>

					<label>Daily Digest Personality</label>
					<input
						type="text"
						placeholder="funny and humorous"
						name="personality"
						value={personality}
						onChange={handlePersonalityChange}
						required
					/>

					<label>Digest Name</label>
					<input
						type="text"
						placeholder="Alex's Digest"
						name="digest_name"
						value={digest_name}
						onChange={handleDigestNameChange}
						required
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
