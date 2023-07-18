import React from "react";
import "./styles/SettingsGrid.css";

const Grid = ({ data }) => {
	return (
		<table className="settings-grid">
			<thead>
				<tr>
					<th className="square-cell"></th>
					<th>Preferences</th>
					<th>Values</th>
				</tr>
			</thead>
			<tbody>
				{data.map((item, index) => (
					<tr key={index} className="data-row">
						<td>
							<ul>
								<li></li>
							</ul>
						</td>
						<td>{item.preference}</td>
						<td>
							<input
								type="text"
								className="editable-input"
								value={item.value}
								onChange={item.onChange}
							/>
						</td>
					</tr>
				))}
			</tbody>
		</table>
	);
};

export default Grid;
