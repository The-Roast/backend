import React, { useState } from "react";

const TextList = () => {
	const [items, setItems] = useState([]);

	const addItem = () => {
		setItems([...items, ""]);
	};

	const removeItem = (index) => {
		const updatedItems = [...items];
		updatedItems.splice(index, 1);
		setItems(updatedItems);
	};

	const handleChange = (index, event) => {
		const updatedItems = [...items];
		updatedItems[index] = event.target.value;
		setItems(updatedItems);
	};

	return (
		<div>
			{items.map((item, index) => (
				<div key={index}>
					<input
						type="text"
						value={item}
						onChange={(event) => handleChange(index, event)}
					/>
					<button onClick={() => removeItem(index)}>&times;</button>
				</div>
			))}
			<button onClick={addItem}>Add Item</button>
		</div>
	);
};

export default TextList;
