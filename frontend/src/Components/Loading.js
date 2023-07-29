import React, { useState, useEffect } from "react";
import "./styles/Loading.css";
import { ThreeDots } from "react-loader-spinner";

const Loading = () => {
	return (
		<div className="loading-page">
			<ThreeDots
				height="80"
				width="80"
				radius="9"
				color="black"
				ariaLabel="three-dots-loading"
				wrapperStyle={{}}
				wrapperClassName=""
				visible={true}
			/>
		</div>
	);
};

export default Loading;
