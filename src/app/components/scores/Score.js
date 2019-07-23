import React, {Component} from "react";
import ScoreOption from './ScoreOption'

class Score extends Component {
	constructor(){
		super()
		this.state = {
			score_rows:[
				{
					id: 0,
					score:0
				}		
			],
			total_scored: 0
		}
		this.handleScorechange = this.handleScorechange.bind(this)
	}
	
	handleScorechange(id, scoreVal){
			
		this.setState(prevState => {
			const updatedRows = prevState.score_rows.map(score_row => {
				if(score_row.id === id){
					score_row.score = scoreVal
				}
				return score_row
			})
			const totalScored = updatedRows.reduce(function(result, row) {
				result += row.score
				return result
			},0)
			
			if(id + 1 < prevState.score_rows.length){
				return {
					score_rows:updatedRows,
					total_scored:totalScored
				}
				
			}
			return {
				score_rows: [...updatedRows,{
								id:id + 1,
								score:0

							}],
							total_scored:totalScored

			}

		})
	}
			
	render() {
		let score_rows = this.state.score_rows.map((score_form, idx) => (
									<tr key={idx}>
										<td>{idx + 1}</td>
										<td><ScoreOption handleChange={this.handleScorechange}
												scoreForm={score_form}/></td>
									</tr>)
								);
		
				
		return (
			<div className="Title-text">
				<h3> Cricket Score Input Form for ****TODO**** </h3>
				<table>
			        <thead>
			          <tr>
			            <th className="Table-header">Ball No.</th>
			            <th className="Table-header">Batting Score</th>
			          </tr>
			        </thead>
			        <tbody>
			        	{score_rows}
						     	
			        </tbody>
					
		        </table>
				<p>Total Scored {this.state.total_scored}</p>
		    </div>
	    );
	}
}
export default Score;