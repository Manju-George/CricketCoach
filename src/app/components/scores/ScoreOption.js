import React, { Component } from 'react';
function ScoreOption(props){
	return (
		<div>
			<label>
				<input 
					type="radio"
					checked={props.scoreForm.score == "1"}
					onChange={() => props.handleChange(props.scoreForm.id, 1)}
					className="radio-option"
					
				/>
				1
			</label>
			<label>
				<input 
					type="radio"
					value="2"
					checked={props.scoreForm.score == "2"}
					onChange={() => props.handleChange(props.scoreForm.id, 2)}
					className="radio-option"
				/>
				2
			</label>
			<label>
				<input
					type="radio"
					value="3"
					checked={props.scoreForm.score == "3"}
					onChange={() => props.handleChange(props.scoreForm.id,3)}
					className="radio-option"
				/>
				3
			</label>
		</div>
	);
}
export default ScoreOption;