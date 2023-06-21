import React from "react";

const Enum = ({ values, onChange }) => {
	return (
		<select onChange={onChange}>
			{values.map((value) => (
				<option key={value} value={value}>
					{value}
				</option>
			))}
		</select>
	);
};

export default Enum;
