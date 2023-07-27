import "./styles/Signin.css";
import { useState, useCallback } from "react";
import { useNavigate } from "react-router-dom";

function Signin() {
	const [email, setEmail] = useState("");
	const [password, setPassword] = useState("");

	const handleEmailChange = (e) => {
		setEmail(e.target.value);
	};

	const handlePasswordChange = (e) => {
		setPassword(e.target.value);
	};

	const navigate = useNavigate();
	const [warningMessage, setWarningMessage] = useState("");
	const [isWarningMessage, setIsWarningMessage] = useState(false);
	const handleSubmit = (event) => {
		event.preventDefault();
		// Send the form data to the server for further processing
		fetch("http://127.0.0.1:5000/login", {
			method: "POST",
			headers: {
				Accept: "application/json",
				"Content-Type": "application/json",
			},
			body: JSON.stringify({ email: email, password: password }),
		})
			.then((response) => response.json())
			.then((response) => {
				if (!response.ok) {
					setWarningMessage("Invalid email.");
					setIsWarningMessage(true);
				} else {
					localStorage.setItem("access_token", response.response.access_token);
					localStorage.setItem(
						"refresh_token",
						response.response.refresh_token
					);
					navigate("/user-view");
				}
			});
	};

	const emailInput = useCallback((inputElement) => {
		if (inputElement) {
			inputElement.focus();
		}
	}, []);

	return (
		<div className="sign-in">
			<div className="form-container">
				<form className="signin-form" onSubmit={handleSubmit}>
					{/* <label></label> */}
					<input
						type="text"
						placeholder="Email"
						name="email"
						value={email}
						onChange={handleEmailChange}
						ref={emailInput}
						required
					/>
					<input
						type="text"
						placeholder="Password"
						name="password"
						value={password}
						onChange={handlePasswordChange}
						required
					/>
					{isWarningMessage ? (
						<div className="warning-message">
							<p>{warningMessage}</p>
						</div>
					) : (
						<div></div>
					)}
					<div style={{ paddingTop: "100px" }} className="button-wrapper">
						<input type="submit" value="Sign in" />
					</div>
				</form>
			</div>
		</div>
	);
}

export default Signin;
