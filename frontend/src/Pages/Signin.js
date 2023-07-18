import "./styles/Signin.css";
import { useState, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import SERVER_API_URL from "../Config";

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
		fetch(`${SERVER_API_URL}/login`, {
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
					setWarningMessage("Invalid email or password.");
					setIsWarningMessage(true);
				} else {
					localStorage.setItem("access_token", response.response.access_token);
					localStorage.setItem(
						"refresh_token",
						response.response.refresh_token
					);
					var delayInMilliseconds = 300; //1 second

					setTimeout(function () {
						navigate("/main");
					}, delayInMilliseconds);
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
					<div
						style={{ paddingBottom: "50px" }}
						className="back-button-wrapper"
					>
						<button
							onClick={() => {
								navigate(-1);
							}}
						>
							Back
						</button>
					</div>
					<div className="input-container">
						<p>Email:</p>
						<input
							type="text"
							name="email"
							value={email}
							onChange={handleEmailChange}
							ref={emailInput}
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

					{isWarningMessage ? (
						<div className="warning-message">
							<p>{warningMessage}</p>
						</div>
					) : (
						<div></div>
					)}
					<div style={{ paddingTop: "50px" }} className="button-wrapper">
						<input type="submit" value="Sign in" />
					</div>
				</form>
			</div>
		</div>
	);
}

export default Signin;
