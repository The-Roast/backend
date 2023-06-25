import "./styles/Signin.css";
import { useState, useCallback } from "react";
import { useNavigate } from "react-router-dom";

function Signin({ setIsSignedIn }) {
	const [email, setEmail] = useState("");
	const handleEmailChange = (e) => {
		setEmail(e.target.value);
	};

	const navigate = useNavigate();
	const [warningMessage, setWarningMessage] = useState("");
	const [isWarningMessage, setIsWarningMessage] = useState(false);
	const handleSubmit = (event) => {
		event.preventDefault();
		console.log(email);
		// Send the form data to the server for further processing
		fetch("http://127.0.0.1:5000/login", {
			method: "POST",
			// mode: "cors",
			headers: {
				Accept: "application/json",
				"Content-Type": "application/json",
				Origin: "http://localhost:3000",
			},
			body: JSON.stringify({ email: email }),
		})
			.then((response) => response.json())
			.then((response) => {
				console.log(response);
				if (response.status == 404) {
					setWarningMessage("Invalid email.");
					setIsWarningMessage(true);
				} else {
					setIsSignedIn(true);
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